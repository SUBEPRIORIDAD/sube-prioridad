"""
SUBE Prioridad — Pasarela de Enlace de Pasajeros Casuales (Casual Gateway).
Este módulo modela el gateway perimetral encargado de orquestar las señales 
provenientes de las validadoras físicas, molinetes y la red de comunicaciones.
Gestiona el flujo hacia la pantalla del chofer y la persistencia en buffers de memoria.

No representa implementación oficial.
No integra SUBE real. No integra Red SUBE real.
No modifica saldos reales. No altera tarifas reales.
No procesa DNI, nombre, domicilio, diagnóstico ni CUD de pasajeros.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Pasarela de Enlace Perimetral (Casual Gateway)"
GATEWAY_VERSION = "0.2.0"
DEMO_MODE = True

PROHIBITED_FIELDS = {
    "dni", "documento", "nombre", "apellido", "domicilio", "direccion", "dirección",
    "telefono", "teléfono", "email", "correo", "diagnostico", "diagnóstico",
    "historia_clinica", "historia_clínica", "certificado_medico", "certificado_médico",
    "cud", "discapacidad", "patologia", "patología", "medico", "médico", "obra_social"
}

class GatewayCommsStatus(str, Enum):
    ONLINE_SYNC = "online_sync"
    DEGRADED_EDGE_BUFFER = "degraded_edge_buffer"
    CRITICAL_DISCONNECTED = "critical_disconnected"

class DriverDisplayMessage(str, Enum):
    ATTRIBUTE_CONFIRMED = "Prioridad Confirmada"
    BONUS_READY_NEXT_TRIP = "Bono Reservado Próx Viaje"
    CONNECTION_DEGRADED = "Red SUBE Offline - FailSafe Activo"
    ACCESS_GRANTED = "Acceso Concedido"
    NONE = "Sin Mensaje"

@dataclass(frozen=True)
class GatewayHardwareContext:
    """Metadatos de infraestructura física inyectados por el bus de comunicaciones."""
    network_demo_id: str
    route_demo_id: str
    vehicle_demo_id: Optional[str]
    station_demo_id: Optional[str]
    turnstile_demo_id: Optional[str]
    is_rail_network: bool

@dataclass(frozen=True)
class CasualGatewaySignalPayload:
    """Paquete mínimo despersonalizado capturado en el molinete o validadora."""
    signal_demo_id: str
    priority_user_token_demo: str
    collaborator_token_demo: str
    validation_timestamp_utc: datetime
    voluntary_seat_yield_declared: bool

@dataclass(frozen=True)
class CasualGatewayResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    comms_status: GatewayCommsStatus
    driver_display_message: DriverDisplayMessage
    payload_buffered_locally: bool
    signal_processed: bool
    risk_flags: List[str]
    reason: str
    privacy_notice: str
    driver_burden_notice: str
    warnings: List[str]
    timestamp_utc: str
def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    normalized_keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))
    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )

def process_casual_gateway_signal(
    payload: CasualGatewaySignalPayload,
    hardware: GatewayHardwareContext,
    is_wan_online: bool = True
) -> CasualGatewayResult:
    """Procesa el flujo físico interconectando la validadora, la pantalla y el backend."""
    assert_no_prohibited_fields({
        "signal_demo_id": payload.signal_demo_id,
        "priority_user_token_demo": payload.priority_user_token_demo,
        "collaborator_token_demo": payload.collaborator_token_demo,
    })
    
    flags: List[str] = []
    if payload.priority_user_token_demo == payload.collaborator_token_demo:
        flags.append("self_sync_attempt")
        
    # Discriminación inteligente de la red de comunicaciones
    if not is_wan_online:
        comms_status = GatewayCommsStatus.DEGRADED_EDGE_BUFFER
        display_msg = DriverDisplayMessage.CONNECTION_DEGRADED
        buffered = True
        reason = "Red central caída. Validadora física opera en modo Fail-Safe encapsulando el lote localmente."
    else:
        comms_status = GatewayCommsStatus.ONLINE_SYNC
        buffered = False
        if flags:
            display_msg = DriverDisplayMessage.NONE
            reason = "Señal rechazada por la pasarela debido a inconsistencias lógicas en el payload."
        else:
            display_msg = DriverDisplayMessage.BONUS_READY_NEXT_TRIP if not hardware.is_rail_network else DriverDisplayMessage.ACCESS_GRANTED
            reason = "Pasarela en línea. Sincronización remitida y mensaje despachado a la consola de control."

    return CasualGatewayResult(
        project=PROJECT_NAME, module=MODULE_NAME, version=GATEWAY_VERSION, demo_mode=DEMO_MODE,
        comms_status=comms_status, driver_display_message=display_msg,
        payload_buffered_locally=buffered, signal_processed=len(flags) == 0,
        risk_flags=flags, reason=reason,
        privacy_notice="La pasarela opera mediante tokens criptográficos despersonalizados. Cero exposición de DNI o CUD.",
        driver_burden_notice="El chofer visualiza la alerta en pantalla de forma pasiva. No calcula, no audita y no interviene.",
        warnings=["Simulación analítica de hardware periférico de transporte público."],
        timestamp_utc=datetime.now(timezone.utc).isoformat()
    )

def run_demo() -> Dict[str, Any]:
    now = datetime.now(timezone.utc)
    # Simulamos un escenario ferroviario (Molinete de Estación Retiro Mitre o Aristóbulo)
    hardware = GatewayHardwareContext(
        network_demo_id="red-sube-mitre", route_demo_id="ramal-tigre",
        vehicle_demo_id=None, station_demo_id="estacion-retiro",
        turnstile_demo_id="molinete-04", is_rail_network=True
    )
    payload = CasualGatewaySignalPayload(
        signal_demo_id="sig-gw-01", priority_user_token_demo="p-token-99",
        collaborator_token_demo="c-token-88", validation_timestamp_utc=now,
        voluntary_seat_yield_declared=True
    )
    # Ejecutamos la simulación con la red WAN activa
    result = process_casual_gateway_signal(payload, hardware, is_wan_online=True)
    return {
        "modulo": result.module,
        "estado_comunicaciones": result.comms_status.value,
        "pantalla_consola_chofer_o_molinete": result.driver_display_message.value,
        "guardado_en_buffer_local": result.payload_buffered_locally,
        "procesado_exitoso": result.signal_processed,
        "motivo_limite": result.reason
    }

if __name__ == "__main__":
    import json
    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
