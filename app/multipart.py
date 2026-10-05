"""Minimal multipart/form-data parser (stdlib only; no cgi)."""

from __future__ import annotations

from dataclasses import dataclass
from email.parser import BytesParser
from email.policy import default as email_default
from typing import Any


@dataclass
class FormFile:
    field_name: str
    filename: str | None
    content_type: str | None
    data: bytes


@dataclass
class FormBody:
    fields: dict[str, str]
    files: dict[str, FormFile]


def parse_multipart(content_type: str, body: bytes) -> FormBody:
    if "multipart/form-data" not in (content_type or ""):
        raise ValueError("Content-Type must be multipart/form-data")
    # Reconstruct a MIME message so stdlib can split parts on the boundary.
    header = f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode("utf-8")
    message = BytesParser(policy=email_default).parsebytes(header + body)
    if not message.is_multipart():
        raise ValueError("multipart body could not be parsed")
    fields: dict[str, str] = {}
    files: dict[str, FormFile] = {}
    for part in message.iter_parts():
        disposition = part.get_content_disposition()
        if disposition != "form-data":
            continue
        name = part.get_param("name", header="content-disposition")
        if not name:
            continue
        filename = part.get_filename()
        payload = part.get_payload(decode=True)
        if payload is None:
            payload = b""
        elif isinstance(payload, str):
            payload = payload.encode("utf-8")
        if filename is not None:
            files[name] = FormFile(
                field_name=name,
                filename=filename,
                content_type=part.get_content_type(),
                data=payload,
            )
        else:
            charset = part.get_content_charset() or "utf-8"
            fields[name] = payload.decode(charset, errors="replace")
    return FormBody(fields=fields, files=files)


def as_dict(form: FormBody) -> dict[str, Any]:
    return {
        "fields": form.fields,
        "files": {k: {"filename": v.filename, "content_type": v.content_type, "size": len(v.data)} for k, v in form.files.items()},
    }
