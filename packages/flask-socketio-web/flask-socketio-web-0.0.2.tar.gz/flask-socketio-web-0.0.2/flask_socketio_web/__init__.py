# -*- coding: utf-8 -*-
import inspect
import os
import sys
import socketio
from flask import Flask
from loguru import logger
from rich.console import Console
from rich.table import Table
from flask_socketio_web.action import get_actions

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)
console = Console()


class FlaskSocketioWeb(object):
    def __init__(self, scan="action", namespace=False, base_route="/"):
        self.sio = socketio.Server(cors_allowed_origins="*")
        self.app = Flask(__name__, instance_path="/{project_folder_abs_path}/instance")
        self.app.config['SECRET_KEY'] = os.urandom(24)
        self.app.wsgi_app = socketio.WSGIApp(self.sio, self.app.wsgi_app)
        self.base_route = base_route
        self.namespace = namespace
        self.scan = scan
        self.regist()

    def regist(self):
        acts = get_actions(self.scan)
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("evevt")
        table.add_column("nsp")
        table.add_column("methods")
        table.add_column("rule")
        for cls in acts:
            if len(cls.ajax_map) == 0 and len(cls.sio_map) == 0:
                continue
            base_name = getattr(cls, "__basename__",
                                str(cls.__class__.__name__)[0].lower() + str(cls.__class__.__name__)[1:])
            for key in cls.ajax_map:
                func = getattr(cls, key)
                ajax = cls.ajax_map[key]
                rule = os.path.join(self.base_route, base_name, key)

                self.app.add_url_rule(rule=rule,
                                      view_func=func,
                                      methods=ajax["methods"])
                table.add_row("-", "-", ','.join(ajax["methods"]), rule)

            for key in cls.sio_map:
                func = getattr(cls, key)
                if not hasattr(cls, "sio"):
                    setattr(cls, "sio", self.sio)
                sio = cls.sio_map[key]
                namespace = sio["namespace"]
                event = sio["event"]
                if namespace is None:
                    if self.namespace:
                        namespace = os.path.join("/" + base_name)
                    else:
                        namespace = "/"
                if not self.namespace:
                    event = base_name + "." + event

                @self.sio.on(event, namespace=namespace)
                def message_handler(sid, msg, cls=cls):
                    args = inspect.getfullargspec(func)
                    if len(args.args) == 1:
                        response = func(cls)
                    elif len(args.args) == 2:
                        response = func(cls, msg)
                    else:
                        response = func(cls, sid, msg)
                    return response

                table.add_row(event, namespace, "-", "-")
        console.print(table)

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
