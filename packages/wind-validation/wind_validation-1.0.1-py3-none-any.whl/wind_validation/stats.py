from abc import ABC, abstractmethod


class Stats(ABC):
    """Abstract class to reuse common stats functions.
    Each data format (ts,bwc,weib) has a child class with
    specific stats mappings defined there.
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

    def _prepare_stats_from_user_input(self, input_):
        """
        Convert user input to list of tuples containing
        variable name, stat name, and stat function.

        Parameters
        ----------
        input_: str, list
            either suite name or list of string or tuples.

        returns
        -------
        list: list of tuples
            input converted to list of tuples containing
            (variable name, stat name, stat function)

        Examples
        --------
        >>> print(_prepare_stats_from_user_input(["ws_mean"]))
        [(VAR_WIND_SPEED, "mean", wind_validation.ts.stats.mean)]
        """
        if isinstance(input_, str):
            lst = self._get_suite(input_)
        elif isinstance(input_, list):
            lst = input_
        else:
            raise ValueError(
                f'Expected list of tuples("var", "stat")' " or str, got {type(input_)}!"
            )
        result = []
        func_map = self._get_func_mapper()
        for item in lst:
            if not isinstance(item, tuple) or len(item) != 2:
                raise ValueError('Expected tuple of ("var", "stat")')
            var, stat = item
            func_map_type = type(list(func_map.keys())[0])
            if func_map_type == tuple:  # others
                key = item
            elif func_map_type == str:  # ts
                key = stat
            else:
                raise ValueError(f"Unknown internal stat func map key!")

            if key not in func_map:
                raise RuntimeError("Provided stat does not exist")
            result.append((var, stat, func_map[key]))

        return result
