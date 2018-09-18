#!/usr/bin/env python

import sys
import json
import getopt

from pymongo import MongoClient
from datetime import datetime

class DB:
    def __init__(self, sql_host, content, title):
        self.sql_host = sql_host 
        self.client = MongoClient(self.sql_host)
        self.db = self.client.kodi

        json_data = {
            "name" : content,
            "label" : title,
            "date" : datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        # Special output captured by Home-Assistant cli sensor
        print("%s\n" % json.dumps(json_data))
        if not self.contains(title):
            self.write(json_data)
        self.client.close()

    def contains(self, title):
        result=self.db.watched.movies.find({"label" : title})
        return not result.count() == 0

    def write(self, json_data):
        result=self.db.watched.movies.insert_one(json_data)


def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "s:c:t:", ["sql=", "content=", "title="])
    except getopt.GetoptError:
        sys.exit(2)

    sql_host = None
    content = None
    title = None

    for opt, arg in opts:
        if opt in ("-c", "--content"):
            content = arg
        elif opt in ("-t", "--title"):
            title = arg
        elif opt in ("-s", "--sql"):
            sql_host = arg

    try:
        DB(sql_host, content, title)
    except:
        pass


if __name__ == "__main__":
    main(sys.argv)
