class DropzoneException(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message

    def __repr__(self):
        return f"{self.__class__.__name__}({self.message})"

    def __str__(self):
        return self.__repr__()


class DZFileError(DropzoneException):
    ...


class DZFileNotFoundError(DZFileError):
    ...


class DZFileMergeError(DZFileError):
    ...
