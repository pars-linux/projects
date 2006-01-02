#!/usr/bin/python
# -*- coding: utf-8 -*-

import kompiter
import socket


class Irc(kompiter.Network):
    def __init__(self, bot):
        kompiter.Network.__init__(self, bot)
        self.sock = None
        self.buffer = ""
    
    def connect(self, servername, nickname, password):
        self.sock = socket.socket()
        self.sock.connect((servername, 6666))
        self._send("NICK %s" % nickname)
        self._send("USER pardus linux irc.freenode.net :kompiter")
        self._send("PRIVMSG NICKSERV : IDENTIFY %s" % nickname)
        self.nickname = nickname
    
    def disconnect(self):
        self._send("QUIT :%s has left the building" % nickname)
        self.sock.close()
        self.sock = None
        self.buffer = ""
    
    def fileno(self):
        return self.sock.fileno()
    
    def _send(self, command):
        print "[[%s]]" % command
        self.sock.sendall(command)
        self.sock.sendall("\r\n")
    
    def _skip(self, data):
        t = data.find(' ') + 1
        if data[t] == ':':
            t += 1
        return data[t:]
    
    def _parse(self, data):
        print "[", data, "]"
        nick = None
        if data[0] == ":":
            tmp = data[:data.find(' ')]
            if tmp.find('!') != -1:
                nick = tmp[1:tmp.find('!')]
            data = data[data.find(' ') + 1:]
        
        if data.startswith("JOIN "):
            data = self._skip(data)
            if nick and nick != self.nickname:
                r = self.findRoom(data)
                if r:
                    self.joinUser(r, nick)
            else:
                self.linkRoom(data)
        
        elif data.startswith("NICK "):
            data = self._skip(data)
            self.nickUser(None, nick, data)
        
        elif data.startswith("QUIT "):
            self.quitUser(nick)
        
        elif data.startswith("PART "):
            data = self._skip(data)
            data = data.split(' ', 1)[0]
            r = self.findRoom(data)
            if r:
                self.partUser(r, self.findUser(r, nick))
        
        elif data.startswith("KICK "):
            data = self._skip(data)
            # FIXME
        
        elif data.startswith("PRIVMSG "):
            data = self._skip(data)
            data = data.split(' ', 1)
            if len(data) < 2:
                return
            rname, msg = data
            if msg[0] == ':':
                msg = msg[1:]
            r = self.findRoom(rname)
            if r:
                self.talkRoom(r, self.findUser(r, nick), msg)
            else:
                u = kompiter.User(self, nick)
                self.messageUser(u, msg)
        
        elif data.startswith("353 "):
            data = data[4:]
            data = data[data.find(' ') + 1:]
            data = data[data.find(' ') + 1:]
            chan, rest = data.split(' ', 1)
            r = self.findRoom(chan)
            if not r:
                return
            if rest[0] == ':':
                rest = rest[1:]
            users = rest.split(' ')
            for u in users:
                if u != "":
                    if u[0] == '@':
                        self.joinUser(r, u[1:])
                    else:
                        self.joinUser(r, u)
    
    def receive(self):
        self.buffer += self.sock.recv(1024)
        while True:
            i = self.buffer.find("\r\n")
            if i == -1:
                break
            data = self.buffer[:i]
            self._parse(data)
            self.buffer = self.buffer[i+2:]
    
    def join(self, roomname):
        self._send("JOIN %s" % roomname)
    
    def talk(self, room, msg):
        self._send("PRIVMSG %s :%s" % (room.name, msg))
    
    def action(self, room, msg):
        self._send("PRIVMSG %s :\001ACTION %s\001" % (room.name, msg))
    
    def message(self, user, msg):
        self._send("PRIVMSG %s :%s" % (user.nick, msg))
