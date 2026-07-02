"""
SUBE Prioridad — Política demostrativa de descuentos Red SUBE y Bono Solidario.
Este módulo modela una regla económica conceptual para pruebas piloto, MVP o
futuras evaluaciones técnicas del Bono Solidario.

No representa implementación oficial.
No integra SUBE real. No integra Red SUBE real.
No modifica tarifas reales. No acredita saldo real. No acredita dinero.
No transfiere beneficios reales. No consulta cuentas reales.
No consulta tarjetas reales. No procesa DNI ni diagnósticos médicos.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Política Demo Red SUBE y Bono Solidario"
POLICY_VERSION = "0.1.0"
DEMO_MODE = True
PERCENT_SCALE = 10_000

ZERO_PERCENT_BPS = 0
FIFTY_PERCENT_BPS = 5_000
SEVENTY_FIVE_PERCENT_BPS = 7_500
ONE_HUNDRED_PERCENT_BPS = 10_000
REGIONAL_TOP_DISCOUNT_BPS = 8_500

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

class DiscountPolicyStatus(str, Enum):
    ELIGIBLE = "eligible"
    REJECTED = "rejected"
    NEEDS_REVIEW = "needs_review"

class SeatType(str, Enum):
    GENERAL_USE = "general_use"
    LEGAL_PRIORITY = "legal_priority"

class BonusUseMode(str, Enum):
    NEXT_TRIP_ONLY = "next_trip_only"
    SAME_WINDOW_NEXT_TRIP = "same_window_next_trip"

@dataclass(frozen=True)
class RedSubeDemoPolicy:
    """Política demostrativa inspirada en atributos generales de Red SUBE."""
    window_hours_demo: int
    max_combinations_demo: int
    second_trip_discount_bps_demo: int
    third_to_fifth_trip_discount_bps_demo: int
    solidary_bonus_extra_discount_bps_demo: int
    max_total_discount_bps_demo: int
    bonus_use_mode: BonusUseMode
    single_use: bool
    non_transferable: bool
    not_cash_redeemable: bool

@dataclass(frozen=True)
class SolidaryBonusEligibilityContext:
    """Contexto mínimo para evaluar si puede calcularse el bono sin identidad civil."""
    collaborator_token: str
    priority_user_token: str
    priority_attribute_active: bool
    previously_accredited_need: bool
    priority_user_confirmed: bool
    security_flow_accepted: bool
    same_transport_context_matched: bool
    validation_window_matched: bool
    voluntary_seat_yield: bool
    seat_type: SeatType
    bonus_already_used: bool
    is_regional_edge_batch: bool = False

@dataclass(frozen=True)
class RedSubeTripCombination:
    """Viaje demostrativo del colaborador dentro de la ventana."""
    combination_number_demo: int
    validation_paid: bool
    validation_timestamp_utc: datetime
    first_trip_timestamp_utc: datetime
    next_trip_is_eligible: bool

@dataclass(frozen=True)
class SolidaryBonusDiscountQuote:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: DiscountPolicyStatus
    base_red_sube_discount_bps_demo: int
    solidary_bonus_extra_discount_bps_demo: int
    final_discount_bps_demo: int
    final_discount_percent_demo: float
    applied_to_next_trip: bool
    single_use: bool
    risk_flags: List[str]
    reason: str
    policy_summary: str
    regulatory_reference_notice: str
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

def create_demo_red_sube_policy(
    window_hours_demo: int = 2,
    max_combinations_demo: int = 5,
    second_trip_discount_bps_demo: int = FIFTY_PERCENT_BPS,
    third_to_fifth_trip_discount_bps_demo: int = SEVENTY_FIVE_PERCENT_BPS,
    solidary_bonus_extra_discount_bps_demo: int = FIFTY_PERCENT_BPS,
    max_total_discount_bps_demo: int = ONE_HUNDRED_PERCENT_BPS,
    bonus_use_mode: BonusUseMode = BonusUseMode.NEXT_TRIP_ONLY,
    single_use: bool = True,
    non_transferable: bool = True,
    not_cash_redeemable: bool = True,
) -> RedSubeDemoPolicy:
    if window_hours_demo <= 0:
        raise ValueError("La ventana demostrativa debe ser mayor a cero horas.")
    if max_combinations_demo <= 0:
        raise ValueError("La cantidad máxima de combinaciones debe ser mayor a cero.")
    
    for field_name, value in {
        "second_trip_discount_bps_demo": second_trip_discount_bps_demo,
        "third_to_fifth_trip_discount_bps_demo": third_to_fifth_trip_discount_bps_demo,
        "solidary_bonus_extra_discount_bps_demo": solidary_bonus_extra_discount_bps_demo,
        "max_total_discount_bps_demo": max_total_discount_bps_demo,
    }.items():
        _validate_bps(field_name, value)
        
    return RedSubeDemoPolicy(
        window_hours_demo=window_hours_demo,
        max_combinations_demo=max_combinations_demo,
        second_trip_discount_bps_demo=second_trip_discount_bps_demo,
        third_to_fifth_trip_discount_bps_demo=third_to_fifth_trip_discount_bps_demo,
        solidary_bonus_extra_discount_bps_demo=solidary_bonus_extra_discount_bps_demo,
        max_total_discount_bps_demo=max_total_discount_bps_demo,
        bonus_use_mode=bonus_use_mode,
        single_use=single_use,
        non_transferable=non_transferable,
        not_cash_redeemable=not_cash_redeemable,
    )
def create_demo_solidary_bonus_eligibility_context(
    collaborator_token: str = "demo-collaborator-001",
    priority_user_token: str = "demo-priority-user-001",
    priority_attribute_active: bool = True,
    previously_accredited_need: bool = True,
    priority_user_confirmed: bool = True,
    security_flow_accepted: bool = True,
    same_transport_context_matched: bool = True,
    validation_window_matched: bool = True,
    voluntary_seat_yield: bool = True,
    seat_type: SeatType = SeatType.GENERAL_USE,
    bonus_already_used: bool = False,
) -> SolidaryBonusEligibilityContext:
    if not collaborator_token or not collaborator_token.strip():
        raise ValueError("El token demostrativo del colaborador no puede estar vacío.")
    if not priority_user_token or not priority_user_token.strip():
        raise ValueError("El token demostrativo del usuario SUBE Prioridad no puede estar vacío.")
    
    assert_no_prohibited_fields({
        "collaborator_token": collaborator_token,
        "priority_user_token": priority_user_token,
    })
    return SolidaryBonusEligibilityContext(
        collaborator_token=collaborator_token.strip(),
        priority_user_token=priority_user_token.strip(),
        priority_attribute_active=priority_attribute_active,
        previously_accredited_need=previously_accredited_need,
        priority_user_confirmed=priority_user_confirmed,
        security_flow_accepted=security_flow_accepted,
        same_transport_context_matched=same_transport_context_matched,
        validation_window_matched=validation_window_matched,
        voluntary_seat_yield=voluntary_seat_yield,
        seat_type=seat_type,
        bonus_already_used=bonus_already_used,
    )

def create_demo_red_sube_trip_combination(
    combination_number_demo: int = 2,
    validation_paid: bool = True,
    validation_timestamp_utc: Optional[datetime] = None,
    first_trip_timestamp_utc: Optional[datetime] = None,
    next_trip_is_eligible: bool = True,
) -> RedSubeTripCombination:
    if combination_number_demo <= 0:
        raise ValueError("El número de combinación demostrativa debe ser mayor a cero.")
    now = validation_timestamp_utc or datetime.now(timezone.utc)
    return RedSubeTripCombination(
        combination_number_demo=combination_number_demo,
        validation_paid=validation_paid,
        validation_timestamp_utc=now,
        first_trip_timestamp_utc=first_trip_timestamp_utc or now,
        next_trip_is_eligible=next_trip_is_eligible,
    )

def calculate_base_red_sube_discount_bps_demo(
    policy: RedSubeDemoPolicy,
    trip: RedSubeTripCombination,
) -> int:
    if trip.combination_number_demo <= 1:
        return ZERO_PERCENT_BPS
    if trip.combination_number_demo == 2:
        return policy.second_trip_discount_bps_demo
    if 3 <= trip.combination_number_demo <= policy.max_combinations_demo:
        return policy.third_to_fifth_trip_discount_bps_demo
    return ZERO_PERCENT_BPS

def calculate_solidary_bonus_discount_quote(
    policy: RedSubeDemoPolicy,
    eligibility_context: SolidaryBonusEligibilityContext,
    trip: RedSubeTripCombination,
) -> SolidaryBonusDiscountQuote:
    assert_no_prohibited_fields({
        "collaborator_token": eligibility_context.collaborator_token,
        "priority_user_token": eligibility_context.priority_user_token,
    })
    
    risk_flags = _risk_flags(policy, eligibility_context, trip)
    base_discount_bps = calculate_base_red_sube_discount_bps_demo(policy, trip)
    
    if risk_flags:
        status = DiscountPolicyStatus.NEEDS_REVIEW if _review_only(risk_flags) else DiscountPolicyStatus.REJECTED
        return SolidaryBonusDiscountQuote(
            project=PROJECT_NAME,
            module=MODULE_NAME,
            version=POLICY_VERSION,
            demo_mode=DEMO_MODE,
            status=status,
            base_red_sube_discount_bps_demo=base_discount_bps,
            solidary_bonus_extra_discount_bps_demo=ZERO_PERCENT_BPS,
            final_discount_bps_demo=base_discount_bps,
            final_discount_percent_demo=_bps_to_percent(base_discount_bps),
            applied_to_next_trip=False,
            single_use=policy.single_use,
            risk_flags=risk_flags,
            reason="No se aplica Bono Solidario demo porque la solicitud no supera las reglas.",
            policy_summary=_policy_summary(policy),
            regulatory_reference_notice=_regulatory_reference_notice(),
            privacy_notice=_privacy_notice(),
            driver_burden=_driver_burden_notice(),
            warnings=_common_warnings(),
            timestamp_utc=_now_utc(),
        )
        
    maximo_tope_permitido = REGIONAL_TOP_DISCOUNT_BPS if eligibility_context.is_regional_edge_batch else policy.max_total_discount_bps_demo
    final_discount_bps = min(base_discount_bps + policy.solidary_bonus_extra_discount_bps_demo, maximo_tope_permitido)
    
    return SolidaryBonusDiscountQuote(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=POLICY_VERSION,
        demo_mode=DEMO_MODE,
        status=DiscountPolicyStatus.ELIGIBLE,
        base_red_sube_discount_bps_demo=base_discount_bps,
        solidary_bonus_extra_discount_bps_demo=policy.solidary_bonus_extra_discount_bps_demo,
        final_discount_bps_demo=final_discount_bps,
        final_discount_percent_demo=_bps_to_percent(final_discount_bps),
        applied_to_next_trip=True,
        single_use=policy.single_use,
        risk_flags=[],
        reason="Bono Solidario demo elegible: se suma un 50% adicional conceptual.",
        policy_summary=_policy_summary(policy),
        regulatory_reference_notice=_regulatory_reference_notice(),
        privacy_notice=_privacy_notice(),
        driver_burden=_driver_burden_notice(),
        warnings=_common_warnings(),
        timestamp_utc=_now_utc(),
    )

def result_to_dict(result: SolidaryBonusDiscountQuote) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "base_red_sube_discount_bps_demo": result.base_red_sube_discount_bps_demo,
        "solidary_bonus_extra_discount_bps_demo": result.solidary_bonus_extra_discount_bps_demo,
        "final_discount_bps_demo": result.final_discount_bps_demo,
        "final_discount_percent_demo": result.final_discount_percent_demo,
        "applied_to_next_trip": result.applied_to_next_trip,
        "single_use": result.single_use,
        "risk_flags": result.risk_flags,
        "reason": result.reason,
        "policy_summary": result.policy_summary,
        "regulatory_reference_notice": result.regulatory_reference_notice,
        "privacy_notice": result.privacy_notice,
        "driver_burden": result.driver_burden,
        "warnings": result.warnings,
        "timestamp_utc": result.timestamp_utc,
    }

def run_demo() -> Dict[str, Any]:
    policy = create_demo_red_sube_policy()
    eligibility_context = create_demo_solidary_bonus_eligibility_context()
    trip = create_demo_red_sube_trip_combination(combination_number_demo=2, validation_paid=True, next_trip_is_eligible=True)
    result = calculate_solidary_bonus_discount_quote(policy=policy, eligibility_context=eligibility_context, trip=trip)
    return result_to_dict(result)

def _risk_flags(policy: RedSubeDemoPolicy, eligibility_context: SolidaryBonusEligibilityContext, trip: RedSubeTripCombination) -> List[str]:
    flags: List[str] = []
    if policy.window_hours_demo <= 0 or policy.max_combinations_demo <= 0:
        flags.append("invalid_policy_configuration")
    if not policy.single_use or not policy.non_transferable or not policy.not_cash_redeemable:
        flags.append("invalid_policy_guardrails")
    if not trip.validation_paid:
        flags.append("validation_payment_not_confirmed")
    if not trip.next_trip_is_eligible:
        flags.append("next_trip_not_eligible")
    if trip.combination_number_demo > policy.max_combinations_demo:
        flags.append("combination_limit_exceeded")
    if not _within_policy_window(policy, trip):
        flags.append("red_sube_demo_window_expired")
    if not eligibility_context.priority_attribute_active or not eligibility_context.previously_accredited_need:
        flags.append("priority_attribute_inactive")
    if not eligibility_context.priority_user_confirmed or not eligibility_context.security_flow_accepted:
        flags.append("confirmation_or_security_flow_missing")
    if not eligibility_context.same_transport_context_matched or not eligibility_context.validation_window_matched:
        flags.append("context_or_window_mismatch")
    if not eligibility_context.voluntary_seat_yield or eligibility_context.seat_type != SeatType.GENERAL_USE:
        flags.append("seat_type_not_eligible")
    if eligibility_context.bonus_already_used:
        flags.append("solidary_bonus_already_used")
    if eligibility_context.collaborator_token == eligibility_context.priority_user_token:
        flags.append("self_bonus_attempt")
    if _looks_like_free_text(eligibility_context.collaborator_token) or _looks_like_free_text(eligibility_context.priority_user_token):
        flags.append("token_contains_suspicious_free_text")
    return flags

def _review_only(risk_flags: List[str]) -> bool:
    return bool(risk_flags) and set(risk_flags).issubset({"combination_limit_exceeded", "red_sube_demo_window_expired"})

def _within_policy_window(policy: RedSubeDemoPolicy, trip: RedSubeTripCombination) -> bool:
    window_end = trip.first_trip_timestamp_utc + timedelta(hours=policy.window_hours_demo)
    return trip.validation_timestamp_utc <= window_end

def _validate_bps(field_name: str, value: int) -> None:
    if value < ZERO_PERCENT_BPS or value > ONE_HUNDRED_PERCENT_BPS:
        raise ValueError(f"{field_name} fuera de la escala de puntos básicos.")

def _bps_to_percent(value: int) -> float:
    return round((value / PERCENT_SCALE) * 100, 2)


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
    }
    return any(term in normalized for term in suspicious_terms) or len(
        normalized.split()
    ) > 1


def _policy_summary(policy: RedSubeDemoPolicy) -> str:
    return f"Política demo: ventana Red SUBE de {policy.window_hours_demo} horas."


def _regulatory_reference_notice() -> str:
    return "Referencias marco: Decreto 84/2009, Resolución 77-E/2018, Decreto 698/2024 y Resolución 40/2026."


def _privacy_notice() -> str:
    return "La política demo no revela DNI, nombre, diagnóstico ni CUD."


def _driver_burden_notice() -> str:
    return "El chofer no calcula, no decide, no administra ni transfiere el Bono Solidario."


def _common_warnings() -> List[str]:
    return ["Política conceptual demostrativa de Red SUBE."]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    import json
    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
