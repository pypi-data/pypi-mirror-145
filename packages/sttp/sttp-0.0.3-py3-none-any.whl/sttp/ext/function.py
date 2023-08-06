"""Function module."""


class Function:
    """A function."""

    cast = str

    _reg = {}

    @classmethod
    def exec(cls, *args):
        """Run the function."""

        return cls.cast(*args)

    @classmethod
    def lookup(cls, name):
        """Return the named function, or `None` if no match with the given name is registered."""

        for scls in cls.mro():
            if name in scls._reg:
                return scls._reg[name]
            if scls is Function:
                return None
        return None
