from __future__ import annotations

import collections.abc as cabc
import json
import typing as t

from .encoding import want_bytes
from .exc import BadPayload
from .exc import BadSignature
from .signer import _make_keys_list
from .signer import Signer

if t.TYPE_CHECKING:
    import typing_extensions as te

    _TSerialized = te.TypeVar("_TSerialized", bound=str | bytes, default=str | bytes)
else:
    _TSerialized = t.TypeVar("_TSerialized", bound=str | bytes)


class _PDataSerializer(t.Protocol[_TSerialized]):
    def loads(self, payload: _TSerialized, /) -> t.Any: ...
    def dumps(self, obj: t.Any, /) -> _TSerialized: ...


def is_text_serializer(
    serializer: _PDataSerializer[t.Any],
) -> te.TypeGuard[_PDataSerializer[str]]:
    pass


class Serializer(t.Generic[_TSerialized]):

    default_serializer: _PDataSerializer[t.Any] = json

    default_signer: type[Signer] = Signer

    default_fallback_signers: list[
        dict[str, t.Any] | tuple[type[Signer], dict[str, t.Any]] | type[Signer]
    ] = []

    @t.overload
    def __init__(
        self: Serializer[str],
        secret_key: str | bytes | cabc.Iterable[str] | cabc.Iterable[bytes],
        salt: str | bytes | None = b"itsdangerous",
        serializer: None | _PDataSerializer[str] = None,
        serializer_kwargs: dict[str, t.Any] | None = None,
        signer: type[Signer] | None = None,
        signer_kwargs: dict[str, t.Any] | None = None,
        fallback_signers: list[
            dict[str, t.Any] | tuple[type[Signer], dict[str, t.Any]] | type[Signer]
        ]
        | None = None,
    ): ...

    @t.overload
    def __init__(
        self: Serializer[bytes],
        secret_key: str | bytes | cabc.Iterable[str] | cabc.Iterable[bytes],
        salt: str | bytes | None,
        serializer: _PDataSerializer[bytes],
        serializer_kwargs: dict[str, t.Any] | None = None,
        signer: type[Signer] | None = None,
        signer_kwargs: dict[str, t.Any] | None = None,
        fallback_signers: list[
            dict[str, t.Any] | tuple[type[Signer], dict[str, t.Any]] | type[Signer]
        ]
        | None = None,
    ): ...

    @t.overload
    def __init__(
        self: Serializer[bytes],
        secret_key: str | bytes | cabc.Iterable[str] | cabc.Iterable[bytes],
        salt: str | bytes | None = b"itsdangerous",
        *,
        serializer: _PDataSerializer[bytes],
        serializer_kwargs: dict[str, t.Any] | None = None,
        signer: type[Signer] | None = None,
        signer_kwargs: dict[str, t.Any] | None = None,
        fallback_signers: list[
            dict[str, t.Any] | tuple[type[Signer], dict[str, t.Any]] | type[Signer]
        ]
        | None = None,
    ): ...

    @t.overload
    def __init__(
        self,
        secret_key: str | bytes | cabc.Iterable[str] | cabc.Iterable[bytes],
        salt: str | bytes | None,
        serializer: t.Any,
        serializer_kwargs: dict[str, t.Any] | None = None,
        signer: type[Signer] | None = None,
        signer_kwargs: dict[str, t.Any] | None = None,
        fallback_signers: list[
            dict[str, t.Any] | tuple[type[Signer], dict[str, t.Any]] | type[Signer]
        ]
        | None = None,
    ): ...

    @t.overload
    def __init__(
        self,
        secret_key: str | bytes | cabc.Iterable[str] | cabc.Iterable[bytes],
        salt: str | bytes | None = b"itsdangerous",
        *,
        serializer: t.Any,
        serializer_kwargs: dict[str, t.Any] | None = None,
        signer: type[Signer] | None = None,
        signer_kwargs: dict[str, t.Any] | None = None,
        fallback_signers: list[
            dict[str, t.Any] | tuple[type[Signer], dict[str, t.Any]] | type[Signer]
        ]
        | None = None,
    ): ...

    def __init__(
        self,
        secret_key: str | bytes | cabc.Iterable[str] | cabc.Iterable[bytes],
        salt: str | bytes | None = b"itsdangerous",
        serializer: t.Any | None = None,
        serializer_kwargs: dict[str, t.Any] | None = None,
        signer: type[Signer] | None = None,
        signer_kwargs: dict[str, t.Any] | None = None,
        fallback_signers: list[
            dict[str, t.Any] | tuple[type[Signer], dict[str, t.Any]] | type[Signer]
        ]
        | None = None,
    ):
        self.secret_keys: list[bytes] = _make_keys_list(secret_key)

        if salt is not None:
            salt = want_bytes(salt)

        self.salt = salt

        if serializer is None:
            serializer = self.default_serializer

        self.serializer: _PDataSerializer[_TSerialized] = serializer
        self.is_text_serializer: bool = is_text_serializer(serializer)

        if signer is None:
            signer = self.default_signer

        self.signer: type[Signer] = signer
        self.signer_kwargs: dict[str, t.Any] = signer_kwargs or {}

        if fallback_signers is None:
            fallback_signers = list(self.default_fallback_signers)

        self.fallback_signers: list[
            dict[str, t.Any] | tuple[type[Signer], dict[str, t.Any]] | type[Signer]
        ] = fallback_signers
        self.serializer_kwargs: dict[str, t.Any] = serializer_kwargs or {}

    @property
    def secret_key(self) -> bytes:
        pass

    def load_payload(
        self, payload: bytes, serializer: _PDataSerializer[t.Any] | None = None
    ) -> t.Any:
        pass

    def dump_payload(self, obj: t.Any) -> bytes:
        pass

    def make_signer(self, salt: str | bytes | None = None) -> Signer:
        pass

    def iter_unsigners(self, salt: str | bytes | None = None) -> cabc.Iterator[Signer]:
        pass

    def dumps(self, obj: t.Any, salt: str | bytes | None = None) -> _TSerialized:
        pass

    def dump(self, obj: t.Any, f: t.IO[t.Any], salt: str | bytes | None = None) -> None:
        pass

    def loads(
        self, s: str | bytes, salt: str | bytes | None = None, **kwargs: t.Any
    ) -> t.Any:
        pass

    def load(self, f: t.IO[t.Any], salt: str | bytes | None = None) -> t.Any:
        pass

    def loads_unsafe(
        self, s: str | bytes, salt: str | bytes | None = None
    ) -> tuple[bool, t.Any]:
        pass

    def _loads_unsafe_impl(
        self,
        s: str | bytes,
        salt: str | bytes | None,
        load_kwargs: dict[str, t.Any] | None = None,
        load_payload_kwargs: dict[str, t.Any] | None = None,
    ) -> tuple[bool, t.Any]:
        pass

    def load_unsafe(
        self, f: t.IO[t.Any], salt: str | bytes | None = None
    ) -> tuple[bool, t.Any]:
        pass
