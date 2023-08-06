# -*- coding: utf-8 -*-
import os
import sys

import socketio
from flask import Flask
from loguru import logger
import logging
from src.action import get_actions


# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)


class FlaskSocketioWeb(object):
    def __init__(self):
        self.sio = socketio.Server(cors_allowed_origins="*")
        self.app = Flask(__name__, instance_path="/{project_folder_abs_path}/instance")
        self.app.wsgi_app = socketio.WSGIApp(self.sio, self.app.wsgi_app)
        self.base = "/"
        self.regist()

    def regist(self):
        acts = get_actions()

        for cls in acts:
            for key in cls.ajax_map:
                ajax = cls.ajax_map[key]
                rule = os.path.join(self.base, cls.base_name, key)
                self.app.add_url_rule(rule=rule,
                                      view_func=getattr(cls(), key),
                                      methods=ajax["methods"])
                logger.info(f"regist ajax {','.join(ajax['methods'])}={rule}")
            for key in cls.sio_map:
                sio = cls.sio_map[key]
                namespace = os.path.join(self.base, cls.base_name, key)

                @self.sio.on(namespace=os.path.join(self.base, sio["namespace"]),
                             event=sio['event'])
                def my_custom_event(sid, data):
                    return sio["func"](self, sid, data)

                logger.info(f"regist sio namespace={namespace},event={sio['event']}")

    def run(self, host='0.0.0.0', port=8090, debug_server=None, debug=True):
        try:
            if len(sys.argv) > 1 and sys.argv[1] == 'debug' or debug_server:
                import pydevd_pycharm
                logger.warning("Debug Server")
                if debug_server is None:
                    pydevd_pycharm.settrace('0.0.0.0', port=19899, stdoutToServer=True, stderrToServer=True)
                else:
                    debug_host, debug_prot = debug_server.split(":")
                    pydevd_pycharm.settrace(debug_host, port=debug_prot, stdoutToServer=True, stderrToServer=True)

            logger.info(f"Running on port http://{host}:{port}")
            self.app.logger = logger
            self.app.run(host=host, port=port, threaded=True, debug=debug)

        except Exception as e:
            logger.exception(e)
