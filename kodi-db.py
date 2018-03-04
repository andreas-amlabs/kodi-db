#!/usr/bin/env python

# This script connects to Kodi via WS and queries for current
# video player. If anything is playing it will try to store
# that name in a dB
# This is a personal mini trakt.tv like script

import threading
import sys
from websocket import create_connection
import json
import getopt

from pymongo import MongoClient
from datetime import datetime

KODI_VIDEOPLAYER_ID=1

#Event
#{"jsonrpc":"2.0","method":"Player.OnPlay","params":{"data":{"item":{"title":"A movie.mkv","type":"movie"},"player":{"playerid":1,"speed":1}},"sender":"xbmc"}}


class KodiWS (threading.Thread):
    ws = None
    kodi_host = None
    sql_host = None
    #sql_db = client.kodi
    #sql_schema = watched.movies

    def __init__(self, kodi_host, sql_host):
        threading.Thread.__init__(self)
        self.kodi_host = kodi_host
        self.sql_host = sql_host
        #print "Using Kodi Host:%s" % (self.kodi_host)
        #print "Using SQL Host:%s" % (self.sql_host)

        self.ws = create_connection("ws://" + self.kodi_host + "/jsonrpc")
        self.client = MongoClient(self.sql_host)
        self.db = self.client.kodi

    def __del__(self):
        if self.ws:
            self.ws.close()

    def run(self):

        if self.ws:
            try:
               self.query()
            except:
               pass


    def contains(self, name, label):
        result=self.db.watched.movies.find({"label" : label})
        return not result.count() == 0

    def write(self, json_data):
        result=self.db.watched.movies.insert_one(json_data)

    def send(self, data):
        self.ws.send(json.dumps(data))
        result = self.ws.recv()
        return result

    def query(self):
        data = {"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": KODI_VIDEOPLAYER_ID}
        r = json.loads(self.send(data))
        if r['result']:
            ##Result: {"id":1,"jsonrpc":"2.0","result":[{"playerid":1,"type":"video"}]}
            # Have active player, check item playing
            data = {"jsonrpc": "2.0", "id": 1, "method": "Player.GetItem", "params": {"properties": [ "file"], "playerid": KODI_VIDEOPLAYER_ID}, "id": "VideoGetItem"}
            r = json.loads(self.send(data))
            #print("Rsp: %s" % str(r))

            if r['result'] and r['result']['item'] and r['result']['item']['file']:
                ##Rsp: {u'jsonrpc': u'2.0', u'id': u'VideoGetItem',
                ##      u'result': {u'item': {u'type': u'unknown',
                ##                            u'file': u'nfs://1.2.3.4/mov/A directory/A movie.mkv',
                ##                            u'label': u'A movie.mkv'}}}
                file_path = r['result']['item']['file'].split('/')
                directory = str(file_path[5])
                file_name = str(file_path[-1])
                #print("Directory: %s" % directory)
                #print("File     : %s" % file_name)

                json_data = {
                    "name" : directory,
                    "label" : file_name,
                    "date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                # Special output captured by Home-Assistant cli sensor
                print("%s\n" % json.dumps(json_data))
                if not self.contains(directory, file_name):
                    self.write(json_data)


def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "k:s:", ["kodi=", "sql="])
    except getopt.GetoptError:
        sys.exit(2)

    sql_host = None
    kodi_host = None

    for opt, arg in opts:
        if opt in ("-s", "--sql"):
            sql_host = arg
        elif opt in ("-k", "--kodi"):
            kodi_host = arg

    try:
        kodi = KodiWS(kodi_host, sql_host)
        kodi.start()
        kodi.join()
    except:
        #print("Kodi querying failed")
        pass


if __name__ == "__main__":
    main(sys.argv)
