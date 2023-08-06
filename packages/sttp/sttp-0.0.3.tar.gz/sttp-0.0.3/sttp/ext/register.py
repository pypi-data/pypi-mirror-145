"""Extension registration module."""

from .match import Match
from .match_fun import MatchFun
from .function import Function
from .. import errors


def register(scope=None):
    r"""
    Register a named match, functional match or function class.

    This is a decorator and should be applied like this for example:

        @register()
        class NumberCoreMatch(sttp.ext.match.Match):
            name  = 'number'
            regex = r'\d+(?:\.\d+|)'
            cast  = float

    May be applied to subclasses of :py:class:`sttp.ext.match.Match` or
    :py:class:`sttp.ext.match_fun.MatchFun` or :py:class:`sttp.ext.function.Function`.

    Optionally a scope parameter may be given, which defaults to one of the
    above classes (and makes the registration global), but if set to the
    Match, MatchFun or Function lexical sub class of a parser, the registration
    will only be for that parser.
    """

    def decorator(cls):
        if issubclass(cls, MatchFun):
            scope_cls = scope or MatchFun

            if '_reg' not in scope_cls.__dict__:
                scope_cls._reg = {}

            if cls.name in scope_cls._reg:
                raise errors.RegistrationNamingClashError(
                    f'match function with name "{cls.name}" already registered',
                )

            scope_cls._reg[cls.name] = cls

        elif issubclass(cls, Match):
            scope_cls = scope or Match

            if '_reg' not in scope_cls.__dict__:
                scope_cls._reg = {}

            if cls.name in scope_cls._reg:
                raise errors.RegistrationNamingClashError(f'match with name "{cls.name}" already registered')

            scope_cls._reg[cls.name] = cls

        elif issubclass(cls, Function):
            scope_cls = scope or Function

            if '_reg' not in scope_cls.__dict__:
                scope_cls._reg = {}

            if cls.name in scope_cls._reg:
                raise errors.RegistrationNamingClashError(f'match with name "{cls.name}" already registered')

            scope_cls._reg[cls.name] = cls

        else:
            raise errors.InternalError('not a recognised class')

        return cls

    return decorator


def unregister_named(name, scope):
    """
    Unregister a named match, functional match or function class by name.

    Returns boolean true or false to indicate if the class was found and
    unregistered, or not found respectively.

    Because the unregistration is by name, and there can be a match named
    "foo" as well as a match function named "foo" for example, the scope
    MUST be givem and it should be :py:class:`sttp.ext.match.Match` or
    :py:class:`sttp.ext.match_fun.MatchFun` or :py:class:`sttp.ext.function.Function`
    OR the Match, MatchFun or Function lexical sub class of a parser which
    was used for the registration you want to undo.
    """

    if '_reg' not in scope.__dict__:
        scope._reg = {}

    if name in scope._reg:
        del scope._reg[name]
        return True

    return False
