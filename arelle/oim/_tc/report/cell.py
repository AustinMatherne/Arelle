"""
See COPYRIGHT.md for copyright information.

Effective values of xBRL-CSV cells and parameters, as seen by table constraints.
"""

from __future__ import annotations

from collections.abc import Iterable

_NULL_LITERALS = frozenset({"", "#nil", "#none"})


class UnknownSpecialValue(ValueError):
    """The literal starts with # but is not one of the xBRL-CSV special values."""


def effective_value(literal: str | None) -> str | None:
    """Applies xBRL-CSV special value processing to a cell or parameter literal.

    Returns None for the null value (JSON null, an empty cell, #nil or #none) and the
    empty string for #empty. Raises UnknownSpecialValue for any other value starting
    with a single #, which xBRL-CSV reports as xbrlce:unknownSpecialValue.
    """
    if literal is None or literal in _NULL_LITERALS:
        return None
    if literal == "#empty":
        return ""
    if literal.startswith("##"):
        return literal[1:]
    if literal.startswith("#"):
        raise UnknownSpecialValue(literal)
    return literal


def row_has_value(row: Iterable[str]) -> bool:
    """True when any cell of the CSV row is a non empty string, whitespace included."""
    return any(cell != "" for cell in row)
