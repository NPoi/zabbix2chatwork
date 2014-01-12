#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
zabbix2chatwork
"""

__auther__ = "Daisuke Nakahara <npoi.japan@gmail.com>"
__version__ ="0.0.1"
__date__ = "11 Jan 2014"

import sys
import urllib
import urllib2
import json


class RoomNameError(Exception):
    """チャットが見つからなかった時の例外"""
    def __init__(self, room_name):
        self.room_name = room_name

    def __str__(self):
        return "Room name '%s' not found in your ChatWork account." % (self.room_name)


def getRoomIdByName(search_name):
    """自分のアカウントにある部屋を文字列から検索してIDを返す関数

        Keyword arguments:
        search_name -- チャットの名前

        Return arguments:
        room['room_id'] -- チャットのID
    """
    url = 'https://api.chatwork.com/v1/rooms'
    req = urllib2.Request(url, None, https_header)

    response = urllib2.urlopen(req).read()

    rooms = json.loads(response)

    for room in rooms:
        if unicode(room['name']) == unicode(search_name):
            return room['room_id']
        else:
            continue

    raise RoomNameError


def postMessage(room_id, subject, message):
    """チャットワークに投稿する関数

    Keyword arguments:
    room_id -- チャットのID
    subject -- Zabbixアラートの題名
    message -- Zabbixアラートの本文
    
    Return arguments:
    json.loads(response)  -- ChatWork APIからのレスポンス
    """
    
    url = 'https://api.chatwork.com/v1/rooms/%s/messages' % room_id

    subject = subject.encode('utf-8')
    message = message.encode('utf-8')
    message_body = urllib.quote("[info][title]%s[/title]%s[/info]" % (subject, message))

    req = urllib2.Request(url,
                          "body=%s" % message_body,
                          https_header)

    response = urllib2.urlopen(req).read()
    return json.loads(response)


u"""
実際の処理
"""

# 入力
# UTF-8として受け取って例外吐いたらcp932として受け取る（Windows対策）
try:
    token_and_postroom = unicode(sys.argv[1], encoding='utf-8')
    post_subject = unicode(sys.argv[2], encoding='utf-8')
    post_message = unicode(sys.argv[3], encoding='utf-8')
except UnicodeDecodeError:
    token_and_postroom = unicode(sys.argv[1], encoding='cp932')
    post_subject = unicode(sys.argv[2], encoding='cp932')
    post_message = unicode(sys.argv[3], encoding='cp932')

chatwork_api_token, post_to = token_and_postroom.split(u":")
https_header = {'X-ChatWorkToken': chatwork_api_token}

room_id = getRoomIdByName(post_to)
postMessage(room_id, post_subject, post_message)

sys.exit()
