"""
Value consolidation

This module defines :class:`.Collector`, which is a class that collects a sequence of parsed values
into a single value.

For example, one may want that the last value for a given parameter overwrites the previous values
(:meth:`.Collector.keep_last`), or that all values are returned in a sequence
(:meth:`.Collector.append`).

.. rubric:: Types

This module uses the following types.

.. py:data:: _Value

    Type of the values to collect

.. py:data:: _Item

    Item in a sequence

"""

from __future__ import annotations

import abc
from typing import Any, Generic, List, Mapping, NoReturn, Sequence, TypeVar

from .userr import Err, Res

_Value = TypeVar("_Value")

_Item = TypeVar("_Item")


class Collector(abc.ABC, Generic[_Value]):
    """
    Collects argument instances and computes the final value
    """

    @abc.abstractmethod
    def arg_required(self) -> bool:
        """
        Returns whether one instance of the argument needs to be present
        """
        pass

    @abc.abstractmethod
    def collect(self, seq: Sequence[_Value]) -> Res[_Value]:
        """
        Collects a sequence of values into a result

        Args:
            seq: Sequence of parsed values

        Returns:
            Either the consolidated value or an error
        """
        pass

    @abc.abstractmethod
    def argparse_argument_kwargs(self) -> Mapping[str, Any]:
        """
        Returns the arguments using in documentation (piggy backing on argparse)
        """
        pass

    @staticmethod
    def keep_last() -> Collector[_Value]:
        """
        Returns a collector that keeps the last value
        """
        return _KeepLast()

    @staticmethod
    def append() -> Collector[Sequence[_Item]]:
        """
        Returns a collector that appends sequences
        """
        return _Append()

    @staticmethod
    def invalid() -> Collector[NoReturn]:
        """
        Returns an invalid collector that always returns an error
        """
        return _Invalid()


class _KeepLast(Collector[_Value]):
    def arg_required(self) -> bool:
        return True

    def collect(self, seq: Sequence[_Value]) -> Res[_Value]:
        if not seq:  # no instances provided
            return Err.make("Argument is required")
        else:  # instances are provided
            return seq[-1]

    def argparse_argument_kwargs(self) -> Mapping[str, Any]:
        return {"action": "store"}


class _Append(Collector[Sequence[_Item]]):
    def arg_required(self) -> bool:
        return False

    def collect(self, seq: Sequence[Sequence[_Item]]) -> Res[Sequence[_Item]]:
        res: List[_Item] = []
        for i in seq:
            res.extend(i)
        return res

    def argparse_argument_kwargs(self) -> Mapping[str, Any]:
        return {"action": "append"}


class _Invalid(Collector[Any]):
    def arg_required(self) -> bool:
        raise NotImplementedError

    def collect(self, seq: Sequence[_Value]) -> Res[_Value]:
        return Err.make("Invalid collector")

    def argparse_argument_kwargs(self) -> Mapping[str, Any]:
        raise NotImplementedError(
            "This should have be replaced by a valid collector during construction"
        )
