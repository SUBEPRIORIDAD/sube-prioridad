"""
SUBE Prioridad — Orquestador MVP end-to-end del Bono Solidario.

Este módulo une las piezas principales del MVP:

    1. Selección de una opción MVP de sincronización.
    2. Evaluación de esa opción.
    3. Acumulación demo del Bono Solidario.
    4. Generación de instrucción demo para próximo viaje elegible.
    5. Registro auditable no sensible.

Opciones actualmente contempladas:

    - Celular a celular con contexto Red SUBE demo.
    - Celular NFC del usuario SUBE Prioridad hacia tarjeta SUBE del colaborador.
    - Validadora asistida con segunda aproximación de tarjeta.

Regla central:
    El orquestador NO aplica beneficios reales.
    Sólo demuestra cómo podría fluir el Bono Solidario dentro de un MVP.

No integra SUBE real.
No integra Red SUBE real.
No consulta tarjetas reales.
No consulta cuentas reales.
No consulta validadoras reales.
No consulta molinetes reales.
No modifica saldo real.
No aplica tarifa real.
No escribe chips reales.
No usa DNI.
No usa nombre.
No usa diagnóstico.
No usa CUD visible.
No usa GPS exacto.
No genera ranking.
No genera sanciones.
No impone carga al chofer.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from solidary_bonus_mvp_accrual_flow import (
    BonusAccrualLedger,
    BonusAccrualPolicy,
    BonusAccrualStatus,
    SolidaryBonusAccrualRequest,
    SolidaryBonusAccrualResult,
    create_demo_bonus_accrual_ledger,
    create_demo_bonus_accrual_policy,
    create_demo_solidary_bonus_accrual_request,
    evaluate_solidary_bonus_mvp_accrual,
    result_to_dict as accrual_result_to_dict,
)

from solidary_bonus_mvp_sync_options import (
    MvpSolidarySyncOptionRequest,
    MvpSolidarySyncOptionResult,
    MvpSyncOption,
    MvpSyncPolicy,
    MvpSyncStatus,
    create_demo_mobile_to_mobile_request,
    create_demo_mvp_sync_policy,
    create_demo_priority_phone_nfc_card_request,
    create_demo_validator_assisted_card_tap_request,
    evaluate_mvp_solidary_sync_option,
    result_to_dict as sync_option_result_to_dict,
)


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Orquestador MVP End-to-End de Bono Solidario"
MODULE_VERSION = "0.1.0"
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


class EndToEndStatus(str, Enum):
    COMPLETED = "completed"
    COMPLETED_WITH_AUDIT = "completed_with_audit"
    REJECTED_AT_SYNC_OPTION = "rejected_at_sync_option"
    REJECTED_AT_ACCRUAL = "rejected_at_accrual"
    NEEDS_REVIEW = "needs_review"


class EndToEndScenario(str, Enum):
    MOBILE_TO_MOBILE = "mobile_to_mobile"
    PRIORITY_PHONE_NFC_CARD = "priority_phone_nfc_card"
    VALIDATOR_ASSISTED_CARD_TAP = "validator_assisted_card_tap"


@dataclass(frozen=True)
class EndToEndPolicy:
    """
    Política general del orquestador.

    stop_on_sync_rejection:
        Si la opción MVP falla, no se intenta acumular el bono.

    stop_on_accrual_rejection:
        Si la acumulación falla, el flujo queda rechazado.

    require_no_real_integration:
        Mantiene el flujo en modo demo conceptual.
    """

    stop_on_sync_rejection: bool
    stop_on_accrual_rejection: bool
    require_no_real_integration: bool
    include_sync_payload_demo: bool
    include_accrual_payload_demo: bool


@dataclass(frozen=True)
class SolidaryBonusMvpEndToEndRequest:
    """
    Solicitud end-to-end.

    Puede recibir una solicitud MVP ya armada o crear una demo según escenario.
    """

    end_to_end_event_demo_id: str
    scenario: EndToEndScenario
    sync_option_request: Optional[MvpSolidarySyncOptionRequest]
    sync_policy: MvpSyncPolicy
    accrual_policy: BonusAccrualPolicy
    accrual_ledger: BonusAccrualLedger
    collaborator_account_demo_token: str
    collaborator_sube_card_token: str
    collaborator_payment_method_demo_token: str


@dataclass(frozen=True)
class SolidaryBonusMvpEndToEndResult:
    project: str
    module: str
    version: str
    demo_mode: bool
    status: EndToEndStatus
    scenario: EndToEndScenario
    selected_mvp_option: str
    sync_option_status: str
    accrual_status: Optional[str]
    instruction_created: bool
    opens_bonus_evaluation_window: bool
    blocks_solidary_bonus_flow: bool
    final_demo_discount_bps_if_eligible: int
    hard_risk_flags: List[str]
    audit_flags: List[str]
    reason: str
    sync_option_result_demo: Optional[Dict[str, Any]]
    accrual_result_demo: Optional[Dict[str, Any]]
    security_summary: Dict[str, Any]
    privacy_notice: str
    legal_scope_notice: str
    driver_burden_notice: str
    warnings: List[str]


def assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    normalized_keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))

    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )


def create_demo_end_to_end_policy(
    stop_on_sync_rejection: bool = True,
    stop_on_accrual_rejection: bool = True,
    require_no_real_integration: bool = True,
    include_sync_payload_demo: bool = True,
    include_accrual_payload_demo: bool = True,
) -> EndToEndPolicy:
    return EndToEndPolicy(
        stop_on_sync_rejection=stop_on_sync_rejection,
        stop_on_accrual_rejection=stop_on_accrual_rejection,
        require_no_real_integration=require_no_real_integration,
        include_sync_payload_demo=include_sync_payload_demo,
        include_accrual_payload_demo=include_accrual_payload_demo,
    )


def create_demo_solidary_bonus_mvp_end_to_end_request(
    end_to_end_event_demo_id: str = "demo-end-to-end-bonus-001",
    scenario: EndToEndScenario = EndToEndScenario.MOBILE_TO_MOBILE,
    sync_option_request: Optional[MvpSolidarySyncOptionRequest] = None,
    sync_policy: Optional[MvpSyncPolicy] = None,
    accrual_policy: Optional[BonusAccrualPolicy] = None,
    accrual_ledger: Optional[BonusAccrualLedger] = None,
    collaborator_account_demo_token: str = "demo-collaborator-account-001",
    collaborator_sube_card_token: str = "demo-collaborator-sube-card-001",
    collaborator_payment_method_demo_token: str = "demo-collaborator-payment-001",
) -> SolidaryBonusMvpEndToEndRequest:
    required_values = {
        "end_to_end_event_demo_id": end_to_end_event_demo_id,
        "collaborator_account_demo_token": collaborator_account_demo_token,
        "collaborator_sube_card_token": collaborator_sube_card_token,
        "collaborator_payment_method_demo_token": collaborator_payment_method_demo_token,
    }

    _validate_required_values(required_values)
    assert_no_prohibited_fields(required_values)

    return SolidaryBonusMvpEndToEndRequest(
        end_to_end_event_demo_id=end_to_end_event_demo_id.strip(),
        scenario=scenario,
        sync_option_request=sync_option_request,
        sync_policy=sync_policy or create_demo_mvp_sync_policy(),
        accrual_policy=accrual_policy or create_demo_bonus_accrual_policy(),
        accrual_ledger=accrual_ledger or create_demo_bonus_accrual_ledger(),
        collaborator_account_demo_token=collaborator_account_demo_token.strip(),
        collaborator_sube_card_token=collaborator_sube_card_token.strip(),
        collaborator_payment_method_demo_token=collaborator_payment_method_demo_token.strip(),
    )


def run_solidary_bonus_mvp_end_to_end(
    request: SolidaryBonusMvpEndToEndRequest,
    policy: Optional[EndToEndPolicy] = None,
) -> SolidaryBonusMvpEndToEndResult:
    """
    Ejecuta el flujo completo del MVP.

    Paso 1:
        Evalúa la opción MVP.

    Paso 2:
        Si la opción abre ventana, intenta crear instrucción demo de acumulación.

    Paso 3:
        Devuelve resultado final auditable.
    """
    policy = policy or create_demo_end_to_end_policy()

    assert_no_prohibited_fields(
        {
            "end_to_end_event_demo_id": request.end_to_end_event_demo_id,
            "collaborator_account_demo_token": request.collaborator_account_demo_token,
            "collaborator_sube_card_token": request.collaborator_sube_card_token,
            "collaborator_payment_method_demo_token": request.collaborator_payment_method_demo_token,
        }
    )

    sync_request = request.sync_option_request or _default_sync_request_for_scenario(
        request.scenario
    )

    sync_result = evaluate_mvp_solidary_sync_option(
        request=sync_request,
        policy=request.sync_policy,
    )

    if sync_result.status == MvpSyncStatus.REJECTED and policy.stop_on_sync_rejection:
        return _result(
            request=request,
            policy=policy,
            status=EndToEndStatus.REJECTED_AT_SYNC_OPTION,
            sync_request=sync_request,
            sync_result=sync_result,
            accrual_request=None,
            accrual_result=None,
            hard_risk_flags=_prefix_flags("sync", sync_result.hard_risk_flags),
            audit_flags=_prefix_flags("sync", sync_result.audit_flags),
            reason=(
                "El flujo end-to-end se detuvo porque la opción MVP de sincronización "
                "fue rechazada."
            ),
        )

    accrual_request = create_demo_solidary_bonus_accrual_request(
        accrual_event_demo_id=f"accrual-{request.end_to_end_event_demo_id}",
        mvp_sync_request=sync_request,
        mvp_sync_result=sync_result,
        collaborator_account_demo_token=request.collaborator_account_demo_token,
        collaborator_sube_card_token=request.collaborator_sube_card_token,
        collaborator_payment_method_demo_token=request.collaborator_payment_method_demo_token,
        base_red_sube_discount_bps_demo=sync_request.current_base_red_sube_discount_bps_demo,
    )

    accrual_result = evaluate_solidary_bonus_mvp_accrual(
        request=accrual_request,
        policy=request.accrual_policy,
        ledger=request.accrual_ledger,
    )

    if accrual_result.status == BonusAccrualStatus.REJECTED and policy.stop_on_accrual_rejection:
        return _result(
            request=request,
            policy=policy,
            status=EndToEndStatus.REJECTED_AT_ACCRUAL,
            sync_request=sync_request,
            sync_result=sync_result,
            accrual_request=accrual_request,
            accrual_result=accrual_result,
            hard_risk_flags=_prefix_flags("accrual", accrual_result.hard_risk_flags),
            audit_flags=_deduplicate(
                _prefix_flags("sync", sync_result.audit_flags)
                + _prefix_flags("accrual", accrual_result.audit_flags)
            ),
            reason=(
                "El flujo end-to-end se detuvo porque la acumulación demo del Bono "
                "Solidario fue rechazada."
            ),
        )

    status = (
        EndToEndStatus.COMPLETED_WITH_AUDIT
        if sync_result.requires_audit_review or accrual_result.requires_audit_review
        else EndToEndStatus.COMPLETED
    )

    return _result(
        request=request,
        policy=policy,
        status=status,
        sync_request=sync_request,
        sync_result=sync_result,
        accrual_request=accrual_request,
        accrual_result=accrual_result,
        hard_risk_flags=[],
        audit_flags=_deduplicate(
            _prefix_flags("sync", sync_result.audit_flags)
            + _prefix_flags("accrual", accrual_result.audit_flags)
        ),
        reason=(
            "Flujo end-to-end completado: la opción MVP abrió una ventana válida "
            "y se creó la instrucción demo de Bono Solidario para próximo viaje elegible."
        ),
    )


def result_to_dict(result: SolidaryBonusMvpEndToEndResult) -> Dict[str, Any]:
    return {
        "project": result.project,
        "module": result.module,
        "version": result.version,
        "demo_mode": result.demo_mode,
        "status": result.status.value,
        "scenario": result.scenario.value,
        "selected_mvp_option": result.selected_mvp_option,
        "sync_option_status": result.sync_option_status,
        "accrual_status": result.accrual_status,
        "instruction_created": result.instruction_created,
        "opens_bonus_evaluation_window": result.opens_bonus_evaluation_window,
        "blocks_solidary_bonus_flow": result.blocks_solidary_bonus_flow,
        "final_demo_discount_bps_if_eligible": result.final_demo_discount_bps_if_eligible,
        "hard_risk_flags": result.hard_risk_flags,
        "audit_flags": result.audit_flags,
        "reason": result.reason,
        "sync_option_result_demo": result.sync_option_result_demo,
        "accrual_result_demo": result.accrual_result_demo,
        "security_summary": result.security_summary,
        "privacy_notice": result.privacy_notice,
        "legal_scope_notice": result.legal_scope_notice,
        "driver_burden_notice": result.driver_burden_notice,
        "warnings": result.warnings,
    }


def run_mobile_to_mobile_demo() -> Dict[str, Any]:
    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        scenario=EndToEndScenario.MOBILE_TO_MOBILE,
    )

    result = run_solidary_bonus_mvp_end_to_end(request)

    return result_to_dict(result)


def run_priority_phone_nfc_card_demo() -> Dict[str, Any]:
    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        scenario=EndToEndScenario.PRIORITY_PHONE_NFC_CARD,
    )

    result = run_solidary_bonus_mvp_end_to_end(request)

    return result_to_dict(result)


def run_validator_assisted_card_tap_demo() -> Dict[str, Any]:
    request = create_demo_solidary_bonus_mvp_end_to_end_request(
        scenario=EndToEndScenario.VALIDATOR_ASSISTED_CARD_TAP,
    )

    result = run_solidary_bonus_mvp_end_to_end(request)

    return result_to_dict(result)


def _default_sync_request_for_scenario(
    scenario: EndToEndScenario,
) -> MvpSolidarySyncOptionRequest:
    if scenario == EndToEndScenario.MOBILE_TO_MOBILE:
        return create_demo_mobile_to_mobile_request()

    if scenario == EndToEndScenario.PRIORITY_PHONE_NFC_CARD:
        return create_demo_priority_phone_nfc_card_request()

    if scenario == EndToEndScenario.VALIDATOR_ASSISTED_CARD_TAP:
        return create_demo_validator_assisted_card_tap_request()

    return create_demo_mobile_to_mobile_request()


def _result(
    request: SolidaryBonusMvpEndToEndRequest,
    policy: EndToEndPolicy,
    status: EndToEndStatus,
    sync_request: MvpSolidarySyncOptionRequest,
    sync_result: MvpSolidarySyncOptionResult,
    accrual_request: Optional[SolidaryBonusAccrualRequest],
    accrual_result: Optional[SolidaryBonusAccrualResult],
    hard_risk_flags: List[str],
    audit_flags: List[str],
    reason: str,
) -> SolidaryBonusMvpEndToEndResult:
    instruction_created = bool(accrual_result and accrual_result.instruction_created)

    return SolidaryBonusMvpEndToEndResult(
        project=PROJECT_NAME,
        module=MODULE_NAME,
        version=MODULE_VERSION,
        demo_mode=DEMO_MODE,
        status=status,
        scenario=request.scenario,
        selected_mvp_option=sync_request.option.value,
        sync_option_status=sync_result.status.value,
        accrual_status=accrual_result.status.value if accrual_result else None,
        instruction_created=instruction_created,
        opens_bonus_evaluation_window=(
            sync_result.opens_bonus_evaluation_window
            and bool(accrual_result and accrual_result.instruction_created)
        ),
        blocks_solidary_bonus_flow=(
            sync_result.blocks_solidary_bonus_flow
            or bool(accrual_result and accrual_result.blocks_solidary_bonus_flow)
            or status
            in {
                EndToEndStatus.REJECTED_AT_SYNC_OPTION,
                EndToEndStatus.REJECTED_AT_ACCRUAL,
            }
        ),
        final_demo_discount_bps_if_eligible=(
            accrual_result.final_demo_discount_bps_if_eligible
            if accrual_result
            else 0
        ),
        hard_risk_flags=hard_risk_flags,
        audit_flags=audit_flags,
        reason=reason,
        sync_option_result_demo=(
            sync_option_result_to_dict(sync_result)
            if policy.include_sync_payload_demo
            else None
        ),
        accrual_result_demo=(
            accrual_result_to_dict(accrual_result)
            if accrual_result and policy.include_accrual_payload_demo
            else None
        ),
        security_summary=_security_summary(
            request=request,
            policy=policy,
            sync_request=sync_request,
            sync_result=sync_result,
            accrual_result=accrual_result,
        ),
        privacy_notice=_privacy_notice(),
        legal_scope_notice=_legal_scope_notice(),
        driver_burden_notice=_driver_burden_notice(),
        warnings=_common_warnings(),
    )


def _security_summary(
    request: SolidaryBonusMvpEndToEndRequest,
    policy: EndToEndPolicy,
    sync_request: MvpSolidarySyncOptionRequest,
    sync_result: MvpSolidarySyncOptionResult,
    accrual_result: Optional[SolidaryBonusAccrualResult],
) -> Dict[str, Any]:
    return {
        "end_to_end_event_demo_id": request.end_to_end_event_demo_id,
        "scenario": request.scenario.value,
        "selected_mvp_option": sync_request.option.value,
        "sync_option_status": sync_result.status.value,
        "sync_opens_bonus_evaluation_window": sync_result.opens_bonus_evaluation_window,
        "sync_blocks_solidary_bonus_flow": sync_result.blocks_solidary_bonus_flow,
        "sync_requires_audit_review": sync_result.requires_audit_review,
        "accrual_status": accrual_result.status.value if accrual_result else None,
        "accrual_instruction_created": (
            accrual_result.instruction_created if accrual_result else False
        ),
        "accrual_requires_audit_review": (
            accrual_result.requires_audit_review if accrual_result else None
        ),
        "final_demo_discount_bps_if_eligible": (
            accrual_result.final_demo_discount_bps_if_eligible
            if accrual_result
            else 0
        ),
        "require_no_real_integration": policy.require_no_real_integration,
        "real_sube_integration": False,
        "real_red_sube_integration": False,
        "real_balance_modified": False,
        "real_tariff_applied": False,
        "driver_console_optional_only": (
            sync_result.driver_console_optional_only
            if hasattr(sync_result, "driver_console_optional_only")
            else False
        ),
    }


def _prefix_flags(prefix: str, flags: List[str]) -> List[str]:
    return [f"{prefix}_{flag}" for flag in flags]


def _privacy_notice() -> str:
    return (
        "El orquestador no revela DNI, nombre, domicilio, diagnóstico, CUD, historia "
        "clínica, certificado médico, teléfono, email, IMEI, MAC, saldo, dinero, "
        "ranking, sanciones ni GPS exacto."
    )


def _legal_scope_notice() -> str:
    return (
        "El flujo end-to-end es conceptual. No aplica descuentos reales, no modifica "
        "saldo real, no escribe tarjetas reales y no integra SUBE ni Red SUBE real. "
        "Toda implementación requeriría autorización, integración oficial, auditoría "
        "y normativa competente."
    )


def _driver_burden_notice() -> str:
    return (
        "El chofer no decide el Bono Solidario, no verifica condiciones personales, "
        "no administra beneficios y no recibe una obligación nueva. Toda intervención "
        "por consola se modela como alternativa piloto opcional o sustituible."
    )


def _common_warnings() -> List[str]:
    return [
        "Orquestador MVP conceptual y demostrativo.",
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
        "El Bono Solidario demo se limita al próximo viaje elegible.",
        "El +50% demo es conceptual y sujeto a límites configurables.",
        "La validadora asistida es una alternativa piloto auditable.",
        "El chofer no debe cargar con una obligación nueva.",
    ]


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


if __name__ == "__main__":
    import json

    print(json.dumps(run_mobile_to_mobile_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_priority_phone_nfc_card_demo(), indent=2, ensure_ascii=False))
    print(json.dumps(run_validator_assisted_card_tap_demo(), indent=2, ensure_ascii=False))
