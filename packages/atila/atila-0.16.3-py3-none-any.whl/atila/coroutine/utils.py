from ..events import *
import ctypes
import threading
from skitai.utility import deallocate_was

WAS_FACTORY = None

def deceive_was (was, coro):
    from skitai.wsgiappservice.wastype import _WASType

    for n, v in coro.cr_frame.f_locals.items ():
        if not isinstance (v, _WASType):
            continue
        coro.cr_frame.f_locals [n] = was
    ctypes.pythonapi.PyFrame_LocalsToFast (ctypes.py_object (coro.cr_frame), ctypes.c_int (0))

def get_cloned_was (was_id):
    global WAS_FACTORY

    assert was_id, 'was.ID should be non-zero'
    if WAS_FACTORY is None:
        import skitai
        WAS_FACTORY = skitai.was

    _was = WAS_FACTORY._get_by_id (was_id)
    assert hasattr (_was, 'app'), 'Task future is available on only Atila'

    if isinstance (was_id, int): # origin
        return _was._clone ()
    return _was

def request_postprocessing (was, exc_info = None):
    def postprocess ():
        success, failed, teardown = None, None, None
        if hasattr (was.request, "_hooks"):
            success, failed, teardown = was.request._hooks

        try:
            try:
                try:
                    if exc_info is None:
                        success and was.execute_function (success, (was,))
                        was.app.emit (EVT_REQ_SUCCESS, None)
                    else:
                        failed and was.execute_function (failed, (was, exc_info))
                        was.app.emit (EVT_REQ_FAILED, exc_info)
                finally:
                    teardown and was.execute_function (teardown, (was,))
                    was.app.emit (EVT_REQ_TEARDOWN)
            except:
                was.traceback ()

        finally:
            deallocate_was (was)

    was.executors.get_tpool ().submit (postprocess)
