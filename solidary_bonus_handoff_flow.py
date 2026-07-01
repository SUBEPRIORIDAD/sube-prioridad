"""
SUBE Prioridad — Handoff seguro de Bono Solidario.

Este módulo conecta conceptualmente:

    1. El frontend demostrativo de Bono Solidario.
    2. El payload mínimo generado por el usuario SUBE Prioridad.
    3. El flujo de seguridad antifraude.
    4. El resultado final demostrativo.

No representa implementación oficial.
No integra SUBE real.
No integra Red SUBE real.
No consulta cuentas reales.
No consulta tarjetas reales.
No transfiere beneficios reales.
No acredita puntos reales.
No modifica tarifas.
No procesa DNI.
No procesa nombre.
No procesa domicilio.
No procesa diagnóstico.
No procesa CUD.
No procesa certificados médicos.
No genera sanciones.
No genera rankings.
No genera vigilancia.
No impone obligaciones a pasajeros.
No impone cargas operativas al chofer.

Regla central:
    El frontend no otorga Bono Solidario.
    El frontend sólo prepara el handoff.
    El handoff sólo puede avanzar si el frontend fue aprobado.
    El resultado final depende del flujo de seguridad antifraude.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


from solidary_bonus_frontend_flow import (
    FrontendDecisionStatus,
    SeatType as FrontendSeatType,
    SolidaryBonusFrontendRequest,
    SolidaryBonusFrontendResult,
    create_demo_solidary_bonus_frontend_request,
    evaluate_solidary_bonus_frontend_request,
    result_to_dict as frontend_result_to_dict,
)

from solidary_sync_security_flow import (
    SeatType as SecuritySeatType,
    SyncSecurityLedger,
    create_demo_sync_request,
    create_demo_transport_sync_context,
    result_to_dict as security_result_to_dict,
    simulate_solidary_sync_security,
)


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Handoff Seguro de Bono Solidario"
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


class HandoffStatus(str, Enum):
    COMPLETED = "completed"
    BLOCKED_BY_FRONTEND = "blocked_by_frontend"
    REJECTED_BY_SECURITY = "rejected_by_security"
    NEEDS_REVIEW = "needs_review"


@dataclass(frozen=True)
class SolidaryBonusHandoffRequest:
    """
    Solicitud conceptual de handoff.

    Recibe una solicitud de frontend y la somete al flujo de seguridad.
    """

    handoff_demo_id: str
    frontend_request: SolidaryBonusFrontendRequest


@dataclass(frozen=True)
class SolidaryBonusHandoffResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: HandoffStatus
    frontend_status: str
    security_status: Optional[str]
    handoff_completed: bool
    frontend_ready: bool
    security_flow_executed: bool
    solidary_point_demo: int
    risk_flags: List[str]
    frontend_result: Dict[str, Any]
    security_result: Dict[str, Any]
    reason: str
    priority_user_control: str
    collaborator_limit: str
    security_notice: str
    privacy_notice: str
    driver_burden: str
    warnings: List[str]
    timestamp_utc: str


def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    """
    Rechaza campos personales, médicos o sensibles.
    """
    normalized_keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))

    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )


def create_demo_solidary_bonus_handoff_request(
    handoff_demo_id: str = "demo-solidary-handoff-001",
    frontend_request: Optional[SolidaryBonusFrontendRequest] = None,
) -> SolidaryBonusHandoffRequest:
    """
    Crea una solicitud demostrativa de handoff.
    """
    if not handoff_demo_id or not handoff_demo_id.strip():
        raise ValueError("El identificador demostrativo de handoff no puede estar vacío.")

    assert_no_prohibited_fields({"handoff_demo_id": handoff_demo_id})

    return SolidaryBonusHandoffRequest(
        handoff_demo_id=handoff_demo_id.strip(),
        frontend_request=frontend_request or create_demo_solidary_bonus_frontend_request(),
    )


def execute_solidary_bonus_handoff(
    request: SolidaryBonusHandoffRequest,
    ledger: Optional[SyncSecurityLedger] = None,
) -> SolidaryBonusHandoffResult:
    """
    Ejecuta el handoff conceptual desde frontend hacia seguridad.

    El flujo se detiene si el frontend no está listo.
    Si el frontend está listo, el payload mínimo se transforma en una solicitud
    del flujo de seguridad antifraude.
    """
    assert_no_prohibited_fields(
        {
            "handoff_demo_id": request.handoff_demo_id,
            "frontend_request_demo_id": request.frontend_request.frontend_request_demo_id,
        }
    )

    frontend_result = evaluate_solidary_bonus_frontend_request(
        request.frontend_request
    )

    frontend_data = frontend_result_to_dict(frontend_result)

    if frontend_result.status != FrontendDecisionStatus.READY_FOR_SECURITY_FLOW:
        return _blocked_by_frontend_result(
            frontend_result=frontend_result,
            frontend_data=frontend_data,
        )

    security_request = _build_security_request_from_frontend_result(
        frontend_result
    )

    security_result = simulate_solidary_sync_security(
        request=security_request,
        ledger=ledger or SyncSecurityLedger(),
    )

    security_data = security_result_to_dict(security_result)

    if security_data["status"] == "accepted":
        return SolidaryBonusHandoffResult(
            project=PROJECT_NAME,
            module=MODULE_NAME,
            version=FLOW_VERSION,
            demo_mode=DEMO_MODE,
            status=HandoffStatus.COMPLETED,
            frontend_status=frontend_data["status"],
            security_status=security_data["status"],
            handoff_completed=True,
            frontend_ready=True,
            security_flow_executed=True,
            solidary_point_demo=security_data["solidary_point_demo"],
            risk_flags=[],
            frontend_result=frontend_data,
            security_result=security_data,
            reason=(
                "Handoff demostrativo completado. El frontend preparó el payload "
                "mínimo y el flujo de seguridad aceptó la sincronización solidaria."
            ),
            priority_user_control=_priority_user_control_notice(),
            collaborator_limit=_collaborator_limit_notice(),
            security_notice=_security_notice(),
            privacy_notice=_privacy_notice(),
            driver_burden=_driver_burden_notice(),
            warnings=_common_warnings(),
            timestamp_utc=_now_utc(),
        )

    if security_data["status"] == "needs_review":
        return SolidaryBonusHandoffResult(
            project=PROJECT_NAME,
            module=MODULE_NAME,
            version=FLOW_VERSION,
            demo_mode=DEMO_MODE,
            status=HandoffStatus.NEEDS_REVIEW,
            frontend_status=frontend_data["status"],
            security_status=security_data["status"],
            handoff_completed=False,
            frontend_ready=True,
            security_flow_executed=True,
            solidary_point_demo=0,
            risk_flags=security_data["risk_flags"],
            frontend_result=frontend_data,
            security_result=security_data,
            reason=(
                "El frontend estaba listo, pero el flujo de seguridad marcó "
                "la sincronización para revisión demostrativa."
            ),
            priority_user_control=_priority_user_control_notice(),
            collaborator_limit=_collaborator_limit_notice(),
            security_notice=_security_notice(),
            privacy_notice=_privacy_notice(),
            driver_burden=_driver_burden_notice(),
            warnings=_common_warnings(),
            timestamp_utc=_now_utc(),
        )

    return SolidaryBonusHandoffResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=FLOW_VERSION,
        demo_mode=DEMO_MODE,
        status=HandoffStatus.REJECTED_BY_SECURITY,
        frontend_status=frontend_data["status"],
        security_status=security_data["status"],
        handoff_completed=False,
        frontend_ready=True,
        security_flow_executed=True,
        solidary_point_demo=0,
        risk_flags=security_data["risk_flags"],
        frontend_result=frontend_data,
        security_result=security_data,
        reason=(
            "El frontend estaba listo, pero el flujo de seguridad rechazó "
            "la sincronización solidaria demostrativa."
        ),
        priority_user_control=_priority_user_control_notice(),
        collaborator_limit=_collaborator_limit_notice(),
        security_notice=_security_notice(),
        privacy_notice=_privacy_notice(),
        driver_burden=_driver_burden_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def result_to_dict(result: SolidaryBonusHandoffResult) -> Dict[str, Any]:
    """
    Convierte el resultado del handoff a diccionario serializable.
    """
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "frontend_status": result.frontend_status,
        "security_status": result.security_status,
        "handoff_completed": result.handoff_completed,
        "frontend_ready": result.frontend_ready,
        "security_flow_executed": result.security_flow_executed,
        "solidary_point_demo": result.solidary_point_demo,
        "risk_flags": result.risk_flags,
        "frontend_result": result.frontend_result,
        "security_result": result.security_result,
        "reason": result.reason,
        "priority_user_control": result.priority_user_control,
        "collaborator_limit": result.collaborator_limit,
        "security_notice": result.security_notice,
        "privacy_notice": result.privacy_notice,
        "driver_burden": result.driver_burden,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    """
    Ejecuta una demostración estable del handoff seguro.
    """
    request = create_demo_solidary_bonus_handoff_request()

    result = execute_solidary_bonus_handoff(request)

    return result_to_dict(result)


def _blocked_by_frontend_result(
    frontend_result: SolidaryBonusFrontendResult,
    frontend_data: Dict[str, Any],
) -> SolidaryBonusHandoffResult:
    return SolidaryBonusHandoffResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=FLOW_VERSION,
        demo_mode=DEMO_MODE,
        status=HandoffStatus.BLOCKED_BY_FRONTEND,
        frontend_status=frontend_data["status"],
        security_status=None,
        handoff_completed=False,
        frontend_ready=False,
        security_flow_executed=False,
        solidary_point_demo=0,
        risk_flags=frontend_data["risk_flags"],
        frontend_result=frontend_data,
        security_result={},
        reason=(
            "El handoff fue bloqueado porque el frontend conceptual no quedó "
            "listo para pasar al flujo de seguridad."
        ),
        priority_user_control=_priority_user_control_notice(),
        collaborator_limit=_collaborator_limit_notice(),
        security_notice=_security_notice(),
        privacy_notice=_privacy_notice(),
        driver_burden=_driver_burden_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def _build_security_request_from_frontend_result(
    frontend_result: SolidaryBonusFrontendResult,
):
    """
    Convierte el payload mínimo del frontend en una solicitud del flujo de seguridad.

    No incorpora datos sensibles.
    No consulta sistemas reales.
    No agrega identidad civil.
    """
    payload = frontend_result.security_flow_payload_demo

    assert_no_prohibited_fields(payload)

    actual_context = create_demo_transport_sync_context(
        country=payload["country"],
        network_demo_id=payload["network_demo_id"],
        route_demo_id=payload["route_demo_id"],
        vehicle_demo_id=payload["vehicle_demo_id"],
        trip_demo_id=payload["trip_demo_id"],
        time_window_demo_id=payload["time_window_demo_id"],
    )

    expected_context = actual_context

    if payload.get("same_transport_context") is False:
        expected_context = create_demo_transport_sync_context(
            country=payload["country"],
            network_demo_id=payload["network_demo_id"],
            route_demo_id=payload["route_demo_id"],
            vehicle_demo_id="different-demo-vehicle",
            trip_demo_id=payload["trip_demo_id"],
            time_window_demo_id=payload["time_window_demo_id"],
        )

    return create_demo_sync_request(
        sync_event_demo_id=payload["sync_event_demo_id"],
        priority_user_token=payload["priority_user_token"],
        priority_attribute_token=payload["priority_attribute_token"],
        collaborator_token=payload["collaborator_token"],
        previously_accredited_need=True,
        priority_user_confirms_sync=payload["priority_user_confirms_sync"],
        voluntary_seat_yield=payload["voluntary_seat_yield"],
        collaborator_claims_reward=False,
        seat_type=_map_seat_type_to_security(payload["seat_type"]),
        actual_context=actual_context,
        expected_context=expected_context,
    )


def _map_seat_type_to_security(seat_type: str) -> SecuritySeatType:
    if seat_type == FrontendSeatType.GENERAL_USE.value:
        return SecuritySeatType.GENERAL_USE

    if seat_type == FrontendSeatType.LEGAL_PRIORITY.value:
        return SecuritySeatType.LEGAL_PRIORITY

    raise ValueError(f"Tipo de asiento demostrativo no reconocido: {seat_type}")


def _priority_user_control_notice() -> str:
    return (
        "El usuario SUBE Prioridad conserva el control de la confirmación. "
        "El handoff no puede ejecutarse sin un frontend previamente aprobado."
    )


def _collaborator_limit_notice() -> str:
    return (
        "El colaborador no puede reclamar Bono Solidario unilateralmente. "
        "El reconocimiento depende de la confirmación del usuario SUBE Prioridad "
        "y del resultado del flujo de seguridad."
    )


def _security_notice() -> str:
    return (
        "El handoff transforma un payload mínimo en una solicitud antifraude. "
        "El frontend no acredita puntos ni beneficios por sí mismo."
    )


def _privacy_notice() -> str:
    return (
        "El handoff no revela DNI, nombre, domicilio, diagnóstico, CUD, historia clínica "
        "ni certificado médico. Sólo utiliza tokens demostrativos y contexto mínimo."
    )


def _driver_burden_notice() -> str:
    return (
        "El chofer no verifica, no decide, no media, no administra ni transfiere "
        "el Bono Solidario."
    )


def _common_warnings() -> List[str]:
    return [
        "Handoff conceptual y demostrativo.",
        "Sin implementación oficial vigente.",
        "Sin integración real con SUBE.",
        "Sin integración real con Red SUBE.",
        "Sin transferencia real de beneficios.",
        "Sin puntos reales.",
        "Sin modificación tarifaria.",
        "Sin consulta a cuentas reales.",
        "Sin consulta a tarjetas reales.",
        "Sin datos sensibles.",
        "Sin diagnóstico médico.",
        "Sin CUD real.",
        "Sin certificados médicos reales.",
        "Sin sanciones.",
        "Sin ranking.",
        "Sin vigilancia.",
        "Sin obligación para pasajeros.",
        "Sin carga operativa para el chofer.",
        "El frontend sólo prepara el handoff.",
        "El flujo de seguridad decide el resultado demostrativo.",
    ]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
