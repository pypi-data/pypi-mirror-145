"""This module was created to help improve the quality of application logs.

It's only uses building libraries, therefore, it has no external dependency.
It is also lightweight and thread-safe, which makes it ideal for use in services and microservices.

However, the module has some limitations.
The most important thing to note in this scenario is that it only works with the CPython implementation.

Typical usage example:

---------------------------------------

# Caller's Stack Frame Depth 0

stack_frame_analyzer = StackFrameAnalyzer("my_service_name")

def foo(bar):
    try:
        ...
    except Exception as error:
        context = stack_frame_analyzer.get_caller_context()
        logging.error(context)

---------------------------------------

# Caller's Stack Frame Depth 1

stack_frame_analyzer = StackFrameAnalyzer("my_service_name")

class MyException(Exception):
    def __init__(self):
        self.context = stack_frame_analyzer.get_caller_context(depth_in_the_stack=1)
        super().__init__()


def foo(bar):
    try:
        ...
    except MyException as error:
        logging.error(error.context)

---------------------------------------

# Caller's Stack Frame Depth 2


class ExceptionWithContext(Exception):
    '''
    Base class to make exceptions capture the context of whoever raises them.
    '''
    def __init__(self, message: str):
        self.message = message
        self.context = stack_frame_analyzer.get_caller_context(depth_in_the_stack=2)
        super().__init__(self.message)


class FooException(ExceptionWithContext):
    def __init__(self, message: str = "message"):
        self.message = message
        super().__init__(self.message)


def foo(bar):
    try:
        raise FooException
    except FooException as error:
        print(error.context)

---------------------------------------

"""

import inspect
import os
import sys
from types import FrameType
from typing import Tuple

from .exceptions import (
    FrameDepthOutOfRange,
    InvalidClassRepresentationNameType,
    InvalidFrameDepth,
    InvalidInstanceRepresentationNameType,
    InvalidProjectNameType,
    StackFrameAnalyzerException,
)


