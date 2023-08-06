from dataclasses import dataclass, field
from typing import Callable, Generic, Iterable, List, Tuple, TypeVar, Union

from typing_extensions import final

from .chain import Append
from .types import Ctx, Loc

V = TypeVar("V")
V_co = TypeVar("V_co", covariant=True)
U = TypeVar("U")
S = TypeVar("S")


@dataclass
@final
class Skip:
    count: int


@dataclass
@final
class Insert:
    label: str


RepairOp = Union[Skip, Insert]


@dataclass
class OpItem:
    op: RepairOp
    loc: Loc
    expected: Iterable[str]
    consumed: bool


@dataclass
class Repair(Generic[V_co, S]):
    value: V_co
    pos: int
    ctx: Ctx[S]
    op: RepairOp
    expected: Iterable[str] = ()
    consumed: bool = False
    ops: List[OpItem] = field(default_factory=list)


def fmap_repair(repair: Repair[V, S], fn: Callable[[V], U]) -> Repair[U, S]:
    return Repair(
        fn(repair.value), repair.pos, repair.ctx, repair.op, repair.expected,
        repair.consumed, repair.ops
    )


@dataclass
@final
class Unselected(Generic[V_co, S]):
    pending: Repair[V_co, S]

    def fmap(self, fn: Callable[[V_co], U]) -> "Unselected[U, S]":
        return Unselected(fmap_repair(self.pending, fn))

    def set_ctx(self, ctx: Ctx[S]) -> "Unselected[V_co, S]":
        self.pending.ctx = ctx
        return self

    def set_expected(self, expected: Iterable[str]) -> "Unselected[V_co, S]":
        pending = self.pending
        if not pending.consumed:
            pending.expected = expected
        ops_set_expected(pending.ops, expected)
        return self

    def prepend_expected(
            self, expected: Iterable[str],
            consumed: bool) -> "Unselected[V_co, S]":
        pending = self.pending
        if not pending.consumed:
            pending.expected = Append(expected, pending.expected)
            pending.consumed |= consumed
        ops_prepend_expected(pending.ops, expected, consumed)
        return self


@dataclass
@final
class Pending(Generic[V_co, S]):
    selected: int
    pending: Repair[V_co, S]
    repairs: List[Tuple[int, Repair[V_co, S]]]

    def fmap(self, fn: Callable[[V_co], U]) -> "Pending[U, S]":
        return Pending(
            self.selected, fmap_repair(self.pending, fn),
            [(g, fmap_repair(r, fn)) for g, r in self.repairs]
        )

    def set_ctx(self, ctx: Ctx[S]) -> "Pending[V_co, S]":
        self.pending.ctx = ctx
        for _, repair in self.repairs:
            repair.ctx = ctx
        return self

    def set_expected(self, expected: Iterable[str]) -> "Pending[V_co, S]":
        pending = self.pending
        if not pending.consumed:
            pending.expected = expected
        ops_set_expected(pending.ops, expected)
        for _, repair in self.repairs:
            if not repair.consumed:
                repair.expected = expected
            ops_set_expected(repair.ops, expected)
        return self

    def prepend_expected(
            self, expected: Iterable[str],
            consumed: bool) -> "Pending[V_co, S]":
        pending = self.pending
        if not pending.consumed:
            pending.expected = Append(expected, pending.expected)
            pending.consumed |= consumed
        ops_prepend_expected(pending.ops, expected, consumed)
        for _, repair in self.repairs:
            if not repair.consumed:
                repair.expected = Append(expected, repair.expected)
                repair.consumed |= consumed
            ops_prepend_expected(repair.ops, expected, consumed)
        return self


@dataclass
@final
class Selected(Generic[V_co, S]):
    selected: int
    repairs: List[Tuple[int, Repair[V_co, S]]]

    def fmap(self, fn: Callable[[V_co], U]) -> "Selected[U, S]":
        return Selected(
            self.selected, [(g, fmap_repair(r, fn)) for g, r in self.repairs]
        )

    def set_ctx(self, ctx: Ctx[S]) -> "Selected[V_co, S]":
        for _, repair in self.repairs:
            repair.ctx = ctx
        return self

    def set_expected(self, expected: Iterable[str]) -> "Selected[V_co, S]":
        for _, repair in self.repairs:
            if not repair.consumed:
                repair.expected = expected
            ops_set_expected(repair.ops, expected)
        return self

    def prepend_expected(
            self, expected: Iterable[str],
            consumed: bool) -> "Selected[V_co, S]":
        for _, repair in self.repairs:
            if not repair.consumed:
                repair.expected = Append(expected, repair.expected)
                repair.consumed |= consumed
            ops_prepend_expected(repair.ops, expected, consumed)
        return self


Repairs = Union[Unselected[V, S], Pending[V, S], Selected[V, S]]


def ops_set_expected(ops: List[OpItem], expected: Iterable[str]) -> None:
    for op in ops:
        if not op.consumed:
            op.expected = expected


def ops_prepend_expected(
        ops: List[OpItem], expected: Iterable[str], consumed: bool) -> None:
    for op in ops:
        if not op.consumed:
            op.expected = Append(expected, op.expected)
            op.consumed |= consumed
