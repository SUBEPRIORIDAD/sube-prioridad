import time
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class CacheEntry:
    value: Any
    expires_at: float


class TTLCache:
    """
    Caché simple con tiempo de vida.

    Uso previsto en el MVP:
    - Evitar consultas repetidas a servicios externos.
    - Mantener respuestas técnicas temporales sin almacenar datos personales.
    - Trabajar con hashes o tokens pseudoanonimizados.
    """

    def __init__(self, default_ttl_seconds: int = 300) -> None:
        self.default_ttl_seconds = default_ttl_seconds
        self._store: Dict[str, CacheEntry] = {}

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        if not key:
            raise ValueError("La clave de caché es obligatoria.")

        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl_seconds
        expires_at = time.time() + ttl

        self._store[key] = CacheEntry(value=value, expires_at=expires_at)

    def get(self, key: str) -> Optional[Any]:
        if not key:
            return None

        entry = self._store.get(key)

        if entry is None:
            return None

        if entry.expires_at < time.time():
            self.delete(key)
            return None

        return entry.value

    def delete(self, key: str) -> None:
        self._store.pop(key, None)

    def clear(self) -> None:
        self._store.clear()

    def size(self) -> int:
        self._purge_expired()
        return len(self._store)

    def _purge_expired(self) -> None:
        now = time.time()
        expired_keys = [
            key for key, entry in self._store.items() if entry.expires_at < now
        ]

        for key in expired_keys:
            self.delete(key)