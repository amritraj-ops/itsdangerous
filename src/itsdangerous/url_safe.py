from __future__ import annotations

import typing as t
import zlib

from ._json import _CompactJSON
from .encoding import base64_decode
from .encoding import base64_encode
from .exc import BadPayload
from .serializer import _PDataSerializer
from .serializer import Serializer
from .timed import TimedSerializer


class URLSafeSerializerMixin(Serializer[str]):

    default_serializer: _PDataSerializer[str] = _CompactJSON

    def load_payload(
        self,
        payload: bytes,
        *args: t.Any,
        serializer: t.Any | None = None,
        **kwargs: t.Any,
    ) -> t.Any:
        pass

    def dump_payload(self, obj: t.Any) -> bytes:
        pass


class URLSafeSerializer(URLSafeSerializerMixin, Serializer[str]):


class URLSafeTimedSerializer(URLSafeSerializerMixin, TimedSerializer[str]):
