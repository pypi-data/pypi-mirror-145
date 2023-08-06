# Future
from __future__ import annotations

# Standard Library
import json
from collections.abc import Callable
from typing import Any, Literal

# Packages
import aiohttp


__all__ = (
    "to_json",
    "from_json",
    "json_or_text",
    "MISSING",
)


to_json: Callable[..., str] = json.dumps
from_json: Callable[..., Any] = json.loads


async def json_or_text(response: aiohttp.ClientResponse) -> dict[str, Any] | str:

    text = await response.text(encoding="utf-8")

    try:
        if response.headers.get("Content-Type", "").lower() in ["application/json", "application/json; charset=utf-8"]:
            return from_json(text)
    except KeyError:
        pass

    return text


class _MissingSentinel:

    def __eq__(self, other: Any) -> Literal[False]:
        return False

    def __bool__(self) -> Literal[False]:
        return False

    def __repr__(self) -> str:
        return "..."


MISSING: Any = _MissingSentinel()
