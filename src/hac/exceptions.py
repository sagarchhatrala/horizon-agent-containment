class HACError(Exception):
    """Base HAC exception."""


class ValidationError(HACError):
    """Raised when an action or state cannot be verified."""


class InvariantViolation(HACError):
    """Raised when a security invariant is violated."""