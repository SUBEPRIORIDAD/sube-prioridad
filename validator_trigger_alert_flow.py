"""
SUBE Prioridad — Flujo conceptual de alerta posterior a validación.

Este módulo modela qué podría ocurrir después de que una persona usuaria de
SUBE Prioridad valida el pago de un pasaje en:

    - una validadora dentro de una unidad de transporte público;
    - un molinete de estación;
    - un punto de validación equivalente del sistema de transporte público.

No representa implementación oficial.
No integra SUBE real.
No integra Red SUBE real.
No modifica validadoras reales.
No modifica molinetes reales.
No consulta cuentas reales.
No consulta tarjetas reales.
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
    La alerta sólo puede surgir después de una validación de pago demostrativa,
    cuando existe un atributo técnico SUBE Prioridad activo y preferencias
    previamente configuradas por el usuario.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Alerta Posterior a Validación"
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


class ValidationPointType(str, Enum):
    VEHICLE_VALIDATOR = "vehicle_validator"
    STATION_TURNSTILE = "station_turnstile"
    ACCESS_GATE = "access_gate"


class ValidationStatus(str, Enum):
    PAID = "paid"
    REJECTED = "rejected"
    UNKNOWN = "unknown"


class AssistanceMode(str, Enum):
    SILENT = "silent"
    PASSIVE = "passive"
    DISCREET = "discreet"
    PREVENTIVE = "preventive"
    VISIBLE_GENERIC = "visible_generic"
    LUMINOUS_GENERIC = "luminous_generic"


class TriggerStatus(str, Enum):
    TRIGGERED = "triggered"
    BLOCKED = "blocked"
    DEGRADED = "degraded"


class AlertChannel(str, Enum):
    NONE = "none"
    PASSIVE_INTERNAL = "passive_internal"
    DISCREET_GENERIC = "discreet_generic"
    VISIBLE_GENERIC = "visible_generic"
    LUMINOUS_GENERIC = "luminous_generic"
    STATION_OPERATOR_NOTIFICATION = "station_operator_notification"


@dataclass(frozen=True)
class ValidationEvent:
    """
    Evento demostrativo de validación de pasaje.

    No representa una transacción real.
    No incluye saldo.
    No incluye tarifa.
    No incluye datos personales.
    """

    validation_event_demo_id: str
    validation_point_type: ValidationPointType
    validation_status: ValidationStatus
    country: str
    network_demo_id: str
    route_demo_id: str
    vehicle_demo_id: Optional[str]
    station_demo_id: Optional[str]
    turnstile_demo_id: Optional[str]
    timestamp_utc: datetime


@dataclass(frozen=True)
class PriorityAttributeSnapshot:
    """
    Foto técnica demostrativa del atributo SUBE Prioridad.

    No expresa diagnóstico.
    No expresa CUD.
    No expresa identidad civil.
    """

    priority_attribute_token: str
    priority_attribute_active: bool
    previously_accredited_need: bool
    preference_version_demo_id: str


@dataclass(frozen=True)
class ValidationAlertPreferences:
    """
    Preferencias previamente configuradas por el usuario desde cuenta SUBE.

    El usuario controla si la alerta será silenciosa, pasiva, visible,
    lumínica o si habilita notificación a operarios.
    """

    assistance_mode: AssistanceMode
    allow_passive_alert_after_validation: bool
    allow_discreet_alert_after_validation: bool
    allow_visible_generic_alert_after_validation: bool
    allow_luminous_alert_after_validation: bool
    allow_station_operator_notification: bool
    allow_emergency_help_notification: bool


@dataclass(frozen=True)
class StationOperatorContext:
    """
    Contexto demostrativo para estaciones con molinetes.

    No identifica operarios reales.
    No envía mensajes reales.
    """

    station_staff_present: bool
    operator_device_channel_available: bool
    station_has_assistance_protocol: bool


@dataclass(frozen=True)
class ValidatorTriggerRequest:
    """
    Solicitud conceptual para evaluar una alerta posterior a validación.
    """

    trigger_request_demo_id: str
    validation_event: ValidationEvent
    priority_snapshot: PriorityAttributeSnapshot
    preferences: ValidationAlertPreferences
    station_operator_context: Optional[StationOperatorContext]


@dataclass(frozen=True)
class ValidatorTriggerResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: TriggerStatus
    validation_paid: bool
    priority_active: bool
    selected_channels: List[AlertChannel]
    station_operator_notification_enabled: bool
    luminous_alert_enabled: bool
    visible_generic_alert_enabled: bool
    passive_alert_enabled: bool
    blocked_reasons: List[str]
    degraded_reasons: List[str]
    message: str
    validation_trigger_notice: str
    station_operator_notice: str
    privacy_notice: str
    driver_burden: str
    passenger_burden: str
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


def create_demo_validation_event(
    validation_event_demo_id: str = "demo-validation-event-001",
    validation_point_type: ValidationPointType = ValidationPointType.VEHICLE_VALIDATOR,
    validation_status: ValidationStatus = ValidationStatus.PAID,
    country: str = "Argentina",
    network_demo_id: str = "demo-network-sube",
    route_demo_id: str = "demo-route-001",
    vehicle_demo_id: Optional[str] = "demo-vehicle-001",
    station_demo_id: Optional[str] = None,
    turnstile_demo_id: Optional[str] = None,
    timestamp_utc: Optional[datetime] = None,
) -> ValidationEvent:
    """
    Crea un evento demostrativo de validación.
    """
    if not validation_event_demo_id or not validation_event_demo_id.strip():
        raise ValueError("El identificador demostrativo de validación no puede estar vacío.")

    assert_no_prohibited_fields(
        {
            "validation_event_demo_id": validation_event_demo_id,
            "network_demo_id": network_demo_id,
            "route_demo_id": route_demo_id,
            "vehicle_demo_id": vehicle_demo_id or "",
            "station_demo_id": station_demo_id or "",
            "turnstile_demo_id": turnstile_demo_id or "",
        }
    )

    return ValidationEvent(
        validation_event_demo_id=validation_event_demo_id.strip(),
        validation_point_type=validation_point_type,
        validation_status=validation_status,
        country=country,
        network_demo_id=network_demo_id,
        route_demo_id=route_demo_id,
        vehicle_demo_id=vehicle_demo_id,
        station_demo_id=station_demo_id,
        turnstile_demo_id=turnstile_demo_id,
        timestamp_utc=timestamp_utc or datetime.now(timezone.utc),
    )


def create_demo_priority_attribute_snapshot(
    priority_attribute_token: str = "demo-priority-attribute-001",
    priority_attribute_active: bool = True,
    previously_accredited_need: bool = True,
    preference_version_demo_id: str = "demo-preference-version-001",
) -> PriorityAttributeSnapshot:
    """
    Crea una foto técnica demostrativa del atributo SUBE Prioridad.
    """
    if not priority_attribute_token or not priority_attribute_token.strip():
        raise ValueError("El token técnico demostrativo de prioridad no puede estar vacío.")

    if not preference_version_demo_id or not preference_version_demo_id.strip():
        raise ValueError("La versión demostrativa de preferencias no puede estar vacía.")

    assert_no_prohibited_fields(
        {
            "priority_attribute_token": priority_attribute_token,
            "preference_version_demo_id": preference_version_demo_id,
        }
    )

    return PriorityAttributeSnapshot(
        priority_attribute_token=priority_attribute_token.strip(),
        priority_attribute_active=priority_attribute_active,
        previously_accredited_need=previously_accredited_need,
        preference_version_demo_id=preference_version_demo_id.strip(),
    )


def create_demo_validation_alert_preferences(
    assistance_mode: AssistanceMode = AssistanceMode.PASSIVE,
    allow_passive_alert_after_validation: bool = True,
    allow_discreet_alert_after_validation: bool = True,
    allow_visible_generic_alert_after_validation: bool = False,
    allow_luminous_alert_after_validation: bool = False,
    allow_station_operator_notification: bool = False,
    allow_emergency_help_notification: bool = False,
) -> ValidationAlertPreferences:
    """
    Crea preferencias demostrativas para alertas posteriores a validación.
    """
    return ValidationAlertPreferences(
        assistance_mode=assistance_mode,
        allow_passive_alert_after_validation=allow_passive_alert_after_validation,
        allow_discreet_alert_after_validation=allow_discreet_alert_after_validation,
        allow_visible_generic_alert_after_validation=allow_visible_generic_alert_after_validation,
        allow_luminous_alert_after_validation=allow_luminous_alert_after_validation,
        allow_station_operator_notification=allow_station_operator_notification,
        allow_emergency_help_notification=allow_emergency_help_notification,
    )


def create_demo_station_operator_context(
    station_staff_present: bool = True,
    operator_device_channel_available: bool = True,
    station_has_assistance_protocol: bool = True,
) -> StationOperatorContext:
    """
    Crea contexto demostrativo para operarios de estación.
    """
    return StationOperatorContext(
        station_staff_present=station_staff_present,
        operator_device_channel_available=operator_device_channel_available,
        station_has_assistance_protocol=station_has_assistance_protocol,
    )


def create_demo_validator_trigger_request(
    trigger_request_demo_id: str = "demo-validator-trigger-001",
    validation_event: Optional[ValidationEvent] = None,
    priority_snapshot: Optional[PriorityAttributeSnapshot] = None,
    preferences: Optional[ValidationAlertPreferences] = None,
    station_operator_context: Optional[StationOperatorContext] = None,
) -> ValidatorTriggerRequest:
    """
    Crea una solicitud demostrativa de alerta posterior a validación.
    """
    if not trigger_request_demo_id or not trigger_request_demo_id.strip():
        raise ValueError("El identificador demostrativo del disparo no puede estar vacío.")

    assert_no_prohibited_fields({"trigger_request_demo_id": trigger_request_demo_id})

    return ValidatorTriggerRequest(
        trigger_request_demo_id=trigger_request_demo_id.strip(),
        validation_event=validation_event or create_demo_validation_event(),
        priority_snapshot=priority_snapshot or create_demo_priority_attribute_snapshot(),
        preferences=preferences or create_demo_validation_alert_preferences(),
        station_operator_context=station_operator_context,
    )


def evaluate_validator_trigger_request(
    request: ValidatorTriggerRequest,
) -> ValidatorTriggerResult:
    """
    Evalúa si corresponde disparar una alerta conceptual luego de validar pasaje.
    """
    assert_no_prohibited_fields(
        {
            "trigger_request_demo_id": request.trigger_request_demo_id,
            "validation_event_demo_id": request.validation_event.validation_event_demo_id,
            "priority_attribute_token": request.priority_snapshot.priority_attribute_token,
            "preference_version_demo_id": request.priority_snapshot.preference_version_demo_id,
        }
    )

    blocked_reasons = _blocked_reasons(request)

    if blocked_reasons:
        return ValidatorTriggerResult(
            project=PROJECT_NAME,
            module=MODULE_NAME,
            version=FLOW_VERSION,
            demo_mode=DEMO_MODE,
            status=TriggerStatus.BLOCKED,
            validation_paid=request.validation_event.validation_status == ValidationStatus.PAID,
            priority_active=request.priority_snapshot.priority_attribute_active,
            selected_channels=[],
            station_operator_notification_enabled=False,
            luminous_alert_enabled=False,
            visible_generic_alert_enabled=False,
            passive_alert_enabled=False,
            blocked_reasons=blocked_reasons,
            degraded_reasons=[],
            message="No se dispara alerta porque el evento demostrativo fue bloqueado.",
            validation_trigger_notice=_validation_trigger_notice(),
            station_operator_notice=_station_operator_notice(False, request),
            privacy_notice=_privacy_notice(),
            driver_burden=_driver_burden_notice(),
            passenger_burden=_passenger_burden_notice(),
            warnings=_common_warnings(),
            timestamp_utc=_now_utc(),
        )

    selected_channels = _select_channels(request)
    degraded_reasons = _degraded_reasons(request, selected_channels)

    status = TriggerStatus.DEGRADED if degraded_reasons else TriggerStatus.TRIGGERED

    return ValidatorTriggerResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=FLOW_VERSION,
        demo_mode=DEMO_MODE,
        status=status,
        validation_paid=True,
        priority_active=True,
        selected_channels=selected_channels,
        station_operator_notification_enabled=AlertChannel.STATION_OPERATOR_NOTIFICATION
        in selected_channels,
        luminous_alert_enabled=AlertChannel.LUMINOUS_GENERIC in selected_channels,
        visible_generic_alert_enabled=AlertChannel.VISIBLE_GENERIC in selected_channels,
        passive_alert_enabled=AlertChannel.PASSIVE_INTERNAL in selected_channels,
        blocked_reasons=[],
        degraded_reasons=degraded_reasons,
        message=_result_message(selected_channels, degraded_reasons),
        validation_trigger_notice=_validation_trigger_notice(),
        station_operator_notice=_station_operator_notice(
            AlertChannel.STATION_OPERATOR_NOTIFICATION in selected_channels,
            request,
        ),
        privacy_notice=_privacy_notice(),
        driver_burden=_driver_burden_notice(),
        passenger_burden=_passenger_burden_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def result_to_dict(result: ValidatorTriggerResult) -> Dict[str, Any]:
    """
    Convierte el resultado a diccionario serializable.
    """
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "validation_paid": result.validation_paid,
        "priority_active": result.priority_active,
        "selected_channels": [channel.value for channel in result.selected_channels],
        "station_operator_notification_enabled": result.station_operator_notification_enabled,
        "luminous_alert_enabled": result.luminous_alert_enabled,
        "visible_generic_alert_enabled": result.visible_generic_alert_enabled,
        "passive_alert_enabled": result.passive_alert_enabled,
        "blocked_reasons": result.blocked_reasons,
        "degraded_reasons": result.degraded_reasons,
        "message": result.message,
        "validation_trigger_notice": result.validation_trigger_notice,
        "station_operator_notice": result.station_operator_notice,
        "privacy_notice": result.privacy_notice,
        "driver_burden": result.driver_burden,
        "passenger_burden": result.passenger_burden,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    """
    Ejecuta una demostración estable de alerta posterior a validación.
    """
    request = create_demo_validator_trigger_request(
        validation_event=create_demo_validation_event(
            validation_point_type=ValidationPointType.VEHICLE_VALIDATOR,
            validation_status=ValidationStatus.PAID,
        ),
        preferences=create_demo_validation_alert_preferences(
            assistance_mode=AssistanceMode.PASSIVE,
            allow_passive_alert_after_validation=True,
            allow_discreet_alert_after_validation=True,
            allow_visible_generic_alert_after_validation=False,
            allow_luminous_alert_after_validation=False,
            allow_station_operator_notification=False,
            allow_emergency_help_notification=False,
        ),
    )

    result = evaluate_validator_trigger_request(request)

    return result_to_dict(result)


def _blocked_reasons(request: ValidatorTriggerRequest) -> List[str]:
    reasons: List[str] = []

    if request.validation_event.country.strip().lower() != "argentina":
        reasons.append("outside_argentina_context")

    if request.validation_event.validation_status != ValidationStatus.PAID:
        reasons.append("validation_payment_not_confirmed")

    if not request.priority_snapshot.priority_attribute_active:
        reasons.append("priority_attribute_not_active")

    if not request.priority_snapshot.previously_accredited_need:
        reasons.append("need_not_previously_accredited")

    if _looks_like_free_text(request.priority_snapshot.priority_attribute_token):
        reasons.append("priority_attribute_token_looks_like_free_text")

    if request.validation_event.validation_point_type == ValidationPointType.VEHICLE_VALIDATOR:
        if not request.validation_event.vehicle_demo_id:
            reasons.append("vehicle_validator_without_vehicle_context")

    if request.validation_event.validation_point_type == ValidationPointType.STATION_TURNSTILE:
        if not request.validation_event.station_demo_id:
            reasons.append("station_turnstile_without_station_context")
        if not request.validation_event.turnstile_demo_id:
            reasons.append("station_turnstile_without_turnstile_context")

    return reasons


def _select_channels(request: ValidatorTriggerRequest) -> List[AlertChannel]:
    preferences = request.preferences
    channels: List[AlertChannel] = []

    if preferences.assistance_mode == AssistanceMode.SILENT:
        return channels

    if preferences.assistance_mode == AssistanceMode.PASSIVE:
        if preferences.allow_passive_alert_after_validation:
            channels.append(AlertChannel.PASSIVE_INTERNAL)
        return channels

    if preferences.assistance_mode == AssistanceMode.DISCREET:
        if preferences.allow_discreet_alert_after_validation:
            channels.append(AlertChannel.DISCREET_GENERIC)
        elif preferences.allow_passive_alert_after_validation:
            channels.append(AlertChannel.PASSIVE_INTERNAL)
        return channels

    if preferences.assistance_mode == AssistanceMode.PREVENTIVE:
        if preferences.allow_passive_alert_after_validation:
            channels.append(AlertChannel.PASSIVE_INTERNAL)
        if _station_operator_notification_allowed(request):
            channels.append(AlertChannel.STATION_OPERATOR_NOTIFICATION)
        return channels

    if preferences.assistance_mode == AssistanceMode.VISIBLE_GENERIC:
        if preferences.allow_visible_generic_alert_after_validation:
            channels.append(AlertChannel.VISIBLE_GENERIC)
        elif preferences.allow_discreet_alert_after_validation:
            channels.append(AlertChannel.DISCREET_GENERIC)
        elif preferences.allow_passive_alert_after_validation:
            channels.append(AlertChannel.PASSIVE_INTERNAL)
        return channels

    if preferences.assistance_mode == AssistanceMode.LUMINOUS_GENERIC:
        if preferences.allow_luminous_alert_after_validation:
            channels.append(AlertChannel.LUMINOUS_GENERIC)
        elif preferences.allow_visible_generic_alert_after_validation:
            channels.append(AlertChannel.VISIBLE_GENERIC)
        elif preferences.allow_discreet_alert_after_validation:
            channels.append(AlertChannel.DISCREET_GENERIC)
        elif preferences.allow_passive_alert_after_validation:
            channels.append(AlertChannel.PASSIVE_INTERNAL)

        if _station_operator_notification_allowed(request):
            channels.append(AlertChannel.STATION_OPERATOR_NOTIFICATION)

        return channels

    return channels


def _station_operator_notification_allowed(
    request: ValidatorTriggerRequest,
) -> bool:
    preferences = request.preferences
    context = request.station_operator_context

    user_allows = (
        preferences.allow_station_operator_notification
        or preferences.allow_emergency_help_notification
    )

    if not user_allows:
        return False

    if request.validation_event.validation_point_type != ValidationPointType.STATION_TURNSTILE:
        return False

    if context is None:
        return False

    return (
        context.station_staff_present
        and context.operator_device_channel_available
        and context.station_has_assistance_protocol
    )


def _degraded_reasons(
    request: ValidatorTriggerRequest,
    selected_channels: List[AlertChannel],
) -> List[str]:
    reasons: List[str] = []

    if request.preferences.assistance_mode != AssistanceMode.SILENT and not selected_channels:
        reasons.append("no_alert_channel_available_under_user_preferences")

    if (
        request.preferences.allow_station_operator_notification
        or request.preferences.allow_emergency_help_notification
    ):
        if AlertChannel.STATION_OPERATOR_NOTIFICATION not in selected_channels:
            reasons.append("station_operator_notification_not_available")

    if (
        request.preferences.assistance_mode == AssistanceMode.LUMINOUS_GENERIC
        and AlertChannel.LUMINOUS_GENERIC not in selected_channels
    ):
        reasons.append("luminous_alert_degraded_to_less_exposed_channel")

    if (
        request.preferences.assistance_mode == AssistanceMode.VISIBLE_GENERIC
        and AlertChannel.VISIBLE_GENERIC not in selected_channels
    ):
        reasons.append("visible_alert_degraded_to_less_exposed_channel")

    return reasons


def _result_message(
    selected_channels: List[AlertChannel],
    degraded_reasons: List[str],
) -> str:
    if not selected_channels:
        return (
            "Validación demostrativa aceptada. El usuario eligió modo silencioso "
            "o no hay canal habilitado, por lo que no se emite alerta al entorno."
        )

    if degraded_reasons:
        return (
            "Validación demostrativa aceptada. La alerta se emite por un canal "
            "menos expuesto o limitado por las preferencias y disponibilidad conceptual."
        )

    return (
        "Validación demostrativa aceptada. Se dispara una alerta genérica conforme "
        "a las preferencias previamente configuradas por el usuario."
    )


def _validation_trigger_notice() -> str:
    return (
        "La alerta conceptual sólo se evalúa después de una validación de pago "
        "en validadora de unidad de transporte público, molinete o punto de acceso equivalente."
    )


def _station_operator_notice(
    notification_enabled: bool,
    request: ValidatorTriggerRequest,
) -> str:
    if notification_enabled:
        return (
            "Se habilita una notificación conceptual a dispositivos de operarios presentes "
            "en estación, sin revelar diagnóstico, identidad civil, CUD ni datos médicos."
        )

    if request.validation_event.validation_point_type != ValidationPointType.STATION_TURNSTILE:
        return (
            "No corresponde notificación a operarios de estación porque la validación "
            "ocurrió en una validadora de unidad o punto no estacionario."
        )

    return (
        "No se habilita notificación a operarios de estación por preferencia del usuario "
        "o por falta de disponibilidad conceptual del canal."
    )


def _privacy_notice() -> str:
    return (
        "La alerta no revela DNI, nombre, domicilio, diagnóstico, CUD, historia clínica "
        "ni certificado médico. Sólo utiliza atributos técnicos demostrativos."
    )


def _driver_burden_notice() -> str:
    return (
        "El chofer no diagnostica, no valida documentación, no administra beneficios, "
        "no decide la alerta y no asume una carga operativa adicional."
    )


def _passenger_burden_notice() -> str:
    return (
        "La alerta no impone obligaciones ni sanciones a otros pasajeros. "
        "Sólo comunica una necesidad de asistencia preventiva de forma genérica."
    )


def _common_warnings() -> List[str]:
    return [
        "Flujo conceptual y demostrativo.",
        "Sin implementación oficial vigente.",
        "Sin integración real con SUBE.",
        "Sin integración real con Red SUBE.",
        "Sin modificación de validadoras reales.",
        "Sin modificación de molinetes reales.",
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
        "La alerta depende de preferencias previas del usuario.",
        "La alerta se evalúa sólo luego de validar el pago del pasaje.",
    ]


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
        "bono",
        "solidario",
    }

    return any(term in normalized for term in suspicious_terms) or len(normalized.split()) > 1


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
