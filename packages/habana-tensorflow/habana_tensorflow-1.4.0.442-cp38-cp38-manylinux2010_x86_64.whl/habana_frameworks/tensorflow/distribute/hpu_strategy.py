# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
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

import copy
import os

import tensorflow
from tensorflow.core.protobuf import tensorflow_server_pb2
from tensorflow.python.distribute import (collective_all_reduce_strategy,
                                          collective_util)
from tensorflow.python.distribute import \
    cross_device_ops as cross_device_ops_lib
from tensorflow.python.distribute import (cross_device_utils, distribute_lib,
                                          multi_worker_util, numpy_dataset)
from tensorflow.python.eager import context
from tensorflow.python.framework import ops
from tensorflow.python.platform import tf_logging as logging


def get_hpu_collective_api_name():
    """ Returns the name of the underlying HPU collective API used by the implementation of HPU support for tf.distribute.
        It is either "hccl" or "hcl".
    """
    habana_hccl_comm_api = os.environ.get("HABANA_HCCL_COMM_API", "1").lower()
    habana_nccl_comm_api = os.environ.get("HABANA_NCCL_COMM_API", "1").lower()
    assert habana_hccl_comm_api in ["0", "false", "1", "true"]
    assert habana_nccl_comm_api in ["0", "false", "1", "true"]
    return "hccl" if ((habana_hccl_comm_api in ["1", "true"]) and (habana_nccl_comm_api in ["1", "true"])) else "hcl"


def disable_collective_reduce_packing():
    """ Disables the automatical packing (grouping/concatenation) of gradients for CollectiveReduceV2.
    """
    from tensorflow.python.distribute import cross_device_utils

    def custom_group_by_size(input_tensors, bytes_per_pack):
        # Ignore bytes_per_pack.
        return [[x] for x in input_tensors]

    cross_device_utils.group_by_size = custom_group_by_size


_is_b50853_wa_installed = False


def _install_b50853_wa_now():
    from tensorflow.python.framework.c_api_util import ScopedTFGraph

    def _noop_func(_):
        pass

    ScopedTFGraph.__del__ = _noop_func


def install_b50853_wa_if_applicable():
    """ Installs a work-around to TensorFlow 2.5.0, 2.5.1, 2.6.0 issue b50853.
        See: https://github.com/tensorflow/tensorflow/issues/50853
    """
    if not tensorflow.executing_eagerly():
        return

    global _is_b50853_wa_installed
    if _is_b50853_wa_installed:
        return

    import atexit
    atexit.register(_install_b50853_wa_now)

    _is_b50853_wa_installed = True


_allcompare_installed = False


def install_allcompare():
    global _allcompare_installed
    if _allcompare_installed:
        return

    from tensorflow.python.ops import collective_ops
    from habana_frameworks.tensorflow.allcompare import AllCompare

    orig_all_reduce_v2 = collective_ops.all_reduce_v2

    def _proxy_all_reduce_v2(t, group_size, *args, **kwargs):
        reduced_t = orig_all_reduce_v2(t, group_size, *args, **kwargs)

        allcompare = AllCompare.access_if_enabled()
        if allcompare is not None:
            err_tensor = allcompare.expect_similar(
                reduced_t / group_size, t)

            with tensorflow.control_dependencies([err_tensor]):
                reduced_t = tensorflow.identity(reduced_t)

        return reduced_t

    collective_ops.all_reduce_v2 = _proxy_all_reduce_v2
    _allcompare_installed = True


def comm_init(num_replicas_in_sync: int):
    import tensorflow as tf
    from tensorflow.python.ops import collective_ops
    from ..library_loader import habana_ops

    with tf.device("/device:HPU:0"):
        x = habana_ops.ops.CollectiveCommHandshakeProducer()
    with tf.device("/device:CPU:0"):
        x = collective_ops.all_gather(
            x, group_size=num_replicas_in_sync, group_key=-1, instance_key=1, communication_hint="ring")
    with tf.device("/device:HPU:0"):
        x = habana_ops.ops.CollectiveCommHandshakeConsumer(i=x)

    return x


