from abc import ABC, abstractmethod
import numpy as np


def error(obs, mod, percent=False, abs=True):
    if percent:
        if abs:
            return np.abs(100.0 * (mod - obs) / obs)
        else:
            return 100.0 * (mod - obs) / obs
    else:
        if abs:
            return np.abs(mod - obs)
        else:
            return mod - obs


def squared_error(obs, mod, percent=False):
    if percent:
        return (100.0 * (mod - obs) / obs) ** 2
    else:
        return (mod - obs) ** 2


class Metrics(ABC):
    """Abstract class to reuse common metrics functions.
    Each data format (ts,bwc,weib) has a child class with
    specific metrics mappings defined there.
    """

    @abstractmethod
    def _get_suite_mapper(self) -> dict:
        pass

    @abstractmethod
    def _get_func_mapper(self) -> dict:
        pass

    def _get_suite(self, suite):
        """get list of tuples of (var, metric_name) for suite name"""
        mapper = self._get_suite_mapper()
        if suite not in mapper:
            raise ValueError(f"Stats suite {suite} not found!")
        return mapper[suite]

    def _prepare_metrics_from_user_input(self, input_):
        """
        Convert user input to list of tuples containing
        variable name, metric name, and metric function.

        Parameters
        ----------
        input_: str, list
            either suite name or list of string or tuples.

        returns
        -------
        list: list of tuples
            input converted to list of tuples containing
            (variable name, metric name, metric function)

        Examples
        --------
        >>> print(_prepare_metrics_from_user_input(["ws_r2"]))
        [(VAR_WIND_SPEED, "r2", wind_validation.ts.metrics.r2)]
        """
        if isinstance(input_, str):
            lst = self._get_suite(input_)
        elif isinstance(input_, list):
            lst = input_
        else:
            raise ValueError(f"Expected list or str, got {type(input_)}!")

        result = []
        func_map = self._get_func_mapper()
        for item in lst:
            if not isinstance(item, tuple) or len(item) != 2:
                raise ValueError('Expected tuple of ("var", "metric")')
            var, metric = item
            if metric not in func_map:
                raise RuntimeError("Provided metric does not exist")
            result.append((var, metric, func_map[metric]))

        return result
