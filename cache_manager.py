import time
from enum import Enum
from typing import Callable, TypeVar, Any, Dict, List


T = TypeVar("T")


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """
    Circuit breaker simple para proteger llamadas a servicios externos.

    Uso previsto:
    - ANDIS / SISA / RENAPER / gateway X-Road u otros servicios públicos.
    - Si hay demasiados errores consecutivos, se abre el circuito.
    - Luego de un tiempo de recuperación, permite una prueba en estado half-open.
    """

    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout_seconds: int = 30,
    ) -> None:
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = CircuitState.CLOSED

    def call(self, function: Callable[..., T], *args, **kwargs) -> T:
        if self.state == CircuitState.OPEN:
            if self._can_attempt_recovery():
                self.state = CircuitState.HALF_OPEN
            else:
                raise RuntimeError(
                    "Circuit breaker abierto: servicio temporalmente no disponible."
                )

        try:
            result = function(*args, **kwargs)
        except Exception:
            self._record_failure()
            raise

        self._record_success()
        return result

    def _record_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _record_success(self) -> None:
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = CircuitState.CLOSED

    def _can_attempt_recovery(self) -> bool:
        return (time.time() - self.last_failure_time) >= self.recovery_timeout_seconds

    def reset(self) -> None:
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = CircuitState.CLOSED


# =====================================================================
# 🆕 EXTENSIÓN DE ARQUITECTURA: RESILIENCIA EN ENTORNOS OFFLINE (EDGE)
# =====================================================================

class TransportEdgeCircuitBreaker(CircuitBreaker):
    """
    Cortocircuito especializado para validadoras y hardware físico de transporte.
    Si la conectividad WAN o las APIs centrales fallan, activa políticas 
    de mitigación y degradación controlada en modo fuera de línea (Fail-Safe).
    """
    
    def __init__(
        self, 
        failure_threshold: int = 3, 
        recovery_timeout_seconds: int = 30
    ) -> None:
        super().__init__(failure_threshold, recovery_timeout_seconds)
        self._local_offline_backup: List[Dict[str, Any]] = []

    def call_with_edge_fallback(
        self, 
        function: Callable[..., T], 
        fallback_function: Callable[..., T], 
        *args: Any, 
        **kwargs: Any
    ) -> T:
        """
        Intenta ejecutar la sincronización en línea. Si el circuito está abierto 
        o la llamada remota falla, ejecuta la función de degradación local.
        """
        try:
            # Intentamos la vía centralizada estándar utilizando el motor base
            return self.call(function, *args, **kwargs)
        except Exception:
            # Si ocurre un fallo y el circuito se abre, conmutamos al flujo offline
            return fallback_function(*args, **kwargs)

    def estado(self) -> Dict[str, Any]:
        """
        Devuelve el estado analítico de resiliencia del hardware de borde.
        """
        return {
            "componente": "TransportEdgeCircuitBreaker",
            "estado_circuito": self.state.value,
            "conteo_fallas": self.failure_count,
            "segundos_recuperacion_configurados": self.recovery_timeout_seconds,
            "modo_operación": "degradado_offline_fail_safe" if self.state == CircuitState.OPEN else "online_sincrono"
        }