class StackFrameAnalyzer:
    """Help to get the context of a frame on the caller's stack, using only the builtin modules.
    This is a thread-safe implementation.
    The main method to use is get_caller_context that return the context of selected caller.


    The main builtin functions used are:
        sys._getframe: Used to get the frame of the caller's stack.
        inspect.getmodule: Used to get the module of the frame.
        inspect.getargvalues: Used to get the args in the frame.


    Limitations:
        Compatible only with CPython implementation.
        Not compatible with pyinstaller.
        It is not possible to reach the decorated function inside the decorator.
        For static class methods it's not possible to get the class name.


    Args:
        project_name (str): Name of your project. Defaults is directory of your '__main__' module.
        instance_representation_name (str): The representation name of the instance in methods. Defaults is 'self'.
        class_representation_name (str): The representation name of the class in classmethods. Defaults is 'cls'.
        context_structure = 'project_name:package_name:module_name:class_name:callable_name(callable_arguments)'


    """

    __slots__ = (
        "_project_name",
        "_instance_representation_name",
        "_class_representation_name",
    )

    DEFAULT_PROJECT_NAME: str = os.path.split(os.path.abspath(os.curdir))[-1]
    CONTEXT_STRUCTURE = (
        "{project_name}:{package}:{module}:{class_name}:{callable_name}({arguments})"
    )

    def __init__(
        self,
        project_name: str = None,
        instance_representation_name: str = "self",
        class_representation_name: str = "cls",
    ) -> "StackFrameAnalyzer":
        self._project_name = None
        self.project_name = project_name
        self._instance_representation_name = None
        self.instance_representation_name = instance_representation_name
        self._class_representation_name = None
        self.class_representation_name = class_representation_name

    @property
    def project_name(self) -> str:
        return self._project_name

    @project_name.setter
    def project_name(self, project_name: str) -> None:
        if project_name is None:
            project_name = self.DEFAULT_PROJECT_NAME
        if not isinstance(project_name, str):
            raise InvalidProjectNameType
        self._project_name = project_name

    @property
    def instance_representation_name(self) -> str:
        return self._instance_representation_name

    @instance_representation_name.setter
    def instance_representation_name(self, instance_representation_name: str) -> None:
        if not isinstance(instance_representation_name, str):
            raise InvalidInstanceRepresentationNameType
        self._instance_representation_name = instance_representation_name

    @property
    def class_representation_name(self) -> str:
        return self._class_representation_name

    @class_representation_name.setter
    def class_representation_name(self, class_representation_name: str) -> None:
        if not isinstance(class_representation_name, str):
            raise InvalidClassRepresentationNameType
        self._class_representation_name = class_representation_name

    def _get_frame(self, stack_frame_depth: int) -> FrameType:
        """Get a frame from the caller stack.

        Args:
            stack_frame_depth (int): Frame index below the top of the caller's stack.

        Raises:
            FrameDepthOutOfRange: Caller's stack is not deep enough.

        Returns:
            FrameType: built-in FrameType
        """
        try:
            return sys._getframe(stack_frame_depth)
        except ValueError as error:
            raise FrameDepthOutOfRange from error

    def _get_package_and_module(self, frame: FrameType) -> Tuple[str, str]:
        module_obj = inspect.getmodule(frame)

        if not module_obj:
            return "", ""

        if module_obj.__name__ == "__main__":  # pragma: no cover
            module = module_obj.__file__.split(".")[0]
            return "", module

        package, module = module_obj.__name__.rsplit(".", 1)
        del module_obj
        return package, module

    def _get_class_name(self, frame: FrameType) -> str:
        instance_representation = frame.f_locals.get(self.instance_representation_name)

        class_representation = frame.f_locals.get(self.class_representation_name)

        if instance_representation and not class_representation:
            class_name = instance_representation.__class__.__name__
        elif class_representation and not instance_representation:
            class_name = class_representation.__name__
        else:
            class_name = ""

        return class_name

    def _get_callable_name(self, frame: FrameType) -> str:
        callable_name = frame.f_code.co_name

        if callable_name == "<module>":  # pragma: no cover
            return ""

        return callable_name

    def _stringfy_armguments(self, arguments: dict) -> str:
        buffer = []
        for key, value in arguments.items():
            buffer.append(f"{key}={value}")

        return ", ".join(buffer)

    def _get_callable_arguments(self, frame: FrameType) -> str:
        args_info = inspect.getargvalues(frame)
        arguments = {}
        for arg in args_info.args:
            if arg == self.instance_representation_name:
                arguments[self.instance_representation_name] = "<instance>"
            elif arg == self.class_representation_name:
                pass
            else:
                arguments[arg] = args_info.locals[arg]

        arguments_string = self._stringfy_armguments(arguments)

        del args_info
        return arguments_string

    def _build_context(
        self,
        package: str,
        module: str,
        class_name: str,
        callable_name: str,
        arguments: str,
    ) -> str:
        context = self.CONTEXT_STRUCTURE.format(
            project_name=self.project_name,
            package=package,
            module=module,
            class_name=class_name,
            callable_name=callable_name,
            arguments=arguments,
        )
        return context

    def get_caller_context(self, depth_in_the_stack: int = 0) -> str:
        f"""Get the context of selected caller.
        The structure of the context is:
          {self.CONTEXT_STRUCTURE}.

        For the caller deapth count start in the source code outside of the StackFrameAnalyzer class,
        the stack_frame_depth will be equal the depth_in_the_stack plus 2.
        So, if the value of depth_in_the_stack is zero, the caller will be the source code that invokes this method.

        Even though the frame only exists as a local variable,
        the reference cycles created when the frame object is referenceated
        is explicitly broken on the finally clause to avoid the delayed destruction of objects
        which can cause increased of memory consumption.

        Args:
            depth_in_the_stack (int):  Depth of the caller in the stack. Defaults is 0.

        Raises:
            InvalidFrameDepth: Invalid stack_frame_depth input value.
            FrameDepthOutOfRange: Caller's stack is not deep enough.
            StackFrameAnalyzerException: Internal error.

        Returns:
            str: A string with the context of the selected frame.
        """

        if not isinstance(depth_in_the_stack, int) or depth_in_the_stack < 0:
            raise InvalidFrameDepth

        stack_frame_depth = depth_in_the_stack + 2

        frame = self._get_frame(stack_frame_depth)

        try:
            package, module = self._get_package_and_module(frame)
            class_name = self._get_class_name(frame)
            callable_name = self._get_callable_name(frame)
            arguments = self._get_callable_arguments(frame)

            context = self._build_context(
                package, module, class_name, callable_name, arguments
            )

            return context

        except Exception as error:  # pragma: no cover
            raise StackFrameAnalyzerException from error

        finally:
            del frame
