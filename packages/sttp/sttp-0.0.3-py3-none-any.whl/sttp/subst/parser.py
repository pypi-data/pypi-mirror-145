"""
Substitution parsing module.

Provides parser for template substitutions, the bits {{ in double curlies }} (by default).
"""

import os
import lark

from .handler import SubstHandler
from .. import errors


class Parser:
    """Substitution parser."""

    @lark.v_args(inline=True)
    class HandlerBuilder(lark.Transformer):
        """Lark transformer for computing substitution handler object from parse tree."""

        def start(self, data):
            return SubstHandler(**data)

        def assignment(self, variable, match_spec, pipes):
            return {**variable, **match_spec, **pipes}

        def untyped_variable(self, var_name):
            return {'var_name': str(var_name)}

        def typed_variable(self, var_type, var_name):
            return {'cast': __builtins__[var_type], 'var_name': str(var_name)}

        def variable(self, var_name):
            return var_name

        def match_spec(self, data):
            return data

        def match_name(self, match_name):
            return {'match_name': str(match_name)}

        def function(self, fun_name, fun_args):
            return {'fun_name': str(fun_name), 'fun_args': fun_args.children}

        def const(self, val):
            return val

        def pipes(self, *funs):
            return {'pipes': list(funs)}

        def ESCAPED_STRING(self, tok):
            return str(tok)[1:-1]

        def INT(self, tok):
            return int(tok)

        def FLOAT(self, tok):
            return float(tok)

    def __init__(self, grammar=None, grammar_filename=None):
        """
        Initialise subst parser.

        Optionally an alternative grammar can be provided with grammar or grammar_filename params.
        """

        if grammar is not None and grammar_filename is not None:
            raise Exception('grammar and grammar_filename are mutually exclusive')

        if grammar_filename is None:
            grammar_filename = os.path.dirname(os.path.realpath(__file__)) + '/grammar.txt'

        with open(grammar_filename) as fp:
            self._grammar_spec = fp.read()

        self._lark = lark.Lark(self._grammar_spec, parser='lalr', transformer=Parser.HandlerBuilder())

    def parse(self, in_text, inline_num=None, tline_num=None):
        """Parse substitution text and return handler."""

        try:
            return self._lark.parse(in_text)
        except lark.exceptions.UnexpectedToken as ex:
            raise errors.BadTemplateError(
                'substitution error (not understood)',
                inline_num=None if inline_num is None else inline_num + 1,
                tline_num=None if tline_num is None else tline_num + 1,
            ) from ex
