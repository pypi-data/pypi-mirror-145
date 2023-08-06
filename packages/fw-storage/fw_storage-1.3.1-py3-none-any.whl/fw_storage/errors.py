"""Storage errors."""
import typing as t

__all__ = [
    "FileExists",
    "FileNotFound",
    "IsADirectory",
    "NotADirectory",
    "PermError",
    "StorageError",
]


class StorageError(Exception):
    """Storage error base class."""

    def __init__(self, message: str, errors: t.Optional[t.List[str]] = None):
        """Initialize exception."""
        super().__init__(message)
        self.errors = errors


class FileExists(StorageError):
    """File exists."""


class FileNotFound(StorageError):
    """File not found."""


class PermError(StorageError):
    """Permission error."""


class IsADirectory(StorageError):
    """Is a directory."""


class NotADirectory(StorageError):
    """Not a directory."""
