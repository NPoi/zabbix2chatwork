#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
zabbix2chatwork
"""

import sys
import urllib
import urllib2
import re

__author__ = "Daisuke Nakahara <npoi.japan@gmail.com>"
__version__ = "0.0.5"
__date__ = "9 July 2016"


try:
    import simplejson as json
except ImportError:
    import json


class RoomNameError(Exception):
    """チャットが見つからなかった時の例外"""
    def __init__(self, room_name):
        self.room_name = room_name

    def __str__(self):
        return "Room name '{0}' not found in your ChatWork account.".format(self.room_name)


def getRoomIdByName(search_name, http_header):
    """自分のアカウントにある部屋を文字列から検索してIDを返す関数

        Keyword arguments:
        search_name -- チャットの名前

        Return arguments:
        room['room_id'] -- チャットのID
    """
    url = 'https://api.chatwork.com/v1/rooms'
    req = urllib2.Request(url, None, https_header)

    try:
        rooms = json.loads(urllib2.urlopen(req).read())
    except ValueError as e:
        sys.stderr.write("JSON encode error.")
        sys.exit()
    except TypeError as e:
        sys.stderr.write("JSON encode error.")
        sys.exit()
    except URLError as e:
        sys.stderr.write(e.code)
        sys.exit()

    for room in rooms:
        if unicode(room['name']) == unicode(search_name):
            return room['room_id']
        else:
            continue

    raise RoomNameError(search_name)


def postMessage(room_id, subject, message, http_header):
    """チャットワークに投稿する関数

    Keyword arguments:
    room_id -- チャットのID
    subject -- Zabbixアラートの題名
    message -- Zabbixアラートの本文

    Return arguments:
    json.loads(response)  -- ChatWork APIからのレスポンス
    """

    url = 'https://api.chatwork.com/v1/rooms/{0}/messages'.format(room_id)

    subject = subject.encode('utf-8')
    message = message.encode('utf-8')
    message_body = urllib.quote_plus("[info][title]{0}[/title][code]{1}[/code][/info]".format(subject, message))

    req = urllib2.Request(url,
                          "body={0}".fortat(message_body),
                          https_header)

    try:
        response = urllib2.urlopen(req).read()
    except URLError as e:
        sys.stderr.write(str(e.code))
        sys.exit()

    try:
        return json.loads(response)
    except ValueError as e:
        sys.stderr.write("JSON encode error.")
        sys.exit()
    except TypeError as e:
        sys.stderr.write("JSON encode error.")
        sys.exit()


def getRooms(url, http_header):
    u"""自分の部屋一覧を取得
    """
    url = 'https://api.chatwork.com/v1/rooms'
    req = urllib2.Request(url, None, https_header)

    try:
        my_rooms = json.loads(urllib2.urlopen(req).read())
    except ValueError:
        sys.stderr.write("JSON encode error.")
        sys.exit()
    except TypeError:
        sys.stderr.write("JSON encode error.")
        sys.exit()

    if len(my_rooms) == 0:
        sys.exit()

    else:
        return [room['room_id'] for room in my_rooms]

u"""
実際の処理
"""

if __name__ == '__main__':
    # 入力
    try:
        token_and_postroom = unicode(sys.argv[1], encoding='utf-8')
        post_subject = unicode(sys.argv[2], encoding='utf-8')
        post_message = unicode(sys.argv[3], encoding='utf-8')

    except IndexError:
        sys.stderr.write("Argument error.")
        sys.exit()

    except UnicodeDecodeError:  # UTF-8として受け取って例外吐いたらcp932として受け取る（Windows対策）
        try:
            token_and_postroom = unicode(sys.argv[1], encoding='cp932')
            post_subject = unicode(sys.argv[2], encoding='cp932')
            post_message = unicode(sys.argv[3], encoding='cp932')
        except UnicodeDecodeError:
            try:
                token_and_postroom = unicode(sys.argv[1], encoding='euc_jp')
                post_subject = unicode(sys.argv[2], encoding='euc_jp')
                post_message = unicode(sys.argv[3], encoding='euc_jp')
            except UnicodeDecodeError:
                sys.stderr.write("Argument charset error.")
                sys.exit()

    chatwork_api_token, post_to = token_and_postroom.split(u":")

    https_header = {'X-ChatWorkToken': str(chatwork_api_token)}

    if re.search(u"^[0-9]+$", post_to) and int(post_to) in getRooms(https_header):
        room_id = post_to
    else:
        room_id = getRoomIdByName(post_to, https_header)

    postMessage(room_id, post_subject, post_message, https_header)

    sys.exit()
