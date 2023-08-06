import abc
import logging
import threading
from importlib import import_module

from gevent.pywsgi import WSGIServer

from evomaster_client.controller.sut_handler import SutHandler
from evomaster_client.instrumentation.import_hook import install_import_hook
from evomaster_client.instrumentation.ast_transformer import NO_INSTRUMENTATION


HOST = '127.0.0.1'
PORT = 5000


class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app

    def run(self):
        self.srv = WSGIServer(('', PORT), self.app)
        self.ctx = self.app.app_context()
        self.ctx.push()
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.stop()
        self.srv.close()


class FlaskHandlerError(Exception):
    pass


class FlaskHandler(SutHandler, metaclass=abc.ABCMeta):
    def __init__(self, instrumentation_level: int = NO_INSTRUMENTATION):
        self.server = None  # SUT is not running
        self.instrumentation_level = instrumentation_level

    def app(self):
        logging.info('Importing Flask application')
        module = import_module(self.flask_module())
        app = module.__getattribute__(self.flask_app())
        return app

    def instrumented_app(self):
        if self.instrumentation_level > 0:
            with install_import_hook(self.package_prefixes_to_cover(), self.instrumentation_level):
                return self.app()
        else:
            return self.app()

    @abc.abstractmethod
    def package_prefixes_to_cover(self):
        pass

    @abc.abstractmethod
    def flask_module(self):
        pass

    @abc.abstractmethod
    def flask_app(self):
        pass

    @abc.abstractmethod
    def get_url(self):
        return f'http://{HOST}:{PORT}'

    def start_sut(self):
        if self.is_sut_running():
            logging.info('Server is already running')
            return self.get_url()
        self.server = ServerThread(self.instrumented_app())
        self.server.start()
        return self.get_url()

    def stop_sut(self):
        if not self.is_sut_running():
            logging.info('Server is already stopped')
            return
        self.server.shutdown()
        self.server = None

    def is_sut_running(self):
        return bool(self.server)

    @abc.abstractmethod
    def reset_state_of_sut(self):
        pass

    @abc.abstractmethod
    def setup_for_generated_test(self):
        pass

    @abc.abstractmethod
    def get_info_for_authentication(self):
        return []

    @abc.abstractmethod
    def get_preferred_output_format(self):
        return 'PYTHON_UNITTEST'

    @abc.abstractmethod
    def get_problem_info(self):
        return {
            'openApiUrl': self.get_url() + '/swagger.json',
            'endpointsToSkip': []
        }