if tensorflow.__version__.startswith("2.5") or tensorflow.__version__.startswith("2.6"):
    class HPUStrategy(collective_all_reduce_strategy.CollectiveAllReduceStrategyV1):
        def __init__(self, cluster_resolver=None, communication_options=None, config: tensorflow.compat.v1.ConfigProto = None, server: tensorflow.distribute.Server = None, enable_scoped_allocator: bool = False):
            if cluster_resolver is None:
                cluster_resolver = tensorflow.distribute.cluster_resolver.TFConfigClusterResolver()

            # Note that 'communication' parameter has been intentionally omitted.
            self.__class__ = collective_all_reduce_strategy.CollectiveAllReduceStrategyV1
            if communication_options is None:
                communication_options = collective_util.Options()
            super(collective_all_reduce_strategy.CollectiveAllReduceStrategyV1, self).__init__(
                HabanaCollectiveAllReduceExtended(
                    self, cluster_resolver=cluster_resolver, communication_options=communication_options, enable_scoped_allocator=enable_scoped_allocator)
            )

            distribute_lib.distribution_strategy_gauge.get_cell(
                "V1").set("MultiWorkerMirroredStrategy")
            # pylint: disable=protected-access
            distribute_lib.distribution_strategy_replica_gauge.get_cell(
                "num_workers").set(self.extended._num_workers)
            distribute_lib.distribution_strategy_replica_gauge.get_cell(
                "num_gpu_per_worker").set(self.extended._num_gpus_per_worker)

            # In TF 1.15 the following update_config_proto() invocation is a necessary hack to the strategy's config_proto to prevent a hang.
            #   See: https://github.com/tensorflow/tensorflow/issues/31499
            # In TF 2.2 it is no longer needed.
            # Apparently it is still required in TF 2.5 for broadcasts.
            if config is None:
                config = tensorflow.compat.v1.ConfigProto()
                config.allow_soft_placement = False
            self._config = self.update_config_proto(config)

            if not tensorflow.executing_eagerly():
                if server is None:
                    # Create and start the gRPC server for this worker.
                    server = tensorflow.distribute.Server(
                        cluster_resolver.cluster_spec(),
                        job_name=cluster_resolver.task_type,
                        task_index=cluster_resolver.task_id,
                        config=self._config)
                self._target = server.target
                self.extended._std_server_started = True

            comm_init_op = comm_init(self.num_replicas_in_sync)

            if not tensorflow.executing_eagerly():
                with tensorflow.compat.v1.Session(self._target) as session:
                    session.run(comm_init_op)

            install_b50853_wa_if_applicable()
            install_allcompare()

    class HabanaCollectiveAllReduceExtended(collective_all_reduce_strategy.CollectiveAllReduceExtended):
        def __init__(self, container_strategy, cluster_resolver, communication_options, enable_scoped_allocator):
            self._enable_scoped_allocator = enable_scoped_allocator
            super(HabanaCollectiveAllReduceExtended, self).__init__(
                container_strategy=container_strategy,
                cluster_resolver=cluster_resolver,
                communication_options=communication_options)
            self.experimental_enable_get_next_as_optional = False

        def _initialize_strategy(self, cluster_resolver):
            if cluster_resolver.cluster_spec().as_dict():
                self._initialize_multi_worker(cluster_resolver)
            else:
                self._initialize_local(cluster_resolver)

        def _initialize_local(self, cluster_resolver, devices=None):
            if devices is None:
                devices = ("/device:HPU:0",)
            super(HabanaCollectiveAllReduceExtended, self)._initialize_local(
                cluster_resolver, devices)

        def _initialize_multi_worker(self, cluster_resolver):
            cluster_spec = multi_worker_util.normalize_cluster_spec(
                cluster_resolver.cluster_spec())
            task_type = cluster_resolver.task_type
            task_id = cluster_resolver.task_id
            if task_type is None or task_id is None:
                raise ValueError("When `cluster_spec` is given, you must also specify "
                                 "`task_type` and `task_id`.")
            self._cluster_spec = cluster_spec
            self._task_type = task_type
            self._task_id = task_id
            self._id_in_cluster = multi_worker_util.id_in_cluster(
                self._cluster_spec, self._task_type, self._task_id)

            self._num_workers = multi_worker_util.worker_count(
                cluster_spec, task_type)
            if not self._num_workers:
                raise ValueError("No `worker`, `chief` or `evaluator` tasks can be found "
                                 "in `cluster_spec`.")

            self._is_chief = multi_worker_util.is_chief(cluster_spec, task_type,
                                                        task_id)

            self._worker_device = "/job:%s/task:%d" % (task_type, task_id)
            self._host_input_device = numpy_dataset.SingleDevice(
                self._worker_device)

            if (ops.executing_eagerly_outside_functions() and
                    not getattr(self, "_local_or_standalone_client_mode", False)):
                context.context().configure_collective_ops(
                    collective_leader=multi_worker_util.collective_leader(
                        cluster_spec, task_type, task_id),
                    scoped_allocator_enabled_ops=(
                        "HpuCollectiveReduce", "CollectiveReduceV2", "CollectiveReduceV3") if self._enable_scoped_allocator else (),
                    device_filters=("/job:%s/task:%d" % (task_type, task_id),))
            self._collective_ops_configured = True

            # Starting a std server in eager mode and in independent worker mode.
            if (context.executing_eagerly() and
                not getattr(self, "_std_server_started", False) and
                    not getattr(self, "_local_or_standalone_client_mode", False)):
                # Checking _local_or_standalone_client_mode as well because we should not
                # create the std server in standalone client mode.
                config_proto = copy.deepcopy(context.context().config)
                config_proto = self._update_config_proto(config_proto)

                if hasattr(cluster_resolver, "port"):
                    port = cluster_resolver.port
                else:
                    port = 0
                server_def = tensorflow_server_pb2.ServerDef(
                    cluster=cluster_spec.as_cluster_def(),
                    default_session_config=config_proto,
                    job_name=task_type,
                    task_index=task_id,
                    protocol=cluster_resolver.rpc_layer or "grpc",
                    port=port)
                context.context().enable_collective_ops(server_def)
                self._std_server_started = True
                # The `ensure_initialized` is needed before calling
                # `context.context().devices()`.
                context.context().ensure_initialized()
                logging.info(
                    "Enabled multi-worker collective ops with available devices: %r",
                    context.context().devices())

            # Habana: Override number of available accelerators to a single HPU:0 device.
            num_gpus = 1
            local_devices = tuple("%s/device:HPU:%d" % (self._worker_device, i)
                                  for i in range(num_gpus))

            self._collective_keys = cross_device_utils.CollectiveKeys(
                group_key_start=1 + self._collective_key_base)
            self._cross_device_ops = cross_device_ops_lib.CollectiveAllReduce(
                devices=local_devices,
                group_size=len(local_devices) * self._num_workers,
                collective_keys=self._collective_keys)
            # CrossDeviceOps for per host tensors.
            self._host_cross_device_ops = cross_device_ops_lib.CollectiveAllReduce(
                devices=[self._worker_device],
                group_size=self._num_workers,
                collective_keys=self._collective_keys)
            super(HabanaCollectiveAllReduceExtended, self)._initialize_single_worker(
                local_devices)

            # Add a default device so that ops without specified devices will not end up
            # on other workers.
            self._default_device = "/job:%s/task:%d" % (task_type, task_id)

            # Save the num_gpus_per_worker and rpc_layer for configure method.
            self._num_gpus_per_worker = num_gpus
            self._rpc_layer = cluster_resolver.rpc_layer
            self._warn_nccl_no_gpu()

            if self._enable_check_health and context.executing_eagerly():
                self._start_check_health_thread()

            logging.info(
                "HPUStrategy with cluster_spec = %r, task_type = %r, "
                "task_id = %r, num_workers = %r, local_devices = %r, "
                "communication = %s", cluster_spec.as_dict(), task_type, task_id,
                self._num_workers, local_devices,
                self._communication_options.implementation)
