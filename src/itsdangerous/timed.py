from __future__ import annotations

import collections.abc as cabc
import time
import typing as t
from datetime import datetime
from datetime import timezone

from .encoding import base64_decode
from .encoding import base64_encode
from .encoding import bytes_to_int
from .encoding import int_to_bytes
from .encoding import want_bytes
from .exc import BadSignature
from .exc import BadTimeSignature
from .exc import SignatureExpired
from .serializer import _TSerialized
from .serializer import Serializer
from .signer import Signer


class TimestampSigner(Signer):

    def get_timestamp(self) -> int:
        pass

    def timestamp_to_datetime(self, ts: int) -> datetime:
        pass

    def sign(self, value: str | bytes) -> bytes:
        pass


    @t.overload
    def unsign(  # pyright: ignore
        self,
        signed_value: str | bytes,
        max_age: int | None = None,
        return_timestamp: t.Literal[False] = False,
    ) -> bytes: ...

    @t.overload
    def unsign(
        self,
        signed_value: str | bytes,
        max_age: int | None = None,
        return_timestamp: t.Literal[True] = True,
    ) -> tuple[bytes, datetime]: ...

    def unsign(
        self,
        signed_value: str | bytes,
        max_age: int | None = None,
        return_timestamp: bool = False,
    ) -> tuple[bytes, datetime] | bytes:
        pass

    def validate(self, signed_value: str | bytes, max_age: int | None = None) -> bool:
        pass


class TimedSerializer(Serializer[_TSerialized]):

    default_signer: type[TimestampSigner] = TimestampSigner  # pyright: ignore

    def iter_unsigners(
        self, salt: str | bytes | None = None
    ) -> cabc.Iterator[TimestampSigner]:
        pass


    def loads(  # type: ignore[override]
        self,
        s: str | bytes,
        max_age: int | None = None,
        return_timestamp: bool = False,
        salt: str | bytes | None = None,
    ) -> t.Any:
        pass

    def loads_unsafe(  # type: ignore[override]
        self,
        s: str | bytes,
        max_age: int | None = None,
        salt: str | bytes | None = None,
    ) -> tuple[bool, t.Any]:
        pass
