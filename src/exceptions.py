## Custom exceptions for dll


class _NoNodeError(Exception):
    pass


class NoNextNodeError(_NoNodeError):
    pass


class NoPreviousNodeError(_NoNodeError):
    pass