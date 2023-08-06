from flask import Flask
from gevent.pywsgi import WSGIServer

from evomaster_client.controller.em_controller import controller

HOST = '127.0.0.1'
PORT = 40100


def run_em(sut_handler, host=HOST, port=PORT) -> None:
    app = Flask(__name__)
    app.register_blueprint(controller(sut_handler))
    server = WSGIServer((host, port), app)
    server.serve_forever()
    return server
