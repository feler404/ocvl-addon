import bpy
import time
import logging


from .engine_app import NodeCommandHandler

bpy.worker_queue = []
handler = NodeCommandHandler
logger = logging.getLogger(__name__)


class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None
    _count = 0
    _wait = 0

    def modal(self, context, event):
        if event.type == 'ESC':
            return self.cancel(context)

        if self._wait > 0:
            self._wait += 1
            return {'PASS_THROUGH'}

        if self._count == 0:
            # finished ok.
            return self.cancel(context)

        if event.type == 'TIMER':
            if self._wait % 2 == 0:
                print(time.time())
            try:
                if bpy.worker_queue:
                    request = bpy.worker_queue.pop(0)
                    kwargs = request.get("kwargs")
                    for kwarg_key, kwarg_value in kwargs.items():
                        if kwarg_value[0] in ["(", "[", "{"]:
                            kwargs[kwarg_key] = eval(kwarg_value)

                    logger.info("Pop request from queue. Command: {}, kwargs: {}".format(request.get("command"), kwargs))
                    getattr(handler, request.get("command"))(**kwargs)

            except Exception as e:
                logger.exception("{}".format(e))



        return {'PASS_THROUGH'}

    def execute(self, context):
        self._count = 16
        self._timer = context.window_manager.event_timer_add(1, context.window)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        context.area.header_text_set()
        context.window_manager.event_timer_remove(self._timer)
        return {'CANCELLED'}


def register():
    bpy.utils.register_class(ModalTimerOperator)


def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)
