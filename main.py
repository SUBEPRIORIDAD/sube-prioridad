from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


app = FastAPI(
    title="SUBE Prioridad API",
    description=(
        "MVP técnico para validación de atributo de prioridad "
        "sin exposición de datos personales ni diagnóstico médico."
    ),
    version="0.1.0",
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
        description="Firma digital del profesional o autoridad sanitaria emisora.",
    )
    entidad_emisora: Optional[str] = Field(
        default=None,
        description="Entidad pública o sanitaria que emitió la validación.",
    )


class VerificationResponse(BaseModel):
    atributo_prioridad_activo: bool
    perfil_alertas_ux: int
    fecha_caducidad: datetime
    motivo: str


@app.get("/")
def root() -> dict:
    return {
        "servicio": "SUBE Prioridad API",
        "estado": "operativo",
        "version": "0.1.0",
    }


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


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
    - Trabaja únicamente sobre un hash técnico.
    """

    if not request.token_tramite_hash.isalnum():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El token_tramite_hash debe ser alfanumérico.",
        )

    fecha_caducidad = datetime.now(timezone.utc) + timedelta(days=180)

    return VerificationResponse(
        atributo_prioridad_activo=True,
        perfil_alertas_ux=2,
        fecha_caducidad=fecha_caducidad,
        motivo="Atributo de prioridad validado para entorno MVP.",
    )
    