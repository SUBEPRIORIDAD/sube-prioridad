from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


APP_VERSION = "0.2.0"

PROJECT_GUARDRAILS = {
    "naturaleza": "MVP conceptual, técnico y demostrativo",
    "implementacion": "gradual, modular, reversible y sujeta a factibilidad",
    "datos_sensibles_en_core": False,
    "diagnostico_medico_en_core": False,
    "modifica_regimen_asientos_prioritarios": False,
    "impone_cargas_al_chofer": False,
    "genera_sanciones_a_pasajeros": False,
    "modifica_recaudacion_sube": False,
    "bono_solidario_es_core_inicial": False,
    "bono_solidario_es_evolucion_futura": True,
    "integraciones_externas_reales": False,
}


PROHIBITED_CORE_FIELDS = {
    "dni",
    "nombre",
    "apellido",
    "domicilio",
    "historia_clinica",
    "historia_clínica",
    "diagnostico",
    "diagnóstico",
    "diagnostico_medico",
    "diagnóstico_médico",
    "certificado_medico",
    "certificado_médico",
}


app = FastAPI(
    title="SUBE Prioridad API",
    description=(
        "MVP conceptual y demostrativo para validación de atributo de prioridad "
        "sin exposición de DNI, nombre, diagnóstico médico ni historia clínica. "
        "El sistema representa una arquitectura posible, no una implementación "
        "definitiva ni una integración real con organismos externos."
    ),
    version=APP_VERSION,
)


class VerificationRequest(BaseModel):
    token_tramite_hash: str = Field(
        ...,
        min_length=64,
        max_length=64,
        description="Hash SHA-256 pseudoanonimizado del trámite o credencial.",
    )
    firma_digital_medico: Optional[str] = Field(
        default=None,
        description=(
            "Referencia técnica opcional de firma digital. "
            "En el MVP no se valida contra servicios reales."
        ),
    )
    entidad_emisora: Optional[str] = Field(
        default=None,
        description=(
            "Entidad pública o sanitaria emisora. "
            "Campo informativo para entorno simulado."
        ),
    )
    perfil_asistencia_preferido: Optional[int] = Field(
        default=2,
        ge=0,
        le=3,
        description=(
            "Preferencia conceptual de asistencia: "
            "0 silenciosa, 1 discreta, 2 preventiva, 3 visible."
        ),
    )


class VerificationResponse(BaseModel):
    atributo_prioridad_activo: bool
    perfil_alertas_ux: int
    fecha_caducidad: datetime
    motivo: str
    entorno: str
    datos_sensibles_procesados: bool
    integracion_real_con_organismos: bool


def assert_safe_payload(payload: dict) -> None:
    """
    Control defensivo mínimo para impedir que el core reciba datos sensibles.
    """

    normalized_keys = {str(key).lower() for key in payload.keys()}
    forbidden = sorted(PROHIBITED_CORE_FIELDS.intersection(normalized_keys))

    if forbidden:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "El payload contiene campos prohibidos para el core del MVP: "
                + ", ".join(forbidden)
            ),
        )


@app.get("/")
def root() -> dict:
    return {
        "servicio": "SUBE Prioridad API",
        "estado": "operativo",
        "version": APP_VERSION,
        "naturaleza": "MVP conceptual, gradual y demostrativo",
        "objetivo": (
            "Facilitar asistencia preventiva para personas con necesidad "
            "acreditada de viajar sentadas."
        ),
    }


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/project/guardrails")
def project_guardrails() -> dict:
    """
    Expone principios rectores no sensibles del MVP.
    """

    return PROJECT_GUARDRAILS


@app.post(
    "/api/v1/prioridad/verificar",
    response_model=VerificationResponse,
    status_code=status.HTTP_200_OK,
)
def verificar_prioridad(request: VerificationRequest) -> VerificationResponse:
    """
    Verifica si un token pseudoanonimizado posee atributo de prioridad activo.

    MVP:
    - No recibe DNI.
    - No recibe nombre.
    - No recibe diagnóstico.
    - No recibe historia clínica.
    - No modifica tarifas.
    - No impone obligaciones al chofer.
    - No altera el régimen legal de asientos prioritarios.
    - No implementa todavía el Bono Solidario como core inicial.
    - No afirma integración real con organismos externos.
    """

    payload = request.model_dump(exclude_none=True)
    assert_safe_payload(payload)

    if not request.token_tramite_hash.isalnum():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El token_tramite_hash debe ser alfanumérico.",
        )

    fecha_caducidad = datetime.now(timezone.utc) + timedelta(days=180)

    return VerificationResponse(
        atributo_prioridad_activo=True,
        perfil_alertas_ux=request.perfil_asistencia_preferido or 2,
        fecha_caducidad=fecha_caducidad,
        motivo=(
            "Atributo de prioridad validado en entorno MVP. "
            "La respuesta es conceptual, no implica implementación definitiva "
            "ni integración real con organismos externos."
        ),
        entorno="simulado_mvp",
        datos_sensibles_procesados=False,
        integracion_real_con_organismos=False,
    )
