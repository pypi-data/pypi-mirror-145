from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)
from fa_purity.cmd import (
    unsafe_unwrap,
)
from fa_purity.frozen import (
    freeze,
    FrozenList,
)
from fa_purity.pure_iter._inner import (
    InnerPureIter,
)
import functools
import more_itertools
from typing import (
    Callable,
    Generic,
    Iterable,
    Iterator,
    TypeVar,
)

_T = TypeVar("_T")
_R = TypeVar("_R")


def _chunked(items: Iterable[_T], size: int) -> Iterator[FrozenList[_T]]:
    return iter(map(freeze, more_itertools.chunked(items, size)))


@dataclass(frozen=True)
class PureIter(Generic[_T]):
    # unsafe_unwrap use is safe due to iters equivalence
    _inner: InnerPureIter[_T]

    def map(self, function: Callable[[_T], _R]) -> PureIter[_R]:
        draft: InnerPureIter[_R] = InnerPureIter(
            self._inner.new_iter.map(lambda i: iter(map(function, i)))
        )
        return PureIter(draft)

    def reduce(self, function: Callable[[_R, _T], _R], init: _R) -> _R:
        return unsafe_unwrap(
            self._inner.new_iter.map(
                lambda i: functools.reduce(function, i, init)
            )
        )

    def filter(self, function: Callable[[_T], bool]) -> PureIter[_T]:
        draft = InnerPureIter(
            self._inner.new_iter.map(lambda i: iter(filter(function, i)))
        )
        return PureIter(draft)

    def chunked(self, size: int) -> PureIter[FrozenList[_T]]:
        draft = InnerPureIter(
            self._inner.new_iter.map(lambda i: _chunked(i, size))
        )
        return PureIter(draft)

    def to_list(self) -> FrozenList[_T]:
        return tuple(self)

    def transform(self, function: Callable[[PureIter[_T]], _R]) -> _R:
        return function(self)

    def __iter__(self) -> Iterator[_T]:
        return iter(unsafe_unwrap(self._inner.new_iter))
