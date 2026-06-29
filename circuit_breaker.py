import time
from enum import Enum
from typing import Callable, TypeVar


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