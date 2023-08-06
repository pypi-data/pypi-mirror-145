"""Error classes."""


class BaseError(Exception):
    """Base error class."""

    def __init__(self, msg, inline_num=None, tline_num=None):
        """
        Initialise error.

        Accepts optional inline_num and tline_num kwargs to specify input and template line numbers.
        """

        if inline_num is not None and tline_num is not None:
            msg = f'line {inline_num} (template line {tline_num}): {msg}'
        elif inline_num is not None:
            msg = f'line {inline_num}: {msg}'
        elif tline_num is not None:
            msg = f'template line {tline_num}: {msg}'

        super().__init__(msg)


class BadTemplateError(BaseError):
    """Raised when the template is invalid."""


class ParseFailedError(BaseError):
    """Raised when input does not match the template."""


class LeftoverInputError(ParseFailedError):
    """Raised when the template is exhausted but there is more input still to parse."""


class NoMoreInputError(ParseFailedError):
    """Raised when there is no more input but some template remains unused."""


class RunError(BaseError):
    """Raised for a run time error, probably relating to the way the template is designed."""


class RegistrationNamingClashError(BaseError):
    """Raised when there is a registration naming clash (for example two matches with the same name)."""


class InternalError(BaseError):
    """Raised for circumstances that should not happen."""
