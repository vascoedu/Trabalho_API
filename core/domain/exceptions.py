class DomainError(Exception):
    """Base exception for domain-related errors."""
    pass

class UserNotFoundException(DomainError):
    """Raised when a user is not found."""
    pass

class UsernameAlreadyExistsException(DomainError):
    """Raised when a username already exists."""
    pass

class TaskNotFoundException(DomainError):
    """Raised when a task is not found."""
    pass

class InvalidCredentialsException(DomainError):
    """Raised when authentication credentials are invalid."""
    pass