"""
SUBE Prioridad — Flujo MVP de acumulación del Bono Solidario.

Este módulo toma una opción MVP de sincronización previamente evaluada y,
si corresponde, crea una instrucción demo de Bono Solidario para el próximo
viaje elegible del colaborador.

Este archivo une conceptualmente:

    1. Opción MVP de sincronización.
    2. Ventana temporal abierta por Red SUBE demo.
    3. Confirmación del usuario SUBE Prioridad.
    4. Asiento de uso general.
    5. Antifraude mínimo.
    6. Bono Solidario demo +50%.
    7. Próximo viaje elegible del colaborador.

Regla central:
    El Bono Solidario MVP no se aplica en el viaje actual.
    Se genera como instrucción demo para el próximo viaje elegible,
    dentro de una ventana temporal determinada.

Importante:
    No integra SUBE real.
    No integra Red SUBE real.
    No modifica saldo real.
    No aplica tarifa real.
    No escribe tarjetas reales.
    No consulta validadores reales.
    No consulta molinetes reales.
    No consulta cuentas reales.
    No usa DNI.
    No usa nombre.
    No usa diagnóstico.
    No usa CUD visible.
    No usa GPS exacto.
    No genera ranking.
    No genera sanciones.
    No impone carga al chofer.

El +50% es conceptual:
    Se suma al descuento base demo tipo Red SUBE,
    con tope configurable,
    sólo para el próximo viaje elegible,
    no transferible,
    no convertible en dinero,
    no reclamable unilateralmente por el colaborador.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from solidary_bonus_mvp_sync_options import (
    AssistedActivationActor,
    BenefitInstructionKind,
    MvpSolidarySyncOptionRequest,
    MvpSolidarySyncOptionResult,
    MvpSyncOption,
    MvpSyncStatus,
    evaluate_mvp_solidary_sync_option,
)


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Flujo MVP de Acumulación de Bono Solidario"
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
    "ranking",
    "sancion",
    "sanción",
}


class BonusAccrualStatus(str, Enum):
    CREATED = "created"
    CREATED_WITH_AUDIT = "created_with_audit"
    NEEDS_REVIEW = "needs_review"
    REJECTED = "rejected"


class BonusAccrualSource(str, Enum):
    MOBILE_TO_MOBILE = "mobile_to_mobile"
    PRIORITY_PHONE_NFC_CARD = "priority_phone_nfc_card"
    VALIDATOR_ASSISTED_CARD_TAP = "validator_assisted_card_tap"


class NextTripEligibilityStatus(str, Enum):
    PENDING_NEXT_ELIGIBLE_TRIP = "pending_next_eligible_trip"
    NOT_ELIGIBLE = "not_eligible"
    NEEDS_REVIEW = "needs_review"


class BonusInstructionMode(str, Enum):
    ACCOUNT_PENDING_DEMO = "account_pending_demo"
    CARD_TOKEN_PENDING_DEMO = "card_token_pending_demo"
    VALIDATOR_PENDING_DEMO = "validator_pending_demo"
    NONE = "none"


@dataclass(frozen=True)
class BonusAccrualPolicy:
    """
    Política demo de acumulación.

    benefit_validity_hours:
        Cantidad de horas en las que el colaborador puede usar el Bono Solidario
        en su próximo viaje elegible.

    bonus_extra_discount_bps_demo:
        +50% demo = 5000 basis points.

    max_total_discount_bps_demo:
        Tope conceptual del beneficio acumulado.

    require_mvp_sync_ready:
        Exige que la opción MVP haya sido aceptada.

    require_next_trip_only:
        Evita que se multiplique indefinidamente.

    require_non_transferable:
        Evita cesión, venta o reclamo por terceros.
    """

    benefit_validity_hours: int
    bonus_extra_discount_bps_demo: int
    max_total_discount_bps_demo: int
    require_mvp_sync_ready: bool
    require_next_trip_only: bool
    require_non_transferable: bool
    require_not_cash_redeemable: bool
    require_no_real_balance_change: bool
    max_bonus_events_per_priority_trip_demo: int
    max_bonus_events_per_collaborator_day_demo: int


@dataclass(frozen=True)
class BonusAccrualLedger:
    """
    Registro demo antifraude.

    No contiene identidad civil.
    No contiene datos médicos.
    No contiene saldo real.
    """

    priority_trip_event_count_demo: int = 0
    collaborator_day_event_count_demo: int = 0
    replay_event_ids: Optional[List[str]] = None


@dataclass(frozen=True)
class SolidaryBonusAccrualRequest:
    """
    Solicitud demo de acumulación.

    Puede venir de cualquiera de las tres opciones MVP:
        - celular a celular;
        - celular NFC del usuario prioritario a tarjeta del colaborador;
        - validadora asistida con segunda aproximación de tarjeta.
    """

    accrual_event_demo_id: str
    mvp_sync_request: MvpSolidarySyncOptionRequest
    mvp_sync_result: Optional[MvpSolidarySyncOptionResult]
    collaborator_account_demo_token: str
    collaborator_sube_card_token: str
    collaborator_payment_method_demo_token: str
    next_trip_window_starts_at_utc: datetime
    next_trip_window_expires_at_utc: datetime
    base_red_sube_discount_bps_demo: int
    previous_bonus_already_used: bool
    collaborator_claims_unilaterally: bool
    priority_user_final_confirmation: bool
    next_trip_only: bool
    non_transferable: bool
    not_cash_redeemable: bool
    real_balance_change_requested: bool
    real_tariff_application_requested: bool


@dataclass(frozen=True)
class SolidaryBonusAccrualInstruction:
    """
    Instrucción demo generada.

    No es una orden real a SUBE.
    No es una orden real a Red SUBE.
    No modifica saldo.
    No aplica tarifa.
    """

    instruction_demo_id: str
    instruction_mode: BonusInstructionMode
    accrual_source: BonusAccrualSource
    collaborator_account_demo_token: str
    collaborator_sube_card_token: str
    collaborator_payment_method_demo_token: str
    next_trip_window_starts_at_utc: str
    next_trip_window_expires_at_utc: str
    applies_to_next_eligible_trip_only: bool
    non_transferable: bool
    not_cash_redeemable: bool
    real_balance_modified: bool
    real_tariff_applied: bool
    base_red_sube_discount_bps_demo: int
    bonus_extra_discount_bps_demo: int
    final_demo_discount_bps_if_eligible: int


@dataclass(frozen=True)
class SolidaryBonusAccrualResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: BonusAccrualStatus
    next_trip_eligibility_status: NextTripEligibilityStatus
    instruction_created: bool
    instruction: Optional[SolidaryBonusAccrualInstruction]
    accrual_source: BonusAccrualSource
    selected_mvp_option: str
    bonus_extra_discount_bps_demo: int
    base_red_sube_discount_bps_demo: int
    final_demo_discount_bps_if_eligible: int
    benefit_validity_hours: int
    blocks_solidary_bonus_flow: bool
    requires_audit_review: bool
    hard_risk_flags: List[str]
    audit_flags: List[str]
    reason: str
    security_summary: Dict[str, Any]
    privacy_notice: str
    legal_scope_notice: str
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


def create_demo_bonus_accrual_policy(
    benefit_validity_hours: int = 24,
    bonus_extra_discount_bps_demo: int = FIFTY_PERCENT_BPS,
    max_total_discount_bps_demo: int = FULL_DISCOUNT_BPS,
    require_mvp_sync_ready: bool = True,
    require_next_trip_only: bool = True,
    require_non_transferable: bool = True,
    require_not_cash_redeemable: bool = True,
    require_no_real_balance_change: bool = True,
    max_bonus_events_per_priority_trip_demo: int = 1,
    max_bonus_events_per_collaborator_day_demo: int = 3,
) -> BonusAccrualPolicy:
    _positive("benefit_validity_hours", benefit_validity_hours)
    _positive("bonus_extra_discount_bps_demo", bonus_extra_discount_bps_demo)
    _positive("max_total_discount_bps_demo", max_total_discount_bps_demo)
    _positive("max_bonus_events_per_priority_trip_demo", max_bonus_events_per_priority_trip_demo)
    _positive("max_bonus_events_per_collaborator_day_demo", max_bonus_events_per_collaborator_day_demo)

    if bonus_extra_discount_bps_demo > FULL_DISCOUNT_BPS:
        raise ValueError("El adicional demo no puede superar el 100%.")

    if max_total_discount_bps_demo > FULL_DISCOUNT_BPS:
        raise ValueError("El tope total demo no puede superar el 100%.")

    return BonusAccrualPolicy(
        benefit_validity_hours=benefit_validity_hours,
        bonus_extra_discount_bps_demo=bonus_extra_discount_bps_demo,
        max_total_discount_bps_demo=max_total_discount_bps_demo,
        require_mvp_sync_ready=require_mvp_sync_ready,
        require_next_trip_only=require_next_trip_only,
        require_non_transferable=require_non_transferable,
        require_not_cash_redeemable=require_not_cash_redeemable,
        require_no_real_balance_change=require_no_real_balance_change,
        max_bonus_events_per_priority_trip_demo=max_bonus_events_per_priority_trip_demo,
        max_bonus_events_per_collaborator_day_demo=max_bonus_events_per_collaborator_day_demo,
    )


def create_demo_bonus_accrual_ledger(
    priority_trip_event_count_demo: int = 0,
    collaborator_day_event_count_demo: int = 0,
    replay_event_ids: Optional[List[str]] = None,
) -> BonusAccrualLedger:
    if priority_trip_event_count_demo < 0:
        raise ValueError("El contador demo del viaje prioritario no puede ser negativo.")

    if collaborator_day_event_count_demo < 0:
        raise ValueError("El contador demo diario del colaborador no puede ser negativo.")

    return BonusAccrualLedger(
        priority_trip_event_count_demo=priority_trip_event_count_demo,
        collaborator_day_event_count_demo=collaborator_day_event_count_demo,
        replay_event_ids=replay_event_ids or [],
    )


def create_demo_solidary_bonus_accrual_request(
    accrual_event_demo_id: str = "demo-bonus-accrual-001",
    mvp_sync_request: Optional[MvpSolidarySyncOptionRequest] = None,
    mvp_sync_result: Optional[MvpSolidarySyncOptionResult] = None,
    collaborator_account_demo_token: str = "demo-collaborator-account-001",
    collaborator_sube_card_token: str = "demo-collaborator-sube-card-001",
    collaborator_payment_method_demo_token: str = "demo-collaborator-payment-001",
    next_trip_window_starts_at_utc: Optional[datetime] = None,
    next_trip_window_expires_at_utc: Optional[datetime] = None,
    base_red_sube_discount_bps_demo: int = FIFTY_PERCENT_BPS,
    previous_bonus_already_used: bool = False,
    collaborator_claims_unilaterally: bool = False,
    priority_user_final_confirmation: bool = True,
    next_trip_only: bool = True,
    non_transferable: bool = True,
    not_cash_redeemable: bool = True,
    real_balance_change_requested: bool = False,
    real_tariff_application_requested: bool = False,
) -> SolidaryBonusAccrualRequest:
    required_values = {
        "accrual_event_demo_id": accrual_event_demo_id,
        "collaborator_account_demo_token": collaborator_account_demo_token,
        "collaborator_sube_card_token": collaborator_sube_card_token,
        "collaborator_payment_method_demo_token": collaborator_payment_method_demo_token,
    }

    _validate_required_values(required_values)
    assert_no_prohibited_fields(required_values)

    if base_red_sube_discount_bps_demo < 0:
        raise ValueError("El descuento base demo no puede ser negativo.")

    if base_red_sube_discount_bps_demo > FULL_DISCOUNT_BPS:
        raise ValueError("El descuento base demo no puede superar el 100%.")

    sync_request = mvp_sync_request or _default_mvp_sync_request()
    sync_result = mvp_sync_result or evaluate_mvp_solidary_sync_option(sync_request)

    starts_at = next_trip_window_starts_at_utc or sync_request.red_sube_context.sync_attempt_timestamp_utc
    expires_at = next_trip_window_expires_at_utc or starts_at + timedelta(hours=24)

    if expires_at <= starts_at:
        raise ValueError("La ventana de próximo viaje debe vencer después de su inicio.")

    return SolidaryBonusAccrualRequest(
        accrual_event_demo_id=accrual_event_demo_id.strip(),
        mvp_sync_request=sync_request,
        mvp_sync_result=sync_result,
        collaborator_account_demo_token=collaborator_account_demo_token.strip(),
        collaborator_sube_card_token=collaborator_sube_card_token.strip(),
        collaborator_payment_method_demo_token=collaborator_payment_method_demo_token.strip(),
        next_trip_window_starts_at_utc=starts_at,
        next_trip_window_expires_at_utc=expires_at,
        base_red_sube_discount_bps_demo=base_red_sube_discount_bps_demo,
        previous_bonus_already_used=previous_bonus_already_used,
        collaborator_claims_unilaterally=collaborator_claims_unilaterally,
        priority_user_final_confirmation=priority_user_final_confirmation,
        next_trip_only=next_trip_only,
        non_transferable=non_transferable,
        not_cash_redeemable=not_cash_redeemable,
        real_balance_change_requested=real_balance_change_requested,
        real_tariff_application_requested=real_tariff_application_requested,
    )


def evaluate_solidary_bonus_mvp_accrual(
    request: SolidaryBonusAccrualRequest,
    policy: Optional[BonusAccrualPolicy] = None,
    ledger: Optional[BonusAccrualLedger] = None,
) -> SolidaryBonusAccrualResult:
    """
    Evalúa si corresponde crear la instrucción demo de Bono Solidario.

    Este paso no aplica el beneficio.
    Sólo deja una instrucción pendiente para el próximo viaje elegible.
    """
    policy = policy or create_demo_bonus_accrual_policy()
    ledger = ledger if ledger is not None else create_demo_bonus_accrual_ledger()

    assert_no_prohibited_fields(
        {
            "accrual_event_demo_id": request.accrual_event_demo_id,
            "collaborator_account_demo_token": request.collaborator_account_demo_token,
            "collaborator_sube_card_token": request.collaborator_sube_card_token,
            "collaborator_payment_method_demo_token": request.collaborator_payment_method_demo_token,
        }
    )

    hard_risk_flags = _hard_risk_flags(request, policy, ledger)
    audit_flags = _audit_flags(request, policy, ledger)
    accrual_source = _accrual_source(request)

    if hard_risk_flags:
        return _result(
            request=request,
            policy=policy,
            ledger=ledger,
            status=BonusAccrualStatus.REJECTED,
            next_trip_eligibility_status=NextTripEligibilityStatus.NOT_ELIGIBLE,
            instruction=None,
            accrual_source=accrual_source,
            blocks_solidary_bonus_flow=True,
            requires_audit_review=True,
            hard_risk_flags=hard_risk_flags,
            audit_flags=audit_flags,
            reason=(
                "No se creó instrucción demo de Bono Solidario porque existen "
                "riesgos duros o faltan condiciones mínimas."
            ),
        )

    instruction = _create_instruction(request, policy, accrual_source)

    status = (
        BonusAccrualStatus.CREATED_WITH_AUDIT
        if audit_flags
        else BonusAccrualStatus.CREATED
    )

    return _result(
        request=request,
        policy=policy,
        ledger=ledger,
        status=status,
        next_trip_eligibility_status=NextTripEligibilityStatus.PENDING_NEXT_ELIGIBLE_TRIP,
        instruction=instruction,
        accrual_source=accrual_source,
        blocks_solidary_bonus_flow=False,
        requires_audit_review=bool(audit_flags),
        hard_risk_flags=[],
        audit_flags=audit_flags,
        reason=(
            "Se creó una instrucción demo de Bono Solidario para el próximo viaje "
            "elegible del colaborador."
        ),
    )


def result_to_dict(result: SolidaryBonusAccrualResult) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "next_trip_eligibility_status": result.next_trip_eligibility_status.value,
        "instruction_created": result.instruction_created,
        "instruction": (
            _instruction_to_dict(result.instruction)
            if result.instruction is not None
            else None
        ),
        "accrual_source": result.accrual_source.value,
        "selected_mvp_option": result.selected_mvp_option,
        "bonus_extra_discount_bps_demo": result.bonus_extra_discount_bps_demo,
        "base_red_sube_discount_bps_demo": result.base_red_sube_discount_bps_demo,
        "final_demo_discount_bps_if_eligible": result.final_demo_discount_bps_if_eligible,
        "benefit_validity_hours": result.benefit_validity_hours,
        "blocks_solidary_bonus_flow": result.blocks_solidary_bonus_flow,
        "requires_audit_review": result.requires_audit_review,
        "hard_risk_flags": result.hard_risk_flags,
        "audit_flags": result.audit_flags,
        "reason": result.reason,
        "security_summary": result.security_summary,
        "privacy_notice": result.privacy_notice,
        "legal_scope_notice": result.legal_scope_notice,
        "driver_burden_notice": result.driver_burden_notice,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }


def run_demo() -> Dict[str, Any]:
    request = create_demo_solidary_bonus_accrual_request()

    result = evaluate_solidary_bonus_mvp_accrual(request)

    return result_to_dict(result)


def _hard_risk_flags(
    request: SolidaryBonusAccrualRequest,
    policy: BonusAccrualPolicy,
    ledger: BonusAccrualLedger,
) -> List[str]:
    flags: List[str] = []

    if _looks_like_free_text(request.accrual_event_demo_id):
        flags.append("accrual_event_id_looks_like_free_text")

    if _looks_like_free_text(request.collaborator_account_demo_token):
        flags.append("collaborator_account_token_looks_like_free_text")

    if _looks_like_free_text(request.collaborator_sube_card_token):
        flags.append("collaborator_sube_card_token_looks_like_free_text")

    if _looks_like_free_text(request.collaborator_payment_method_demo_token):
        flags.append("collaborator_payment_token_looks_like_free_text")

    if policy.require_mvp_sync_ready:
        if request.mvp_sync_result is None:
            flags.append("mvp_sync_result_required")

        elif request.mvp_sync_result.status not in {
            MvpSyncStatus.READY,
            MvpSyncStatus.READY_WITH_AUDIT,
        }:
            flags.append("mvp_sync_not_ready")

        elif request.mvp_sync_result.blocks_solidary_bonus_flow:
            flags.append("mvp_sync_blocks_solidary_bonus_flow")

    if request.previous_bonus_already_used:
        flags.append("previous_bonus_already_used")

    if request.collaborator_claims_unilaterally:
        flags.append("collaborator_unilateral_claim")

    if not request.priority_user_final_confirmation:
        flags.append("priority_user_final_confirmation_required")

    if policy.require_next_trip_only and not request.next_trip_only:
        flags.append("next_trip_only_required")

    if policy.require_non_transferable and not request.non_transferable:
        flags.append("non_transferable_required")

    if policy.require_not_cash_redeemable and not request.not_cash_redeemable:
        flags.append("not_cash_redeemable_required")

    if policy.require_no_real_balance_change and request.real_balance_change_requested:
        flags.append("real_balance_change_not_allowed_in_demo")

    if request.real_tariff_application_requested:
        flags.append("real_tariff_application_not_allowed_in_demo")

    if request.next_trip_window_expires_at_utc <= request.next_trip_window_starts_at_utc:
        flags.append("invalid_next_trip_window")

    if ledger.replay_event_ids and request.accrual_event_demo_id in ledger.replay_event_ids:
        flags.append("replay_accrual_event_id")

    if ledger.priority_trip_event_count_demo >= policy.max_bonus_events_per_priority_trip_demo:
        flags.append("priority_trip_bonus_limit_exceeded")

    if ledger.collaborator_day_event_count_demo >= policy.max_bonus_events_per_collaborator_day_demo:
        flags.append("collaborator_day_bonus_limit_exceeded")

    return _deduplicate(flags)


def _audit_flags(
    request: SolidaryBonusAccrualRequest,
    policy: BonusAccrualPolicy,
    ledger: BonusAccrualLedger,
) -> List[str]:
    flags: List[str] = []

    flags.append("bonus_accrual_audit")
    flags.append(f"source_{_accrual_source(request).value}")
    flags.append(f"mvp_option_{request.mvp_sync_request.option.value}")

    if request.mvp_sync_result and request.mvp_sync_result.requires_audit_review:
        flags.append("mvp_sync_requires_audit_review")

    if request.mvp_sync_request.assisted_activation_actor == AssistedActivationActor.DRIVER_CONSOLE_OPTIONAL:
        flags.append("driver_console_optional_only_audit")
        flags.append("no_driver_obligation_audit")

    if request.mvp_sync_request.option == MvpSyncOption.VALIDATOR_ASSISTED_CARD_TAP:
        flags.append("validator_assisted_bonus_accrual_audit")

    if request.mvp_sync_request.option == MvpSyncOption.PRIORITY_PHONE_NFC_TO_COLLABORATOR_CARD:
        flags.append("nfc_card_bonus_accrual_audit")

    if request.mvp_sync_request.option == MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT:
        flags.append("mobile_to_mobile_bonus_accrual_audit")

    if _final_demo_discount_bps(request, policy) == policy.max_total_discount_bps_demo:
        flags.append("discount_cap_applied_demo")

    if ledger.priority_trip_event_count_demo > 0:
        flags.append("priority_trip_has_existing_bonus_events_demo")

    if ledger.collaborator_day_event_count_demo > 0:
        flags.append("collaborator_day_has_existing_bonus_events_demo")

    return _deduplicate(flags)


def _create_instruction(
    request: SolidaryBonusAccrualRequest,
    policy: BonusAccrualPolicy,
    accrual_source: BonusAccrualSource,
) -> SolidaryBonusAccrualInstruction:
    return SolidaryBonusAccrualInstruction(
        instruction_demo_id=f"instruction-{request.accrual_event_demo_id}",
        instruction_mode=_instruction_mode(request),
        accrual_source=accrual_source,
        collaborator_account_demo_token=request.collaborator_account_demo_token,
        collaborator_sube_card_token=request.collaborator_sube_card_token,
        collaborator_payment_method_demo_token=request.collaborator_payment_method_demo_token,
        next_trip_window_starts_at_utc=request.next_trip_window_starts_at_utc.isoformat(),
        next_trip_window_expires_at_utc=request.next_trip_window_expires_at_utc.isoformat(),
        applies_to_next_eligible_trip_only=True,
        non_transferable=True,
        not_cash_redeemable=True,
        real_balance_modified=False,
        real_tariff_applied=False,
        base_red_sube_discount_bps_demo=request.base_red_sube_discount_bps_demo,
        bonus_extra_discount_bps_demo=policy.bonus_extra_discount_bps_demo,
        final_demo_discount_bps_if_eligible=_final_demo_discount_bps(request, policy),
    )


def _result(
    request: SolidaryBonusAccrualRequest,
    policy: BonusAccrualPolicy,
    ledger: BonusAccrualLedger,
    status: BonusAccrualStatus,
    next_trip_eligibility_status: NextTripEligibilityStatus,
    instruction: Optional[SolidaryBonusAccrualInstruction],
    accrual_source: BonusAccrualSource,
    blocks_solidary_bonus_flow: bool,
    requires_audit_review: bool,
    hard_risk_flags: List[str],
    audit_flags: List[str],
    reason: str,
) -> SolidaryBonusAccrualResult:
    return SolidaryBonusAccrualResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=MODULE_VERSION,
        demo_mode=DEMO_MODE,
        status=status,
        next_trip_eligibility_status=next_trip_eligibility_status,
        instruction_created=instruction is not None,
        instruction=instruction,
        accrual_source=accrual_source,
        selected_mvp_option=request.mvp_sync_request.option.value,
        bonus_extra_discount_bps_demo=policy.bonus_extra_discount_bps_demo,
        base_red_sube_discount_bps_demo=request.base_red_sube_discount_bps_demo,
        final_demo_discount_bps_if_eligible=(
            instruction.final_demo_discount_bps_if_eligible if instruction else 0
        ),
        benefit_validity_hours=policy.benefit_validity_hours,
        blocks_solidary_bonus_flow=blocks_solidary_bonus_flow,
        requires_audit_review=requires_audit_review,
        hard_risk_flags=hard_risk_flags,
        audit_flags=audit_flags,
        reason=reason,
        security_summary=_security_summary(request, policy, ledger),
        privacy_notice=_privacy_notice(),
        legal_scope_notice=_legal_scope_notice(),
        driver_burden_notice=_driver_burden_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )


def _security_summary(
    request: SolidaryBonusAccrualRequest,
    policy: BonusAccrualPolicy,
    ledger: BonusAccrualLedger,
) -> Dict[str, Any]:
    sync_result = request.mvp_sync_result

    return {
        "accrual_event_demo_id": request.accrual_event_demo_id,
        "mvp_sync_event_demo_id": request.mvp_sync_request.mvp_sync_event_demo_id,
        "selected_mvp_option": request.mvp_sync_request.option.value,
        "mvp_sync_status": sync_result.status.value if sync_result else None,
        "mvp_sync_blocks_flow": sync_result.blocks_solidary_bonus_flow if sync_result else None,
        "mvp_sync_requires_audit": sync_result.requires_audit_review if sync_result else None,
        "instruction_mode": _instruction_mode(request).value,
        "accrual_source": _accrual_source(request).value,
        "base_red_sube_discount_bps_demo": request.base_red_sube_discount_bps_demo,
        "bonus_extra_discount_bps_demo": policy.bonus_extra_discount_bps_demo,
        "max_total_discount_bps_demo": policy.max_total_discount_bps_demo,
        "final_demo_discount_bps_if_eligible": _final_demo_discount_bps(request, policy),
        "next_trip_window_starts_at_utc": request.next_trip_window_starts_at_utc.isoformat(),
        "next_trip_window_expires_at_utc": request.next_trip_window_expires_at_utc.isoformat(),
        "previous_bonus_already_used": request.previous_bonus_already_used,
        "priority_user_final_confirmation": request.priority_user_final_confirmation,
        "next_trip_only": request.next_trip_only,
        "non_transferable": request.non_transferable,
        "not_cash_redeemable": request.not_cash_redeemable,
        "real_balance_change_requested": request.real_balance_change_requested,
        "real_tariff_application_requested": request.real_tariff_application_requested,
        "priority_trip_event_count_demo": ledger.priority_trip_event_count_demo,
        "collaborator_day_event_count_demo": ledger.collaborator_day_event_count_demo,
        "max_bonus_events_per_priority_trip_demo": policy.max_bonus_events_per_priority_trip_demo,
        "max_bonus_events_per_collaborator_day_demo": policy.max_bonus_events_per_collaborator_day_demo,
    }


def _instruction_to_dict(
    instruction: SolidaryBonusAccrualInstruction,
) -> Dict[str, Any]:
    return {
        "instruction_demo_id": instruction.instruction_demo_id,
        "instruction_mode": instruction.instruction_mode.value,
        "accrual_source": instruction.accrual_source.value,
        "collaborator_account_demo_token": instruction.collaborator_account_demo_token,
        "collaborator_sube_card_token": instruction.collaborator_sube_card_token,
        "collaborator_payment_method_demo_token": instruction.collaborator_payment_method_demo_token,
        "next_trip_window_starts_at_utc": instruction.next_trip_window_starts_at_utc,
        "next_trip_window_expires_at_utc": instruction.next_trip_window_expires_at_utc,
        "applies_to_next_eligible_trip_only": instruction.applies_to_next_eligible_trip_only,
        "non_transferable": instruction.non_transferable,
        "not_cash_redeemable": instruction.not_cash_redeemable,
        "real_balance_modified": instruction.real_balance_modified,
        "real_tariff_applied": instruction.real_tariff_applied,
        "base_red_sube_discount_bps_demo": instruction.base_red_sube_discount_bps_demo,
        "bonus_extra_discount_bps_demo": instruction.bonus_extra_discount_bps_demo,
        "final_demo_discount_bps_if_eligible": instruction.final_demo_discount_bps_if_eligible,
    }


def _instruction_mode(request: SolidaryBonusAccrualRequest) -> BonusInstructionMode:
    if request.mvp_sync_result is None:
        return BonusInstructionMode.NONE

    if request.mvp_sync_result.benefit_instruction_kind == BenefitInstructionKind.NEXT_TRIP_DEMO_WINDOW:
        return BonusInstructionMode.ACCOUNT_PENDING_DEMO

    if request.mvp_sync_result.benefit_instruction_kind == BenefitInstructionKind.CARD_UPDATE_PENDING_DEMO:
        return BonusInstructionMode.CARD_TOKEN_PENDING_DEMO

    if request.mvp_sync_result.benefit_instruction_kind == BenefitInstructionKind.VALIDATOR_TAP_PENDING_DEMO:
        return BonusInstructionMode.VALIDATOR_PENDING_DEMO

    return BonusInstructionMode.NONE


def _accrual_source(request: SolidaryBonusAccrualRequest) -> BonusAccrualSource:
    if request.mvp_sync_request.option == MvpSyncOption.MOBILE_TO_MOBILE_REDSUBE_CONTEXT:
        return BonusAccrualSource.MOBILE_TO_MOBILE

    if request.mvp_sync_request.option == MvpSyncOption.PRIORITY_PHONE_NFC_TO_COLLABORATOR_CARD:
        return BonusAccrualSource.PRIORITY_PHONE_NFC_CARD

    if request.mvp_sync_request.option == MvpSyncOption.VALIDATOR_ASSISTED_CARD_TAP:
        return BonusAccrualSource.VALIDATOR_ASSISTED_CARD_TAP

    return BonusAccrualSource.MOBILE_TO_MOBILE


def _final_demo_discount_bps(
    request: SolidaryBonusAccrualRequest,
    policy: BonusAccrualPolicy,
) -> int:
    return min(
        request.base_red_sube_discount_bps_demo + policy.bonus_extra_discount_bps_demo,
        policy.max_total_discount_bps_demo,
    )


def _default_mvp_sync_request() -> MvpSolidarySyncOptionRequest:
    from solidary_bonus_mvp_sync_options import create_demo_mobile_to_mobile_request

    return create_demo_mobile_to_mobile_request()


def _privacy_notice() -> str:
    return (
        "El flujo de acumulación no revela DNI, nombre, domicilio, diagnóstico, CUD, "
        "historia clínica, certificado médico, teléfono, email, IMEI, MAC, saldo, "
        "dinero ni GPS exacto. Sólo utiliza tokens demo y contexto de validación."
    )


def _legal_scope_notice() -> str:
    return (
        "La instrucción de Bono Solidario es conceptual. No modifica saldo real, "
        "no aplica tarifa real, no escribe tarjetas reales y no integra Red SUBE real. "
        "Una implementación requeriría autorización, integración oficial, auditoría "
        "y normativa competente."
    )


def _driver_burden_notice() -> str:
    return (
        "El chofer no decide la acumulación del Bono Solidario, no verifica condiciones "
        "personales, no administra beneficios y no recibe una obligación nueva."
    )


def _common_warnings() -> List[str]:
    return [
        "Flujo MVP conceptual y demostrativo.",
        "Sin implementación oficial vigente.",
        "Sin integración real con SUBE.",
        "Sin integración real con Red SUBE.",
        "Sin consulta a cuentas reales.",
        "Sin consulta a tarjetas reales.",
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
        "El Bono Solidario demo se reserva para el próximo viaje elegible.",
        "El +50% demo es conceptual y acumulable sólo dentro de límites configurables.",
        "La instrucción no es transferible ni convertible en dinero.",
        "El colaborador no puede reclamar unilateralmente el bono.",
        "El chofer no debe cargar con una obligación nueva.",
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

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
