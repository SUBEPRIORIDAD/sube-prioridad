"""
SUBE Prioridad — Simulador demo de Bono Solidario.
Este módulo modela el reconocimiento solidario conceptual cuando una persona
usuaria de SUBE Prioridad recibe voluntariamente un asiento de uso general.

Reglas centrales:
 - No integra SUBE real.
 - No integra Red SUBE real.
 - No modifica saldo real.
 - No aplica descuentos reales.
 - No usa DNI.
 - No usa diagnóstico.
 - No usa CUD visible.
 - No expone causa médica.
 - No premia la ocupación de asientos legalmente prioritarios.
 - No obliga a otros pasajeros.
 - No obliga al chofer.
 - No reemplaza derechos ya existentes.

Compatibilidad:
 Este archivo acepta nombres de parámetros viejos y nuevos:
 - collaborator_token
 - collaborator_user_token
 - priority_user_confirms
 - priority_user_confirms_seat_yield
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Simulador Demo de Bono Solidario"
SIMULATOR_VERSION = "0.3.0"
DEMO_MODE = True

PROHIBITED_FIELDS = {
    "dni",
    "documento",
    "nombre",
    "apellido",
    "domicilio",
    "direccion",
    "dirección",
    "telefono",
    "teléfono",
    "phone",
    "email",
    "correo",
    "diagnostico",
    "diagnóstico",
    "patologia",
    "patología",
    "historia_clinica",
    "historia_clínica",
    "certificado_medico",
    "certificado_médico",
    "cud",
    "discapacidad",
    "medico",
    "médico",
    "obra_social",
    "saldo",
    "dinero",
    "gps",
    "latitud",
    "longitud",
    "latitude",
    "longitude",
}

class SeatType(str, Enum):
    GENERAL_USE = "general_use"
    LEGAL_PRIORITY = "legal_priority"

class SolidaryRecognitionStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"

class SolidaryRejectionReason(str, Enum):
    NONE = "none"
    PRIORITY_USER_DID_NOT_CONFIRM = "priority_user_did_not_confirm"
    NO_VOLUNTARY_SEAT_YIELD = "no_voluntary_seat_yield"
    NOT_SAME_TRANSPORT_CONTEXT = "not_same_transport_context"
    LEGAL_PRIORITY_SEAT_NOT_REWARDABLE = "legal_priority_seat_not_rewardable"
    SAME_USER_NOT_ALLOWED = "same_user_not_allowed"
    SENSITIVE_DATA_REJECTED = "sensitive_data_rejected"
    COLLABORATOR_SELF_RECOGNITION_NOT_ALLOWED = "collaborator_self_recognition_not_allowed"

@dataclass(frozen=True)
class SolidaryEvent:
    event_demo_id: str
    priority_user_token: str
    collaborator_token: str
    voluntary_seat_yield: bool
    priority_user_confirms_seat_yield: bool
    same_transport_context: bool
    seat_type: SeatType
    event_timestamp_utc: datetime
    source: str
    demo_mode: bool

    @property
    def collaborator_user_token(self) -> str:
        return self.collaborator_token

    @property
    def priority_user_confirms(self) -> bool:
        return self.priority_user_confirms_seat_yield

@dataclass(frozen=True)
class SolidaryRecognitionResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: SolidaryRecognitionStatus
    accepted: bool
    recognition_token: Optional[str]
    priority_user_token: str
    collaborator_token: str
    seat_type: SeatType
    rejection_reason: SolidaryRejectionReason
    risk_flags: List[str]
    audit_flags: List[str]
    bonus_summary: Dict[str, Any]
    privacy_notice: str
    legal_scope_notice: str
    driver_burden: str
    timestamp_utc: str

# =====================================================================
# 🆕 CAPA DE ABSTRACCIÓN DEL LIBRO DE REGISTROS (RESUELVE EL IMPORT ERROR)
# =====================================================================

class BaseRecognitionLedger(ABC):
    """Interfaz abstracta para el desacoplamiento de la persistencia cívica (DIP)."""
    @abstractmethod
    def register_interaction(self, event: SolidaryEvent) -> bool:
        pass

class DemoRecognitionLedger(BaseRecognitionLedger):
    """Implementación conceptual en memoria para auditorías transaccionales de tests."""
    def __init__(self) -> None:
        self._ledger: Dict[str, Dict[str, Any]] = {}

    def register_interaction(self, event: SolidaryEvent) -> bool:
        if not event.priority_user_token or not event.collaborator_token:
            return False
        
        # Simulación de registro asíncrono indexado despersonalizado
        self._ledger[event.event_demo_id] = {
            "priority_user_token": event.priority_user_token,
            "collaborator_token": event.collaborator_token,
            "registered_at_utc": event.event_timestamp_utc.isoformat(),
            "status": "pending_async_batch_sync"
        }
        return True

    def clear(self) -> None:
        self._ledger.clear()

    @property
    def size(self) -> int:
        return len(self._ledger)


# =====================================================================
# 🏛️ FUNCIONES CORE DE NEGOCIO (PRESERVADAS DE FORMA FIDELÍSIMA)
# =====================================================================

def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(keys.intersection(PROHIBITED_FIELDS))
    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )

def create_demo_solidary_event(
    event_demo_id: str = "demo-solidary-event-001",
    priority_user_token: str = "demo-priority-user-001",
    collaborator_token: Optional[str] = None,
    collaborator_user_token: Optional[str] = None,
    voluntary_seat_yield: bool = True,
    priority_user_confirms: Optional[bool] = None,
    priority_user_confirms_seat_yield: Optional[bool] = None,
    same_transport_context: bool = True,
    seat_type: SeatType = SeatType.GENERAL_USE,
    event_timestamp_utc: Optional[datetime] = None,
    source: str = "demo-validator-or-user-confirmation",
    **legacy_kwargs: Any,
) -> SolidaryEvent:
    """
    Crea un evento demo de Bono Solidario.
    Acepta nombres viejos y nuevos para no romper tests ni endpoints previos.
    """
    if "priority_token" in legacy_kwargs:
        priority_user_token = legacy_kwargs["priority_token"]
    if "collaborator" in legacy_kwargs and collaborator_token is None:
        collaborator_token = legacy_kwargs["collaborator"]
    if "collaborator_user" in legacy_kwargs and collaborator_user_token is None:
        collaborator_user_token = legacy_kwargs["collaborator_user"]
    if "priority_user_confirmed" in legacy_kwargs and priority_user_confirms is None:
        priority_user_confirms = legacy_kwargs["priority_user_confirmed"]
    if (
        "priority_user_confirms_seat_yield" in legacy_kwargs
        and priority_user_confirms_seat_yield is None
    ):
        priority_user_confirms_seat_yield = legacy_kwargs[
            "priority_user_confirms_seat_yield"
        ]

    collaborator = (
        collaborator_token
        or collaborator_user_token
        or "demo-collaborator-user-001"
    )

    if priority_user_confirms_seat_yield is None:
        priority_user_confirms_seat_yield = (
            True if priority_user_confirms is None else priority_user_confirms
        )

    payload = {
        "event_demo_id": event_demo_id,
        "priority_user_token": priority_user_token,
        "collaborator_token": collaborator,
        "source": source,
    }
    assert_no_prohibited_fields(payload)
    _require_non_empty(payload)

    if isinstance(seat_type, str):
        seat_type = SeatType(seat_type)

    return SolidaryEvent(
        event_demo_id=event_demo_id.strip(),
        priority_user_token=priority_user_token.strip(),
        collaborator_token=collaborator.strip(),
        voluntary_seat_yield=voluntary_seat_yield,
        priority_user_confirms_seat_yield=priority_user_confirms_seat_yield,
        same_transport_context=same_transport_context,
        seat_type=seat_type,
        event_timestamp_utc=event_timestamp_utc or datetime.now(timezone.utc),
        source=source.strip(),
        demo_mode=DEMO_MODE,
    )

def simulate_solidary_recognition(
    event: SolidaryEvent,
) -> SolidaryRecognitionResult:
    risk_flags = _risk_flags(event)
    audit_flags = _audit_flags(event)
    if risk_flags:
        return _result(
            event=event,
            status=SolidaryRecognitionStatus.REJECTED,
            accepted=False,
            recognition_token=None,
            rejection_reason=_primary_rejection_reason(risk_flags),
            risk_flags=risk_flags,
            audit_flags=audit_flags,
        )
    recognition_token = f"solidary-recognition-{event.event_demo_id}"
    return _result(
        event=event,
        status=SolidaryRecognitionStatus.ACCEPTED,
        accepted=True,
        recognition_token=recognition_token,
        rejection_reason=SolidaryRejectionReason.NONE,
        risk_flags=[],
        audit_flags=audit_flags,
    )

def result_to_dict(result: SolidaryRecognitionResult) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "accepted": result.accepted,
        "recognition_token": result.recognition_token,
        "priority_user_token": result.priority_user_token,
        "collaborator_token": result.collaborator_token,
        "collaborator_user_token": result.collaborator_token,
        "seat_type": result.seat_type.value,
        "rejection_reason": result.rejection_reason.value,
        "risk_flags": result.risk_flags,
        "audit_flags": result.audit_flags,
        "bonus_summary": result.bonus_summary,
        "privacy_notice": result.privacy_notice,
        "legal_scope_notice": result.legal_scope_notice,
        "driver_burden": result.driver_burden,
