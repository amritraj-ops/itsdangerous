from __future__ import annotations

import typing as t
from datetime import datetime


class BadData(Exception):

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


class BadSignature(BadData):

    def __init__(self, message: str, payload: t.Any | None = None):
        super().__init__(message)

        self.payload: t.Any | None = payload


class BadTimeSignature(BadSignature):

    def __init__(
        self,
        message: str,
        payload: t.Any | None = None,
        date_signed: datetime | None = None,
    ):
        super().__init__(message, payload)

        self.date_signed = date_signed


class SignatureExpired(BadTimeSignature):


class BadHeader(BadSignature):

    def __init__(
        self,
        message: str,
        payload: t.Any | None = None,
        header: t.Any | None = None,
        original_error: Exception | None = None,
    ):
        super().__init__(message, payload)

        self.header: t.Any | None = header

        self.original_error: Exception | None = original_error


class BadPayload(BadData):

    def __init__(self, message: str, original_error: Exception | None = None):
        super().__init__(message)

        self.original_error: Exception | None = original_error
