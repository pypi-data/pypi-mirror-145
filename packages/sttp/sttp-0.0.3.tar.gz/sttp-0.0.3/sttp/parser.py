"""Main parser module."""

import re
import math
import logging

from . import ext
from . import errors
from . import utils
from . import subst


class Parser:
    """Parser class."""

    subst_start = '{{'
    subst_end = '}}'
    prefix_sep = '> '

    class Match(ext.match.Match):
        """Match class, can be overridden to provide custom matches for this parser."""

    class MatchFun(ext.match_fun.MatchFun):
        """Match class, can be overridden to provide custom matche functions for this parser."""

    class Function(ext.function.Function):
        """Match class, can be overridden to provide custom functions for this parser."""

    class SubstParser(subst.parser.Parser):
        """Substitution parser class."""

    class CompiledTemplLine:
        def __init__(
            self,
            raw,
            line_num,
            min_matches,
            max_matches,
            ret_rtype,
            var_name,
            plain,
            plain_match,
            regex_str,
            regex,
            present,
            capproc_fmap,
        ):
            self.raw = raw
            self.line_num = line_num
            self.min_matches = min_matches
            self.max_matches = max_matches
            self.ret_rtype = ret_rtype
            self.var_name = var_name
            self.plain = plain
            self.plain_match = plain_match
            self.regex_str = regex_str
            self.regex = regex
            self.present = present
            self.capproc_fmap = capproc_fmap

    def __init__(self, template, itlel=True, allow_mixed_lists=False):
        """
        Initialise parser.

        Takes one positional required param, the template.

        If kwarg itlel (ignore the last empty line) is `True` then the
        last empty line of the input (if the last line is empty) will be ignored.
        This stops a template failure due to a final implied but forgotten/hidden
        line which is there because the last line has a newline on the end.

        If kwarg allow_mixed_lists is `True` then dict values will be combined into
        a list context, which will result in an exception being raised otherwise.
        Only do this is you are sure it's really what you want.
        """

        self._raw_template = template
        self._itlel = itlel
        self._allow_mixed_lists = allow_mixed_lists
        self._log = logging.getLogger(__name__)

        self._match_prefix_re = re.compile(
            r'^(?P<repeat_modifier>'
            r'\*|\+|\?|\{(?P<rm_min>\d+)'
            r'(?:,(?P<rm_max>\d+)|)'
            r'\}|)'
            r'(?:\('
            r'(?P<var_name>[a-zA-Z][a-zA-Z0-9_]*|\.)'
            r'\)|)'
            r'(?:/'
            r'(?P<flags>\!?[a-zA-Z][a-zA-Z0-9_]*(?:,\!?[a-zA-Z][a-zA-Z0-9_])*)'
            r'|)' + self.prefix_sep + r'(?P<tail>.*)$'
        )

        self._comp_template = self._compile_template(template)

    def _compile_template(self, template):
        ctlines = template.split('\n')
        if len(ctlines) > 0 and ctlines[-1] == '':
            ctlines.pop()

        subst_parser = self.SubstParser()

        return [
            self._compile_tline(
                subst_parser,
                ctlines[tline_num],
                tline_num,
            )
            for tline_num in range(0, len(ctlines))
        ]

    def _compile_tline(self, subst_parser, tline, tline_num):
        if tline[0] == 'm':
            return self._compile_prefix_m_tline(tline, subst_parser, tline[1:], tline_num)
        elif tline[0] == 'r':
            return self._compile_prefix_r_tline(tline, subst_parser, tline[1:], tline_num)

        raise errors.BadTemplateError(
            f'template prefix "{tline[0]}" unsupported',
            tline_num=tline_num + 1,
        )

    def _compile_prefix_m_tline(self, raw, subst_parser, tline, tline_num):
        (min_matches, max_matches, ret_rtype, tline, var_name, flags) = self._parse_tmodifiers(tline, tline_num)

        tline_tail = tline
        regex_str = ''
        capproc_fmap = {}

        while tline_tail.find(self.subst_start) != -1:
            sub_start = tline_tail.find(self.subst_start)
            sub_end = tline_tail.find(self.subst_end)

            head = tline_tail[:sub_start]
            sub = tline_tail[sub_start + len(self.subst_start) : sub_end]
            tail = tline_tail[sub_end + len(self.subst_end) :]

            subst_handler = subst_parser.parse(sub, tline_num=tline_num)

            if subst_handler.match_name is not None:
                match_cls = self.lookup_match_cls(subst_handler.match_name)
                if match_cls is None:
                    raise errors.BadTemplateError(
                        f'match named "{subst_handler.match_name}" not recognised',
                        tline_num=tline_num + 1,
                    )
                match = match_cls()
            elif subst_handler.fun_name is not None:
                match_cls = self.lookup_match_fun_cls(subst_handler.fun_name)
                if match_cls is None:
                    raise errors.BadTemplateError(
                        f'match function named "{subst_handler.fun_name}" not recognised',
                        tline_num=tline_num + 1,
                    )
                match = match_cls(*subst_handler.fun_args)

            if subst_handler.var_name is None:
                regex_str += re.escape(head) + '(?:' + match.regex + ')'
            else:
                cap_name = subst_handler.var_name.replace('.', '__dot__')
                if subst_handler.cast is not None:
                    cap_name += '__type_' + subst_handler.cast.__name__ + '__'

                regex_str += re.escape(head) + '(?P<' + cap_name + '>' + match.regex + ')'

                def gen_capproc_fun(match, pipes):
                    def capproc_fun_no_pipes(cap_val):
                        return match.post_proc(cap_val)

                    def capproc_fun_pipes(cap_val):
                        cap_val = match.post_proc(cap_val)
                        for pipe in pipes:
                            cap_val = pipe['fun'].exec(cap_val, *pipe['fun_args'])
                        return cap_val

                    if len(pipes) == 0:
                        return capproc_fun_no_pipes

                    return capproc_fun_pipes

                def add_pipe_fun(pipe):
                    fun_name = pipe['fun_name']
                    pipe_fun = self.lookup_fun_cls(fun_name)
                    if pipe_fun is None:
                        raise errors.BadTemplateError(
                            f'function named "{fun_name}" not recognised',
                            tline_num=tline_num + 1,
                        )

                    pipe['fun'] = pipe_fun
                    return pipe

                capproc_fmap[cap_name] = gen_capproc_fun(
                    match,
                    [add_pipe_fun(pipe) for pipe in subst_handler.pipes],
                )

            tline_tail = tail

        regex_str += re.escape(tline_tail)

        if flags['lax']:
            if len(regex_str) == 0 or regex_str[:3] != '^.*':
                regex_str = '^.*' + regex_str
            if len(regex_str) == 0 or regex_str[-3:] != '.*$':
                regex_str = regex_str + '.*$'
        else:
            if len(regex_str) == 0 or regex_str[0] != '^':
                regex_str = '^' + regex_str
            if len(regex_str) == 0 or regex_str[-1] != '$':
                regex_str = regex_str + '$'

        return self.CompiledTemplLine(
            raw,
            tline_num,
            min_matches,
            max_matches,
            None if len(capproc_fmap) == 0 else ret_rtype,
            var_name,
            tline,
            tline.find(self.subst_start) == -1,
            None if tline.find(self.subst_start) == -1 else regex_str,
            None if tline.find(self.subst_start) == -1 else re.compile(regex_str),
            'compound',
            capproc_fmap,
        )

    def _compile_prefix_r_tline(self, raw, subst_parser, tline, tline_num):
        (min_matches, max_matches, ret_rtype, tline, var_name, flags) = self._parse_tmodifiers(tline, tline_num)

        regex_str = tline
        capproc_fmap = {}

        if var_name is not None:
            cap_name = var_name.replace('.', '__dot__')

            regex_str = '(?P<' + cap_name + '>' + regex_str + ')'

            capproc_fmap[var_name] = lambda x: x

        if flags['lax']:
            if len(regex_str) == 0 or regex_str[:3] != '^.*':
                regex_str = '^.*' + regex_str
            if len(regex_str) == 0 or regex_str[-3:] != '.*$':
                regex_str = regex_str + '.*$'
        else:
            if len(regex_str) == 0 or regex_str[0] != '^':
                regex_str = '^' + regex_str
            if len(regex_str) == 0 or regex_str[-1] != '$':
                regex_str = regex_str + '$'

        return self.CompiledTemplLine(
            raw,
            tline_num,
            min_matches,
            max_matches,
            None if var_name is None else ret_rtype,
            var_name if var_name != '.' else None,
            tline,
            False,
            regex_str,
            re.compile(regex_str),
            'simple',
            capproc_fmap,
        )

    def _parse_tmodifiers(self, tline, tline_num):
        match = self._match_prefix_re.match(tline)

        def flags_to_bool_map_dict(flags):
            """Convert string like `'foo,!bar'` to `{'foo': True, 'bar': True}` and apply defaults."""

            return {
                **{'lax': False},
                **{k[1:] if k[0] == '!' else k: k[0] != '!' for k in (flags.split(',') if flags is not None else [])},
            }

        if match:
            repeat_modifier = match.group('repeat_modifier')

            min_matches = None
            max_matches = None
            ret_rtype = None

            if repeat_modifier == '':
                min_matches = 1
                max_matches = 1
                ret_rtype = dict
            elif repeat_modifier == '*':
                min_matches = 0
                max_matches = math.inf
                ret_rtype = list
            elif repeat_modifier == '+':
                min_matches = 1
                max_matches = math.inf
                ret_rtype = list
            elif repeat_modifier == '?':
                min_matches = 0
                max_matches = 1
                ret_rtype = list
            elif repeat_modifier[0] == '{':
                min_matches = int(match.group('rm_min'))
                max_matches = int(match.group('rm_max')) if match.group('rm_max') else math.inf
                ret_rtype = list
            else:
                raise errors.BadTemplateError(
                    f'modifier not supported, line "{tline}" processing failed',
                    tline_num=tline_num + 1,
                )

            return (
                min_matches,
                max_matches,
                ret_rtype,
                match.group('tail'),
                match.group('var_name'),
                flags_to_bool_map_dict(match.group('flags')),
            )

        raise errors.BadTemplateError(
            f'modifier not supported, line "{tline}" did not match',
            tline_num=tline_num + 1,
        )

    def parse(self, in_text):
        """Parse the input text and return the result."""

        inlines = in_text.split('\n')
        if self._itlel and len(inlines) > 0 and inlines[-1] == '':
            inlines.pop()

        out_struct = None
        ctlines = self._comp_template
        tline_num = 0
        inline_num = 0

        while inline_num < len(inlines) and tline_num < len(ctlines) > 0:
            ctline = ctlines[tline_num]
            self._log.debug('processing template (line %d): %s', ctline.line_num + 1, ctline.raw)

            (numof_inlines_consumed, add_out_struct) = self._regex_consume(
                ctline,
                inlines,
                inline_num,
            )

            if add_out_struct is None:
                self._log.debug(
                    'template (line %d) matched %d input lines (no data)',
                    ctline.line_num + 1,
                    numof_inlines_consumed,
                )
            else:
                self._log.debug(
                    'template (line %d) matched %d input lines (%s data)',
                    ctline.line_num + 1,
                    numof_inlines_consumed,
                    type(add_out_struct).__name__,
                )

            inline_num += numof_inlines_consumed
            if out_struct is None:
                out_struct = add_out_struct
            elif add_out_struct is not None:
                if isinstance(out_struct, dict) and isinstance(add_out_struct, dict):
                    out_struct = utils.dict_deepmerge(out_struct, add_out_struct)
                elif isinstance(out_struct, list) and isinstance(add_out_struct, list):
                    out_struct = out_struct + add_out_struct
                elif isinstance(out_struct, list) and isinstance(add_out_struct, dict) and self._allow_mixed_lists:
                    out_struct.append(add_out_struct)
                else:
                    raise errors.RunError(
                        f'output merge type conflict {type(out_struct).__name__}'
                        f' vs {type(add_out_struct).__name__}',
                        inline_num=inline_num + 1,
                        tline_num=ctline.line_num + 1,
                    )

            tline_num += 1

        if inline_num < len(inlines) and tline_num == len(ctlines):
            raise errors.LeftoverInputError(
                'template finished but input line(s) remaining',
                inline_num=inline_num + 1,
            )
        if tline_num < len(ctlines) and inline_num == len(inlines):
            raise errors.NoMoreInputError(
                'all input consumed but template unfinished',
                tline_num=ctline.line_num + 1,
            )

        return out_struct

    def _regex_consume(self, ctline, inlines, inline_num):
        def regex_caps_to_data(caps, capproc_fmap):
            for k in list(caps.keys()):
                if '__dot__' in k:
                    klist = k.split('__dot__')
                    kleaf = klist.pop()
                    subcaps = caps
                else:
                    klist = []
                    kleaf = k

                subcaps = caps
                kval = caps[k]
                ktype = None

                if '__type_' in kleaf:
                    tname = kleaf[kleaf.find('__') + 7 : -2]
                    kleaf = kleaf[: kleaf.find('__')]
                    ktype = __builtins__[tname]

                if '__' in k:
                    del caps[k]

                for subk in klist:
                    if subk not in subcaps:
                        subcaps[subk] = {}
                    subcaps = subcaps[subk]

                subcaps[kleaf] = capproc_fmap[k](kval)
                if ktype is not None:
                    subcaps[kleaf] = ktype(subcaps[kleaf])

            return caps

        match_data = None if ctline.ret_rtype is None else ctline.ret_rtype()
        match_count = 0

        while match_count < ctline.max_matches and inline_num + match_count < len(inlines):
            if ctline.plain_match:
                if inlines[inline_num + match_count] == ctline.plain:
                    self._log.debug(
                        'matched input (line %d) without data (%d/%s-%s): %s',
                        inline_num + 1,
                        match_count,
                        ctline.min_matches,
                        ctline.max_matches,
                        inlines[inline_num],
                    )
                    match_count += 1
                else:
                    break

            elif ctline.regex:
                self._log.debug('attempting match against: %s', ctline.regex_str)

                match = ctline.regex.match(inlines[inline_num + match_count])
                if match:
                    self._log.debug(
                        'matched input (line %d)%s entry (%d/%s-%s): %s',
                        inline_num + match_count + 1,
                        '' if match_data is None else ' to ' + type(match_data).__name__,
                        match_count,
                        ctline.min_matches,
                        ctline.max_matches,
                        inlines[inline_num + match_count],
                    )
                    match_count += 1
                    if type(match_data) == dict:
                        match_data = regex_caps_to_data(match.groupdict(), ctline.capproc_fmap)
                    elif type(match_data) == list:
                        if ctline.present == 'compound':
                            match_data.append(regex_caps_to_data(match.groupdict(), ctline.capproc_fmap))
                        elif ctline.present == 'simple':
                            match_data.append(match.group(0))
                else:
                    break

        if match_count < ctline.min_matches:
            raise errors.ParseFailedError(
                f'no match ({ctline.min_matches}-{ctline.max_matches} required' f' but {match_count} matches made)',
                inline_num=inline_num + 1,
                tline_num=ctline.line_num + 1,
            )

        if match_data is None:
            return (match_count, None)

        if type(match_data) == dict:
            return (match_count, match_data)

        if type(match_data) == list:
            return (
                match_count,
                match_data if ctline.var_name is None else {ctline.var_name: match_data},
            )

        raise errors.InternalError(
            f'type switch return malfunction, unhandled {repr(type(match_data))}',
            inline_num=inline_num + 1,
            tline_num=ctline.line_num + 1,
        )

    def lookup_match_cls(self, name):
        """Lookup match by name."""

        return self.Match.lookup(name)

    def lookup_match_fun_cls(self, name):
        """Lookup match function by name."""

        return self.MatchFun.lookup(name)

    def lookup_fun_cls(self, name):
        """Lookup function by name."""

        return self.Function.lookup(name)
