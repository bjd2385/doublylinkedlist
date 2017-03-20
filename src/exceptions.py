## Custom exceptions for dll

__all__ = ['NoNextNodeError', 'NoPreviousNodeError']


class _NoNodeError(Exception):
    pass


class NoNextNodeError(_NoNodeError):
    pass


class NoPreviousNodeError(_NoNodeError):
    pass