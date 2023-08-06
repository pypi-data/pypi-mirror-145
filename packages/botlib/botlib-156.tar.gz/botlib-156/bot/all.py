# This file is placed in the Public Domain.


"all modules"


def __dir__():
    return (
        "fnd",
        "log",
        "irc",
        "rss",
        "sts",
        "tdo",
        "udp",
        "usr"
    )


from otb import Table


from bot import fnd
from bot import log
from bot import irc
from bot import rss
from bot import sts
from bot import tdo
from bot import udp
from bot import usr


for mn in __dir__():
    md = getattr(locals(), mn, None)
    if md:
        Table.add(md)
