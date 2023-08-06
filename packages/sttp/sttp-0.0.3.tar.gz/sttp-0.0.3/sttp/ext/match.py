"""Named match module."""


class Match:
    """A named match; essentially a regular expression with extra typing and processing."""

    name = None
    regex = None
    cast = str

    _reg = {}

    def __str__(self):
        """Return the (string) regular expression when cast as a string."""

        return self.regex

    def post_proc(self, *args):
        """
        Post process string value captured from regex match.

        Default behaviour is just so cast using the data type.

        It is perfectly reasonable to override this method, but if you do so then do
        call the super class implementation before or after the sub class (whatever is
        appropriate) as it may increase forwards compatibility. Also consider if the
        reason for override is valid, could you instead define a custom type class?
        For example, by default `cast` is set to `str`, but you could set it to any
        class, such as `StrippedString` defined as follows:

            class StrippedString():
                def __init__(self, string):
                    self._string = string

                def __str__(self):
                    return self._string

                def post_proc(self, string):
                    return self._string.lstrip().rstrip()

        Consider if your use case implies a type though, creating a type that adds 1
        to an integer is probably abuse, `AddOneToInteger` isn't really a new type, it
        is still an `int` really, so setting `cast` to `int` and overriding `post_proc`
        to do that AFTER calling the super class is fairer.

        Another example would be date/time values, imagine a case where it is necessary
        to interpret two or more different formats of date/time. One solution is a to
        set `regex` to something that will match both, set `cast` to `datetime.datetime`
        and make `post_proc` interpret the string regex match result BEFORE calling the
        super class.
        """

        return self.cast(*args)

    @classmethod
    def lookup(cls, name):
        """Return the named match, or `None` if no match with the given name is registered."""

        for scls in cls.mro():
            if name in scls._reg:
                return scls._reg[name]
            if scls is Match:
                return None
        return None
