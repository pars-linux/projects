#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import irc
import select


class User:
    def __init__(self, net, nick):
        self.net = net
        self.nick = nick
    
    def message(self, msg):
        self.net.message(self, msg)


class Room:
    def __init__(self, net, name):
        self.net = net
        self.name = name
        self.nr_users = 0
        self.users = {}
    
    def talk(self, msg):
        self.net.talk(self, msg)
    
    def action(self, msg):
        self.net.action(self, msg)


class Network:
    def __init__(self, bot):
        self.__bot = bot
        self.__rooms = {}
    
    def linkRoom(self, roomname):
        r = Room(self, roomname)
        self.__rooms[roomname] = r
        self.__bot.fireEvent("roomLinkEvent", r)
        return r
    
    def unlinkRoom(self, room):
        key = room.name
        if self.__rooms.has_key(key):
            self.__bot.fireEvent("roomUnlinkEvent", self.__rooms[key])
            del self.__rooms[key]
    
    def findRoom(self, roomname):
        if self.__rooms.has_key(roomname):
            return self.__rooms[roomname]
        return None
    
    def findUser(self, room, nick):
        if room.users.has_key(nick):
            return room.users[nick]
        return None
    
    def joinUser(self, room, nick):
        u = User(self, nick)
        room.users[nick] = u
        room.nr_users += 1
        self.__bot.fireEvent("userJoinEvent", room, user)
    
    def partUser(self, room, user):
        self.__bot.fireEvent("userPartEvent", room, user)
        del room.users[user.nick]
        room.nr_users -= 1
    
    def quitUser(self, nick):
        for r in self.__rooms:
            u = self.findUser(r, nick)
            if u:
                self.partUser(r, u)
    
    def nickUser(self, room, nick, new_nick):
        if room:
            u = self.findUser(room, nick)
            if u:
                u.nick = new_nick
        else:
            for r in self.__rooms:
                u = self.findUser(room, nick)
                if u:
                    u.nick = new_nick
    
    def kickUser(self):
        pass
    
    def talkRoom(self, room, user, msg):
        self.__bot.fireEvent("roomTalkEvent", room, user, msg)
    
    def messageUser(self, user, msg):
        self.__bot.fireEvent("userMessageEvent", user, msg)


class Module:
    def __init__(self, bot):
        self.__bot = bot
    
    # Events, override in your subclasses
    roomLinkEvent = None
    roomUnlinkEvent = None
    roomTalkEvent = None
    roomActionEvent = None
    userJoinEvent = None
    userPartEvent = None
    userNickEvent = None
    userMessageEvent = None
    timeTickEvent = None


class Kompiter:
    def __init__(self):
        self.networks = []
        self.modules = []
        self.poller = select.poll()
    
    def load_module(self, name):
        mod = __import__(name)
        print mod.kompiter_module
        m = mod.kompiter_module["modclass"](self)
        self.modules.append(m)
    
    def load_modules(self):
        old = sys.path
        sys.path.insert(0, "mods")
        for fn in os.listdir('mods'):
            if fn.endswith(".py"):
                self.load_module(fn[:-3])
        sys.path = old
    
    def start(self):
        while True:
            events = self.poller.poll(250)
            for event in events:
                for net in self.networks:
                    if net.fileno() == event[0]:
                        net.receive()
            else:
                self.fireEvent("timeTickEvent")
    
    def fireEvent(self, event, *args):
        for mod in self.modules:
            func = mod.__dict__[event]
            if func:
                func(*args)


if __name__ == "__main__":
    k = Kompiter()
    
    k.load_modules()
    
    irc = irc.Irc(k)
    irc.connect("chat.freenode.net", "kompiter", "lala")
    irc.join("#pardus-devel")
    k.networks.append(irc)
    k.poller.register(irc.fileno(), select.POLLIN)
    
    k.start()
