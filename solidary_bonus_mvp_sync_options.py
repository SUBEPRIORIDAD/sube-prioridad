"""
SUBE Prioridad — Opciones MVP de sincronización para Bono Solidario.

Este módulo enumera y evalúa tres alternativas iniciales para sincronizar
un evento solidario dentro del transporte público.

Opciones MVP:

1. MOBILE_TO_MOBILE_REDSUBE_CONTEXT
   Sincronización entre celulares, usando Red SUBE demo como contexto:
   validación paga, misma red, misma línea/servicio/ventana y confirmación
   del usuario SUBE Prioridad.

2. PRIORITY_PHONE_NFC_TO_COLLABORATOR_CARD
   El usuario con atributo SUBE Prioridad tiene celular con NFC.
   El colaborador acerca su tarjeta SUBE física.
   El celular tokeniza la tarjeta en modo demo y genera una instrucción
   conceptual de próximo viaje.

3. VALIDATOR_ASSISTED_CARD_TAP
   Alternativa para colectivos, Tren de la Costa o medios con validadora a bordo:
   luego de validarse el viaje del usuario SUBE Prioridad, se abre una ventana
   temporal. El colaborador que cedió un asiento de uso general puede acercar
   su tarjeta a la validadora para registrar el Bono Solidario demo.

   Esta opción puede requerir un modo asistido por consola, validadora,
   terminal u operador. No debe interpretarse como obligación del chofer.
   El chofer no decide el beneficio, no verifica discapacidad, no controla
   diagnósticos y no administra sanciones.

Este módulo NO acredita beneficios reales.
Este módulo NO calcula tarifa real.
Este módulo NO escribe tarjetas reales.
Este módulo NO integra SUBE real.
Este módulo NO integra Red SUBE real.
Este módulo NO consulta validadoras reales.
Este módulo NO consulta molinetes reales.
Este módulo NO usa DNI.
Este módulo NO usa nombre.
Este módulo NO usa diagnóstico.
Este módulo NO usa CUD visible.
Este módulo NO usa GPS exacto.
Este módulo NO impone carga operativa al chofer.

La salida de este módulo debe combinarse luego con:
    - handoff antifraude;
    - matcher temporal/contextual;
    - guardia de proximidad no excluyente;
    - política demo Red SUBE + Bono Solidario +50%;
    - auditoría agregada no sensible.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Opciones MVP de Sincronización para Bono Solidario"
MODULE_VERSION = "0.1.0"
DEMO_MODE = True

PERCENT_SCALE = 10000
FIFTY_PERCENT_BPS = 5000
FULL_DISCOUNT_BPS = 10000


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
    "gps",
    "latitud",
    "longitud",
    "latitude",
    "longitude",
    "imei",
    "mac",
    "saldo",
    "dinero",
}


class MvpSyncOption(str, Enum):
    MOBILE_TO_MOBILE_REDSUBE_CONTEXT = "mobile_to_mobile_redsube_context"
    PRIORITY_PHONE_NFC_TO_COLLABORATOR_CARD = "priority_phone_nfc_to_collaborator_card"
    VALIDATOR_ASSISTED_CARD_TAP = "validator_assisted_card_tap"


class MvpSyncStatus(str, Enum):
    READY = "ready"
    READY_WITH_AUDIT = "ready_with_audit"
    NEEDS_REVIEW = "needs_review"
    REJECTED = "rejected"


class TransportMode(str, Enum):
    BUS = "bus"
    TRAIN = "train"
    SUBWAY = "subway"
    COASTAL_TRAIN_OR_ONBOARD_VALIDATOR = "coastal_train_or_onboard_validator"
    OTHER_PUBLIC_TRANSPORT = "other_public_transport"


class ValidationPointType(str, Enum):
    VEHICLE_VALIDATOR = "vehicle_validator"
    ONBOARD_TRAIN_VALIDATOR = "onboard_train_validator"
    STATION_TURNSTILE = "station_turnstile"
    STATION_ACCESS_GATE = "station_access_gate"
    TERMINAL_VALIDATOR = "terminal_validator"
    UNKNOWN = "unknown"


class SeatType(str, Enum):
    GENERAL_USE = "general_use"
    LEGAL_PRIORITY = "legal_priority"


class AssistedActivationActor(str, Enum):
    SYSTEM_AUTOMATED = "system_automated"
    VALIDATOR_DEVICE_MODE = "validator_device_mode"
    DRIVER_CONSOLE_OPTIONAL = "driver_console_optional"
    STATION_OR_OPERATOR_ASSISTED = "station_or_operator_assisted"
    NOT_REQUIRED = "not_required"


class BenefitInstructionKind(str, Enum):
    NEXT_TRIP_DEMO_WINDOW = "next_trip_demo_window"
    CARD_UPDATE_PENDING_DEMO = "card_update_pending_demo"
    VALIDATOR_TAP_PENDING_DEMO = "validator_tap_pending_demo"
    NONE = "none"


@dataclass(frozen=True)
class MvpSyncPolicy:
    mobile_to_mobile_window_minutes: int
    priority_phone_nfc_window_minutes: int
    validator_assisted_window_minutes: int
    station_turnstile_window_minutes: int
    benefit_validity_hours: int
    bonus_extra_discount_bps_demo: int
    max_total_discount_bps_demo: int
    require_priority_attribute_active: bool
    require_priority_paid_validation: bool
    require_collaborator_paid_validation: bool
    require_priority_confirmation: bool
    require_general_use_seat: bool
    allow_driver_console_optional_mode: bool
    driver_console_must_not_be_mandatory: bool
    allow_good_faith_social_recognition_audit: bool
    max_events_per_priority_trip_demo: int
    max_events_per_collaborator_day_demo: int


@dataclass(frozen=True)
class MvpParticipantContext:
    priority_user_token: str
    priority_attribute_token: str
    collaborator_user_token: str
    collaborator_sube_card_token: str
    priority_user_has_active_attribute: bool
    priority_need_previously_accredited: bool
    priority_has_mobile_device: bool
    priority_mobile_has_nfc: bool
    collaborator_has_mobile_device: bool
    collaborator_has_physical_sube_card: bool


@dataclass(frozen=True)
class MvpRedSubeContext:
    network_demo_id: str
    route_demo_id: str
    service_window_demo_id: str
    validator_or_turnstile_demo_id: str
    vehicle_demo_id: Optional[str]
    trainset_demo_id: Optional[str]
    station_demo_id: Optional[str]
    platform_demo_id: Optional[str]
    transport_mode: TransportMode
    validation_point_type: ValidationPointType
    priority_paid_validation_confirmed: bool
    collaborator_paid_validation_confirmed: bool
    priority_validation_timestamp_utc: datetime
    collaborator_validation_timestamp_utc: Optional[datetime]
    sync_attempt_timestamp_utc: datetime


@dataclass(frozen=True)
class MvpSolidarySyncOptionRequest:
    mvp_sync_event_demo_id: str
    option: MvpSyncOption
    participant_context: MvpParticipantContext
    red_sube_context: MvpRedSubeContext
    seat_type: SeatType
    priority_user_confirms_seat_yield: bool
    voluntary_seat_yield_declared: bool
    collaborator_claims_unilaterally: bool
    same_network_demo_id: bool
    same_route_demo_id: bool
    same_service_window_demo_id: bool
    same_validator_or_turnstile_demo_id: bool
    same_vehicle_demo_id: bool
    same_trainset_demo_id: bool
    same_station_demo_id: bool
    same_platform_demo_id: bool
    mobile_handshake_available: bool
    nfc_card_tap_available: bool
    validator_second_tap_available: bool
    assisted_activation_actor: AssistedActivationActor
    good_faith_social_recognition_declared: bool
    current_base_red_sube_discount_bps_demo: int


@dataclass(frozen=True)
class MvpSolidarySyncOptionResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    option: MvpSyncOption
    status: MvpSyncStatus
    benefit_instruction_kind: BenefitInstructionKind
    opens_bonus_evaluation_window: bool
    blocks_solidary_bonus_flow: bool
    requires_audit_review: bool
    window_minutes: int
    window_matched: bool
    final_demo_discount_bps_if_eligible: int
    bonus_extra_discount_bps_demo: int
    base_red_sube_discount_bps_demo: int
    assisted_activation_actor: AssistedActivationActor
    driver_console_optional_only: bool
    hard_risk_flags: List[str]
    audit_flags: List[str]
    reason: str
    security_summary: Dict[str, Any]
    benefit_window_demo: Optional[Dict[str, Any]]
    privacy_notice: str
    driver_burden_notice: str
    legal_scope_notice: str
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


def create_demo_mvp_sync_policy(
    mobile_to_mobile_window_minutes: int = 10,
    priority_phone_nfc_window_minutes: int = 10,
    validator_assisted_window_minutes: int = 8,
    station_turnstile_window_minutes: int = 60,
    benefit_validity_hours: int = 24,
    bonus_extra_discount_bps_demo: int = FIFTY_PERCENT_BPS,
    max_total_discount_bps_demo: int = FULL_DISCOUNT_BPS,
    require_priority_attribute_active: bool = True,
    require_priority_paid_validation: bool = True,
    require_collaborator_paid_validation: bool = True,
    require_priority_confirmation: bool = True,
    require_general_use_seat: bool = True,
    allow_driver_console_optional_mode: bool = True,
    driver_console_must_not_be_mandatory: bool = True,
    allow_good_faith_social_recognition_audit: bool = True,
    max_events_per_priority_trip_demo: int = 1,
    max_events_per_collaborator_day_demo: int = 3,
) -> MvpSyncPolicy:
    _positive("mobile_to_mobile_window_minutes", mobile_to_mobile_window_minutes)
    _positive("priority_phone_nfc_window_minutes", priority_phone_nfc_window_minutes)
    _positive("validator_assisted_window_minutes", validator_assisted_window_minutes)
    _positive("station_turnstile_window_minutes", station_turnstile_window_minutes)
    _positive("benefit_validity_hours", benefit_validity_hours)
    _positive("bonus_extra_discount_bps_demo", bonus_extra_discount_bps_demo)
    _positive("max_total_discount_bps_demo", max_total_discount_bps_demo)
    _positive("max_events_per_priority_trip_demo", max_events_per_priority_trip_demo)
    _positive("max_events_per_collaborator_day_demo", max_events_per_collaborator_day_demo)

    if bonus_extra_discount_bps_demo > FULL_DISCOUNT_BPS:
        raise ValueError("El adicional demo no puede superar el 100%.")

    if max_total_discount_bps_demo > FULL_DISCOUNT_BPS:
        raise ValueError("El tope total demo no puede superar el 100%.")

    return MvpSyncPolicy(
        mobile_to_mobile_window_minutes=mobile_to_mobile_window_minutes,
        priority_phone_nfc_window_minutes=priority_phone_nfc_window_minutes,
        validator_assisted_window_minutes=validator_assisted_window_minutes,
        station_turnstile_window_minutes=station_turnstile_window_minutes,
        benefit_validity_hours=benefit_validity_hours,
        bonus_extra_discount_bps_demo=bonus_extra_discount_bps_demo,
        max_total_discount_bps_demo=max_total_discount_bps_demo,
        require_priority_attribute_active=require_priority_attribute_active,
        require_priority_paid_validation=require_priority_paid_validation,
        require_collaborator_paid_validation=require_collaborator_paid_validation,
        require_priority_confirmation=require_priority_confirmation,
        require_general_use_seat=require_general_use_seat,
        allow_driver_console_optional_mode=allow_driver_console_optional_mode,
        driver_console_must_not_be_mandatory=driver_console_must_not_be_mandatory,
        allow_good_faith_social_recognition_audit=allow_good_faith_social_recognition_audit,
        max_events_per_priority_trip_demo=max_events_per_priority_trip_demo,
        max_events_per_collaborator_day_demo=max_events_per_collaborator_day_demo,
    )


def create_demo_mvp_participant_context(
    priority_user_token: str = "demo-priority-user-001",
    priority_attribute_token: str = "demo-priority-attribute-001",
    collaborator_user_token: str = "demo-collaborator-user-001",
    collaborator_sube_card_token: str = "demo-collaborator-sube-card-001",
    priority_user_has_active_attribute: bool = True,
    priority_need_previously_accredited: bool = True,
    priority_has_mobile_device: bool = True,
    priority_mobile_has_nfc: bool = True,
    collaborator_has_mobile_device: bool = True,
    collaborator_has_physical_sube_card: bool = True,
) -> MvpParticipantContext:
    required_values = {
        "priority_user_token": priority_user_token,
        "priority_attribute_token": priority_attribute_token,
        "collaborator_user_token": collaborator_user_token,
        "collaborator_sube_card_token": collaborator_sube_card_token,
    }

    _validate_required_values(required_values)
    assert_no_prohibited_fields(required_values)

    return MvpParticipantContext(
        priority_user_token=priority_user_token.strip(),
        priority_attribute_token=priority_attribute_token.strip(),
        collaborator_user_token=collaborator_user_token.strip(),
        collaborator_sube_card_token=collaborator_sube_card_token.strip(),
        priority_user_has_active_attribute=priority_user_has_active_attribute,
        priority_need_previously_accredited=priority_need_previously_accredited,
        priority_has_mobile_device=priority_has_mobile_device,
        priority_mobile_has_nfc=priority_mobile_has_nfc,
        collaborator_has_mobile_device=collaborator_has_mobile_device,
        collaborator_has_physical_sube_card=collaborator_has_physical_sube_card,
    )


def create_demo_mvp_red_sube_context(
    network_demo_id: str = "demo-red-sube-network-001",
    route_demo_id: str = "demo-route-001",
    service_window_demo_id: str = "demo-service-window-001",
    validator_or_turnstile_demo_id: str = "demo-validator-001",
    vehicle_demo_id: Optional[str] = "demo-vehicle-001",
    trainset_demo_id: Optional[str] = None,
    station_demo_id: Optional[str] = None,
    platform_demo_id: Optional[str] = None,
    transport_mode: TransportMode = TransportMode.BUS,
    validation_point_type: ValidationPointType = ValidationPointType.VEHICLE_VALIDATOR,
    priority_paid_validation_confirmed: bool = True,
    collaborator_paid_validation_confirmed: bool = True,
    priority_validation_timestamp_utc: Optional[datetime] = None,
    collaborator_validation_timestamp_utc: Optional[datetime] = None,
    sync_attempt_timestamp_utc: Optional[datetime] = None,
) -> MvpRedSubeContext:
    required_values = {
        "network_demo_id": network_demo_id,
        "route_demo_id": route_demo_id,
        "service_window_demo_id": service_window_demo_id,
        "validator_or_turnstile_demo_id": validator_or_turnstile_demo_id,
    }

    _validate_required_values(required_values)
    assert_no_prohibited_fields(required_values)

    now = priority_validation_timestamp_utc or datetime.now(timezone.utc)

    return MvpRedSubeContext(
        network_demo_id=network_demo_id.strip(),
        route_demo_id=route_demo_id.strip(),
        service_window_demo_id=service_window_demo_id.strip(),
        validator_or_turnstile_demo_id=validator_or_turnstile_demo_id.strip(),
        vehicle_demo_id=_strip_optional(vehicle_demo_id),
        trainset_demo_id=_strip_optional(trainset_demo_id),
        station_demo_id=_strip_optional(station_demo_id),
        platform_demo_id=_strip_optional(platform_demo_id),
        transport_mode=transport_mode,
        validation_point_type=validation_point_type,
        priority_paid_validation_confirmed=priority_paid_validation_confirmed,
        collaborator_paid_validation_confirmed=collaborator_paid_validation_confirmed,
        priority_validation_timestamp_utc=now,
        collaborator_validation_timestamp_utc=collaborator_validation_timestamp_utc
        or now + timedelta(minutes=1),
        sync_attempt_timestamp_utc=sync_attempt_timestamp_utc or now + timedelta(minutes=3),
    )


def create_demo_mobile_to_mobile_request(
    created_at_utc: Optional[datetime] = None,
) -> MvpSolidarySyncOptionRequest:
    timestamp = created_at_utc or datetime.now(timezone.utc)

    return create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="demo-mobile-to-mobile-redsube-001",
        option=MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
        participant_context=create_demo_mvp_participant_context(
            priority_has_mobile_device=True,
            priority_mobile_has_nfc=False,
            collaborator_has_mobile_device=True,
            collaborator_has_physical_sube_card=True,
        ),
        red_sube_context=create_demo_mvp_red_sube_context(
            priority_validation_timestamp_utc=timestamp,
            collaborator_validation_timestamp_utc=timestamp + timedelta(minutes=1),
            sync_attempt_timestamp_utc=timestamp + timedelta(minutes=4),
        ),
        mobile_handshake_available=True,
        nfc_card_tap_available=False,
        validator_second_tap_available=False,
        assisted_activation_actor=AssistedActivationActor.NOT_REQUIRED,
    )


def create_demo_priority_phone_nfc_card_request(
    created_at_utc: Optional[datetime] = None,
) -> MvpSolidarySyncOptionRequest:
    timestamp = created_at_utc or datetime.now(timezone.utc)

    return create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="demo-priority-phone-nfc-card-001",
        option=MvpSyncOption.PRIORITY_PHONE_NFC_TO_COLLABORATOR_CARD,
        participant_context=create_demo_mvp_participant_context(
            priority_has_mobile_device=True,
            priority_mobile_has_nfc=True,
            collaborator_has_mobile_device=False,
            collaborator_has_physical_sube_card=True,
        ),
        red_sube_context=create_demo_mvp_red_sube_context(
            priority_validation_timestamp_utc=timestamp,
            collaborator_validation_timestamp_utc=timestamp + timedelta(minutes=1),
            sync_attempt_timestamp_utc=timestamp + timedelta(minutes=5),
        ),
        mobile_handshake_available=False,
        nfc_card_tap_available=True,
        validator_second_tap_available=False,
        assisted_activation_actor=AssistedActivationActor.NOT_REQUIRED,
    )


def create_demo_validator_assisted_card_tap_request(
    created_at_utc: Optional[datetime] = None,
    transport_mode: TransportMode = TransportMode.BUS,
    validation_point_type: ValidationPointType = ValidationPointType.VEHICLE_VALIDATOR,
) -> MvpSolidarySyncOptionRequest:
    timestamp = created_at_utc or datetime.now(timezone.utc)

    trainset_id = (
        "demo-trainset-001"
        if transport_mode == TransportMode.COASTAL_TRAIN_OR_ONBOARD_VALIDATOR
        else None
    )

    vehicle_id = (
        None
        if transport_mode == TransportMode.COASTAL_TRAIN_OR_ONBOARD_VALIDATOR
        else "demo-vehicle-001"
    )

    return create_demo_mvp_sync_option_request(
        mvp_sync_event_demo_id="demo-validator-assisted-card-tap-001",
        option=MvpSyncOption.VALIDATOR_ASSISTED_CARD_TAP,
        participant_context=create_demo_mvp_participant_context(
            priority_has_mobile_device=False,
            priority_mobile_has_nfc=False,
            collaborator_has_mobile_device=False,
            collaborator_has_physical_sube_card=True,
        ),
        red_sube_context=create_demo_mvp_red_sube_context(
            transport_mode=transport_mode,
            validation_point_type=validation_point_type,
            vehicle_demo_id=vehicle_id,
            trainset_demo_id=trainset_id,
            priority_validation_timestamp_utc=timestamp,
            collaborator_validation_timestamp_utc=timestamp + timedelta(minutes=2),
            sync_attempt_timestamp_utc=timestamp + timedelta(minutes=6),
        ),
        mobile_handshake_available=False,
        nfc_card_tap_available=False,
        validator_second_tap_available=True,
        assisted_activation_actor=AssistedActivationActor.DRIVER_CONSOLE_OPTIONAL,
        same_vehicle_demo_id=transport_mode != TransportMode.COASTAL_TRAIN_OR_ONBOARD_VALIDATOR,
        same_trainset_demo_id=transport_mode == TransportMode.COASTAL_TRAIN_OR_ONBOARD_VALIDATOR,
        good_faith_social_recognition_declared=True,
    )


def create_demo_mvp_sync_option_request(
    mvp_sync_event_demo_id: str = "demo-mvp-sync-option-001",
    option: MvpSyncOption = MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT,
    participant_context: Optional[MvpParticipantContext] = None,
    red_sube_context: Optional[MvpRedSubeContext] = None,
    seat_type: SeatType = SeatType.GENERAL_USE,
    priority_user_confirms_seat_yield: bool = True,
    voluntary_seat_yield_declared: bool = True,
    collaborator_claims_unilaterally: bool = False,
    same_network_demo_id: bool = True,
    same_route_demo_id: bool = True,
    same_service_window_demo_id: bool = True,
    same_validator_or_turnstile_demo_id: bool = True,
    same_vehicle_demo_id: bool = True,
    same_trainset_demo_id: bool = False,
    same_station_demo_id: bool = False,
    same_platform_demo_id: bool = False,
    mobile_handshake_available: bool = True,
    nfc_card_tap_available: bool = False,
    validator_second_tap_available: bool = False,
    assisted_activation_actor: AssistedActivationActor = AssistedActivationActor.NOT_REQUIRED,
    good_faith_social_recognition_declared: bool = False,
    current_base_red_sube_discount_bps_demo: int = FIFTY_PERCENT_BPS,
) -> MvpSolidarySyncOptionRequest:
    required_values = {"mvp_sync_event_demo_id": mvp_sync_event_demo_id}

    _validate_required_values(required_values)
    assert_no_prohibited_fields(required_values)

    if current_base_red_sube_discount_bps_demo < 0:
        raise ValueError("El descuento base demo no puede ser negativo.")

    if current_base_red_sube_discount_bps_demo > FULL_DISCOUNT_BPS:
        raise ValueError("El descuento base demo no puede superar el 100%.")

    return MvpSolidarySyncOptionRequest(
        mvp_sync_event_demo_id=mvp_sync_event_demo_id.strip(),
        option=option,
        participant_context=participant_context or create_demo_mvp_participant_context(),
        red_sube_context=red_sube_context or create_demo_mvp_red_sube_context(),
        seat_type=seat_type,
        priority_user_confirms_seat_yield=priority_user_confirms_seat_yield,
        voluntary_seat_yield_declared=voluntary_seat_yield_declared,
        collaborator_claims_unilaterally=collaborator_claims_unilaterally,
        same_network_demo_id=same_network_demo_id,
        same_route_demo_id=same_route_demo_id,
        same_service_window_demo_id=same_service_window_demo_id,
        same_validator_or_turnstile_demo_id=same_validator_or_turnstile_demo_id,
        same_vehicle_demo_id=same_vehicle_demo_id,
        same_trainset_demo_id=same_trainset_demo_id,
        same_station_demo_id=same_station_demo_id,
        same_platform_demo_id=same_platform_demo_id,
        mobile_handshake_available=mobile_handshake_available,
        nfc_card_tap_available=nfc_card_tap_available,
        validator_second_tap_available=validator_second_tap_available,
        assisted_activation_actor=assisted_activation_actor,
        good_faith_social_recognition_declared=good_faith_social_recognition_declared,
        current_base_red_sube_discount_bps_demo=current_base_red_sube_discount_bps_demo,
    )


def evaluate_mvp_solidary_sync_option(
    request: MvpSolidarySyncOptionRequest,
    policy: Optional[MvpSyncPolicy] = None,
) -> MvpSolidarySyncOptionResult:
    policy = policy or create_demo_mvp_sync_policy()

    assert_no_prohibited_fields(
        {
            "mvp_sync_event_demo_id": request.mvp_sync_event_demo_id,
            "priority_user_token": request.participant_context.priority_user_token,
            "priority_attribute_token": request.participant_context.priority_attribute_token,
            "collaborator_user_token": request.participant_context.collaborator_user_token,
            "collaborator_sube_card_token": request.participant_context.collaborator_sube_card_token,
        }
    )

    window_minutes = _window_minutes_for_option(request, policy)
    window_matched = _window_matched(request.red_sube_context, window_minutes)
    hard_risk_flags = _hard_risk_flags(request, policy, window_matched)
    audit_flags = _audit_flags(request, policy)

    if hard_risk_flags:
        return _result(
            request=request,
            policy=policy,
            status=MvpSyncStatus.REJECTED,
            benefit_instruction_kind=BenefitInstructionKind.NONE,
            opens_bonus_evaluation_window=False,
            blocks_solidary_bonus_flow=True,
            requires_audit_review=True,
            window_minutes=window_minutes,
            window_matched=window_matched,
            hard_risk_flags=hard_risk_flags,
            audit_flags=audit_flags,
            reason=(
                "La opción MVP fue rechazada porque faltan condiciones mínimas "
                "o existen riesgos duros para el Bono Solidario demo."
            ),
        )

    instruction_kind = _benefit_instruction_kind(request)

    if request.option == MvpSyncOption.VALIDATOR_ASSISTED_CARD_TAP:
        return _result(
            request=request,
            policy=policy,
            status=MvpSyncStatus.READY_WITH_AUDIT,
            benefit_instruction_kind=instruction_kind,
            opens_bonus_evaluation_window=True,
            blocks_solidary_bonus_flow=False,
            requires_audit_review=True,
            window_minutes=window_minutes,
            window_matched=window_matched,
            hard_risk_flags=[],
            audit_flags=audit_flags,
            reason=(
                "La opción por validadora queda lista como alternativa piloto auditable. "
                "La participación del chofer o consola es opcional, no obligatoria, "
                "y no decide el beneficio."
            ),
        )

    return _result(
        request=request,
        policy=policy,
        status=MvpSyncStatus.READY,
        benefit_instruction_kind=instruction_kind,
        opens_bonus_evaluation_window=True,
        blocks_solidary_bonus_flow=False,
        requires_audit_review=bool(audit_flags),
        window_minutes=window_minutes,
        window_matched=window_matched,
        hard_risk_flags=[],
        audit_flags=audit_flags,
        reason=(
            "La opción MVP queda lista para abrir una ventana de evaluación "
            "del Bono Solidario demo."
        ),
    )


def result_to_dict(result: MvpSolidarySyncOptionResult) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "option": result.option.value,
        "status": result.status.value,
        "benefit_instruction_kind": result.benefit_instruction_kind.value,
        "opens_bonus_evaluation_window": result.opens_bonus_evaluation_window,
        "blocks_solidary_bonus_flow": result.blocks_solidary_bonus_flow,
        "requires_audit_review": result.requires_audit_review,
        "window_minutes": result.window_minutes,
        "window_matched": result.window_matched,
        "final_demo_discount_bps_if_eligible": result.final_demo_discount_bps_if_eligible,
        "bonus_extra_discount_bps_demo": result.bonus_extra_discount_bps_demo,
        "base_red_sube_discount_bps_demo": result.base_red_sube_discount_bps_demo,
        "assisted_activation_actor": result.assisted_activation_actor.value,
        "driver_console_optional_only": result.driver_console_optional_only,
        "hard_risk_flags": result.hard_risk_flags,
        "audit_flags": result.audit_flags,
        "reason": result.reason,
        "security_summary": result.security_summary,
        "benefit_window_demo": result.benefit_window_demo,
        "privacy_notice": result.privacy_notice,
        "driver_burden_notice": result.driver_burden_notice,
        "legal_scope_notice": result.legal_scope_notice,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }


def run_mobile_to_mobile_demo() -> Dict[str, Any]:
    request = create_demo_mobile_to_mobile_request()

    result = evaluate_mvp_solidary_sync_option(request)

    return result_to_dict(result)


def run_priority_phone_nfc_card_demo() -> Dict[str, Any]:
    request = create_demo_priority_phone_nfc_card_request()

    result = evaluate_mvp_solidary_sync_option(request)

    return result_to_dict(result)


def run_validator_assisted_card_tap_demo() -> Dict[str, Any]:
    request = create_demo_validator_assisted_card_tap_request()

    result = evaluate_mvp_solidary_sync_option(request)

    return result_to_dict(result)


def _hard_risk_flags(
    request: MvpSolidarySyncOptionRequest,
    policy: MvpSyncPolicy,
    window_matched: bool,
) -> List[str]:
    flags: List[str] = []
    participant = request.participant_context
    context = request.red_sube_context

    if _looks_like_free_text(request.mvp_sync_event_demo_id):
        flags.append("mvp_sync_event_id_looks_like_free_text")

    if _looks_like_free_text(participant.priority_user_token):
        flags.append("priority_user_token_looks_like_free_text")

    if _looks_like_free_text(participant.collaborator_user_token):
        flags.append("collaborator_user_token_looks_like_free_text")

    if participant.priority_user_token == participant.collaborator_user_token:
        flags.append("same_user_token_not_allowed")

    if policy.require_priority_attribute_active and not participant.priority_user_has_active_attribute:
        flags.append("priority_attribute_not_active")

    if not participant.priority_need_previously_accredited:
        flags.append("priority_need_not_previously_accredited")

    if policy.require_priority_paid_validation and not context.priority_paid_validation_confirmed:
        flags.append("priority_paid_validation_required")

    if (
        policy.require_collaborator_paid_validation
        and request.option != MvpSyncOption.VALIDATOR_ASSISTED_CARD_TAP
        and not context.collaborator_paid_validation_confirmed
    ):
        flags.append("collaborator_paid_validation_required")

    if policy.require_priority_confirmation and not request.priority_user_confirms_seat_yield:
        flags.append("priority_user_confirmation_required")

    if request.collaborator_claims_unilaterally:
        flags.append("collaborator_unilateral_claim")

    if not request.voluntary_seat_yield_declared:
        flags.append("voluntary_seat_yield_required")

    if policy.require_general_use_seat and request.seat_type != SeatType.GENERAL_USE:
        flags.append("legal_priority_seat_not_eligible_for_bonus")

    if not window_matched:
        flags.append("sync_window_expired")

    if _context_score(request) <= 0:
        flags.append("no_shared_transport_context")

    flags.extend(_option_specific_hard_flags(request, policy))

    return _deduplicate(flags)


def _option_specific_hard_flags(
    request: MvpSolidarySyncOptionRequest,
    policy: MvpSyncPolicy,
) -> List[str]:
    participant = request.participant_context
    context = request.red_sube_context
    flags: List[str] = []

    if request.option == MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT:
        if not participant.priority_has_mobile_device:
            flags.append("priority_mobile_required_for_mobile_to_mobile_option")

        if not participant.collaborator_has_mobile_device:
            flags.append("collaborator_mobile_required_for_mobile_to_mobile_option")

        if not request.mobile_handshake_available:
            flags.append("mobile_handshake_required_for_mobile_to_mobile_option")

    if request.option == MvpSyncOption.PRIORITY_PHONE_NFC_TO_COLLABORATOR_CARD:
        if not participant.priority_has_mobile_device:
            flags.append("priority_mobile_required_for_nfc_card_option")

        if not participant.priority_mobile_has_nfc:
            flags.append("priority_mobile_nfc_required_for_nfc_card_option")

        if not participant.collaborator_has_physical_sube_card:
            flags.append("collaborator_physical_card_required_for_nfc_card_option")

        if not request.nfc_card_tap_available:
            flags.append("nfc_card_tap_required_for_nfc_card_option")

    if request.option == MvpSyncOption.VALIDATOR_ASSISTED_CARD_TAP:
        if context.validation_point_type not in {
            ValidationPointType.VEHICLE_VALIDATOR,
            ValidationPointType.ONBOARD_TRAIN_VALIDATOR,
        }:
            flags.append("validator_assisted_option_requires_onboard_validator")

        if context.transport_mode not in {
            TransportMode.BUS,
            TransportMode.COASTAL_TRAIN_OR_ONBOARD_VALIDATOR,
        }:
            flags.append("validator_assisted_option_limited_to_bus_or_onboard_validator_demo")

        if not participant.collaborator_has_physical_sube_card:
            flags.append("collaborator_physical_card_required_for_validator_option")

        if not request.validator_second_tap_available:
            flags.append("validator_second_tap_required_for_validator_option")

        if (
            request.assisted_activation_actor == AssistedActivationActor.DRIVER_CONSOLE_OPTIONAL
            and not policy.allow_driver_console_optional_mode
        ):
            flags.append("driver_console_optional_mode_not_allowed_by_policy")

        if not policy.driver_console_must_not_be_mandatory:
            flags.append("driver_console_cannot_be_mandatory")

    return flags


def _audit_flags(
    request: MvpSolidarySyncOptionRequest,
    policy: MvpSyncPolicy,
) -> List[str]:
    flags: List[str] = []

    flags.append("mvp_option_audit")
    flags.append(f"option_{request.option.value}")

    if request.option == MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT:
        flags.append("mobile_to_mobile_redsube_context_audit")

    if request.option == MvpSyncOption.PRIORITY_PHONE_NFC_TO_COLLABORATOR_CARD:
        flags.append("priority_phone_nfc_to_card_audit")

    if request.option == MvpSyncOption.VALIDATOR_ASSISTED_CARD_TAP:
        flags.append("validator_assisted_card_tap_audit")
        flags.append("driver_console_optional_only_audit")
        flags.append("no_driver_obligation_audit")
        flags.append("social_good_faith_recognition_not_decisive_audit")

        if request.good_faith_social_recognition_declared:
            flags.append("good_faith_social_recognition_declared_audit")

    if not request.participant_context.priority_has_mobile_device:
        flags.append("priority_user_without_mobile_supported")

    if not request.participant_context.collaborator_has_mobile_device:
        flags.append("collaborator_without_mobile_supported")

    if request.same_vehicle_demo_id or request.same_trainset_demo_id:
        flags.append("onboard_context_audit")

    if request.same_station_demo_id or request.same_platform_demo_id:
        flags.append("station_or_platform_context_audit")

    if request.current_base_red_sube_discount_bps_demo + policy.bonus_extra_discount_bps_demo > policy.max_total_discount_bps_demo:
        flags.append("discount_cap_applied_demo")

    return _deduplicate(flags)


def _benefit_instruction_kind(
    request: MvpSolidarySyncOptionRequest,
) -> BenefitInstructionKind:
    if request.option == MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT:
        return BenefitInstructionKind.NEXT_TRIP_DEMO_WINDOW

    if request.option == MvpSyncOption.PRIORITY_PHONE_NFC_TO_COLLABORATOR_CARD:
        return BenefitInstructionKind.CARD_UPDATE_PENDING_DEMO

    if request.option == MvpSyncOption.VALIDATOR_ASSISTED_CARD_TAP:
        return BenefitInstructionKind.VALIDATOR_TAP_PENDING_DEMO

    return BenefitInstructionKind.NONE


def _window_minutes_for_option(
    request: MvpSolidarySyncOptionRequest,
    policy: MvpSyncPolicy,
) -> int:
    if request.option == MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT:
        return policy.mobile_to_mobile_window_minutes

    if request.option == MvpSyncOption.PRIORITY_PHONE_NFC_TO_COLLABORATOR_CARD:
        return policy.priority_phone_nfc_window_minutes

    if request.option == MvpSyncOption.VALIDATOR_ASSISTED_CARD_TAP:
        return policy.validator_assisted_window_minutes

    if request.red_sube_context.validation_point_type in {
        ValidationPointType.STATION_TURNSTILE,
        ValidationPointType.STATION_ACCESS_GATE,
    }:
        return policy.station_turnstile_window_minutes

    return policy.mobile_to_mobile_window_minutes


def _window_matched(
    context: MvpRedSubeContext,
    window_minutes: int,
) -> bool:
    earliest = context.priority_validation_timestamp_utc

    if context.collaborator_validation_timestamp_utc is not None:
        earliest = min(earliest, context.collaborator_validation_timestamp_utc)

    elapsed_seconds = abs((context.sync_attempt_timestamp_utc - earliest).total_seconds())

    return elapsed_seconds <= timedelta(minutes=window_minutes).total_seconds()


def _context_score(request: MvpSolidarySyncOptionRequest) -> int:
    score = 0

    if request.same_network_demo_id:
        score += 1

    if request.same_route_demo_id:
        score += 1

    if request.same_service_window_demo_id:
        score += 1

    if request.same_validator_or_turnstile_demo_id:
        score += 2

    if request.same_vehicle_demo_id:
        score += 2

    if request.same_trainset_demo_id:
        score += 2

    if request.same_station_demo_id:
        score += 1

    if request.same_platform_demo_id:
        score += 2

    return score


def _result(
    request: MvpSolidarySyncOptionRequest,
    policy: MvpSyncPolicy,
    status: MvpSyncStatus,
    benefit_instruction_kind: BenefitInstructionKind,
    opens_bonus_evaluation_window: bool,
    blocks_solidary_bonus_flow: bool,
    requires_audit_review: bool,
    window_minutes: int,
    window_matched: bool,
    hard_risk_flags: List[str],
    audit_flags: List[str],
    reason: str,
) -> MvpSolidarySyncOptionResult:
    final_discount = _final_demo_discount_bps(request, policy)

    return MvpSolidarySyncOptionResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=MODULE_VERSION,
        demo_mode=DEMO_MODE,
        option=request.option,
        status=status,
        benefit_instruction_kind=benefit_instruction_kind,
        opens_bonus_evaluation_window=opens_bonus_evaluation_window,
        blocks_solidary_bonus_flow=blocks_solidary_bonus_flow,
        requires_audit_review=requires_audit_review,
        window_minutes=window_minutes,
        window_matched=window_matched,
        final_demo_discount_bps_if_eligible=final_discount if opens_bonus_evaluation_window else 0,
        bonus_extra_discount_bps_demo=policy.bonus_extra_discount_bps_demo,
        base_red_sube_discount_bps_demo=request.current_base_red_sube_discount_bps_demo,
        assisted_activation_actor=request.assisted_activation_actor,
        driver_console_optional_only=(
            request.assisted_activation_actor == AssistedActivationActor.DRIVER_CONSOLE_OPTIONAL
        ),
        hard_risk_flags=hard_risk_flags,
        audit_flags=audit_flags,
        reason=reason,
        security_summary=_security_summary(request, policy, window_minutes, window_matched),
        benefit_window_demo=(
            _benefit_window_demo(request, policy, benefit_instruction_kind)
            if opens_bonus_evaluation_window
            else None
        ),
        privacy_notice=_privacy_notice(),
        driver_burden_notice=_driver_burden_notice(),
        legal_scope_notice=_legal_scope_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def _benefit_window_demo(
    request: MvpSolidarySyncOptionRequest,
    policy: MvpSyncPolicy,
    benefit_instruction_kind: BenefitInstructionKind,
) -> Dict[str, Any]:
    starts_at = request.red_sube_context.sync_attempt_timestamp_utc
    expires_at = starts_at + timedelta(hours=policy.benefit_validity_hours)

    return {
        "instruction_kind": benefit_instruction_kind.value,
        "starts_at_utc": starts_at.isoformat(),
        "expires_at_utc": expires_at.isoformat(),
        "applies_to_next_eligible_trip_only": True,
        "non_transferable": True,
        "not_cash_redeemable": True,
        "bonus_extra_discount_bps_demo": policy.bonus_extra_discount_bps_demo,
        "max_total_discount_bps_demo": policy.max_total_discount_bps_demo,
        "direct_card_write_performed": False,
        "real_tariff_applied": False,
        "real_balance_modified": False,
    }


def _final_demo_discount_bps(
    request: MvpSolidarySyncOptionRequest,
    policy: MvpSyncPolicy,
) -> int:
    return min(
        request.current_base_red_sube_discount_bps_demo + policy.bonus_extra_discount_bps_demo,
        policy.max_total_discount_bps_demo,
    )


def _security_summary(
    request: MvpSolidarySyncOptionRequest,
    policy: MvpSyncPolicy,
    window_minutes: int,
    window_matched: bool,
) -> Dict[str, Any]:
    participant = request.participant_context
    context = request.red_sube_context

    return {
        "mvp_sync_event_demo_id": request.mvp_sync_event_demo_id,
        "option": request.option.value,
        "transport_mode": context.transport_mode.value,
        "validation_point_type": context.validation_point_type.value,
        "window_minutes": window_minutes,
        "window_matched": window_matched,
        "context_score": _context_score(request),
        "priority_attribute_active": participant.priority_user_has_active_attribute,
        "priority_need_previously_accredited": participant.priority_need_previously_accredited,
        "priority_paid_validation_confirmed": context.priority_paid_validation_confirmed,
        "collaborator_paid_validation_confirmed": context.collaborator_paid_validation_confirmed,
        "priority_has_mobile_device": participant.priority_has_mobile_device,
        "priority_mobile_has_nfc": participant.priority_mobile_has_nfc,
        "collaborator_has_mobile_device": participant.collaborator_has_mobile_device,
        "collaborator_has_physical_sube_card": participant.collaborator_has_physical_sube_card,
        "mobile_handshake_available": request.mobile_handshake_available,
        "nfc_card_tap_available": request.nfc_card_tap_available,
        "validator_second_tap_available": request.validator_second_tap_available,
        "assisted_activation_actor": request.assisted_activation_actor.value,
        "driver_console_must_not_be_mandatory": policy.driver_console_must_not_be_mandatory,
        "good_faith_social_recognition_declared": (
            request.good_faith_social_recognition_declared
        ),
        "good_faith_social_recognition_is_decisive": False,
        "same_network_demo_id": request.same_network_demo_id,
        "same_route_demo_id": request.same_route_demo_id,
        "same_service_window_demo_id": request.same_service_window_demo_id,
        "same_validator_or_turnstile_demo_id": request.same_validator_or_turnstile_demo_id,
        "same_vehicle_demo_id": request.same_vehicle_demo_id,
        "same_trainset_demo_id": request.same_trainset_demo_id,
        "same_station_demo_id": request.same_station_demo_id,
        "same_platform_demo_id": request.same_platform_demo_id,
        "max_events_per_priority_trip_demo": policy.max_events_per_priority_trip_demo,
        "max_events_per_collaborator_day_demo": (
            policy.max_events_per_collaborator_day_demo
        ),
    }


def _privacy_notice() -> str:
    return (
        "Las opciones MVP no revelan DNI, nombre, domicilio, diagnóstico, CUD, "
        "historia clínica, certificado médico, teléfono, email, IMEI, MAC, saldo "
        "ni GPS exacto. Sólo utilizan tokens demo y contexto de validación."
    )


def _driver_burden_notice() -> str:
    return (
        "El chofer no está obligado a activar el Bono Solidario, no decide el beneficio, "
        "no verifica condiciones personales, no administra sanciones y no debe recibir "
        "una carga operativa nueva. La opción por consola se modela sólo como alternativa "
        "piloto, opcional, configurable o sustituible por sistema, validadora, terminal "
        "u operador."
    )


def _legal_scope_notice() -> str:
    return (
        "El Bono Solidario MVP es conceptual. No aplica descuento real, no modifica saldo, "
        "no escribe tarjetas reales y no integra Red SUBE real. El +50% es una regla demo "
        "para próximo viaje elegible, sujeta a futura autorización, normativa, auditoría "
        "e integración oficial."
    )


def _common_warnings() -> List[str]:
    return [
        "Opciones MVP conceptuales y demostrativas.",
        "Sin implementación oficial vigente.",
        "Sin integración real con SUBE.",
        "Sin integración real con Red SUBE.",
        "Sin consulta a tarjetas reales.",
        "Sin consulta a cuentas reales.",
        "Sin consulta a validadoras reales.",
        "Sin consulta a molinetes reales.",
        "Sin saldo real.",
        "Sin tarifa real.",
        "Sin escritura real sobre chip SUBE.",
        "Sin DNI.",
        "Sin diagnóstico médico.",
        "Sin CUD visible.",
        "Sin teléfono real.",
        "Sin email real.",
        "Sin IMEI real.",
        "Sin MAC real.",
        "Sin GPS exacto.",
        "Sin vigilancia.",
        "Sin ranking.",
        "Sin sanciones.",
        "Sin obligación de tener celular.",
        "La sincronización entre celulares es sólo una opción.",
        "El NFC teléfono-tarjeta es sólo una opción.",
        "La validadora asistida es sólo una opción piloto auditable.",
        "La buena fe social puede registrarse, pero no decide por sí sola.",
        "El chofer no debe cargar con una obligación nueva.",
        "El +50% demo sólo abre una hipótesis de próximo viaje elegible.",
        "El resultado debe combinarse con matcher temporal, handoff, antifraude y política demo de descuento.",
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
        "premio",
        "puntos",
        "bono solidario",
        "red sube",
        "gps",
        "telefono",
        "teléfono",
        "email",
        "saldo",
        "dinero",
    }

    return any(term in normalized for term in suspicious_terms) or len(normalized.split()) > 1


def _positive(field_name: str, value: int) -> None:
    if value <= 0:
        raise ValueError(f"El campo {field_name} debe ser mayor a cero.")


def _validate_required_values(required_values: Dict[str, str]) -> None:
    for field_name, value in required_values.items():
        if not value or not value.strip():
            raise ValueError(f"El campo demostrativo {field_name} no puede estar vacío.")


def _strip_optional(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None

    stripped = value.strip()
    return stripped if stripped else None


def _deduplicate(flags: List[str]) -> List[str]:
    seen = set()
    result = []

    for flag in flags:
        if flag not in seen:
            seen.add(flag)
            result.append(flag)

    return result


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    import json

    print(json.dumps(run_mobile_to_mobile_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_priority_phone_nfc_card_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_validator_assisted_card_tap_demo(), indent=2, ensure_ascii=False))
