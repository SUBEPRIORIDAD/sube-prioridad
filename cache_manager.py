"""
SUBE Prioridad — Cache Manager y Dispositivo de Resiliencia Periférica (Edge).
Este módulo modela un Circuit Breaker conceptual diseñado para proteger las llamadas 
del hardware de transporte hacia microservicios remotos (RENAPER, ANDIS, Red SUBE).
Implementa un modo degradado fuera de línea (Fail-Safe) para validadoras sin señal.

No representa implementación oficial.
No integra SUBE real. No integra Red SUBE real.
No consulta bases ni gateways reales. No altera tarjetas reales.
No procesa DNI, nombre, domicilio, diagnóstico ni CUD de pasajeros.
"""

from __future__ import annotations
import time
from enum import Enum
from typing import Callable, TypeVar, Any, Dict, List

T = TypeVar("T")

PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Gestor de Resiliencia y Cache Periférica"
FLOW_VERSION = "0.2.0"
DEMO_MODE = True

PROHIBITED_FIELDS = {
    "dni", "documento", "nombre", "apellido", "domicilio", "direccion", "dirección",
    "telefono", "teléfono", "email", "correo", "diagnostico", "diagnóstico",
    "historia_clinica", "historia_clínica", "certificado_medico", "certificado_médico",
    "cud", "discapacidad", "patologia", "patología", "medico", "médico", "obra_social"
}

class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    """
    Circuit breaker simple para proteger llamadas a servicios externos.
    Si hay demasiados errores consecutivos, abre el circuito para evitar saturación.
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

    def call(self, function: Callable[..., T], *args: Any, **kwargs: Any) -> T:
        # Inyección analítica de tiempo para evitar desincronizaciones de hardware offline (Sección XV)
        current_time = kwargs.pop("_hardware_time_override", None) or time.time()

        if self.state == CircuitState.OPEN:
            if self._can_attempt_recovery_with_time(current_time):
                self.state = CircuitState.HALF_OPEN
            else:
                raise RuntimeError(
                    "Circuit breaker abierto: servicio temporalmente no disponible."
                )

        try:
            result = function(*args, **kwargs)
        except Exception:
            self._record_failure_with_time(current_time)
            raise

        self._record_success()
        return result

    def _record_failure_with_time(self, current_time: float) -> None:
        self.failure_count += 1
        self.last_failure_time = current_time

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

    def _record_success(self) -> None:
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = CircuitState.CLOSED

    def _can_attempt_recovery_with_time(self, current_time: float) -> bool:
        return (current_time - self.last_failure_time) >= self.recovery_timeout_seconds

    def reset(self) -> None:
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = CircuitState.CLOSED
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
            return self.call(function, *args, **kwargs)
        except Exception:
            return fallback_function(*args, **kwargs)

    def estado(self) -> Dict[str, Any]:
        """Devuelve el estado analítico de resiliencia del hardware de borde."""
        return {
            "componente": "TransportEdgeCircuitBreaker",
            "estado_circuito": self.state.value,
            "conteo_fallas": self.failure_count,
            "segundos_recuperacion_configurados": self.recovery_timeout_seconds,
            "modo_operacion": "degradado_offline_fail_safe" if self.state == CircuitState.OPEN else "online_sincrono"
        }

def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    normalized_keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))
    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )

def purge_prohibited_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Sección XXXVII: Purga en memoria de cualquier vector prohibido antes del cacheado."""
    if not isinstance(payload, dict):
        return payload
    sanitized_payload = {}
    for key, value in payload.items():
        normalized_key = str(key).strip().lower()
        if normalized_key in PROHIBITED_FIELDS:
            continue
        if isinstance(value, dict):
            sanitized_payload[key] = purge_prohibited_fields(value)
        else:
            sanitized_payload[key] = value
    return sanitized_payload
def run_demo() -> Dict[str, Any]:
    def remote_sync_mock():
        raise ConnectionError("Fallo simulado de red WAN en molinetes ferroviarios.")
        
    def local_offline_fallback():
        raw_result = {"status": "stored_offline_in_validadora_buffer", "fallback_applied": True}
        # Doble blindaje: sanitizamos el retorno simulado antes de pasarlo a la telemetría del test
        return purge_prohibited_fields(raw_result)

    breaker = TransportEdgeCircuitBreaker(failure_threshold=2, recovery_timeout_seconds=5)
    
    # Forzamos fallas consecutivas para abrir el cortocircuito demostrativo
    for _ in range(2):
        try:
            breaker.call_with_edge_fallback(remote_sync_mock, local_offline_fallback)
        except Exception:
            pass
            
    # Auditamos y protegemos el diccionario final de telemetría
    telemetry_state = breaker.estado()
    telemetry_state["timestamp_utc"] = datetime.now(timezone.utc).isoformat() if hasattr(time, "time") else "iso-fallback"
    return purge_prohibited_fields(telemetry_state)

if __name__ == "__main__":
    import json
    from datetime import datetime
    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
