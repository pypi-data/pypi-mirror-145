"""Match functions included as standard in the core."""

from ..ext.match_fun import MatchFun
from ..ext.register import register


@register()
class ReCoreMatchFun(MatchFun):
    """Integer match."""

    name = 're'

    def __init__(self, regex):
        """Initialise re (regex) match function."""

        self.regex = regex


@register()
class FixedWidthColumnCoreMatchFun(MatchFun):
    """Integer match."""

    name = 'fixedwidth'

    def __init__(self, width, strip=True):
        """Initialise re (regex) match function."""

        self.regex = '.{' + str(width) + '}'
        self._strip = strip

    def post_proc(self, string):
        """
        Strip white space from both ends of the result (by default).

        This makes sense for a fixed width column field is normally there would be white space.
        """

        return super().post_proc(string.lstrip().rstrip() if self._strip else string)
