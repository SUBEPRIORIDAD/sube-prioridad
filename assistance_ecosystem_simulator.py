"""
SUBE Prioridad — Simulador conceptual de ecosistema de asistencia.

Este módulo modela, de manera demostrativa, la secuencia conceptual prevista
por SUBE Prioridad:

    necesidad previamente acreditada
    ↓
    atributo técnico no sensible
    ↓
    preferencia de asistencia configurada por el usuario
    ↓
    validación demostrativa
    ↓
    sincronización conceptual con el ecosistema
    ↓
    alerta pasiva, silenciosa, discreta, preventiva, visible o lumínica
    ↓
    asistencia preventiva sin exponer datos sensibles

No representa implementación oficial vigente.
No integra SUBE real.
No integra Red SUBE real.
No integra Mi Argentina real.
No integra ANDIS real.
No integra SISA real.
No integra RENAPER real.
No integra CNRT real.
No modifica validadoras reales.
No procesa DNI.
No procesa nombre.
No procesa domicilio.
No procesa diagnóstico.
No procesa historia clínica.
No procesa CUD.
No procesa certificados médicos.
No genera sanciones.
No genera rankings.
No genera vigilancia.
No impone obligaciones a pasajeros.
No impone cargas operativas al chofer.

Finalidad:
    Mostrar cómo podría organizarse una arquitectura conceptual, modular y
    progresiva para comunicar una necesidad de asistencia sin revelar su causa.

Principio rector:
    El transporte no necesita conocer el diagnóstico.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Ecosistema de Asistencia"
SIMULATOR_VERSION = "0.1.0"
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
    """
    Modalidades conceptuales de asistencia configurables por el usuario.

    No son diagnósticos.
    No son categorías médicas.
    No son certificados.
    """

    SILENT = "silent"
    PASSIVE = "passive"
    DISCREET = "discreet"
    PREVENTIVE = "preventive"
    VISIBLE = "visible"
    LUMINOUS = "luminous"


class EcosystemNode(str, Enum):
    """
    Nodos conceptuales del ecosistema.

    Todos son demostrativos.
    Ninguno representa integración productiva real.
    """

    PRIORITY_ATTRIBUTE = "priority_attribute"
    USER_PREFERENCES = "user_preferences"
    VALIDATOR_EDGE = "validator_edge"
    TRANSPORT_UNIT = "transport_unit"
    PASSENGER_ENVIRONMENT = "passenger_environment"
    ACCESSIBILITY_RESOURCE = "accessibility_resource"
    AGGREGATE_EVALUATION = "aggregate_evaluation"


class SequenceStatus(str, Enum):
    READY = "ready"
    BLOCKED = "blocked"
    DEGRADED = "degraded"


class SyncStatus(str, Enum):
    SIMULATED_SYNC = "simulated_sync"
    LOCAL_ONLY = "local_only"
    NOT_SYNCED = "not_synced"


class AlertVisibility(str, Enum):
    NONE = "none"
    INTERNAL = "internal"
    PASSIVE = "passive"
    DISCREET = "discreet"
    GENERIC_VISIBLE = "generic_visible"
    GENERIC_LUMINOUS = "generic_luminous"


@dataclass(frozen=True)
class AssistancePreference:
    """
    Preferencia demostrativa de asistencia.

    La persona usuaria conserva el control sobre cómo desea viajar.
    """

    mode: AssistanceMode
    allow_passive_alert: bool
    allow_luminous_alert: bool
    allow_visible_generic_alert: bool
    allow_accessibility_resource_ping: bool


@dataclass(frozen=True)
class PriorityContext:
    """
    Contexto demostrativo del atributo de prioridad.

    No contiene datos sensibles.
    No contiene diagnóstico.
    No contiene identidad civil.
    """

    priority_attribute_token: str
    previously_accredited_need: bool
    active: bool
    valid_until_demo: Optional[str] = None


@dataclass(frozen=True)
class TransportEcosystemContext:
    """
    Contexto operativo conceptual del viaje.

    No representa geolocalización real.
    No representa una unidad real.
    No consulta sistemas externos.
    """

    country: str
    network_demo_id: str
    route_demo_id: str
    vehicle_demo_id: str
    validator_demo_id: str
    trip_demo_id: str
    occupancy_level: str = "medium"


@dataclass(frozen=True)
class AssistanceSequenceInput:
    """
    Entrada conceptual para evaluar la secuencia de asistencia.

    Este payload no debe contener datos personales ni médicos.
    """

    priority_context: PriorityContext
    preference: AssistancePreference
    transport_context: TransportEcosystemContext
    requested_nodes: List[EcosystemNode] = field(default_factory=list)


@dataclass(frozen=True)
class PassiveAlertPlan:
    """
    Plan de alerta resultante.

    La alerta es genérica.
    No identifica causa.
    No expone diagnóstico.
    """

    visibility: AlertVisibility
    message: str
    luminous_enabled: bool
    driver_action_required: bool
    passenger_action_required: bool
    accessibility_resource_ping: bool


@dataclass(frozen=True)
class EcosystemSyncResult:
    """
    Resultado conceptual de sincronización.

    No existe sincronización real.
    Sólo se simula coherencia entre nodos.
    """

    sync_status: SyncStatus
    synchronized_nodes: List[EcosystemNode]
    degraded_nodes: List[EcosystemNode]
    reason: str


@dataclass(frozen=True)
class AssistanceSequenceResult:
    """
    Resultado final de la secuencia conceptual de asistencia.
    """

    project: str
    module: str
    version: str
    demo_mode: bool
    sequence_status: SequenceStatus
    priority_active: bool
    previously_accredited_need: bool
    assistance_mode: AssistanceMode
    alert_plan: PassiveAlertPlan
    sync_result: EcosystemSyncResult
    privacy_notice: str
    driver_burden: str
    warnings: List[str]
    blocked_reasons: List[str]
    timestamp_utc: str


def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    """
    Rechaza datos personales, médicos o sensibles incompatibles con el proyecto.
    """
    normalized_keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))

    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )


def create_demo_priority_context(
    priority_attribute_token: str = "demo-priority-attribute-001",
    previously_accredited_need: bool = True,
    active: bool = True,
    valid_until_demo: Optional[str] = "demo-validity-window",
) -> PriorityContext:
    """
    Crea un atributo técnico demostrativo.

    No acredita una condición real.
    No consulta organismos.
    No contiene diagnóstico.
    """
    if not priority_attribute_token or not priority_attribute_token.strip():
        raise ValueError("El token técnico demostrativo no puede estar vacío.")

    assert_no_prohibited_fields({"priority_attribute_token": priority_attribute_token})

    return PriorityContext(
        priority_attribute_token=priority_attribute_token.strip(),
        previously_accredited_need=previously_accredited_need,
        active=active,
        valid_until_demo=valid_until_demo,
    )


def create_demo_preference(
    mode: AssistanceMode = AssistanceMode.PREVENTIVE,
    allow_passive_alert: bool = True,
    allow_luminous_alert: bool = False,
    allow_visible_generic_alert: bool = False,
    allow_accessibility_resource_ping: bool = False,
) -> AssistancePreference:
    """
    Crea preferencias demostrativas de asistencia.

    El usuario decide el modo.
    El sistema no fuerza exposición visible.
    """
    return AssistancePreference(
        mode=mode,
        allow_passive_alert=allow_passive_alert,
        allow_luminous_alert=allow_luminous_alert,
        allow_visible_generic_alert=allow_visible_generic_alert,
        allow_accessibility_resource_ping=allow_accessibility_resource_ping,
    )


def create_demo_transport_context(
    country: str = "Argentina",
    network_demo_id: str = "demo-network-sube",
    route_demo_id: str = "demo-route-001",
    vehicle_demo_id: str = "demo-vehicle-001",
    validator_demo_id: str = "demo-validator-001",
    trip_demo_id: str = "demo-trip-001",
    occupancy_level: str = "medium",
) -> TransportEcosystemContext:
    """
    Crea un contexto demostrativo del ecosistema de transporte.
    """
    return TransportEcosystemContext(
        country=country,
        network_demo_id=network_demo_id,
        route_demo_id=route_demo_id,
        vehicle_demo_id=vehicle_demo_id,
        validator_demo_id=validator_demo_id,
        trip_demo_id=trip_demo_id,
        occupancy_level=occupancy_level,
    )


def create_demo_sequence_input(
    priority_context: Optional[PriorityContext] = None,
    preference: Optional[AssistancePreference] = None,
    transport_context: Optional[TransportEcosystemContext] = None,
    requested_nodes: Optional[List[EcosystemNode]] = None,
) -> AssistanceSequenceInput:
    """
    Construye una entrada demostrativa completa para simular el ecosistema.
    """
    return AssistanceSequenceInput(
        priority_context=priority_context or create_demo_priority_context(),
        preference=preference or create_demo_preference(),
        transport_context=transport_context or create_demo_transport_context(),
        requested_nodes=requested_nodes or _default_requested_nodes(),
    )


def simulate_assistance_sequence(
    sequence_input: AssistanceSequenceInput,
) -> AssistanceSequenceResult:
    """
    Simula la secuencia conceptual de asistencia preventiva.

    La salida no identifica personas.
    La salida no revela motivos médicos.
    La salida no ordena conductas.
    La salida no impone tareas al chofer.
    """
    assert_no_prohibited_fields(
        {
            "priority_attribute_token": sequence_input.priority_context.priority_attribute_token,
            "network_demo_id": sequence_input.transport_context.network_demo_id,
            "route_demo_id": sequence_input.transport_context.route_demo_id,
            "vehicle_demo_id": sequence_input.transport_context.vehicle_demo_id,
            "validator_demo_id": sequence_input.transport_context.validator_demo_id,
            "trip_demo_id": sequence_input.transport_context.trip_demo_id,
        }
    )

    blocked_reasons = _blocked_reasons(sequence_input)

    if blocked_reasons:
        alert_plan = _build_no_alert_plan()
        sync_result = _build_not_synced_result(reason="La secuencia fue bloqueada por reglas de seguridad.")

        return AssistanceSequenceResult(
            project=PROJECT_NAME,
            module=MODULE_NAME,
            version=SIMULATOR_VERSION,
            demo_mode=DEMO_MODE,
            sequence_status=SequenceStatus.BLOCKED,
            priority_active=False,
            previously_accredited_need=sequence_input.priority_context.previously_accredited_need,
            assistance_mode=sequence_input.preference.mode,
            alert_plan=alert_plan,
            sync_result=sync_result,
            privacy_notice=_privacy_notice(),
            driver_burden=_driver_burden_notice(),
            warnings=_common_warnings(),
            blocked_reasons=blocked_reasons,
            timestamp_utc=_now_utc(),
        )

    sync_result = _simulate_ecosystem_sync(sequence_input)
    alert_plan = _build_alert_plan(sequence_input)

    sequence_status = (
        SequenceStatus.DEGRADED
        if sync_result.degraded_nodes
        else SequenceStatus.READY
    )

    return AssistanceSequenceResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=SIMULATOR_VERSION,
        demo_mode=DEMO_MODE,
        sequence_status=sequence_status,
        priority_active=True,
        previously_accredited_need=True,
        assistance_mode=sequence_input.preference.mode,
        alert_plan=alert_plan,
        sync_result=sync_result,
        privacy_notice=_privacy_notice(),
        driver_burden=_driver_burden_notice(),
        warnings=_common_warnings(),
        blocked_reasons=[],
        timestamp_utc=_now_utc(),
    )


def result_to_dict(result: AssistanceSequenceResult) -> Dict[str, Any]:
    """
    Convierte el resultado en un diccionario serializable.
    """
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "sequence_status": result.sequence_status.value,
        "priority_active": result.priority_active,
        "previously_accredited_need": result.previously_accredited_need,
        "assistance_mode": result.assistance_mode.value,
        "alert_plan": {
            "visibility": result.alert_plan.visibility.value,
            "message": result.alert_plan.message,
            "luminous_enabled": result.alert_plan.luminous_enabled,
            "driver_action_required": result.alert_plan.driver_action_required,
            "passenger_action_required": result.alert_plan.passenger_action_required,
            "accessibility_resource_ping": result.alert_plan.accessibility_resource_ping,
        },
        "sync_result": {
            "sync_status": result.sync_result.sync_status.value,
            "synchronized_nodes": [node.value for node in result.sync_result.synchronized_nodes],
            "degraded_nodes": [node.value for node in result.sync_result.degraded_nodes],
            "reason": result.sync_result.reason,
        },
        "privacy_notice": result.privacy_notice,
        "driver_burden": result.driver_burden,
        "warnings": result.warnings,
        "blocked_reasons": result.blocked_reasons,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    """
    Ejecuta una demostración completa del ecosistema de asistencia.
    """
    sequence_input = create_demo_sequence_input(
        preference=create_demo_preference(
            mode=AssistanceMode.PREVENTIVE,
            allow_passive_alert=True,
            allow_luminous_alert=False,
            allow_visible_generic_alert=False,
            allow_accessibility_resource_ping=False,
        )
    )

    result = simulate_assistance_sequence(sequence_input)

    return result_to_dict(result)


def _blocked_reasons(sequence_input: AssistanceSequenceInput) -> List[str]:
    reasons: List[str] = []

    if sequence_input.transport_context.country.strip().lower() != "argentina":
        reasons.append("outside_argentina_context")

    if not sequence_input.priority_context.previously_accredited_need:
        reasons.append("need_not_previously_accredited")

    if not sequence_input.priority_context.active:
        reasons.append("priority_attribute_not_active")

    if _looks_like_free_text(sequence_input.priority_context.priority_attribute_token):
        reasons.append("priority_attribute_token_looks_like_free_text")

    if not sequence_input.requested_nodes:
        reasons.append("no_ecosystem_nodes_requested")

    return reasons


def _simulate_ecosystem_sync(
    sequence_input: AssistanceSequenceInput,
) -> EcosystemSyncResult:
    requested = list(sequence_input.requested_nodes)

    degraded_nodes: List[EcosystemNode] = []

    if sequence_input.preference.mode == AssistanceMode.SILENT:
        degraded_nodes.append(EcosystemNode.PASSENGER_ENVIRONMENT)

    if not sequence_input.preference.allow_accessibility_resource_ping:
        degraded_nodes.append(EcosystemNode.ACCESSIBILITY_RESOURCE)

    synchronized_nodes = [
        node for node in requested if node not in degraded_nodes
    ]

    if degraded_nodes:
        return EcosystemSyncResult(
            sync_status=SyncStatus.LOCAL_ONLY,
            synchronized_nodes=synchronized_nodes,
            degraded_nodes=degraded_nodes,
            reason=(
                "Sincronización demostrativa limitada por preferencias del usuario. "
                "El sistema respeta modos silenciosos o pasivos sin forzar exposición."
            ),
        )

    return EcosystemSyncResult(
        sync_status=SyncStatus.SIMULATED_SYNC,
        synchronized_nodes=synchronized_nodes,
        degraded_nodes=[],
        reason=(
            "Sincronización conceptual entre nodos demostrativos del ecosistema. "
            "No existe integración productiva real."
        ),
    )


def _build_alert_plan(sequence_input: AssistanceSequenceInput) -> PassiveAlertPlan:
    preference = sequence_input.preference

    if preference.mode == AssistanceMode.SILENT:
        return PassiveAlertPlan(
            visibility=AlertVisibility.NONE,
            message=(
                "Modo silencioso: no se emite alerta visible. "
                "La preferencia del usuario bloquea la exposición al entorno."
            ),
            luminous_enabled=False,
            driver_action_required=False,
            passenger_action_required=False,
            accessibility_resource_ping=False,
        )

    if preference.mode == AssistanceMode.PASSIVE:
        return PassiveAlertPlan(
            visibility=AlertVisibility.PASSIVE,
            message=(
                "Alerta pasiva demostrativa: registro interno de asistencia preventiva "
                "sin mensaje visible al público."
            ),
            luminous_enabled=False,
            driver_action_required=False,
            passenger_action_required=False,
            accessibility_resource_ping=False,
        )

    if preference.mode == AssistanceMode.DISCREET:
        return PassiveAlertPlan(
            visibility=AlertVisibility.DISCREET,
            message=(
                "Alerta discreta demostrativa: señal genérica de asistencia sin causa, "
                "sin diagnóstico y sin identificación personal."
            ),
            luminous_enabled=False,
            driver_action_required=False,
            passenger_action_required=False,
            accessibility_resource_ping=preference.allow_accessibility_resource_ping,
        )

    if preference.mode == AssistanceMode.VISIBLE and preference.allow_visible_generic_alert:
        return PassiveAlertPlan(
            visibility=AlertVisibility.GENERIC_VISIBLE,
            message=(
                "Alerta visible genérica: una persona puede requerir asistencia preventiva. "
                "No se informa el motivo."
            ),
            luminous_enabled=False,
            driver_action_required=False,
            passenger_action_required=False,
            accessibility_resource_ping=preference.allow_accessibility_resource_ping,
        )

    if preference.mode == AssistanceMode.LUMINOUS and preference.allow_luminous_alert:
        return PassiveAlertPlan(
            visibility=AlertVisibility.GENERIC_LUMINOUS,
            message=(
                "Alerta lumínica genérica demostrativa: señal no verbal de asistencia "
                "preventiva sin exposición de datos personales."
            ),
            luminous_enabled=True,
            driver_action_required=False,
            passenger_action_required=False,
            accessibility_resource_ping=preference.allow_accessibility_resource_ping,
        )

    return PassiveAlertPlan(
        visibility=AlertVisibility.PASSIVE,
        message=(
            "Alerta preventiva pasiva por defecto: el sistema conserva privacidad "
            "y evita exposición innecesaria."
        ),
        luminous_enabled=False,
        driver_action_required=False,
        passenger_action_required=False,
        accessibility_resource_ping=preference.allow_accessibility_resource_ping,
    )


def _build_no_alert_plan() -> PassiveAlertPlan:
    return PassiveAlertPlan(
        visibility=AlertVisibility.NONE,
        message="No se emite alerta porque la secuencia demostrativa fue bloqueada.",
        luminous_enabled=False,
        driver_action_required=False,
        passenger_action_required=False,
        accessibility_resource_ping=False,
    )


def _build_not_synced_result(reason: str) -> EcosystemSyncResult:
    return EcosystemSyncResult(
        sync_status=SyncStatus.NOT_SYNCED,
        synchronized_nodes=[],
        degraded_nodes=[],
        reason=reason,
    )


def _default_requested_nodes() -> List[EcosystemNode]:
    return [
        EcosystemNode.PRIORITY_ATTRIBUTE,
        EcosystemNode.USER_PREFERENCES,
        EcosystemNode.VALIDATOR_EDGE,
        EcosystemNode.TRANSPORT_UNIT,
        EcosystemNode.PASSENGER_ENVIRONMENT,
        EcosystemNode.ACCESSIBILITY_RESOURCE,
        EcosystemNode.AGGREGATE_EVALUATION,
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
    }

    return any(term in normalized for term in suspicious_terms) or len(normalized.split()) > 1


def _privacy_notice() -> str:
    return (
        "La secuencia no revela DNI, nombre, domicilio, diagnóstico, CUD, "
        "historia clínica ni certificado médico. Sólo opera con atributos "
        "técnicos demostrativos no sensibles."
    )


def _driver_burden_notice() -> str:
    return (
        "El personal de conducción no diagnostica, no valida documentación, "
        "no administra beneficios, no sanciona y no decide la prioridad."
    )


def _common_warnings() -> List[str]:
    return [
        "Módulo conceptual y demostrativo.",
        "Sin implementación oficial vigente.",
        "Sin integración real con SUBE.",
        "Sin integración real con Red SUBE.",
        "Sin integración real con organismos públicos.",
        "Sin modificación de validadoras reales.",
        "Sin geolocalización real.",
        "Sin procesamiento de datos sensibles.",
        "Sin diagnóstico médico.",
        "Sin CUD real.",
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
