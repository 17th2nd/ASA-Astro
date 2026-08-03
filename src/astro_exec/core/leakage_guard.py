"""Fail-closed filesystem capability enforcement for separated roles."""

from __future__ import annotations

from pathlib import Path

from .config import RoleCapabilities
from .errors import LeakageViolation


class LeakageGuard:
    """Authorize role file access only beneath immutable declared roots."""

    def __init__(self, workspace_root: str | Path, capabilities: RoleCapabilities) -> None:
        """Bind one role's capabilities to a concrete workspace root."""

        self.workspace_root = Path(workspace_root).resolve()
        self.capabilities = capabilities

    def _permitted_roots(self, access: str) -> tuple[Path, ...]:
        values = self.capabilities.read_roots if access == "read" else self.capabilities.write_roots
        return tuple((self.workspace_root / value).resolve() for value in values)

    def authorize(self, path: str | Path, *, access: str) -> Path:
        """Return the resolved path if permitted, otherwise raise ``LeakageViolation``."""

        if access not in {"read", "write"}:
            raise LeakageViolation("unknown capability access mode", details={"access": access})
        requested = Path(path)
        candidate = (self.workspace_root / requested).resolve() if not requested.is_absolute() else requested.resolve()
        for root in self._permitted_roots(access):
            try:
                candidate.relative_to(root)
                return candidate
            except ValueError:
                continue
        raise LeakageViolation(
            "role filesystem access denied",
            details={"access": access, "path": str(requested), "role": self.capabilities.role},
        )

    def read_bytes(self, path: str | Path) -> bytes:
        """Read bytes after applying the role's read capability."""

        return self.authorize(path, access="read").read_bytes()

    def write_bytes(self, path: str | Path, content: bytes) -> Path:
        """Write bytes after applying the role's write capability."""

        destination = self.authorize(path, access="write")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(content)
        return destination
