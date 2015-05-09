from __future__ import unicode_literals
import os

import tornado.web
from tornado.escape import json_encode

import json

from .. import mem

class RequestHandler(tornado.web.RequestHandler):
    instance = None

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST")
        self.set_header("Access-Control-Allow-Headers", "Accept, Authorization, Origin, Content-Type")
        self.set_header("Access-Control-Max-Age", "60480")
        
    def initialize(self, core, config, instance):
        self.core = core
        self.instance = instance

    def get(self, type):
        response = {}

        if(type == "queue"):
            response = self.instance.queue

        if(type == "playlist"):
            response = self.instance.playlist

        if(type == "shuffle"):
            response = self.instance.shuffled

        if(type == "all"):
            response = {
                "queue": self.instance.queue,
                "playlist": self.instance.playlist,
                "version": self.instance.version,
                "shuffle": self.instance.shuffled
            }

        self.write({"data": response, "version": self.instance.version})

    def post(self, type):
        response = {}

        # Get post body
        postdata = tornado.escape.json_decode(self.request.body)

        action = postdata["action"]
        data = postdata["data"]

        data = json.loads(data);

        if(type == "general"):
            if(action == "replace"):
                self.instance.replace_all(data)

        if(type == "queue"):
            if(action == "add"):
                self.instance.add_to_queue(data)

            if(action == "next"):
                self.instance.add_play_next(data)

            if(action == "remove"):
                self.instance.remove_from_queue(data)
                self.instance.remove_from_playlist(data)

            if(action == "clear"):
                self.instance.clear_queue()

            response = self.instance.queue

        if(type == "playlist"):
            if(action == "set"):
                self.instance.set_playlist(data)

            response = self.instance.playlist

        if(type == "shuffle"):
            if(action == "shuffle"):
                self.instance.shuffled = True;
                self.instance.shuffle_playlist(data)

            if(action == "resetshuffle"):
                self.instance.shuffled = False;
                self.instance.shuffle_reset()

            response = {
                "queue": self.instance.queue,
                "playlist": self.instance.playlist,
                "version": self.instance.version,
                "shuffle": self.instance.shuffled
            }

        self.write({"data": response, "version": self.instance.version})

    def options(self, type):
        self.write("")