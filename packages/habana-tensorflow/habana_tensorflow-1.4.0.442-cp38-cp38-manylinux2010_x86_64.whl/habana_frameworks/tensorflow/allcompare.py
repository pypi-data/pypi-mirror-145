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

""" This script contains support for all-compare diagnostic mode.
"""

import logging
import tensorflow as tf

from .util import condition_env_var

HABANA_ALLCOMPARE_ENV_VAR_NAME = "HABANA_TF_ALLCOMPARE"

_log = logging.getLogger("AllCompare")


def _compute_dissimilarity_coeff(a, b):
    """ Computes the difference between given tensors relative to their lengths. Zero means they are identical.
    """
    return tf.norm(a - b) / (0.5 + tf.norm(0.5 * (a + b)))


class DissimilariyCoeff:
    def __init__(self, name):
        self.name = name
        self.value = float("nan")
        self.variable = tf.Variable(
            initial_value=self.value, name=name, dtype=tf.float32)


class AllCompare:
    """ Provides means to execute all-compare technique by asserting that worker's gradiends do not change after all-reduce operation.
        By instantiating this class, the user states that the training script supports the technique by providing means to ensure
        that every worker runs non-randomized operations (no dropouts) and processes identical input batches as other workers (no data sharding).
    """
    _instance = None
    _is_enabled_by_env = condition_env_var(
        HABANA_ALLCOMPARE_ENV_VAR_NAME, False)

    def __init__(self, override_enabled: bool = None, compute_dissimilarity_coeff_fn=_compute_dissimilarity_coeff):
        assert AllCompare._instance is None, "There may be only one instance of AllCompare class."
        AllCompare._instance = self

        self._is_enabled = override_enabled if override_enabled is not None else AllCompare._is_enabled_by_env
        if self._is_enabled:
            _log.warning("All-compare diagnostic mode enabled.")

        self._compute_dissimilarity_coeff_fn = compute_dissimilarity_coeff_fn
        self._dissimilarity_coeffs = {}
        self.error_count = 0

    @classmethod
    def access(cls):
        """ Returns AllCompare singleton instance or None if it was not instantiated.
        """
        assert cls._instance is not None or not cls._is_enabled_by_env, "The current training script does not support all-compare diagnostic mode."
        return cls._instance

    @classmethod
    def access_if_enabled(cls):
        """ Returns AllCompare singleton instance if it was instantiated and is enabled, otherwise None.
        """
        allcompare = cls.access()
        return allcompare if (allcompare is not None and allcompare.is_enabled) else None

    @property
    def is_enabled(self):
        """ Indicates whether the all-compare feature has been enabled and collects dissimilarity coefficients.
        """
        return self._is_enabled

    def enable(self):
        self._is_enabled = True

    def disable(self):
        self._is_enabled = False

    def clear_all_dissimilarity_coeffs(self):
        assert self.is_enabled, "Unable to use AllCompare feature unless enabled."
        self._dissimilarity_coeffs.clear()

    def expect_similar(self, tensor, tensor_expected, name=None):
        assert self.is_enabled, "Unable to use AllCompare feature unless enabled."

        if name is None:
            name = f"AllCompare/{tensor_expected.name}".replace(":", "_")

        _log.warning(
            f"Expecting similarity: '{name}'")

        if name in self._dissimilarity_coeffs:
            coeff = self._dissimilarity_coeffs[name]
        else:
            coeff = DissimilariyCoeff(name)
            self._dissimilarity_coeffs[name] = coeff

        coeff_tensor = self._compute_dissimilarity_coeff_fn(
            tensor, tensor_expected)

        coeff.variable.assign(coeff_tensor)

        tf.py_function(func=AllCompare._on_dissimilarity_coeff,
                       inp=[name, coeff_tensor], Tout=[])

        return coeff_tensor

    @staticmethod
    def _on_dissimilarity_coeff(name, coeff_tensor):
        name = name.numpy().decode("ascii")
        coeff_value = float(coeff_tensor)

        if coeff_value != 0:
            _log.error(
                f"'{name}' has dissimilarity coefficient: {coeff_value:.5f}")
            is_err = True
        else:
            _log.warning(f"All-compare OK: '{name}'")
            is_err = False

        allcompare = AllCompare.access_if_enabled()
        if allcompare is None:
            _log.error(
                f"Service unavailable: Value of '{name}' will not be stored.")
            return

        coeffs = allcompare._dissimilarity_coeffs
        if name not in coeffs:
            _log.error(
                f"Dissimilarity coefficient '{name}' not present in the list of tracked tensors.")
            return

        coeff = coeffs[name]
        coeff.value = coeff_value

        if is_err:
            allcompare.error_count += 1


class AllCompareStopOnErrorCallback(tf.keras.callbacks.Callback):
    """ A Keras callback to be used to track the all-compare dissimilarity coefficients and report errors.
    """

    def __init__(self, stop_on_error=True):
        self._allcompare = AllCompare.access_if_enabled()
        self.stop_on_error = stop_on_error

    def on_train_begin(self, logs=None):
        if self._allcompare is None:
            return

        self._allcompare.clear_all_dissimilarity_coeffs()

    def on_train_batch_end(self, batch, logs=None):
        if self._allcompare is None:
            return

        if self.stop_on_error and self._allcompare.error_count != 0:
            assert False, "Stopping due to all-compare errors."

    def on_train_end(self, logs=None):
        if self._allcompare is None:
            return

        self._allcompare.clear_all_dissimilarity_coeffs()
