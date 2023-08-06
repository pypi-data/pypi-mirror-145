"""Substitution handler module."""


class SubstHandler:
    """Substitution handler. Essentially a repository of data about the substitution."""

    def __init__(self, var_name=None, cast=None, match_name=None, fun_name=None, fun_args=None, pipes=None):
        """Initialise substitution handler object."""

        self._var_name = var_name
        self._cast = cast
        self._match_name = match_name
        self._fun_name = fun_name
        self._fun_args = fun_args or []
        self._pipes = pipes or []

    @property
    def var_name(self):
        """Variable name or `None` if not an assignment."""

        return self._var_name

    @property
    def cast(self):
        """Cast type or `None` if not an assignment or there is no cast."""

        return self._cast

    @property
    def match_name(self):
        """Match name or `None` if not a named match."""

        return self._match_name

    @property
    def fun_name(self):
        """Name of function or `None` if not a functional match."""

        return self._fun_name

    @property
    def fun_args(self):
        """Arguments of function or `None` if not a functional match."""

        return self._fun_args

    @property
    def pipes(self):
        """
        Pipes (a list of dicts, each with `fun_name` and `fun_args` keys).

        Pipes are invoked in sequence, the first passed the match result as
        the first argument, the second passed the output of the first pipe
        function, etc. The return value of the last pipe is what is returned
        and assigned ultimately.
        """

        return self._pipes
