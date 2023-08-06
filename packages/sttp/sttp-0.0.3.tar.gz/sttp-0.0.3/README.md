# Strict Text Template Parse (sttp) [![test](https://github.com/mwri/sttp/actions/workflows/test.yml/badge.svg)](https://github.com/mwri/sttp/actions/workflows/test.yml) [![codecov](https://codecov.io/gh/mwri/sttp/branch/main/graph/badge.svg?token=FZXOQQR4QM)](https://codecov.io/gh/mwri/sttp) [![Documentation Status](https://readthedocs.org/projects/py-sttp/badge/?version=latest)](https://py-sttp.readthedocs.io/en/latest/?badge=latest)

Please see [full documentation on readthedocs](https://py-sttp.readthedocs.io/en/latest/).

STTP allows you to parse text strictly (see [why strict parsing](#why-strict-parsing)
below for a discussion on why parsing should be strict) but very easily, using
a template which can be built by copying some sample output, marking the bits which
change, and adding simple prefixes to the lines to indicate where they can recur
multiple times.

Parsing is often a choice between doing something pragmatic, quick and
dirty and getting stuff done... or spending a lot more time doing something
better and more robust. STTP is about getting the best of both worlds, a
super robust solution that is also quick and easy.

To give you an quick idea, take this made up input:

```text
Num   Server               Uptime
1     wibble.domain.com    1d 5h
2     zap.domain.com       100d 1h
3     foobar.domain.com    3d 10h
```

You can parse this with this template:

```text
m> Num   Server               Uptime
m*> {{ num = integer }}{{ ws }}{{ server = non_ws }}{{ ws }}{{ uptime = string }}
```

The result would be:

```python
[
    {'num': 1, 'server': 'wibble.domain.com', 'uptime': '1d 5h'},
    {'num': 2, 'server': 'zap.domain.com',    'uptime': '100d 1h'},
    {'num': 3, 'server': 'foobar.domain.com', 'uptime': '3d 10h'},
]
```

You would do it like this:

```python
parser = sttp.Parser(template = in_template)
out_struct = parser.parse(in_text)
```

Another quick example parsing the output of a ping command (such as `ping -c3 dns.google`):

```text
PING dns.google (8.8.4.4) 56(84) bytes of data.
64 bytes from dns.google (8.8.4.4): icmp_seq=1 ttl=54 time=11.7 ms
64 bytes from dns.google (8.8.4.4): icmp_seq=2 ttl=54 time=12.5 ms
64 bytes from dns.google (8.8.4.4): icmp_seq=3 ttl=54 time=11.7 ms

--- dns.google ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 11.719/11.973/12.465/0.347 ms
```

This can be achieved with this template:

```text
m> PING {{ target = hostname }} ({{ ipaddr = ipaddr }}) {{ integer }}({{ integer }}) bytes of data.
m*(replies)> {{ len = integer }} bytes from {{ target = hostname }} ({{ ipaddr = ipaddr }}): icmp_seq={{ seq = integer }} ttl={{ ttl = integer }} time={{ latency = number }} ms
m>
m> --- {{ target = hostname }} ping statistics ---
m> {{ stats.transmitted = integer }} packets transmitted, {{ stats.received = integer }} received, {{ stats.loss = integer }}% packet loss, time {{ stats.time = number }}ms
m> rtt min/avg/max/mdev = {{ stats.min = number }}/{{ stats.avg = number }}/{{ stats.max = number }}/{{ stats.mdev = number }} ms
```

The result would be:

```python
{
    'ipaddr': '8.8.4.4',
    'target': 'dns.google',
    'replies': [
        {'len': 64, 'target': 'dns.google', 'ipaddr': '8.8.4.4', 'seq': 1, 'ttl': 54, 'latency': 11.7},
        {'len': 64, 'target': 'dns.google', 'ipaddr': '8.8.4.4', 'seq': 2, 'ttl': 54, 'latency': 12.5},
        {'len': 64, 'target': 'dns.google', 'ipaddr': '8.8.4.4', 'seq': 3, 'ttl': 54, 'latency': 11.7},
    ],
    'stats': {
        'transmitted': 3,
        'received': 3,
        'loss': 0,
        'time': 2002.0,
        'min': 11.719,
        'max': 12.465,
        'avg': 11.973,
        'mdev': 0.347,
    },
}
```

## Why strict parsing?

To give you an quick idea of the parsing problems that can arise with the simplest of
cases, take this made up input (the same input is used in the quick start):

```text
Num   Server               Uptime
1     wibble.domain.com    1d 5h
2     zap.domain.com       100d 1h
3     foobar.domain.com    3d 10h
```

You can parse this simply like this:

```python
>>> import re
>>> in_text = '''Num   Server               Uptime
... 1     wibble.domain.com    1d 5h
... 2     zap.domain.com       100d 1h
... 3     foobar.domain.com    3d 10h
... '''
>>> out_struct = [
...     entry.groupdict() for entry in
...     [re.match(r'(?P<num>\d+)\s+(?P<server>\S+)\s+(?P<uptime>\d+d \d+h)', line)
...         for line in in_text.split('\n')]
...     if entry is not None
... ]
>>> assert out_struct == [
...     {'num': '1', 'server': 'wibble.domain.com', 'uptime': '1d 5h'},
...     {'num': '2', 'server': 'zap.domain.com',    'uptime': '100d 1h'},
...     {'num': '3', 'server': 'foobar.domain.com', 'uptime': '3d 10h'}
... ], out_struct
```

This sort of parsing can be a quick and pragmatic way to get what you want but even this is not
nearly as fast to write (and maintain) as using STTP, and there are pitfalls. For example if
the output was completely unexpected, an error instead of the table for example, then the parse
would still succeed! The result would be an empty array, but that might be perfectly legitimate
if it wasn’t for the error. Or, what if there were table entries but with an error or warning as
well. Of course you could check explicitly for errors you know about, or maybe you can recognise
errors generally, but if there is an unexpected error or the error reporting format changes, you
could be back to getting an empty array with an error check that doesn’t see an error any more.
This sort of parsing is not strict, and it can be dangerous.

Naturally you can implement extremely strict parsing which will only tolerate exactly what you
know of the text you are parsing and nothing else. Let’s see what that could look like in this
example:

```python
>>> in_text = '''Num   Server               Uptime
... 1     wibble.domain.com    1d 5h
... 2     zap.domain.com       100d 1h
... 3     foobar.domain.com    3d 10h
... '''
>>> lines = in_text.split('\n')
>>> if len(lines) == 0:
...     raise Exception('input is empty')
>>> header = lines.pop(0)
>>> if header != 'Num   Server               Uptime':
...     raise Exception('input line 1 was not recognised header: ' + header)
>>> out_struct = []
>>> while lines:
...     line = lines.pop(0)
...     match = re.match(r'(?P<num>\d+)\s+(?P<server>\S+)\s+(?P<uptime>\d+d \d+h)', line)
...
...     if match:
...         out_struct.append(match.groupdict())
...     elif line != '' or len(lines) != 0:
...         raise Exception('unexpected line parsing table entries: ' + line)
>>> assert out_struct == [
...     {'num': '1', 'server': 'wibble.domain.com', 'uptime': '1d 5h'},
...     {'num': '2', 'server': 'zap.domain.com',    'uptime': '100d 1h'},
...     {'num': '3', 'server': 'foobar.domain.com', 'uptime': '3d 10h'}
... ], out_struct
```

There’s nothing difficult about this, but WOW, 14 lines of code, it’s a long way from that
pragmatic one liner, and it would take you a LOT longer to write it than the STTP template
version, where the only interesting bit is the template:

```text
m> Num   Server               Uptime
m*> {{ int num = integer }}{{ ws }}{{ server = non_ws }}{{ ws }}{{ uptime = string }}
```

### Fail fast

In parsing terms this means “only accept what you know, handle it correctly and crash for
any unknown”. That is a Fail fast approach. Fail fast advocates that if something unexpected
happens it’s better to fail immediately and clearly with all the context of the failure
intact, than try to carry on with possibly invalid results (and no way of knowing it), causing
any number of side effects later, such as an exception not obviously related to the parse at
all, or simply incorrect data, and maybe that data could be put in a database, and there’s
probably no chance anyone will easily figure out why that bit of data is wrong this time
next week…

Fail fast might mean that something crashes in production that wouldn’t have if you had less
strict parsing, but isn’t that crash better than corrupting a database without knowing it?
A crash and stack trace at the right time can often provide developers all they need to
know to understand what went wrong, and with good monitoring, efficient agile toolchains
and release processes, a new unit test could have been written, the bug fixed, and a new
revision released to production in minutes!
