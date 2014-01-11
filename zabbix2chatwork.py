#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib
import urllib2
import json


token_and_postroom = unicode(sys.argv[1], encoding='utf-8')
chatwork_api_token, post_to = token_and_postroom.split(u":")

post_subject = unicode(sys.argv[2], encoding='utf-8')
post_message = unicode(sys.argv[3], encoding='utf-8')

https_header = {"X-ChatWorkToken": chatwork_api_token}


def getRoomIdByName(search_name):
    url = "https://api.chatwork.com/v1/rooms"
    req = urllib2.Request(url, None, https_header)

    response = urllib2.urlopen(req).read()

    rooms = json.loads(response)

    for room in rooms:
        if unicode(room["name"]) == unicode(search_name):
            return room["room_id"]
        else:
            continue

    return False


def postMessage(room_id, subject, message):
    url = "https://api.chatwork.com/v1/rooms/%s/messages"
    subject = subject.encode('utf-8')
    message = message.encode('utf-8')
    message_body = urllib.quote("%s\n[info]%s[/info]" % (subject, message))

    req = urllib2.Request(url % room_id,
                          "body=%s" % message_body,
                          https_header)

    response = urllib2.urlopen(req).read()
    return json.loads(response)


class RoomNameError(Exception):
    pass


room_id = getRoomIdByName(post_to)

try:
    if room_id is False:
        raise RoomNameError
except RoomNameError as e:
    print "Error"

postMessage(room_id, post_subject, post_message)

sys.exit()
