"""
SUBE Prioridad — API demo.

Esta API expone endpoints conceptuales para el proyecto SUBE Prioridad.

Importante:
    No integra SUBE real.
    No integra Red SUBE real.
    No consulta tarjetas reales.
    No consulta cuentas reales.
    No consulta validadores reales.
    No consulta molinetes reales.
    No aplica tarifas reales.
    No modifica saldo real.
    No escribe chips reales.
    No usa DNI.
    No usa diagnóstico.
    No usa CUD visible.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from bono_solidario_simulator import (
    SeatType,
    create_demo_solidary_event,
    result_to_dict as bono_result_to_dict,
    simulate_solidary_recognition,
)


APP_NAME = "SUBE Prioridad"
PROJECT_NAME = APP_NAME
APP_VERSION = "0.4.2"
DEMO_MODE = True


app = FastAPI(
    title=APP_NAME,
    description=(
        "API demo conceptual para asistencia preventiva, alertas de prioridad "
        "y Bono Solidario en transporte público."
    ),
    version=APP_VERSION,
)


class PriorityVerificationRequest(BaseModel):
    """
    Payload de verificación demo.

    Los campos centrales son requeridos para mantener compatibilidad con tests
    y evitar que un payload vacío sea aceptado como válido.
    """

    priority_attribute_active: bool = Field(...)
    previously_accredited_need: bool = Field(...)
    validation_paid: bool = Field(...)
    user_token: Optional[str] = Field(default="demo-priority-user-001")
    priority_attribute_token: Optional[str] = Field(default="demo-priority-attribute-001")


class SolidaryBonusSimulationRequest(BaseModel):
    """
    Payload para simulación simple del Bono Solidario.

    Se conserva compatibilidad con el endpoint previo.
    """

    priority_user_token: str = Field(default="demo-priority-user-001")
    collaborator_user_token: str = Field(default="demo-collaborator-user-001")
    voluntary_seat_yield: bool = Field(default=True)
    priority_user_confirms: bool = Field(default=True)
    same_transport_context: bool = Field(default=True)
    seat_type: str = Field(default="general_use")


class SolidaryBonusMvpEndToEndRequest(BaseModel):
    """
    Solicitud del flujo end-to-end MVP.

    Escenarios admitidos:
        - mobile_to_mobile
        - priority_phone_nfc_card
        - validator_assisted_card_tap
    """

    scenario: str = Field(default="mobile_to_mobile")
    collaborator_account_demo_token: str = Field(default="demo-collaborator-account-001")
    collaborator_sube_card_token: str = Field(default="demo-collaborator-sube-card-001")
    collaborator_payment_method_demo_token: str = Field(default="demo-collaborator-payment-001")


@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "app_name": APP_NAME,
        "project": PROJECT_NAME,
        "version": APP_VERSION,
        "demo_mode": DEMO_MODE,
        "status": "ok",
        "message": (
            "SUBE Prioridad API demo. Proyecto conceptual sin integración real "
            "con SUBE ni Red SUBE."
        ),
        "docs": "/docs",
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "app_name": APP_NAME,
        "project": PROJECT_NAME,
        "version": APP_VERSION,
        "demo_mode": DEMO_MODE,
        "status": "ok",
    }


@app.get("/project/guardrails")
def project_guardrails() -> Dict[str, Any]:
    return {
        "app_name": APP_NAME,
        "project": PROJECT_NAME,
        "version": APP_VERSION,
        "demo_mode": DEMO_MODE,
        "status": "ok",
        "guardrails": [
            "Sin integración real con SUBE.",
            "Sin integración real con Red SUBE.",
            "Sin consulta a tarjetas reales.",
            "Sin consulta a cuentas reales.",
            "Sin consulta a validadores reales.",
            "Sin consulta a molinetes reales.",
            "Sin tarifa real.",
            "Sin saldo real.",
            "Sin escritura real sobre chip SUBE.",
            "Sin DNI.",
            "Sin diagnóstico médico.",
            "Sin CUD visible.",
            "Sin historia clínica.",
            "Sin certificado médico.",
            "Sin GPS exacto.",
            "Sin vigilancia.",
            "Sin ranking.",
            "Sin sanciones.",
            "Sin obligación de tener celular.",
            "Sin obligación nueva para choferes.",
            "El transporte no necesita conocer el diagnóstico.",
        ],
    }


@app.post("/api/v1/prioridad/verificar")
def verificar_prioridad(
    request: PriorityVerificationRequest,
) -> Dict[str, Any]:
    """
    Verificación demo del atributo SUBE Prioridad.

    No consulta bases reales.
    No valida documentación real.
    No expone información sensible.
    """
    eligible = (
        request.priority_attribute_active
        and request.previously_accredited_need
        and request.validation_paid
    )

    risk_flags = []

    if not request.priority_attribute_active:
        risk_flags.append("priority_attribute_not_active")

    if not request.previously_accredited_need:
        risk_flags.append("priority_need_not_previously_accredited")

    if not request.validation_paid:
        risk_flags.append("validation_payment_not_confirmed")

    return {
        "app_name": APP_NAME,
        "project": PROJECT_NAME,
        "demo_mode": DEMO_MODE,
        "eligible": eligible,
        "priority_attribute_active": request.priority_attribute_active,
        "previously_accredited_need": request.previously_accredited_need,
        "validation_paid": request.validation_paid,
        "risk_flags": risk_flags,
        "privacy_notice": (
            "La verificación demo no usa DNI, diagnóstico, CUD, certificado médico "
            "ni historia clínica."
        ),
        "legal_scope_notice": (
            "Resultado conceptual sin integración real con SUBE ni Red SUBE."
        ),
    }


@app.post("/api/v1/bono-solidario/simular")
def simular_bono_solidario(
    request: SolidaryBonusSimulationRequest,
) -> Dict[str, Any]:
    """
    Simulación base del Bono Solidario.

    Este endpoint conserva la simulación simple previa del proyecto.
    """
    seat_type_map = {
        "general_use": SeatType.GENERAL_USE,
        "legal_priority": SeatType.LEGAL_PRIORITY,
    }

    if request.seat_type not in seat_type_map:
        raise HTTPException(
            status_code=400,
            detail="seat_type debe ser general_use o legal_priority.",
        )

    event = create_demo_solidary_event(
        priority_user_token=request.priority_user_token,
        collaborator_token=request.collaborator_user_token,
        voluntary_seat_yield=request.voluntary_seat_yield,
        priority_user_confirms=request.priority_user_confirms,
        same_transport_context=request.same_transport_context,
        seat_type=seat_type_map[request.seat_type],
    )

    result = simulate_solidary_recognition(event)

    return bono_result_to_dict(result)


@app.post("/api/v1/bono-solidario-mvp/end-to-end")
def bono_solidario_mvp_end_to_end(
    request: SolidaryBonusMvpEndToEndRequest,
) -> Dict[str, Any]:
    """
    Ejecuta el flujo end-to-end del Bono Solidario MVP.

    Este endpoint:
        - evalúa la opción MVP;
        - abre una ventana demo;
        - ejecuta acumulación demo;
        - genera instrucción conceptual para próximo viaje elegible;
        - no aplica beneficios reales.
    """
    from solidary_bonus_mvp_end_to_end_flow import (
        EndToEndScenario,
        create_demo_solidary_bonus_mvp_end_to_end_request,
        result_to_dict,
        run_solidary_bonus_mvp_end_to_end,
    )

    scenario_map = {
        "mobile_to_mobile": EndToEndScenario.MOBILE_TO_MOBILE,
        "priority_phone_nfc_card": EndToEndScenario.PRIORITY_PHONE_NFC_CARD,
        "validator_assisted_card_tap": EndToEndScenario.VALIDATOR_ASSISTED_CARD_TAP,
    }

    if request.scenario not in scenario_map:
        raise HTTPException(
            status_code=400,
            detail=(
                "scenario debe ser uno de: mobile_to_mobile, "
                "priority_phone_nfc_card, validator_assisted_card_tap."
            ),
        )

    end_to_end_request = create_demo_solidary_bonus_mvp_end_to_end_request(
        scenario=scenario_map[request.scenario],
        collaborator_account_demo_token=request.collaborator_account_demo_token,
        collaborator_sube_card_token=request.collaborator_sube_card_token,
        collaborator_payment_method_demo_token=request.collaborator_payment_method_demo_token,
    )

    result = run_solidary_bonus_mvp_end_to_end(end_to_end_request)

    return result_to_dict(result)
