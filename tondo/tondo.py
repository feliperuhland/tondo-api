# -*- coding: utf-8 -*-

import os
import codecs
import datetime
import json
import random
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


def get_timestamp():
    '''Returns timestamp for response'''
    return str(datetime.datetime.utcnow())


def loadjsons():
    data_dir = '{}/{}'.format(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'data/')
    result_dict = dict()
    for json_file in os.listdir(data_dir):
        if json_file.endswith('.json'):
            result_dict.update({
                json_file.split('.')[0]: json.load(codecs.open('{}{}'.format(data_dir, json_file), 'r', encoding='utf-8'))
            })
    return result_dict


class MainHandler(tornado.web.RequestHandler):
    ''' Main Handler '''
    def prepare(self):
        self.set_header('Content-Type', 'application/json')
        self.add_header('Access-Control-Allow-Origin', '*')
        self.add_header(
            'Access-Control-Allow-Headers',
            'Origin, X-Requested-With, Content-Type, Accept'
        )
        self.set_status(200)

    def get_tip(self, subject):
        subject_dict = self.application.tips_json.get(subject)
        if subject_dict:
            return random.choice(subject_dict)


class TipHandler(MainHandler):
    def get(self, subject):
        tip = self.get_tip(subject)
        if tip:
            self.write(tornado.escape.json_encode({
                'timestamp': get_timestamp(),
                'tip': tip,
            }))
            return
        self.set_status(404)


class PingHandler(MainHandler):
    ''' Ping Handler '''
    def get(self):
        self.write(tornado.escape.json_encode({'ping': 'pong'}))


class Application(tornado.web.Application):
    ''' Application class '''
    def __init__(self):
        handlers = [
            (r'/tip/(\w+)', TipHandler),
            (r'/ping', PingHandler),
        ]
        settings = dict(
            debug=True,
        )
        self.tips_json = loadjsons()
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    ''' Main method '''
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
