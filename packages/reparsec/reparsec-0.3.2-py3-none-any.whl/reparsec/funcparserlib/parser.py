# from abc import abstractmethod
# from typing import (
#     Any, Callable, Generic, Sequence, Tuple, TypeVar, Union, overload
# )

# from reparsec.core import combinators, types
# from reparsec.core.result import Ok, Result
# from reparsec.core\.types import Ctx, Loc


# A = TypeVar("A")
# B = TypeVar("B")
# C = TypeVar("C")
# D = TypeVar("D")
# Self = TypeVar("Self", bound="_Parser[Any, Any]")


# class _FnParseObj(types.ParseObj[Sequence[A], B]):
#     __slots__ = "fn"

#     def __init__(self, fn: types.ParseFn[Sequence[A], B]):
#         self.fn = fn

#     def parse_fn(
#             self, stream: Sequence[A], pos: int, ctx: Ctx[Sequence[A]],
#             rm: types.RecoverySteps) -> Result[B, Sequence[A]]:
#         return self.fn(stream, pos, ctx, rm)

#     def to_fn(self) -> types.ParseFn[Sequence[A], B]:
#         return self.fn


# class NoParseError(Exception):
#     def __init__(self, msg="", state=None):
#         self.msg = msg
#         self\.types = state

#     def __str__(self):
#         return self.msg


# class _Parser(Generic[A, B]):
#     def __init__(self, parse_fn: types.ParseFn[Sequence[A], B]):
#         self.name = ""
#         self._parse_fn = parse_fn

#     def named(self: Self, name: str) -> Self:
#         self.name = name
#         return self

#     def define(self, p: "_Parser[A, B]") -> None:
#         self._parse_fn = p._parse_fn
#         self.named(p.name)

#     def parse(self, tokens: Sequence[A]) -> B:
#         r = self._parse_fn(
#             tokens, 0, Ctx(0, Loc(0, 0, 0), lambda _, __, p: Loc(p, 0, 0)),
#             None
#         )
#         if type(r) is Ok:
#             return r.value
#         raise ValueError()

#     def __or__(self, other: "_Parser[A, C]") -> "Parser[A, Union[B, C]]":
#         return Parser(combinators.alt(self._parse_fn, other._parse_fn))

#     def __rshift__(self, f: Callable[[B], C]) -> "Parser[A, C]":
#         return Parser(combinators.fmap(self._parse_fn, f))

#     def bind(self, f: Callable[[B], "_Parser[A, C]"]) -> "Parser[A, C]":
#         return Parser(
#             combinators.bind(
#                 self._parse_fn,
#                 lambda v: _FnParseObj(f(v)._parse_fn)
#             )
#         )

#     def __neg__(self) -> "_IgnoredParser[A]":
#         return _IgnoredParser(self._parse_fn)


# class _IgnoredParser(_Parser[A, Any]):
#     @overload
#     def __add__(self, other: "Parser[A, C]") -> "Parser[A, C]": ...
#     @overload
#     def __add__(self, other: "_IgnoredParser[A]") -> "_IgnoredParser[A]": ...

#     @overload
#     def __add__(
#             self, other: "_TupleParser[A, C, D]") -> "_TupleParser[A, C, D]":
#         ...

#     @abstractmethod
#     def __add__(
#             self,
#             other: Union[
#                 "Parser[A, C]", "_IgnoredParser[A]", "_TupleParser[A, C, D]"
#             ]
#     ) -> Union["Parser[A, C]", "_IgnoredParser[A]", "_TupleParser[A, C, D]"]:
#         parse_fn = combinators.seqr(self._parse_fn, other._parse_fn)
#         if isinstance(other, _IgnoredParser):
#             return _IgnoredParser(parse_fn)

#         return Parser(parse_fn)


# class _TupleParser(_Parser[A, Tuple[B, C]]):
#     @overload
#     def __add__(self, other: "Parser[A, Any]") -> "Parser[A, Any]": ...
#     @overload
#     def __add__(self, other: _IgnoredParser[A]) -> "_TupleParser[A, B, C]": ...

#     @overload
#     def __add__(
#             self,
#             other: "_TupleParser[A, Any, Any]") -> "Parser[A, Any]":
#         ...

#     def __add__(
#         self,
#         other: Union[
#             "Parser[A, Any]",
#             _IgnoredParser[A],
#             "_TupleParser[A, Any, Any]"
#         ]
#     ) -> Union["Parser[A, Any]", "_TupleParser[A, B, C]"]:
#         raise RuntimeError("Should not be called")


# class Parser(_Parser[A, B]):
#     @overload
#     def __add__(self, other: "Parser[A, C]") -> _TupleParser[A, B, C]: ...
#     @overload
#     def __add__(self, other: _IgnoredParser[A]) -> "Parser[A, B]": ...

#     @overload
#     def __add__(self, other: _TupleParser[A, Any, Any]) -> "Parser[A, Any]":
#         ...

#     def __add__(
#         self,
#         other: Union[
#             "Parser[A, C]", _IgnoredParser[A], _TupleParser[A, Any, Any]
#         ]
#     ) -> Union[_TupleParser[A, B, C], "Parser[A, B]", "Parser[A, Any]"]:
#         if isinstance(other, _IgnoredParser):
#             return Parser(combinators.seql(self._parse_fn, other._parse_fn))

#         def merge(a: B, b: Any) -> _Tuple:
#             if isinstance(a, _Tuple):
#                 return _Tuple(a + (b,))
#             return _Tuple((a, b))

#         return Parser(combinators._seq(self._parse_fn, other._parse_fn, merge))


# class _Tuple(Tuple[Any, ...]):
#     ...
