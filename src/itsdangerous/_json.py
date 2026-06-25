from __future__ import annotations

import json as _json
import typing as t


class _CompactJSON:

    @staticmethod
    def loads(payload: str | bytes) -> t.Any:
        pass

    @staticmethod
    def dumps(obj: t.Any, **kwargs: t.Any) -> str:
        pass
