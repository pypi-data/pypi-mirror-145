"""Matches included as standard in the core."""

from ..ext.match import Match
from ..ext.register import register


@register()
class IntegerCoreMatch(Match):
    """Integer match."""

    name = 'integer'
    regex = r'\d+'
    cast = int


@register()
class NonWhiteSpaceCoreMatch(Match):
    """Non white space match."""

    name = 'non_ws'
    regex = r'\S+'


@register()
class WordCoreMatch(Match):
    """Word match."""

    name = 'word'
    regex = r'\w+'


@register()
class WhiteSpaceCoreMatch(Match):
    """White space match."""

    name = 'ws'
    regex = r'\s+'


@register()
class StringCoreMatch(Match):
    """String match (any text up to the end of the line)."""

    name = 'string'
    regex = r'.*'


@register()
class HostnameCoreMatch(Match):
    """Hostname match."""

    name = 'hostname'
    regex = r'(?:[a-zA-Z][a-zA-Z0-9]*\.)*[a-zA-Z][a-zA-Z0-9]*'


@register()
class IPv4AddrCoreMatch(Match):
    """IPv4 address match."""

    name = 'ipaddr'
    regex = (
        r'(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?|0)' r'(?:\.(?:25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?|0)){3}'
    )


@register()
class NumberCoreMatch(Match):
    """Number match (floating point, though a decimal is not required so it will match integers too)."""

    name = 'number'
    regex = r'\d+(?:\.\d+|)'
    cast = float


@register()
class CiscoIosXrCmdDatetimeCoreMatch(Match):
    """Cisco IOS-XR command response date time match."""

    name = 'cisco_iosxr_cmd_dt'
    regex = (
        r'(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)'
        r'\s+(?:Jan|Feb|Mar:Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
        r'\s+\d+\s+\d\d:\d\d:\d\d.\d+'
        r'\s+\S+'
    )
