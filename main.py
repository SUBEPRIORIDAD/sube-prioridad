"""
SUBE Prioridad — API demostrativa del MVP.

Esta API forma parte de un MVP conceptual y demostrativo.

No representa implementación oficial vigente.
No representa integración real con SUBE.
No representa conexión real con organismos públicos.
No modifica validadoras reales.
No procesa DNI.
No procesa nombre ni apellido.
No procesa domicilio.
No procesa diagnóstico.
No procesa historia clínica.
No procesa CUD.
No procesa certificados médicos.
No genera sanciones.
No genera vigilancia.
No reemplaza derechos vigentes.

Finalidad:
    Demostrar cómo una necesidad previamente acreditada fuera del transporte
    podría representarse mediante un atributo técnico mínimo, no sensible,
    verificable de manera demostrativa y respetuoso de la privacidad.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator


APP_NAME = "SUBE Prioridad"
APP_VERSION = "0.2.1"
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


DEMO_PRIORITY_REGISTRY = {
    "demo-priority-attribute-001": {
        "priority_status": "demo_active",
        "default_assistance_preference": 2,
        "description": "Atributo técnico demostrativo activo.",
    },
    "demo-priority-attribute-preventive": {
        "priority_status": "demo_active",
        "default_assistance_preference": 2,
        "description": "Atributo técnico demostrativo preventivo.",
    },
    "demo-priority-attribute-visible": {
        "priority_status": "demo_active",
        "default_assistance_preference": 3,
        "description": "Atributo técnico demostrativo visible.",
    },
}


class AssistancePreference(int, Enum):
    """
    Preferencias demostrativas de asistencia.

    No representan diagnósticos.
    No representan categorías médicas.
    Sólo indican modalidad operativa de asistencia.
    """

    SILENCIOSA = 0
    DISCRETA = 1
    PREVENTIVA = 2
    VISIBLE = 3


class VerificationStatus(str, Enum):
    """
    Estados posibles de la verificación demostrativa.
    """

    VALID = "valid"
    INVALID = "invalid"


class VerificationRequest(BaseModel):
    """
    Solicitud de verificación demostrativa.

    Se aceptan nombres en castellano para facilitar uso desde Swagger UI,
    pero el contenido sigue siendo técnico y no sensible.
    """

    token_prioridad: str = Field(
        ...,
        description=(
            "Token técnico demostrativo. No debe ser DNI, CUD, diagnóstico, "
            "certificado médico ni texto libre de beneficio."
        ),
        examples=["demo-priority-attribute-001"],
    )
    preferencia_asistencia: Optional[AssistancePreference] = Field(
        default=None,
        description=(
            "Preferencia demostrativa: 0 silenciosa, 1 discreta, "
            "2 preventiva, 3 visible."
        ),
        examples=[2],
    )
    linea: Optional[str] = Field(
        default=None,
        description="Identificador demostrativo de línea. No representa operación real.",
        examples=["demo-linea-001"],
    )
    unidad: Optional[str] = Field(
        default=None,
        description="Identificador demostrativo de unidad. No representa unidad real.",
        examples=["demo-unidad-001"],
    )

    @model_validator(mode="before")
    @classmethod
    def reject_sensitive_fields(cls, values: Any) -> Any:
        if not isinstance(values, dict):
            return values

        normalized_keys = {str(key).strip().lower() for key in values.keys()}
        forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))

        if forbidden:
            raise ValueError(
                "La solicitud contiene campos prohibidos para SUBE Prioridad: "
                + ", ".join(forbidden)
            )

        return values


class VerificationResponse(BaseModel):
    """
    Respuesta demostrativa de verificación.
    """

    project: str
    version: str
    demo_mode: bool
    status: VerificationStatus
    prioridad_activa: bool
    token_verificado: bool
    motivo: str
    preferencia_asistencia: Optional[int]
    alerta: str
    privacidad: str
    rol_chofer: str
    linea: Optional[str]
    unidad: Optional[str]
    timestamp_utc: str
    advertencias: List[str]


class GuardrailsResponse(BaseModel):
    project: str
    version: str
    demo_mode: bool
    guardrails: List[str]


app = FastAPI(
    title="SUBE Prioridad — MVP API",
    version=APP_VERSION,
    description=(
        "API demostrativa para validar un atributo técnico mínimo y no sensible. "
        "No representa implementación oficial, integración real con SUBE ni "
        "conexión con organismos públicos."
    ),
)


@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "project": APP_NAME,
        "version": APP_VERSION,
        "demo_mode": DEMO_MODE,
        "status": "ok",
        "message": "SUBE Prioridad — MVP conceptual y demostrativo.",
        "documentation": "/docs",
        "guardrails": "/project/guardrails",
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "project": APP_NAME,
        "version": APP_VERSION,
        "demo_mode": DEMO_MODE,
        "timestamp_utc": _now_utc(),
    }


@app.get("/project/guardrails", response_model=GuardrailsResponse)
def project_guardrails() -> GuardrailsResponse:
    return GuardrailsResponse(
        project=APP_NAME,
        version=APP_VERSION,
        demo_mode=DEMO_MODE,
        guardrails=[
            "MVP conceptual y demostrativo.",
            "Sin implementación oficial vigente.",
            "Sin integración real con SUBE.",
            "Sin conexión real con organismos públicos.",
            "Sin modificación de validadoras reales.",
            "Sin procesamiento de DNI.",
            "Sin procesamiento de diagnósticos.",
            "Sin procesamiento de CUD.",
            "Sin certificados médicos en el core.",
            "Sin historia clínica.",
            "Sin vigilancia.",
            "Sin sanciones.",
            "Sin ranking de pasajeros.",
            "Sin sobrecarga al personal de conducción.",
            "Separación entre acreditación institucional y operación técnica.",
            "El transporte no necesita conocer el diagnóstico.",
        ],
    )


@app.post(
    "/api/v1/prioridad/verificar",
    response_model=VerificationResponse,
    summary="Verificar Prioridad",
)
def verificar_prioridad(request: VerificationRequest) -> VerificationResponse:
    """
    Verifica de manera demostrativa un atributo técnico de prioridad.

    Importante:
        - No interpreta texto libre.
        - No valida beneficios reales.
        - No valida CUD.
        - No consulta organismos públicos.
        - No procesa datos sensibles.
        - No activa prioridad por palabras mágicas.
    """
    token = request.token_prioridad.strip()

    if _looks_like_free_text_or_benefit(token):
        return _invalid_response(
            motivo=(
                "El valor recibido parece describir un beneficio, trámite o texto libre. "
                "El MVP no interpreta beneficios reales ni textos descriptivos. "
                "Debe utilizarse un atributo técnico demostrativo previamente emitido."
            ),
            request=request,
        )

    registry_entry = DEMO_PRIORITY_REGISTRY.get(token)

    if registry_entry is None:
        return _invalid_response(
            motivo=(
                "No se registra atributo técnico demostrativo activo para el token informado. "
                "Esto evita falsos positivos: el sistema no activa prioridad por frases, "
                "palabras sueltas ni tokens inventados."
            ),
            request=request,
        )

    preference = (
        request.preferencia_asistencia
        if request.preferencia_asistencia is not None
        else AssistancePreference(registry_entry["default_assistance_preference"])
    )

    return VerificationResponse(
        project=APP_NAME,
        version=APP_VERSION,
        demo_mode=DEMO_MODE,
        status=VerificationStatus.VALID,
        prioridad_activa=True,
        token_verificado=True,
        motivo=(
            "Atributo técnico demostrativo verificado. "
            "La prioridad se activa sólo porque el token existe en el registro demo, "
            "no por interpretación de texto libre."
        ),
        preferencia_asistencia=int(preference.value),
        alerta=_build_alert(preference),
        privacidad=(
            "La verificación demostrativa no revela DNI, nombre, diagnóstico, CUD, "
            "certificado médico ni historia clínica."
        ),
        rol_chofer=(
            "El personal de conducción no evalúa diagnósticos, no solicita certificados "
            "y no administra datos sensibles."
        ),
        linea=request.linea,
        unidad=request.unidad,
        timestamp_utc=_now_utc(),
        advertencias=_common_warnings(),
    )


def _invalid_response(
    motivo: str,
    request: VerificationRequest,
) -> VerificationResponse:
    return VerificationResponse(
        project=APP_NAME,
        version=APP_VERSION,
        demo_mode=DEMO_MODE,
        status=VerificationStatus.INVALID,
        prioridad_activa=False,
        token_verificado=False,
        motivo=motivo,
        preferencia_asistencia=None,
        alerta=(
            "No se emite alerta de prioridad. "
            "La respuesta inválida no implica decisión médica ni sanción."
        ),
        privacidad=(
            "No se procesa ni solicita información sensible para esta respuesta."
        ),
        rol_chofer=(
            "El personal de conducción no debe resolver la validez del atributo."
        ),
        linea=request.linea,
        unidad=request.unidad,
        timestamp_utc=_now_utc(),
        advertencias=_common_warnings(),
    )


def _looks_like_free_text_or_benefit(token: str) -> bool:
    """
    Detecta valores que no son atributos técnicos demostrativos.

    Esto evita confundir frases descriptivas, beneficios o textos libres
    con un token técnico emitido.
    """
    normalized = token.lower().strip()

    suspicious_terms = {
        "bono",
        "solidario",
        "tarifa",
        "social",
        "beneficio",
        "vigente",
        "gratis",
        "cud",
        "andis",
        "medico",
        "médico",
        "diagnostico",
        "diagnóstico",
        "certificado",
    }

    if any(term in normalized for term in suspicious_terms):
        return True

    if len(normalized.split()) > 1:
        return True

    return False


def _build_alert(preference: AssistancePreference) -> str:
    messages = {
        AssistancePreference.SILENCIOSA: (
            "Preferencia silenciosa registrada. Sin alerta visible."
        ),
        AssistancePreference.DISCRETA: (
            "Asistencia prioritaria solicitada de manera discreta."
        ),
        AssistancePreference.PREVENTIVA: (
            "Asistencia preventiva sugerida. Mensaje genérico sin diagnóstico."
        ),
        AssistancePreference.VISIBLE: (
            "Asistencia prioritaria visible solicitada. Mensaje genérico sin diagnóstico."
        ),
    }

    return messages[preference]


def _common_warnings() -> List[str]:
    return [
        "MVP conceptual y demostrativo.",
        "Sin implementación oficial vigente.",
        "Sin integración real con SUBE.",
        "Sin conexión real con organismos públicos.",
        "Sin modificación de validadoras reales.",
        "Sin procesamiento de datos sensibles reales.",
        "Sin diagnóstico médico en el core.",
        "Sin validación de CUD real.",
        "Sin firma gubernamental real en el core.",
        "Sin sanciones, vigilancia ni ranking de pasajeros.",
    ]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()
