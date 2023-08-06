class InvalidProjectNameType(ValueError):
    """Exception raised for errors in the input value of project_name attribute of StackFrameAnalyzer class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidFrameDepth":
        self.message = "Invalid project_name input value. It must be a string."
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class InvalidInstanceRepresentationNameType(ValueError):
    """Exception raised for errors in the input value of instance_representation_name attribute of StackFrameAnalyzer class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidFrameDepth":
        self.message = (
            "Invalid instance_representation_name input value. It must be a string."
        )
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class InvalidClassRepresentationNameType(ValueError):
    """Exception raised for errors in the input value of class_representation_name attribute of StackFrameAnalyzer class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidFrameDepth":
        self.message = (
            "Invalid class_representation_name input value. It must be a string."
        )
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class InvalidFrameDepth(ValueError):
    """Exception raised for errors in get_caller_context method of StackFrameAnalyzer class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidFrameDepth":
        self.message = (
            "Invalid stack_frame_depth input value. It must be a natural number."
        )
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class FrameDepthOutOfRange(ValueError):
    """Exception raised for errors in get_caller_context method of StackFrameAnalyzer class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidFrameDepth":
        self.message = (
            "Caller's stack is not deep enough. stack_frame_depth is out of range."
        )
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"


class StackFrameAnalyzerException(Exception):
    """Exception raised for errors in get_caller_context method of StackFrameAnalyzer class.

    Args:
        message: explanation of the error
    """

    def __init__(self) -> "InvalidFrameDepth":
        self.message = (
            "Internal error from get_caller_context method of StackFrameAnalyzer class."
        )
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}"
