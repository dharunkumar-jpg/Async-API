class UserAlreadyExistsException(Exception):
    """Raised when a user with the given email already exists."""

    def __init__(self) -> None:
        self.message = "User with this email already exists."
        super().__init__(self.message)


class UserNotFoundException(Exception):
    """Raised when a user cannot be found."""

    def __init__(self) -> None:
        self.message = "User not found."
        super().__init__(self.message)


class TaskNotFoundException(Exception):
    """Raised when a task cannot be found."""

    def __init__(self) -> None:
        self.message = "Task not found."
        super().__init__(self.message)

class InvalidTokenException(Exception):
    """Raised when a JWT token is invalid or expired."""

    def __init__(self) -> None:
        self.message = "Invalid or expired authentication token."
        super().__init__(self.message)

class InvalidCredentialsException(Exception):
    """Raised when the email or password is invalid."""

    def __init__(self) -> None:
        self.message = "Invalid email or password."
        super().__init__(self.message)


class InvalidPasswordException(Exception):
    """Raised when the current password is incorrect."""

    def __init__(self) -> None:
        self.message = "Current password is incorrect."
        super().__init__(self.message)


class SamePasswordException(Exception):
    """Raised when the new password matches the current password."""

    def __init__(self) -> None:
        self.message = "New password cannot be the same as the current password."
        super().__init__(self.message)