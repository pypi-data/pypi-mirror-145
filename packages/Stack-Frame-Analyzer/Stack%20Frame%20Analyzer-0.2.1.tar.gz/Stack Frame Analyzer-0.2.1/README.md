# Stack Frame Analyzer
This package was created to help improve the quality of application logs.

It's only uses building libraries, therefore, it has no external dependency.
It is also lightweight and thread-safe, which makes it ideal for use in services and micro-services.

However, the module has some limitations.
The most important thing to note in this scenario is that it only works with the **CPython** implementation.

The returned context is formatted according to the following pattern:
    *project_name:package_name:module_name:class_name:callable_name(callable_arguments)*

An example of the context returned could be:
    *authentication_service:src.domain.user:model:UserModel:has_permission(self=..., permission="add_user")*

## Typical usage example:


### With Caller's Stack Frame Depth 0
```python
stack_frame_analyzer = StackFrameAnalyzer("my_service_name")

def foo(bar):
    try:
        ...
    except Exception as error:
        context = stack_frame_analyzer.get_caller_context()
        logging.error(context)
```

### With Caller's Stack Frame Depth 1
```python
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
```

### With Caller's Stack Frame Depth 2


------------

```python
class ExceptionWithContext(Exception):
    """
    Base class to make exceptions capture the context of whoever raises them.
    """
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
        logging.error(error.context)
```

## Test Coverage
```
Name                                                      Stmts   Miss  Cover
-----------------------------------------------------------------------------
src/__init__.py                                               1      0   100%
src/stack_frame_analyzer/__init__.py                          2      0   100%
src/stack_frame_analyzer/exceptions.py                       36      0   100%
src/stack_frame_analyzer/main.py                            100      0   100%
tests/__init__.py                                             0      0   100%
tests/stack_frame_analyzer/__init__.py                        0      0   100%
tests/stack_frame_analyzer/test_exceptions.py                27      0   100%
tests/stack_frame_analyzer/test_in_class.py                  17      0   100%
tests/stack_frame_analyzer/test_main.py                     131      0   100%
tests/stack_frame_analyzer/test_memory_leak.py               55      0   100%
tests/stack_frame_analyzer/test_on_function.py               12      0   100%
tests/stack_frame_analyzer/test_speed.py                      7      0   100%
tests/stack_frame_analyzer/test_with_decorator.py             8      0   100%
tests/stack_frame_analyzer/test_with_depth_two_frame.py      13      0   100%
tests/stack_frame_analyzer/test_with_exception.py             8      0   100%
tests/stack_frame_analyzer/test_with_threads.py              33      0   100%
tests/stack_frame_analyzer/utils/__init__.py                  0      0   100%
tests/stack_frame_analyzer/utils/bar.py                       4      0   100%
tests/stack_frame_analyzer/utils/baz.py                      13      0   100%
tests/stack_frame_analyzer/utils/child.py                     7      0   100%
tests/stack_frame_analyzer/utils/foo.py                       4      0   100%
tests/stack_frame_analyzer/utils/foo_with_decorator.py       11      0   100%
tests/stack_frame_analyzer/utils/foo_with_exception.py        7      0   100%
tests/stack_frame_analyzer/utils/main.py                      2      0   100%
tests/stack_frame_analyzer/utils/memory_leak.py               6      0   100%
tests/stack_frame_analyzer/utils/parent.py                    8      0   100%
tests/stack_frame_analyzer/utils/solve_with_queue.py          7      0   100%
-----------------------------------------------------------------------------
TOTAL                                                       519      0   100%
```