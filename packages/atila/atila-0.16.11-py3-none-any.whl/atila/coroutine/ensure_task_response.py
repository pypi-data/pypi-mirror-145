from skitai.exceptions import HTTPError
from skitai.utility import make_pushables
import sys
from skitai.wastuff.api import API
import ctypes
from rs4.misc import producers
from skitai.protocols.sock.impl.ws import *
from skitai.tasks import proto
from . import utils
from skitai.tasks import tasks
from skitai.tasks.httpbase.task import DEFAULT_TIMEOUT
from skitai.tasks.pth import sp_task
from skitai.tasks.pth import task as pth_task
from skitai.utility import deallocate_was

class ResponsibleTask:
    def _get_was (self):
        _was = utils.get_cloned_was (self.meta ['__was_id'])
        if "coro" in self.meta: # deciving `was` object
            utils.deceive_was (_was, self.meta ["coro"])
        return _was

    def _late_respond (self, tasks_or_content):
        def cleanup ():
            deallocate_was (self._was)
            self._was = None

        if hasattr (self._was, 'websocket'):
            self._fulfilled (self._was, tasks_or_content)
            return

        # NEED self._fulfilled and self._was
        if not hasattr (self._was, 'response'):
            # already responsed: SEE app2.map_in_thread
            return

        response = self._was.response
        content = None
        expt  = None

        try:
            if self._fulfilled == 'self':
                content = tasks_or_content.fetch ()
            else:
                content = self._fulfilled (self._was, tasks_or_content)
            self._fulfilled = None

        except MemoryError:
            raise

        except HTTPError as e:
            response.start_response (e.status)
            content = content or response.build_error_template (e.explain or (self._was.app.debug and e.exc_info), e.errno, was = self._was)
            expt = sys.exc_info ()

        except:
            self._was.traceback ()
            response.start_response ("502 Bad Gateway")
            content = content or response.build_error_template (self._was.app.debug and sys.exc_info () or None, 0, was = self._was)
            expt = sys.exc_info ()

        if isinstance (content, API) and self._was.env.get ('ATILA_SET_SEPC'):
            content.set_spec (self._was.app)

        will_be_push = make_pushables (response, content)
        if will_be_push is None:
            return # future

        utils.request_postprocessing (self._was, expt)
        try:
            for part in will_be_push:
                response.push (part)
            response.done ()

        finally:
            if isinstance (content, producers.Sendable): # IMP: DO NOT release
                content.execute_when_done (cleanup)
            else:
                self._was = None


# add late response methods --------------------------
if not hasattr (tasks.Future, "_get_was"):
    for cls in (tasks.Future, tasks.Futures, tasks.Tasks, tasks.Mask, pth_task.Task, sp_task.Task):
        for meth in ('_get_was', '_late_respond'):
            setattr (cls, meth, getattr (ResponsibleTask, meth))
