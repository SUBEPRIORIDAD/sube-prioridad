"""
SUBE Prioridad — Frontend conceptual de Bono Solidario.
Este módulo modela la capa de usuario desde la cual una persona usuaria de
SUBE Prioridad podría confirmar, desde su cuenta SUBE demostrativa, una
sincronización de Bono Solidario hacia otro usuario/dispositivo.

No representa implementación oficial.
No integra SUBE real. No integra Red SUBE real.
No transfiere beneficios reales. No acredita puntos reales. No modifica tarifas.
No consulta cuentas reales. No consulta tarjetas reales.
No procesa DNI, nombre, domicilio, diagnóstico ni CUD.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Frontend Conceptual de Bono Solidario"
FLOW_VERSION = "0.1.0"
DEMO_MODE = True

PROHIBITED_FIELDS = {
    "dni",
    "documento",
    "nombre",
    "apellido",
    "domicilio",
    "direccion",
    "dirección",
    "diagnostico",
    "diagnóstico",
    "historia_clinica",
    "historia_clínica",
    "certificado_medico",
    "certificado_médico",
    "cud",
    "discapacidad",
    "patologia",
    "patología",
    "medico",
    "médico",
    "obra_social",
    "telefono",
    "teléfono",
    "email",
    "correo",
}

class FrontendChannel(str, Enum):
    WEB_PORTAL = "web_portal"
    MOBILE_APP = "mobile_app"
    ACCOUNT_PANEL = "account_panel"
    ASSISTED_DIGITAL_CHANNEL = "assisted_digital_channel"

class RecipientSelectionMethod(str, Enum):
    DEVICE_PROXIMITY_DEMO = "device_proximity_demo"
    TEMPORARY_QR_DEMO = "temporary_qr_demo"
    TEMPORARY_CODE_DEMO = "temporary_code_demo"
    SAME_TRIP_CONTEXT_DEMO = "same_trip_context_demo"

class SeatType(str, Enum):
    GENERAL_USE = "general_use"
    LEGAL_PRIORITY = "legal_priority"

class FrontendDecisionStatus(str, Enum):
    READY_FOR_SECURITY_FLOW = "ready_for_security_flow"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"

@dataclass(frozen=True)
class PriorityAccountFrontendContext:
    """Contexto demostrativo de cuenta SUBE del usuario prioritario sin identidad civil."""
    account_demo_id: str
    card_demo_id: str
    priority_user_token: str
    priority_attribute_token: str
    account_active: bool
    card_associated: bool
    priority_attribute_active: bool
    previously_accredited_need: bool
    solidary_bonus_frontend_enabled: bool

@dataclass(frozen=True)
class SolidaryFrontendTransportContext:
    """Contexto mínimo demostrativo del viaje sin geolocalización real."""
    country: str
    network_demo_id: str
    route_demo_id: str
    vehicle_demo_id: str
    trip_demo_id: str
    time_window_demo_id: str
    validation_paid: bool

@dataclass(frozen=True)
class CandidateCollaborator:
    """Posible destinatario demostrativo del Bono Solidario sin datos personales."""
    collaborator_token: str
    selection_method: RecipientSelectionMethod
    same_transport_context: bool
    voluntary_seat_yield_declared: bool
    collaborator_claims_reward: bool
    seat_type: SeatType

@dataclass(frozen=True)
class SolidaryBonusFrontendRequest:
    """Solicitud conceptual iniciada desde el frontend del usuario SUBE Prioridad."""
    frontend_request_demo_id: str
    frontend_channel: FrontendChannel
    priority_account_context: PriorityAccountFrontendContext
    transport_context: SolidaryFrontendTransportContext
    candidate_collaborator: CandidateCollaborator
    priority_user_confirms_send: bool
    priority_user_understands_demo_scope: bool

@dataclass(frozen=True)
class SolidaryBonusFrontendResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: FrontendDecisionStatus
    frontend_ready: bool
    handoff_to_security_flow_enabled: bool
    solidary_point_demo: int
    risk_flags: List[str]
    reason: str
    frontend_channel: FrontendChannel
    recipient_selection_method: RecipientSelectionMethod
    security_flow_payload_demo: Dict[str, Any]
    priority_user_control: str
    collaborator_limit: str
    validation_context_notice: str
    privacy_notice: str
    driver_burden: str
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

def create_demo_priority_account_frontend_context(
    account_demo_id: str = "demo-sube-account-001",
    card_demo_id: str = "demo-sube-card-001",
    priority_user_token: str = "demo-priority-user-001",
    priority_attribute_token: str = "demo-priority-attribute-001",
    account_active: bool = True,
    card_associated: bool = True,
    priority_attribute_active: bool = True,
    previously_accredited_need: bool = True,
    solidary_bonus_frontend_enabled: bool = True,
) -> PriorityAccountFrontendContext:
    required_values = {
        "account_demo_id": account_demo_id,
        "card_demo_id": card_demo_id,
        "priority_user_token": priority_user_token,
        "priority_attribute_token": priority_attribute_token,
    }
    for field_name, value in required_values.items():
        if not value or not value.strip():
            raise ValueError(f"El campo demostrativo {field_name} no puede estar vacío.")
    assert_no_prohibited_fields(required_values)
    return PriorityAccountFrontendContext(
        account_demo_id=account_demo_id.strip(),
        card_demo_id=card_demo_id.strip(),
        priority_user_token=priority_user_token.strip(),
        priority_attribute_token=priority_attribute_token.strip(),
        account_active=account_active,
        card_associated=card_associated,
        priority_attribute_active=priority_attribute_active,
        previously_accredited_need=previously_accredited_need,
        solidary_bonus_frontend_enabled=solidary_bonus_frontend_enabled,
    )
def create_demo_solidary_frontend_transport_context(
    country: str = "Argentina",
    network_demo_id: str = "demo-network-sube",
    route_demo_id: str = "demo-route-001",
    vehicle_demo_id: str = "demo-vehicle-001",
    trip_demo_id: str = "demo-trip-001",
    time_window_demo_id: str = "demo-window-001",
    validation_paid: bool = True,
) -> SolidaryFrontendTransportContext:
    assert_no_prohibited_fields({
        "network_demo_id": network_demo_id,
        "route_demo_id": route_demo_id,
        "vehicle_demo_id": vehicle_demo_id,
        "trip_demo_id": trip_demo_id,
        "time_window_demo_id": time_window_demo_id,
    })
    return SolidaryFrontendTransportContext(
        country=country,
        network_demo_id=network_demo_id,
        route_demo_id=route_demo_id,
        vehicle_demo_id=vehicle_demo_id,
        trip_demo_id=trip_demo_id,
        time_window_demo_id=time_window_demo_id,
        validation_paid=validation_paid,
    )

def create_demo_candidate_collaborator(
    collaborator_token: str = "demo-collaborator-001",
    selection_method: RecipientSelectionMethod = RecipientSelectionMethod.SAME_TRIP_CONTEXT_DEMO,
    same_transport_context: bool = True,
    voluntary_seat_yield_declared: bool = True,
    collaborator_claims_reward: bool = False,
    seat_type: SeatType = SeatType.GENERAL_USE,
) -> CandidateCollaborator:
    if not collaborator_token or not collaborator_token.strip():
        raise ValueError("El token demostrativo del colaborador no puede estar vacío.")
    assert_no_prohibited_fields({"collaborator_token": collaborator_token})
    return CandidateCollaborator(
        collaborator_token=collaborator_token.strip(),
        selection_method=selection_method,
        same_transport_context=same_transport_context,
        voluntary_seat_yield_declared=voluntary_seat_yield_declared,
        collaborator_claims_reward=collaborator_claims_reward,
        seat_type=seat_type,
    )

def create_demo_solidary_bonus_frontend_request(
    frontend_request_demo_id: str = "demo-solidary-frontend-request-001",
    frontend_channel: FrontendChannel = FrontendChannel.MOBILE_APP,
    priority_account_context: Optional[PriorityAccountFrontendContext] = None,
    transport_context: Optional[SolidaryFrontendTransportContext] = None,
    candidate_collaborator: Optional[CandidateCollaborator] = None,
    priority_user_confirms_send: bool = True,
    priority_user_understands_demo_scope: bool = True,
) -> SolidaryBonusFrontendRequest:
    if not frontend_request_demo_id or not frontend_request_demo_id.strip():
        raise ValueError("El identificador demostrativo del frontend no puede estar vacío.")
    assert_no_prohibited_fields({"frontend_request_demo_id": frontend_request_demo_id})
    return SolidaryBonusFrontendRequest(
        frontend_request_demo_id=frontend_request_demo_id.strip(),
        frontend_channel=frontend_channel,
        priority_account_context=priority_account_context or create_demo_priority_account_frontend_context(),
        transport_context=transport_context or create_demo_solidary_frontend_transport_context(),
        candidate_collaborator=candidate_collaborator or create_demo_candidate_collaborator(),
        priority_user_confirms_send=priority_user_confirms_send,
        priority_user_understands_demo_scope=priority_user_understands_demo_scope,
    )
def evaluate_solidary_bonus_frontend_request(
    request: SolidaryBonusFrontendRequest,
) -> SolidaryBonusFrontendResult:
    assert_no_prohibited_fields({
        "frontend_request_demo_id": request.frontend_request_demo_id,
        "account_demo_id": request.priority_account_context.account_demo_id,
        "card_demo_id": request.priority_account_context.card_demo_id,
        "priority_user_token": request.priority_account_context.priority_user_token,
        "priority_attribute_token": request.priority_account_context.priority_attribute_token,
        "collaborator_token": request.candidate_collaborator.collaborator_token,
    })
    
    risk_flags = _risk_flags(request)
    if _requires_review_only(risk_flags):
        return _needs_review_result(request, risk_flags)
    if risk_flags:
        return _rejected_result(request, risk_flags)
        
    return SolidaryBonusFrontendResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=FLOW_VERSION,
        demo_mode=DEMO_MODE,
        status=FrontendDecisionStatus.READY_FOR_SECURITY_FLOW,
        frontend_ready=True,
        handoff_to_security_flow_enabled=True,
        solidary_point_demo=0,
        risk_flags=[],
        reason="El frontend conceptual está listo para remitir la solicitud al flujo de seguridad.",
        frontend_channel=request.frontend_channel,
        recipient_selection_method=request.candidate_collaborator.selection_method,
        security_flow_payload_demo=_security_flow_payload_demo(request),
        priority_user_control=_priority_user_control_notice(),
        collaborator_limit=_collaborator_limit_notice(),
        validation_context_notice=_validation_context_notice(),
        privacy_notice=_privacy_notice(),
        driver_burden=_driver_burden_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )

def result_to_dict(result: SolidaryBonusFrontendResult) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "frontend_ready": result.frontend_ready,
        "handoff_to_security_flow_enabled": result.handoff_to_security_flow_enabled,
        "solidary_point_demo": result.solidary_point_demo,
        "risk_flags": result.risk_flags,
        "reason": result.reason,
        "frontend_channel": result.frontend_channel.value,
        "recipient_selection_method": result.recipient_selection_method.value,
        "security_flow_payload_demo": result.security_flow_payload_demo,
        "priority_user_control": result.priority_user_control,
        "collaborator_limit": result.collaborator_limit,
        "validation_context_notice": result.validation_context_notice,
        "privacy_notice": result.privacy_notice,
        "driver_burden": result.driver_burden,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }

def run_demo() -> Dict[str, Any]:
    request = create_demo_solidary_bonus_frontend_request(
        frontend_channel=FrontendChannel.MOBILE_APP,
        priority_user_confirms_send=True,
        priority_user_understands_demo_scope=True,
    )
    result = evaluate_solidary_bonus_frontend_request(request)
    return result_to_dict(result)
def _risk_flags(request: SolidaryBonusFrontendRequest) -> List[str]:
    flags: List[str] = []
    account = request.priority_account_context
    context = request.transport_context
    collaborator = request.candidate_collaborator
    
    if context.country.strip().lower() != "argentina":
        flags.append("outside_argentina_context")
    if not context.validation_paid:
        flags.append("validation_payment_not_confirmed")
    if not account.account_active:
        flags.append("sube_account_not_active")
    if not account.card_associated:
        flags.append("sube_card_not_associated")
    if not account.priority_attribute_active:
        flags.append("priority_attribute_not_active")
    if not account.previously_accredited_need:
        flags.append("need_not_previously_accredited")
    if not account.solidary_bonus_frontend_enabled:
        flags.append("solidary_bonus_frontend_not_enabled_by_user")
    if not request.priority_user_confirms_send:
        flags.append("priority_user_confirmation_required")
    if not request.priority_user_understands_demo_scope:
        flags.append("demo_scope_acknowledgement_required")
    if _looks_like_free_text(account.priority_user_token):
        flags.append("priority_user_token_looks_like_free_text")
    if _looks_like_free_text(account.priority_attribute_token):
        flags.append("priority_attribute_token_looks_like_free_text")
    if _looks_like_free_text(collaborator.collaborator_token):
        flags.append("collaborator_token_looks_like_free_text")
    if account.priority_user_token == collaborator.collaborator_token:
        flags.append("self_bonus_attempt")
    if not collaborator.same_transport_context:
        flags.append("different_transport_context")
    if not collaborator.voluntary_seat_yield_declared:
        flags.append("no_voluntary_seat_yield_declared")
    if collaborator.collaborator_claims_reward:
        flags.append("collaborator_unilateral_claim")
    if collaborator.seat_type != SeatType.GENERAL_USE:
        flags.append("legal_priority_seat_not_eligible")
    return flags

def _requires_review_only(risk_flags: List[str]) -> bool:
    return bool(risk_flags) and set(risk_flags).issubset({"demo_scope_acknowledgement_required"})

def _rejected_result(request: SolidaryBonusFrontendRequest, risk_flags: List[str]) -> SolidaryBonusFrontendResult:
    return SolidaryBonusFrontendResult(
        project=PROJECT_NAME, module=MODULE_NAME, version=FLOW_VERSION, demo_mode=DEMO_MODE,
        status=FrontendDecisionStatus.REJECTED, frontend_ready=False, handoff_to_security_flow_enabled=False,
        solidary_point_demo=0, risk_flags=risk_flags,
        reason="El frontend conceptual no puede preparar el handoff porque la solicitud no supera los filtros.",
        frontend_channel=request.frontend_channel, recipient_selection_method=request.candidate_collaborator.selection_method,
        security_flow_payload_demo={}, priority_user_control=_priority_user_control_notice(),
        collaborator_limit=_collaborator_limit_notice(), validation_context_notice=_validation_context_notice(),
        privacy_notice=_privacy_notice(), driver_burden=_driver_burden_notice(), warnings=_common_warnings(), timestamp_utc=_now_utc(),
    )

def _needs_review_result(request: SolidaryBonusFrontendRequest, risk_flags: List[str]) -> SolidaryBonusFrontendResult:
    return SolidaryBonusFrontendResult(
        project=PROJECT_NAME, module=MODULE_NAME, version=FLOW_VERSION, demo_mode=DEMO_MODE,
        status=FrontendDecisionStatus.NEEDS_REVIEW, frontend_ready=False, handoff_to_security_flow_enabled=False,
        solidary_point_demo=0, risk_flags=risk_flags,
        reason="La solicitud conceptual requiere revisión o una confirmación adicional.",
        frontend_channel=request.frontend_channel, recipient_selection_method=request.candidate_collaborator.selection_method,
        security_flow_payload_demo={}, priority_user_control=_priority_user_control_notice(),
        collaborator_limit=_collaborator_limit_notice(), validation_context_notice=_validation_context_notice(),
        privacy_notice=_privacy_notice(), driver_burden=_driver_burden_notice(), warnings=_common_warnings(), timestamp_utc=_now_utc(),
    )

def _security_flow_payload_demo(request: SolidaryBonusFrontendRequest) -> Dict[str, Any]:
    return {
        "sync_event_demo_id": request.frontend_request_demo_id,
        "priority_user_token": request.priority_account_context.priority_user_token,
        "priority_attribute_token": request.priority_account_context.priority_attribute_token,
        "collaborator_token": request.candidate_collaborator.collaborator_token,
        "country": request.transport_context.country,
        "network_demo_id": request.transport_context.network_demo_id,
        "route_demo_id": request.transport_context.route_demo_id,
        "vehicle_demo_id": request.transport_context.vehicle_demo_id,
        "trip_demo_id": request.transport_context.trip_demo_id,
        "time_window_demo_id": request.transport_context.time_window_demo_id,
        "seat_type": request.candidate_collaborator.seat_type.value,
        "priority_user_confirms_sync": request.priority_user_confirms_send,
        "voluntary_seat_yield": request.candidate_collaborator.voluntary_seat_yield_declared,
        "same_transport_context": request.candidate_collaborator.same_transport_context,
    }

def _looks_like_free_text(token: str) -> bool:
    normalized = token.lower().strip()
    suspicious_terms = {"quiero", "gratis", "beneficio", "tarifa", "social", "diagnostico", "diagnóstico", "cud", "certificado", "medico", "médico", "andis", "sancion", "sanción", "ranking", "vigilancia", "premio", "puntos", "bono solidario"}
    return any(term in normalized for term in suspicious_terms) or len(normalized.split()) > 1

def _priority_user_control_notice() -> str:
    return "El usuario SUBE Prioridad inicia y confirma el envío conceptual. Sin su confirmación no hay handoff al flujo de seguridad."

def _collaborator_limit_notice() -> str:
    return "El colaborador no puede reclamar Bono Solidario unilateralmente. Su eventual reconocimiento depende de la confirmación del usuario SUBE Prioridad."

def _validation_context_notice() -> str:
    return "El frontend conceptual presupone un contexto de viaje validado. El Bono Solidario no se prepara si no existe validación demostrativa de pago."

def _privacy_notice() -> str:
    return "El frontend no revela DNI, nombre, domicilio, diagnóstico, CUD, historia clínica ni certificado médico. Sólo utiliza tokens demostrativos."

def _driver_burden_notice() -> str:
    return "El chofer no verifica, no decide, no media, no administra ni transfiere el Bono Solidario."

def _common_warnings() -> List[str]:
    return ["Frontend conceptual y demostrativo.", "Sin implementación oficial vigente.", "Sin integración real con SUBE.", "Sin integración real con Red SUBE.", "Sin transferencia real de beneficios."]

def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()

if __name__ == "__main__":
    import json
    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
