# This file is placed in the Public Domain.


"todo items"


def __dir__():
    return (
        "todo"
    )


import time



from ocl import Class
from ocm import Command
from odb import find, fntime, save
from obj import Object
from opr import aliases, elapsed


class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


def todo(event):
    if not event.rest:
        nr = 0
        for fn, o in find("todo"):
            event.reply("%s %s %s" % (nr, o.txt, elapsed(time.time() - fntime(fn))))
        return
    o = Todo()
    o.txt = event.rest
    save(o)
    event.reply("ok")


Class.add(Todo)
Command.add(todo)
aliases.tdo = "todo"