else:
    class HPUStrategy(collective_all_reduce_strategy.CollectiveAllReduceStrategy):
        def __init__(self, cluster_resolver=None, communication_options=None, config: tensorflow.compat.v1.ConfigProto = None, server: tensorflow.distribute.Server = None, enable_scoped_allocator: bool = False):
            if cluster_resolver is None:
                cluster_resolver = tensorflow.distribute.cluster_resolver.TFConfigClusterResolver()

            # Note that 'communication' parameter has been intentionally omitted.
            self.__class__ = collective_all_reduce_strategy.CollectiveAllReduceStrategy
            if communication_options is None:
                communication_options = collective_util.Options()
            super(collective_all_reduce_strategy.CollectiveAllReduceStrategy, self).__init__(
                HabanaCollectiveAllReduceExtended(
                    self, cluster_resolver=cluster_resolver, communication_options=communication_options, enable_scoped_allocator=enable_scoped_allocator)
            )

            distribute_lib.distribution_strategy_gauge.get_cell(
                "V2").set("MultiWorkerMirroredStrategy")
            # pylint: disable=protected-access
            distribute_lib.distribution_strategy_replica_gauge.get_cell(
                "num_workers").set(self.extended._num_workers)
            distribute_lib.distribution_strategy_replica_gauge.get_cell(
                "num_replicas_per_worker").set(self.extended._num_devices_per_worker)

            # In TF 1.15 the following update_config_proto() invocation is a necessary hack to the strategy's config_proto to prevent a hang.
            #   See: https://github.com/tensorflow/tensorflow/issues/31499
            # In TF 2.2 it is no longer needed.
            # Apparently it is still required in TF 2.5 for broadcasts.
            if config is None:
                config = tensorflow.compat.v1.ConfigProto()
                config.allow_soft_placement = False
            self._config = self.update_config_proto(config)

            if not tensorflow.executing_eagerly():
                if server is None:
                    # Create and start the gRPC server for this worker.
                    server = tensorflow.distribute.Server(
                        cluster_resolver.cluster_spec(),
                        job_name=cluster_resolver.task_type,
                        task_index=cluster_resolver.task_id,
                        config=self._config)
                self._target = server.target
                self.extended._std_server_started = True

            comm_init_op = comm_init(self.num_replicas_in_sync)

            if not tensorflow.executing_eagerly():
                with tensorflow.compat.v1.Session(self._target) as session:
                    session.run(comm_init_op)

            install_b50853_wa_if_applicable()
            install_allcompare()

    class HabanaCollectiveAllReduceExtended(collective_all_reduce_strategy.CollectiveAllReduceExtended):
        def __init__(self, container_strategy, cluster_resolver, communication_options, enable_scoped_allocator):
            self._enable_scoped_allocator = enable_scoped_allocator
            super(HabanaCollectiveAllReduceExtended, self).__init__(
                container_strategy=container_strategy,
                cluster_resolver=cluster_resolver,
                communication_options=communication_options)
            self.experimental_enable_get_next_as_optional = False

        def _initialize_strategy(self, cluster_resolver):
            if cluster_resolver.cluster_spec().as_dict():
                self._initialize_multi_worker(cluster_resolver)
            else:
                self._initialize_local(cluster_resolver)

        def _initialize_local_devices(self, cluster_resolver, worker_device):
            local_devices = (
                f"{worker_device}/device:HPU:0",)
            print(f"   local_devices={local_devices}")
            return local_devices, "HPU"

        def _initialize_local(self, cluster_resolver, devices=None):
            # Pass devices=None, so _initialize_local_devices will be used to pick up HPU device.
            super(HabanaCollectiveAllReduceExtended, self)._initialize_local(
                cluster_resolver, devices=None)
