"""
SUBE Prioridad — Flujo conceptual de preferencias desde cuenta SUBE.

Este módulo modela cómo una persona usuaria de SUBE Prioridad podría configurar
sus preferencias desde una cuenta SUBE demostrativa asociada a una tarjeta SUBE.

No representa implementación oficial.
No integra SUBE real.
No integra Red SUBE real.
No consulta usuarios reales.
No consulta tarjetas reales.
No modifica perfiles reales.
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

Finalidad:
    Representar el origen legítimo de las preferencias del usuario antes de
    cualquier validación en validadora, molinete, alerta pasiva, alerta lumínica,
    notificación a operarios o sincronización solidaria.

Principios:
    - La preferencia nace desde el usuario.
    - La preferencia está asociada a una cuenta SUBE demostrativa.
    - La preferencia es revocable.
    - La preferencia no revela diagnóstico.
    - La Red SUBE demostrativa sólo sincroniza atributos técnicos mínimos.
    - El transporte no necesita conocer el diagnóstico.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Preferencias desde Cuenta SUBE"
FLOW_VERSION = "0.1.1"
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


class PreferenceSource(str, Enum):
    """
    Canal conceptual desde el cual el usuario podría configurar preferencias.

    Todos los canales son demostrativos.
    No representan sistemas reales.
    """

    WEB_PORTAL = "web_portal"
    MOBILE_APP = "mobile_app"
    SELF_SERVICE_TERMINAL = "self_service_terminal"
    ASSISTED_CHANNEL = "assisted_channel"


class AssistancePreferenceMode(str, Enum):
    """
    Modo elegido por el usuario.

    No es diagnóstico.
    No es categoría médica.
    No es certificado.
    """

    SILENT = "silent"
    PASSIVE = "passive"
    DISCREET = "discreet"
    PREVENTIVE = "preventive"
    VISIBLE_GENERIC = "visible_generic"
    LUMINOUS_GENERIC = "luminous_generic"


class PreferenceUpdateStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"


class SyncTarget(str, Enum):
    """
    Destinos conceptuales de sincronización.

    No son integraciones reales.
    """

    SUBE_ACCOUNT = "sube_account"
    SUBE_CARD_PROFILE = "sube_card_profile"
    VALIDATOR_EDGE = "validator_edge"
    TURNSTILE_EDGE = "turnstile_edge"
    STATION_OPERATOR_DEVICES = "station_operator_devices"
    SOLIDARY_SYNC_FRONTEND = "solidary_sync_frontend"


@dataclass(frozen=True)
class SubeAccountContext:
    """
    Cuenta SUBE demostrativa.

    No contiene identidad real.
    No contiene DNI.
    No contiene datos de contacto.
    """

    account_demo_id: str
    card_demo_id: str
    priority_attribute_token: str
    account_active: bool
    card_associated: bool
    priority_attribute_active: bool


@dataclass(frozen=True)
class UserAssistancePreferences:
    """
    Preferencias configurables por el usuario.

    El usuario conserva control sobre exposición, alertas y notificaciones.
    """

    assistance_mode: AssistancePreferenceMode
    allow_passive_alert_after_validation: bool
    allow_luminous_alert_after_validation: bool
    allow_visible_generic_alert_after_validation: bool
    allow_station_operator_notification: bool
    allow_solidary_bonus_sync_frontend: bool
    allow_emergency_help_notification: bool
    preference_revocable: bool


@dataclass(frozen=True)
class PreferenceUpdateRequest:
    """
    Solicitud conceptual de actualización de preferencias.

    No debe incluir información personal, médica ni sensible.
    """

    request_demo_id: str
    source: PreferenceSource
    account_context: SubeAccountContext
    preferences: UserAssistancePreferences
    requested_sync_targets: List[SyncTarget]
    user_confirms_update: bool


@dataclass(frozen=True)
class PreferenceUpdateResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: PreferenceUpdateStatus
    preferences_saved_demo: bool
    simulated_sync_enabled: bool
    synchronized_targets: List[SyncTarget]
    blocked_targets: List[SyncTarget]
    risk_flags: List[str]
    reason: str
    account_scope: str
    validation_trigger_notice: str
    station_operator_notice: str
    solidary_bonus_frontend_notice: str
    privacy_notice: str
    driver_burden: str
    warnings: List[str]
    timestamp_utc: str


def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    """
    Rechaza campos incompatibles con privacidad por diseño.
    """
    normalized_keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))

    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )


def create_demo_sube_account_context(
    account_demo_id: str = "demo-sube-account-001",
    card_demo_id: str = "demo-sube-card-001",
    priority_attribute_token: str = "demo-priority-attribute-001",
    account_active: bool = True,
    card_associated: bool = True,
    priority_attribute_active: bool = True,
) -> SubeAccountContext:
    """
    Crea una cuenta SUBE demostrativa asociada a una tarjeta SUBE demostrativa.
    """
    if not account_demo_id or not account_demo_id.strip():
        raise ValueError("El identificador demostrativo de cuenta SUBE no puede estar vacío.")

    if not card_demo_id or not card_demo_id.strip():
        raise ValueError("El identificador demostrativo de tarjeta SUBE no puede estar vacío.")

    if not priority_attribute_token or not priority_attribute_token.strip():
        raise ValueError("El token técnico demostrativo de prioridad no puede estar vacío.")

    assert_no_prohibited_fields(
        {
            "account_demo_id": account_demo_id,
            "card_demo_id": card_demo_id,
            "priority_attribute_token": priority_attribute_token,
        }
    )

    return SubeAccountContext(
        account_demo_id=account_demo_id.strip(),
        card_demo_id=card_demo_id.strip(),
        priority_attribute_token=priority_attribute_token.strip(),
        account_active=account_active,
        card_associated=card_associated,
        priority_attribute_active=priority_attribute_active,
    )


def create_demo_user_assistance_preferences(
    assistance_mode: AssistancePreferenceMode = AssistancePreferenceMode.PASSIVE,
    allow_passive_alert_after_validation: bool = True,
    allow_luminous_alert_after_validation: bool = False,
    allow_visible_generic_alert_after_validation: bool = False,
    allow_station_operator_notification: bool = False,
    allow_solidary_bonus_sync_frontend: bool = True,
    allow_emergency_help_notification: bool = False,
    preference_revocable: bool = True,
) -> UserAssistancePreferences:
    """
    Crea preferencias demostrativas de usuario.

    Por defecto se prioriza privacidad:
        - alerta pasiva habilitada;
        - alerta lumínica deshabilitada;
        - alerta visible deshabilitada;
        - notificación a operarios deshabilitada;
        - Bono Solidario como opción futura habilitable desde frontend.
    """
    return UserAssistancePreferences(
        assistance_mode=assistance_mode,
        allow_passive_alert_after_validation=allow_passive_alert_after_validation,
        allow_luminous_alert_after_validation=allow_luminous_alert_after_validation,
        allow_visible_generic_alert_after_validation=allow_visible_generic_alert_after_validation,
        allow_station_operator_notification=allow_station_operator_notification,
        allow_solidary_bonus_sync_frontend=allow_solidary_bonus_sync_frontend,
        allow_emergency_help_notification=allow_emergency_help_notification,
        preference_revocable=preference_revocable,
    )


def create_demo_preference_update_request(
    request_demo_id: str = "demo-preference-update-001",
    source: PreferenceSource = PreferenceSource.WEB_PORTAL,
    account_context: Optional[SubeAccountContext] = None,
    preferences: Optional[UserAssistancePreferences] = None,
    requested_sync_targets: Optional[List[SyncTarget]] = None,
    user_confirms_update: bool = True,
) -> PreferenceUpdateRequest:
    """
    Crea una solicitud demostrativa de actualización de preferencias.

    Regla importante:
        - None significa usar destinos demostrativos por defecto.
        - [] significa que el usuario o el canal no solicitó ningún destino,
          y debe ser evaluado como riesgo de seguridad.
    """
    if not request_demo_id or not request_demo_id.strip():
        raise ValueError("El identificador demostrativo de solicitud no puede estar vacío.")

    assert_no_prohibited_fields({"request_demo_id": request_demo_id})

    sync_targets = (
        _default_sync_targets()
        if requested_sync_targets is None
        else requested_sync_targets
    )

    return PreferenceUpdateRequest(
        request_demo_id=request_demo_id.strip(),
        source=source,
        account_context=account_context or create_demo_sube_account_context(),
        preferences=preferences or create_demo_user_assistance_preferences(),
        requested_sync_targets=sync_targets,
        user_confirms_update=user_confirms_update,
    )


def evaluate_preference_update_request(
    request: PreferenceUpdateRequest,
) -> PreferenceUpdateResult:
    """
    Evalúa una actualización conceptual de preferencias desde cuenta SUBE.

    Esta evaluación no guarda datos reales.
    Sólo simula validaciones de seguridad y sincronización conceptual.
    """
    assert_no_prohibited_fields(
        {
            "request_demo_id": request.request_demo_id,
            "account_demo_id": request.account_context.account_demo_id,
            "card_demo_id": request.account_context.card_demo_id,
            "priority_attribute_token": request.account_context.priority_attribute_token,
        }
    )

    risk_flags = _risk_flags(request)

    if risk_flags:
        return PreferenceUpdateResult(
            project=PROJECT_NAME,
            module=MODULE_NAME,
            version=FLOW_VERSION,
            demo_mode=DEMO_MODE,
            status=PreferenceUpdateStatus.REJECTED,
            preferences_saved_demo=False,
            simulated_sync_enabled=False,
            synchronized_targets=[],
            blocked_targets=list(request.requested_sync_targets),
            risk_flags=risk_flags,
            reason="La actualización demostrativa de preferencias fue rechazada por reglas de seguridad.",
            account_scope=_account_scope_notice(),
            validation_trigger_notice=_validation_trigger_notice(),
            station_operator_notice=_station_operator_notice(request.preferences),
            solidary_bonus_frontend_notice=_solidary_bonus_frontend_notice(request.preferences),
            privacy_notice=_privacy_notice(),
            driver_burden=_driver_burden_notice(),
            warnings=_common_warnings(),
            timestamp_utc=_now_utc(),
        )

    synchronized_targets, blocked_targets = _split_sync_targets(request)

    status = (
        PreferenceUpdateStatus.NEEDS_REVIEW
        if blocked_targets
        else PreferenceUpdateStatus.ACCEPTED
    )

    return PreferenceUpdateResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=FLOW_VERSION,
        demo_mode=DEMO_MODE,
        status=status,
        preferences_saved_demo=True,
        simulated_sync_enabled=True,
        synchronized_targets=synchronized_targets,
        blocked_targets=blocked_targets,
        risk_flags=[] if status == PreferenceUpdateStatus.ACCEPTED else ["some_targets_blocked_by_user_preferences"],
        reason=(
            "Preferencias demostrativas aceptadas desde cuenta SUBE. "
            "La sincronización es conceptual y queda limitada por las opciones elegidas por el usuario."
        ),
        account_scope=_account_scope_notice(),
        validation_trigger_notice=_validation_trigger_notice(),
        station_operator_notice=_station_operator_notice(request.preferences),
        solidary_bonus_frontend_notice=_solidary_bonus_frontend_notice(request.preferences),
        privacy_notice=_privacy_notice(),
        driver_burden=_driver_burden_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def result_to_dict(result: PreferenceUpdateResult) -> Dict[str, Any]:
    """
    Convierte el resultado a diccionario serializable.
    """
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "preferences_saved_demo": result.preferences_saved_demo,
        "simulated_sync_enabled": result.simulated_sync_enabled,
        "synchronized_targets": [target.value for target in result.synchronized_targets],
        "blocked_targets": [target.value for target in result.blocked_targets],
        "risk_flags": result.risk_flags,
        "reason": result.reason,
        "account_scope": result.account_scope,
        "validation_trigger_notice": result.validation_trigger_notice,
        "station_operator_notice": result.station_operator_notice,
        "solidary_bonus_frontend_notice": result.solidary_bonus_frontend_notice,
        "privacy_notice": result.privacy_notice,
        "driver_burden": result.driver_burden,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    """
    Ejecuta una demostración estable de actualización de preferencias.
    """
    preferences = create_demo_user_assistance_preferences(
        assistance_mode=AssistancePreferenceMode.PASSIVE,
        allow_passive_alert_after_validation=True,
        allow_luminous_alert_after_validation=False,
        allow_visible_generic_alert_after_validation=False,
        allow_station_operator_notification=False,
        allow_solidary_bonus_sync_frontend=True,
        allow_emergency_help_notification=False,
        preference_revocable=True,
    )

    request = create_demo_preference_update_request(
        source=PreferenceSource.WEB_PORTAL,
        preferences=preferences,
    )

    result = evaluate_preference_update_request(request)

    return result_to_dict(result)


def _risk_flags(request: PreferenceUpdateRequest) -> List[str]:
    flags: List[str] = []

    if not request.user_confirms_update:
        flags.append("user_confirmation_required")

    if not request.account_context.account_active:
        flags.append("sube_account_not_active")

    if not request.account_context.card_associated:
        flags.append("sube_card_not_associated")

    if not request.account_context.priority_attribute_active:
        flags.append("priority_attribute_not_active")

    if not request.preferences.preference_revocable:
        flags.append("preference_must_be_revocable")

    if _looks_like_free_text(request.account_context.priority_attribute_token):
        flags.append("priority_attribute_token_looks_like_free_text")

    if not request.requested_sync_targets:
        flags.append("no_sync_targets_requested")

    return flags


def _split_sync_targets(
    request: PreferenceUpdateRequest,
) -> tuple[List[SyncTarget], List[SyncTarget]]:
    synchronized: List[SyncTarget] = []
    blocked: List[SyncTarget] = []

    for target in request.requested_sync_targets:
        if target == SyncTarget.STATION_OPERATOR_DEVICES:
            if (
                request.preferences.allow_station_operator_notification
                or request.preferences.allow_emergency_help_notification
            ):
                synchronized.append(target)
            else:
                blocked.append(target)
            continue

        if target == SyncTarget.SOLIDARY_SYNC_FRONTEND:
            if request.preferences.allow_solidary_bonus_sync_frontend:
                synchronized.append(target)
            else:
                blocked.append(target)
            continue

        if target == SyncTarget.VALIDATOR_EDGE:
            if _any_alert_after_validation_enabled(request.preferences):
                synchronized.append(target)
            else:
                blocked.append(target)
            continue

        if target == SyncTarget.TURNSTILE_EDGE:
            if _any_alert_after_validation_enabled(request.preferences):
                synchronized.append(target)
            else:
                blocked.append(target)
            continue

        synchronized.append(target)

    return synchronized, blocked


def _any_alert_after_validation_enabled(
    preferences: UserAssistancePreferences,
) -> bool:
    return (
        preferences.allow_passive_alert_after_validation
        or preferences.allow_luminous_alert_after_validation
        or preferences.allow_visible_generic_alert_after_validation
        or preferences.allow_station_operator_notification
        or preferences.allow_emergency_help_notification
    )


def _default_sync_targets() -> List[SyncTarget]:
    return [
        SyncTarget.SUBE_ACCOUNT,
        SyncTarget.SUBE_CARD_PROFILE,
        SyncTarget.VALIDATOR_EDGE,
        SyncTarget.TURNSTILE_EDGE,
        SyncTarget.STATION_OPERATOR_DEVICES,
        SyncTarget.SOLIDARY_SYNC_FRONTEND,
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


def _account_scope_notice() -> str:
    return (
        "Las preferencias se asocian conceptualmente a una cuenta SUBE demostrativa "
        "y a una tarjeta SUBE demostrativa. No se consulta ni modifica una cuenta real."
    )


def _validation_trigger_notice() -> str:
    return (
        "Las alertas configuradas no se disparan en este módulo. "
        "Quedan preparadas para un flujo posterior que se activa luego de validar "
        "el pago en validadora de unidad de transporte público o molinete."
    )


def _station_operator_notice(
    preferences: UserAssistancePreferences,
) -> str:
    if (
        preferences.allow_station_operator_notification
        or preferences.allow_emergency_help_notification
    ):
        return (
            "El usuario habilitó conceptualmente la notificación a dispositivos de operarios "
            "presentes en estaciones o ámbitos con molinetes, sólo para asistencia genérica "
            "y sin revelar diagnóstico."
        )

    return (
        "El usuario no habilitó notificación a operarios. "
        "El sistema no debe enviar avisos a dispositivos de estación."
    )


def _solidary_bonus_frontend_notice(
    preferences: UserAssistancePreferences,
) -> str:
    if preferences.allow_solidary_bonus_sync_frontend:
        return (
            "El usuario habilitó conceptualmente el frontend de sincronización de Bono Solidario. "
            "Cualquier envío futuro a otro usuario requiere confirmación del usuario SUBE Prioridad "
            "y filtros de seguridad específicos."
        )

    return (
        "El usuario no habilitó el frontend de sincronización de Bono Solidario."
    )


def _privacy_notice() -> str:
    return (
        "La actualización de preferencias no revela DNI, nombre, domicilio, diagnóstico, CUD, "
        "historia clínica ni certificado médico. Sólo opera con tokens demostrativos."
    )


def _driver_burden_notice() -> str:
    return (
        "El personal de conducción no configura preferencias, no diagnostica, no valida "
        "documentación médica y no administra beneficios."
    )


def _common_warnings() -> List[str]:
    return [
        "Flujo conceptual y demostrativo.",
        "Sin implementación oficial vigente.",
        "Sin integración real con SUBE.",
        "Sin integración real con Red SUBE.",
        "Sin consulta a cuentas reales.",
        "Sin consulta a tarjetas reales.",
        "Sin modificación de perfiles reales.",
        "Sin modificación de validadoras reales.",
        "Sin procesamiento de datos sensibles.",
        "Sin diagnóstico médico.",
        "Sin CUD real.",
        "Sin certificados médicos reales.",
        "Sin sanciones.",
        "Sin ranking.",
        "Sin vigilancia.",
        "Sin obligación para pasajeros.",
        "Sin carga operativa para el chofer.",
        "El usuario conserva control sobre sus preferencias.",
        "Las preferencias son revocables.",
    ]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
