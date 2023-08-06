###############################################################################
# Copyright (C) 2021 Habana Labs, Ltd. an Intel Company
# All Rights Reserved.
#
# Unauthorized copying of this file or any element(s) within it, via any medium
# is strictly prohibited.
# This file contains Habana Labs, Ltd. proprietary and confidential information
# and is subject to the confidentiality and license agreements under which it
# was provided.
#
###############################################################################

import imp
from collections import namedtuple
import tensorflow as tf
from tensorflow.core.util import event_pb2
from enum import IntEnum

from habana_frameworks.tensorflow.library_loader import is_loaded


def _load_habana_device_binary():
    # import of habana_device binding and load_habana_modules both introduce
    # habana_device.so into the process load_habana_modules must execute first,
    # otherwise htf.habana_ops will be empty!
    assert is_loaded(), "make sure to call load_habana_modules() before importing habana_device binding"
    from habana_frameworks.tensorflow.sysconfig import get_lib_dir

    version_suffix = ".".join(tf.__version__.split(".")[0:3])
    habana_device_wrapper_so_path = f"{get_lib_dir()}/habana_device_binding.so.{version_suffix}"
    return imp.load_dynamic("habana_device", habana_device_wrapper_so_path)


_habana_device = _load_habana_device_binary()
_EventTag = type(
    "EventTag",
    (object,),
    {name: _habana_device.EventTagName(tag) for name, (tag, _) in _habana_device._EventTag.__entries.items()},
)


class event_log:
    enable_event_log = _habana_device.enable_event_log

    GraphCompilationEvent = namedtuple("GraphCompilationEvent", ("graph_name", "duration", "is_success"))

    @staticmethod
    def create_graph_compilation_tuple_from_event(event):
        summary = event.summary
        assert summary.value[0].tag == event_log.EventTag.GraphCompilation, "Expecting GraphCompilation event"
        assert summary.value[1].tag == "duration"
        assert summary.value[2].tag == "is_success"
        graph_name = summary.value[0].tensor.string_val[0]
        duration_in_seconds = summary.value[1].tensor.double_val[0]
        is_success = summary.value[2].tensor.bool_val[0]
        return event_log.GraphCompilationEvent(graph_name, duration_in_seconds, is_success)

    @staticmethod
    def set_event_dispatcher(func):
        def parse_event_func(r):
            func(event_pb2.Event.FromString(r))

        return _habana_device.set_event_dispatcher(parse_event_func)

    @staticmethod
    def log_custom_event(message: str):
        """
        Function to log custom TF Event in EventLog enabled via enable_event_log()

        It creates TF event with 'custom_event' tag and stores message as value string tensor inside.
        """
        _habana_device.log_custom_event(message)

    EventTag = _EventTag


def get_hw_capabilities():
    return _habana_device.get_hw_capabilities()


def get_type():
    try:
        with open("/sys/class/habanalabs/hl0/device_type", "r") as f:
            return f.read().split("\n", 1)[0]
    except:
        log.warning("Unable to read habanalabs driver file - probably driver missing in the system")


class log:
    """
    Class to emit log for different levels via habana device bindings.
    """
    class level(IntEnum):
        info = 0
        warning = 1
        error = 2
        fatal = 3
    @staticmethod
    def _log(level, message) -> None:
        _habana_device.emit_tf_log(level, message)

    @staticmethod
    def info(message: str) -> None:
        log._log(log.level.info, message)
    @staticmethod
    def warning(message: str) -> None:
        log._log(log.level.warning, message)
    @staticmethod
    def error(message: str) -> None:
        log._log(log.level.error, message)
    @staticmethod
    def fatal(message: str) -> None:
        log._log(log.level.fatal, message)
