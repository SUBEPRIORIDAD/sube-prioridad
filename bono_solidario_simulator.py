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

class BaseRecognitionLedger(ABC):
    """Interfaz abstracta para el desacoplamiento de la persistencia cívica (DIP)."""
    @abstractmethod
    def register_interaction(self, event: SolidaryEvent) -> bool:
        pass

class DemoRecognitionLedger(BaseRecognitionLedger):
    """Implementación conceptual en memoria exigida por las pruebas unitarias."""
    def __init__(self) -> None:
        self._ledger: Dict[str, Dict[str, Any]] = {}

    def register_interaction(self, event: SolidaryEvent) -> bool:
        if not event.priority_user_token or not event.collaborator_token:
            return False
        
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
        "timestamp_utc": result.timestamp_utc,
    }

def run_demo() -> Dict[str, Any]:
    event = create_demo_solidary_event()
    result = simulate_solidary_recognition(event)
    return result_to_dict(result)

def run_rejected_demo() -> Dict[str, Any]:
    event = create_demo_solidary_event(
        voluntary_seat_yield=False,
    )
    result = simulate_solidary_recognition(event)
    return result_to_dict(result)

def _risk_flags(event: SolidaryEvent) -> List[str]:
    flags: List[str] = []
    if event.priority_user_token == event.collaborator_token:
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
        "timestamp_utc": result.timestamp_utc,
    }

def run_demo() -> Dict[str, Any]:
    event = create_demo_solidary_event()
    result = simulate_solidary_recognition(event)
    return result_to_dict(result)

def run_rejected_demo() -> Dict[str, Any]:
    event = create_demo_solidary_event(
        voluntary_seat_yield=False,
    )
    result = simulate_solidary_recognition(event)
    return result_to_dict(result)

def _risk_flags(event: SolidaryEvent) -> List[str]:
    flags: List[str] = []
    if event.priority_user_token == event.collaborator_token:
        flags.append("same_user_not_allowed")
    if not event.voluntary_seat_yield:
        flags.append("no_voluntary_seat_yield")
    if not event.priority_user_confirms_seat_yield:
        flags.append("priority_user_did_not_confirm")
    if not event.same_transport_context:
        flags.append("not_same_transport_context")
    if event.seat_type == SeatType.LEGAL_PRIORITY:
        flags.append("legal_priority_seat_not_rewardable")
    if _looks_like_free_text(event.priority_user_token):
        flags.append("priority_user_token_looks_like_free_text")
    if _looks_like_free_text(event.collaborator_token):
        flags.append("collaborator_token_looks_like_free_text")
    return _deduplicate(flags)

def _audit_flags(event: SolidaryEvent) -> List[str]:
    flags = [
        "solidary_bonus_demo",
        "voluntary_action_required",
        "priority_user_confirmation_required",
        "same_transport_context_required",
        "general_use_seat_required",
        "no_diagnosis_visible",
        "no_cud_visible",
        "no_real_sube_integration",
        "no_real_discount_applied",
    ]
    if event.seat_type == SeatType.GENERAL_USE:
        flags.append("general_use_seat_context")
    if event.seat_type == SeatType.LEGAL_PRIORITY:
        flags.append("legal_priority_seat_context_not_rewardable")
    return _deduplicate(flags)

def _primary_rejection_reason(
    risk_flags: List[str],
) -> SolidaryRejectionReason:
    if "same_user_not_allowed" in risk_flags:
        return SolidaryRejectionReason.SAME_USER_NOT_ALLOWED
    if "no_voluntary_seat_yield" in risk_flags:
        return SolidaryRejectionReason.NO_VOLUNTARY_SEAT_YIELD
    if "priority_user_did_not_confirm" in risk_flags:
        return SolidaryRejectionReason.PRIORITY_USER_DID_NOT_CONFIRM
    if "not_same_transport_context" in risk_flags:
        return SolidaryRejectionReason.NOT_SAME_TRANSPORT_CONTEXT
    if "legal_priority_seat_not_rewardable" in risk_flags:
        return SolidaryRejectionReason.LEGAL_PRIORITY_SEAT_NOT_REWARDABLE
    return SolidaryRejectionReason.SENSITIVE_DATA_REJECTED

def _result(
    event: SolidaryEvent,
    status: SolidaryRecognitionStatus,
    accepted: bool,
    recognition_token: Optional[str],
    rejection_reason: SolidaryRejectionReason,
    risk_flags: List[str],
    audit_flags: List[str],
) -> SolidaryRecognitionResult:
    return SolidaryRecognitionResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=SIMULATOR_VERSION,
        demo_mode=DEMO_MODE,
        status=status,
        accepted=accepted,
        recognition_token=recognition_token,
        priority_user_token=event.priority_user_token,
        collaborator_token=event.collaborator_token,
        seat_type=event.seat_type,
        rejection_reason=rejection_reason,
        risk_flags=_deduplicate(risk_flags),
        audit_flags=_deduplicate(audit_flags),
        bonus_summary={
            "demo_only": True,
            "real_discount_applied": False,
            "real_balance_modified": False,
            "recognition_type": (
                "solidary_bonus_demo" if accepted else "no_bonus_generated"
            ),
            "seat_type": event.seat_type.value,
            "same_transport_context": event.same_transport_context,
            "voluntary_seat_yield": event.voluntary_seat_yield,
            "priority_user_confirmed": event.priority_user_confirms_seat_yield,
            "public_visibility": "Usuario SUBE Prioridad",
            "contains_diagnosis": False,
            "contains_cud_visible": False,
            "contains_medical_certificate": False,
            "contains_identity_data": False,
        },
        privacy_notice=(
            "El Bono Solidario demo no expone DNI, nombre, diagnóstico, CUD "
            "visible, certificado médico, historia clínica ni causa de prioridad."
        ),
        legal_scope_notice=(
            "Modelo conceptual sin integración real con SUBE, Red SUBE, "
            "validadores, molinetes, tarjetas, saldo ni tarifa real."
        ),
        driver_burden=(
            "El chofer no decide beneficios, no valida causas médicas y no asume "
            "una obligación nueva."
        ),
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
    )

def _looks_like_free_text(token: str) -> bool:
    normalized = token.lower().strip()
    suspicious_terms = {
        "dni",
        "diagnostico",
        "diagnóstico",
        "cud",
        "certificado",
        "medico",
        "médico",
        "embarazo",
        "fractura",
        "lesion",
        "lesión",
        "discapacidad",
        "saldo",
        "dinero",
        "tarifa",
        "gratis",
        "bono solidario",
        "red sube",
    }
    return any(term in normalized for term in suspicious_terms) or len(
        normalized.split()
    ) > 1

def _require_non_empty(payload: Dict[str, str]) -> None:
    for field_name, value in payload.items():
        if not value or not str(value).strip():
            raise ValueError(
                f"El campo demostrativo {field_name} no puede estar vacío."
            )

def _deduplicate(flags: List[str]) -> List[str]:
    seen = set()
    result = []
    for flag in flags:
        if flag not in seen:
            seen.add(flag)
            result.append(flag)
    return result

if __name__ == "__main__":
    import json
    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_rejected_demo(), indent=2, ensure_ascii=False))
