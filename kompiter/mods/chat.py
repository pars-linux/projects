#!/usr/bin/python
# -*- coding: utf-8 -*-

import kompiter


class Chat(kompiter.Module):
    def __init__(self, bot):
        kompiter.Module.__init__(self, bot)
    
    def roomTalkEvent(self, room, user, msg):
        if msg == "avast!":
            room.talk("%s: yarrrr!" % user.nick)


kompiter_module = {
    "name": "chat",
    "modclass": Chat
}
