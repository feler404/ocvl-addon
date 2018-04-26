import threading
import tornado
import bpy
from tornado.ioloop import IOLoop
from logging import getLogger

from .egine_app import tutorial_engine_app
from .settings import TUTORIAL_ENGINE_PORT

logger = getLogger(__name__)


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        logger.info("Tutorial engine thread stop.")
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def start(self, *args, **kwargs):
        logger.info("Worker tread started.")
        bpy.ops.wm.modal_timer_operator()
        logger.info("Modal timer operator started.")
        super().start(*args, **kwargs)


def tutorial_engine_worker():
    bpy.ioloop = IOLoop.current()
    tornado.log.enable_pretty_logging()
    app = tutorial_engine_app()
    app.listen(TUTORIAL_ENGINE_PORT)
    logger.info("Tutorial Engine worker started.")
    IOLoop.current().start()


engine_worker_thread = StoppableThread(target=tutorial_engine_worker)
bpy.engine_worker_thread = engine_worker_thread