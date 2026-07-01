"""
SUBE Prioridad — Flujo conceptual de preferencias y alertas pasivas.

Este módulo modela cómo una persona usuaria de SUBE Prioridad podría configurar
la forma en que desea recibir o comunicar asistencia durante un viaje.

No representa implementación oficial.
No integra SUBE real.
No integra Red SUBE real.
No modifica validadoras reales.
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

Principios:
    - La asistencia debe respetar la autonomía del usuario.
    - El usuario conserva control sobre el modo de exposición.
    - El sistema debe privilegiar modos pasivos, silenciosos o discretos.
    - Toda alerta debe ser genérica.
    - El transporte no necesita conocer el diagnóstico.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Preferencias y Alertas Pasivas"
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


class AssistanceMode(str, Enum):
    SILENT = "silent"
    PASSIVE = "passive"
    DISCREET = "discreet"
    PREVENTIVE = "preventive"
    VISIBLE_GENERIC = "visible_generic"
    LUMINOUS_GENERIC = "luminous_generic"


class AlertChannel(str, Enum):
    NONE = "none"
    INTERNAL_RECORD = "internal_record"
    PASSIVE_SIGNAL = "passive_signal"
    DISCREET_SIGNAL = "discreet_signal"
    GENERIC_VISUAL_SIGNAL = "generic_visual_signal"
    GENERIC_LUMINOUS_SIGNAL = "generic_luminous_signal"


class AlertDecisionStatus(str, Enum):
    ALLOWED = "allowed"
    BLOCKED = "blocked"
    DEGRADED = "degraded"


@dataclass(frozen=True)
class UserAlertPreference:
    """
    Preferencia demostrativa del usuario.

    No expresa diagnóstico.
    No expresa condición médica.
    No expresa identidad civil.
    """

    assistance_mode: AssistanceMode
    allow_passive_signal: bool
    allow_discreet_signal: bool
    allow_visible_generic_signal: bool
    allow_luminous_generic_signal: bool
    allow_internal_record: bool


@dataclass(frozen=True)
class AlertContext:
    """
    Contexto conceptual del viaje.

    No contiene geolocalización real.
    No representa una unidad real.
    No consulta sistemas externos.
    """

    country: str
    network_demo_id: str
    route_demo_id: str
    vehicle_demo_id: str
    trip_demo_id: str
    occupancy_level: str
    priority_attribute_active: bool
    previously_accredited_need: bool


@dataclass(frozen=True)
class PassiveAlertRequest:
    """
    Solicitud conceptual de alerta.

    No debe incluir datos personales ni médicos.
    """

    alert_request_demo_id: str
    priority_attribute_token: str
    preference: UserAlertPreference
    context: AlertContext


@dataclass(frozen=True)
class PassiveAlertResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: AlertDecisionStatus
    selected_channel: AlertChannel
    assistance_mode: AssistanceMode
    alert_enabled: bool
    exposure_level: str
    message: str
    blocked_reasons: List[str]
    privacy_notice: str
    driver_burden: str
    passenger_burden: str
    warnings: List[str]
    timestamp_utc: str


def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    """
    Rechaza datos incompatibles con el diseño de privacidad.
    """
    normalized_keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))

    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )


def create_demo_user_alert_preference(
    assistance_mode: AssistanceMode = AssistanceMode.PASSIVE,
    allow_passive_signal: bool = True,
    allow_discreet_signal: bool = True,
    allow_visible_generic_signal: bool = False,
    allow_luminous_generic_signal: bool = False,
    allow_internal_record: bool = True,
) -> UserAlertPreference:
    """
    Crea una preferencia demostrativa de asistencia.

    Por defecto se prioriza el modo pasivo y no visible.
    """
    return UserAlertPreference(
        assistance_mode=assistance_mode,
        allow_passive_signal=allow_passive_signal,
        allow_discreet_signal=allow_discreet_signal,
        allow_visible_generic_signal=allow_visible_generic_signal,
        allow_luminous_generic_signal=allow_luminous_generic_signal,
        allow_internal_record=allow_internal_record,
    )


def create_demo_alert_context(
    country: str = "Argentina",
    network_demo_id: str = "demo-network-sube",
    route_demo_id: str = "demo-route-001",
    vehicle_demo_id: str = "demo-vehicle-001",
    trip_demo_id: str = "demo-trip-001",
    occupancy_level: str = "medium",
    priority_attribute_active: bool = True,
    previously_accredited_need: bool = True,
) -> AlertContext:
    """
    Crea un contexto demostrativo de viaje.
    """
    return AlertContext(
        country=country,
        network_demo_id=network_demo_id,
        route_demo_id=route_demo_id,
        vehicle_demo_id=vehicle_demo_id,
        trip_demo_id=trip_demo_id,
        occupancy_level=occupancy_level,
        priority_attribute_active=priority_attribute_active,
        previously_accredited_need=previously_accredited_need,
    )


def create_demo_passive_alert_request(
    alert_request_demo_id: str = "demo-alert-request-001",
    priority_attribute_token: str = "demo-priority-attribute-001",
    preference: Optional[UserAlertPreference] = None,
    context: Optional[AlertContext] = None,
) -> PassiveAlertRequest:
    """
    Crea una solicitud demostrativa de alerta.
    """
    if not alert_request_demo_id or not alert_request_demo_id.strip():
        raise ValueError("El identificador demostrativo de alerta no puede estar vacío.")

    if not priority_attribute_token or not priority_attribute_token.strip():
        raise ValueError("El token técnico demostrativo de prioridad no puede estar vacío.")

    assert_no_prohibited_fields(
        {
            "alert_request_demo_id": alert_request_demo_id,
            "priority_attribute_token": priority_attribute_token,
        }
    )

    return PassiveAlertRequest(
        alert_request_demo_id=alert_request_demo_id.strip(),
        priority_attribute_token=priority_attribute_token.strip(),
        preference=preference or create_demo_user_alert_preference(),
        context=context or create_demo_alert_context(),
    )


def evaluate_passive_alert_request(
    request: PassiveAlertRequest,
) -> PassiveAlertResult:
    """
    Evalúa la alerta conceptual según la preferencia del usuario.

    La salida no revela diagnóstico.
    La salida no identifica a la persona.
    La salida no exige acción al chofer.
    La salida no obliga a otros pasajeros.
    """
    assert_no_prohibited_fields(
        {
            "alert_request_demo_id": request.alert_request_demo_id,
            "priority_attribute_token": request.priority_attribute_token,
            "network_demo_id": request.context.network_demo_id,
            "route_demo_id": request.context.route_demo_id,
            "vehicle_demo_id": request.context.vehicle_demo_id,
            "trip_demo_id": request.context.trip_demo_id,
        }
    )

    blocked_reasons = _blocked_reasons(request)

    if blocked_reasons:
        return PassiveAlertResult(
            project=PROJECT_NAME,
            module=MODULE_NAME,
            version=FLOW_VERSION,
            demo_mode=DEMO_MODE,
            status=AlertDecisionStatus.BLOCKED,
            selected_channel=AlertChannel.NONE,
            assistance_mode=request.preference.assistance_mode,
            alert_enabled=False,
            exposure_level="none",
            message="No se emite alerta porque la solicitud demostrativa fue bloqueada.",
            blocked_reasons=blocked_reasons,
            privacy_notice=_privacy_notice(),
            driver_burden=_driver_burden_notice(),
            passenger_burden=_passenger_burden_notice(),
            warnings=_common_warnings(),
            timestamp_utc=_now_utc(),
        )

    channel = _select_alert_channel(request.preference)

    if channel == AlertChannel.NONE:
        return PassiveAlertResult(
            project=PROJECT_NAME,
            module=MODULE_NAME,
            version=FLOW_VERSION,
            demo_mode=DEMO_MODE,
            status=AlertDecisionStatus.ALLOWED,
            selected_channel=AlertChannel.NONE,
            assistance_mode=request.preference.assistance_mode,
            alert_enabled=False,
            exposure_level="none",
            message=(
                "Modo silencioso: no se emite alerta visible ni señal al entorno. "
                "Se respeta la decisión del usuario."
            ),
            blocked_reasons=[],
            privacy_notice=_privacy_notice(),
            driver_burden=_driver_burden_notice(),
            passenger_burden=_passenger_burden_notice(),
            warnings=_common_warnings(),
            timestamp_utc=_now_utc(),
        )

    if _is_degraded_channel(request.preference, channel):
        status = AlertDecisionStatus.DEGRADED
    else:
        status = AlertDecisionStatus.ALLOWED

    return PassiveAlertResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=FLOW_VERSION,
        demo_mode=DEMO_MODE,
        status=status,
        selected_channel=channel,
        assistance_mode=request.preference.assistance_mode,
        alert_enabled=True,
        exposure_level=_exposure_level(channel),
        message=_alert_message(channel),
        blocked_reasons=[],
        privacy_notice=_privacy_notice(),
        driver_burden=_driver_burden_notice(),
        passenger_burden=_passenger_burden_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def result_to_dict(result: PassiveAlertResult) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "selected_channel": result.selected_channel.value,
        "assistance_mode": result.assistance_mode.value,
        "alert_enabled": result.alert_enabled,
        "exposure_level": result.exposure_level,
        "message": result.message,
        "blocked_reasons": result.blocked_reasons,
        "privacy_notice": result.privacy_notice,
        "driver_burden": result.driver_burden,
        "passenger_burden": result.passenger_burden,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    """
    Ejecuta una demostración estable de alerta pasiva.
    """
    request = create_demo_passive_alert_request(
        preference=create_demo_user_alert_preference(
            assistance_mode=AssistanceMode.PASSIVE,
            allow_passive_signal=True,
            allow_discreet_signal=True,
            allow_visible_generic_signal=False,
            allow_luminous_generic_signal=False,
            allow_internal_record=True,
        )
    )

    result = evaluate_passive_alert_request(request)

    return result_to_dict(result)


def _blocked_reasons(request: PassiveAlertRequest) -> List[str]:
    reasons: List[str] = []

    if request.context.country.strip().lower() != "argentina":
        reasons.append("outside_argentina_context")

    if not request.context.previously_accredited_need:
        reasons.append("need_not_previously_accredited")

    if not request.context.priority_attribute_active:
        reasons.append("priority_attribute_not_active")

    if _looks_like_free_text(request.priority_attribute_token):
        reasons.append("priority_attribute_token_looks_like_free_text")

    return reasons


def _select_alert_channel(preference: UserAlertPreference) -> AlertChannel:
    if preference.assistance_mode == AssistanceMode.SILENT:
        return AlertChannel.NONE

    if preference.assistance_mode == AssistanceMode.PASSIVE:
        if preference.allow_passive_signal:
            return AlertChannel.PASSIVE_SIGNAL
        if preference.allow_internal_record:
            return AlertChannel.INTERNAL_RECORD
        return AlertChannel.NONE

    if preference.assistance_mode == AssistanceMode.DISCREET:
        if preference.allow_discreet_signal:
            return AlertChannel.DISCREET_SIGNAL
        if preference.allow_passive_signal:
            return AlertChannel.PASSIVE_SIGNAL
        if preference.allow_internal_record:
            return AlertChannel.INTERNAL_RECORD
        return AlertChannel.NONE

    if preference.assistance_mode == AssistanceMode.PREVENTIVE:
        if preference.allow_passive_signal:
            return AlertChannel.PASSIVE_SIGNAL
        if preference.allow_discreet_signal:
            return AlertChannel.DISCREET_SIGNAL
        if preference.allow_internal_record:
            return AlertChannel.INTERNAL_RECORD
        return AlertChannel.NONE

    if preference.assistance_mode == AssistanceMode.VISIBLE_GENERIC:
        if preference.allow_visible_generic_signal:
            return AlertChannel.GENERIC_VISUAL_SIGNAL
        if preference.allow_discreet_signal:
            return AlertChannel.DISCREET_SIGNAL
        if preference.allow_passive_signal:
            return AlertChannel.PASSIVE_SIGNAL
        if preference.allow_internal_record:
            return AlertChannel.INTERNAL_RECORD
        return AlertChannel.NONE

    if preference.assistance_mode == AssistanceMode.LUMINOUS_GENERIC:
        if preference.allow_luminous_generic_signal:
            return AlertChannel.GENERIC_LUMINOUS_SIGNAL
        if preference.allow_visible_generic_signal:
            return AlertChannel.GENERIC_VISUAL_SIGNAL
        if preference.allow_discreet_signal:
            return AlertChannel.DISCREET_SIGNAL
        if preference.allow_passive_signal:
            return AlertChannel.PASSIVE_SIGNAL
        if preference.allow_internal_record:
            return AlertChannel.INTERNAL_RECORD
        return AlertChannel.NONE

    return AlertChannel.NONE


def _is_degraded_channel(
    preference: UserAlertPreference,
    selected_channel: AlertChannel,
) -> bool:
    expected_by_mode = {
        AssistanceMode.SILENT: AlertChannel.NONE,
        AssistanceMode.PASSIVE: AlertChannel.PASSIVE_SIGNAL,
        AssistanceMode.DISCREET: AlertChannel.DISCREET_SIGNAL,
        AssistanceMode.PREVENTIVE: AlertChannel.PASSIVE_SIGNAL,
        AssistanceMode.VISIBLE_GENERIC: AlertChannel.GENERIC_VISUAL_SIGNAL,
        AssistanceMode.LUMINOUS_GENERIC: AlertChannel.GENERIC_LUMINOUS_SIGNAL,
    }

    return expected_by_mode.get(preference.assistance_mode) != selected_channel


def _exposure_level(channel: AlertChannel) -> str:
    if channel == AlertChannel.NONE:
        return "none"

    if channel == AlertChannel.INTERNAL_RECORD:
        return "internal_only"

    if channel == AlertChannel.PASSIVE_SIGNAL:
        return "minimal_passive"

    if channel == AlertChannel.DISCREET_SIGNAL:
        return "low_discreet"

    if channel == AlertChannel.GENERIC_VISUAL_SIGNAL:
        return "generic_visible"

    if channel == AlertChannel.GENERIC_LUMINOUS_SIGNAL:
        return "generic_luminous"

    return "unknown"


def _alert_message(channel: AlertChannel) -> str:
    if channel == AlertChannel.INTERNAL_RECORD:
        return (
            "Registro interno demostrativo de asistencia preventiva. "
            "No se emite señal al entorno."
        )

    if channel == AlertChannel.PASSIVE_SIGNAL:
        return (
            "Señal pasiva demostrativa: podría requerirse asistencia preventiva "
            "sin exponer datos personales."
        )

    if channel == AlertChannel.DISCREET_SIGNAL:
        return (
            "Señal discreta demostrativa: asistencia genérica sin diagnóstico, "
            "sin identidad civil y sin documentación médica."
        )

    if channel == AlertChannel.GENERIC_VISUAL_SIGNAL:
        return (
            "Alerta visible genérica: una persona puede requerir asistencia preventiva. "
            "No se informa el motivo."
        )

    if channel == AlertChannel.GENERIC_LUMINOUS_SIGNAL:
        return (
            "Alerta lumínica genérica: señal no verbal de asistencia preventiva "
            "sin datos personales ni médicos."
        )

    return "No se emite alerta."


def _looks_like_free_text(token: str) -> bool:
    normalized = token.lower().strip()

    suspicious_terms = {
        "quiero",
        "gratis",
        "beneficio",
        "tarifa",
        "social",
        "diagnostico",
        "diagnóstico",
        "cud",
        "certificado",
        "medico",
        "médico",
        "andis",
        "sancion",
        "sanción",
        "ranking",
        "vigilancia",
    }

    return any(term in normalized for term in suspicious_terms) or len(normalized.split()) > 1


def _privacy_notice() -> str:
    return (
        "La alerta no revela DNI, nombre, domicilio, diagnóstico, CUD, "
        "historia clínica ni certificado médico."
    )


def _driver_burden_notice() -> str:
    return (
        "El personal de conducción no diagnostica, no valida documentación, "
        "no administra beneficios, no sanciona y no decide la asistencia."
    )


def _passenger_burden_notice() -> str:
    return (
        "La alerta no impone obligaciones ni sanciones a otros pasajeros. "
        "Sólo comunica una necesidad de asistencia de forma genérica."
    )


def _common_warnings() -> List[str]:
    return [
        "Flujo conceptual y demostrativo.",
        "Sin implementación oficial vigente.",
        "Sin integración real con SUBE.",
        "Sin integración real con Red SUBE.",
        "Sin integración real con organismos públicos.",
        "Sin modificación de validadoras reales.",
        "Sin datos sensibles.",
        "Sin diagnóstico médico.",
        "Sin CUD real.",
        "Sin certificados médicos reales.",
        "Sin sanciones.",
        "Sin ranking.",
        "Sin vigilancia.",
        "Sin obligación para pasajeros.",
        "Sin carga operativa para el chofer.",
        "El usuario conserva control sobre el modo de asistencia.",
    ]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
