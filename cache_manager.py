from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional


@dataclass
class CacheEntry:
    """
    Entrada conceptual de caché para el MVP.

    No debe utilizarse para almacenar DNI, nombre, apellido, diagnóstico médico,
    historia clínica, certificados médicos ni datos de salud identificables.
    """

    key: str
    value: Any
    created_at: datetime
    expires_at: Optional[datetime] = None

    def is_expired(self, now: Optional[datetime] = None) -> bool:
        """
        Indica si la entrada se encuentra vencida.
        """

        if self.expires_at is None:
            return False

        current_time = now or datetime.now(timezone.utc)
        return current_time >= self.expires_at


class CacheManager:
    """
    Caché simple en memoria para uso demostrativo del MVP.

    Este componente no es almacenamiento productivo.
    No persiste datos.
    No se conecta con organismos públicos.
    No se conecta con SUBE real.
    No se conecta con Mi Argentina.
    No debe almacenar datos personales sensibles.

    Su finalidad es permitir pruebas técnicas locales o conceptuales.
    """

    def __init__(self, default_ttl_seconds: int = 300) -> None:
        self.default_ttl_seconds = default_ttl_seconds
        self._items: Dict[str, CacheEntry] = {}

    def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: Optional[int] = None,
    ) -> None:
        """
        Guarda un valor en caché con vencimiento opcional.

        Si ttl_seconds no se informa, se utiliza el TTL por defecto.
        Si ttl_seconds es 0 o negativo, la entrada no tendrá vencimiento.
        """

        self._validate_key(key)

        created_at = datetime.now(timezone.utc)
        ttl = self.default_ttl_seconds if ttl_seconds is None else ttl_seconds

        expires_at = None
        if ttl > 0:
            expires_at = created_at + timedelta(seconds=ttl)

        self._items[key] = CacheEntry(
            key=key,
            value=value,
            created_at=created_at,
            expires_at=expires_at,
        )

    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtiene un valor de caché.

        Si la entrada no existe o está vencida, devuelve default.
        """

        self._validate_key(key)

        entry = self._items.get(key)

        if entry is None:
            return default

        if entry.is_expired():
            self.delete(key)
            return default

        return entry.value

    def has(self, key: str) -> bool:
        """
        Indica si existe una entrada vigente para la clave indicada.
        """

        self._validate_key(key)

        entry = self._items.get(key)

        if entry is None:
            return False

        if entry.is_expired():
            self.delete(key)
            return False

        return True

    def delete(self, key: str) -> bool:
        """
        Elimina una entrada de caché.

        Devuelve True si existía y fue eliminada.
        """

        self._validate_key(key)

        if key in self._items:
            del self._items[key]
            return True

        return False

    def clear(self) -> None:
        """
        Limpia toda la caché en memoria.
        """

        self._items.clear()

    def cleanup_expired(self) -> int:
        """
        Elimina entradas vencidas.

        Devuelve la cantidad de entradas eliminadas.
        """

        now = datetime.now(timezone.utc)

        expired_keys = [
            key for key, entry in self._items.items() if entry.is_expired(now)
        ]

        for key in expired_keys:
            del self._items[key]

        return len(expired_keys)

    def size(self) -> int:
        """
        Devuelve la cantidad de entradas vigentes en caché.
        """

        self.cleanup_expired()
        return len(self._items)

    def keys(self) -> list[str]:
        """
        Devuelve las claves vigentes.
        """

        self.cleanup_expired()
        return list(self._items.keys())

    def estado(self) -> Dict[str, Any]:
        """
        Devuelve estado conceptual del componente.
        """

        self.cleanup_expired()

        return {
            "componente": "CacheManager",
            "entorno": "mvp-conceptual",
            "tipo": "cache_en_memoria",
            "items_en_cache": len(self._items),
            "default_ttl_seconds": self.default_ttl_seconds,
            "persistencia_productiva": False,
            "procesa_datos_sensibles": False,
            "integracion_real_con_organismos": False,
            "integracion_real_sube": False,
            "integracion_real_mi_argentina": False,
        }

    def _validate_key(self, key: str) -> None:
        if not isinstance(key, str) or not key.strip():
            raise ValueError("La clave de caché debe ser un string no vacío.")


def crear_cache_demo() -> CacheManager:
    """
    Crea una instancia demostrativa del cache manager.
    """

    cache = CacheManager(default_ttl_seconds=300)

    cache.set(
        key="demo-prioridad",
        value={
            "prioridad_activa": True,
            "entorno": "mvp-conceptual",
            "datos_sensibles_procesados": False,
        },
    )

    return cache


def cache_demo_estado() -> Dict[str, Any]:
    """
    Devuelve estado serializable de una caché demostrativa.
    """

    cache = crear_cache_demo()

    return {
        "valor_demo": cache.get("demo-prioridad"),
        "estado": cache.estado(),
    }


__all__ = [
    "CacheEntry",
    "CacheManager",
    "crear_cache_demo",
    "cache_demo_estado",
]
