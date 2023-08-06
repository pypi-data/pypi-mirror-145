"""Functions included as standard in the core."""

from ..ext.function import Function
from ..ext.register import register


@register()
class RightStripCoreFunFunction(Function):
    """Strip right hand side white space."""

    name = 'rstrip'

    @classmethod
    def exec(cls, string):
        """Execute function."""

        return super().exec(string.rstrip())


@register()
class LeftStripCoreFunFunction(Function):
    """Strip left hand side white space."""

    name = 'lstrip'

    @classmethod
    def exec(cls, string):
        """Execute function."""

        return super().exec(string.lstrip())
