# This file is placed in the Public Domain.


"users"


from ocm import Command
from odb import find, save
from obj import Object, update
from opr import aliases


def __dir__():
    return (
        "NoUser",
        "Users",
        "delete",
        "meet"
    )


class NoUser(Exception):

    pass



class User(Object):

    def __init__(self, val=None):
        super().__init__()
        self.user = ""
        self.perms = []
        if val:
            update(self, val)


class Users(Object):

    userhosts = Object()

    def allowed(self, origin, perm):
        perm = perm.upper()
        origin = getattr(self.userhosts, origin, origin)
        user = self.get_user(origin)
        if user:
            if perm in user.perms:
                return True
        return False

    def delete(self, origin, perm):
        for user in self.get_users(origin):
            try:
                user.perms.remove(perm)
                save(user)
                return True
            except ValueError:
                pass

    def get_users(self, origin=""):
        s = {"user": origin}
        return find("user", s)

    def get_user(self, origin):
        u = list(self.get_users(origin))
        if u:
            return u[-1][-1]

    def perm(self, origin, permission):
        user = self.get_user(origin)
        if not user:
            raise NoUser(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            save(user)
        return user


def delete(event):
    if not event.args:
        event.reply("delete <username>")
        return
    selector = {"user": event.args[0]}
    for _fn, o in find("user", selector):
        o._deleted = True
        save(o)
        event.reply("ok")
        break


def meet(event):
    if not event.args:
        event.reply("meet <userhost>")
        return
    user = User()
    user.user = event.rest
    user.perms = ["USER"]
    save(user)
    event.reply("ok")


Command.add(delete)
Command.add(meet)
aliases.dlt = "delete"
aliases.met = "meet"
