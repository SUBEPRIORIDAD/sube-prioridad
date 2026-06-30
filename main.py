from datetime import date
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="SUBE Prioridad API",
    description=(
        "MVP conceptual, técnico y demostrativo para asistencia preventiva, "
        "accesibilidad efectiva, privacidad por diseño y convivencia en el "
        "transporte público."
    ),
    version="0.1.0",
)


class VerificacionPrioridadRequest(BaseModel):
    """
    Solicitud conceptual de verificación.

    Este MVP no recibe ni procesa DNI, nombre, apellido, domicilio,
    diagnóstico médico, historia clínica, certificados médicos en texto plano
    ni datos de salud identificables.

    El campo token_prioridad representa un identificador técnico,
    pseudoanonimizado o simulado, utilizado exclusivamente para fines
    demostrativos dentro del MVP conceptual.
    """

    token_prioridad: str = Field(
        ...,
        description=(
            "Token técnico o identificador pseudoanonimizado de prioridad. "
            "No debe contener DNI, nombre, diagnóstico ni datos sensibles."
        ),
        examples=["demo-prioridad-activa"],
    )
    linea: Optional[str] = Field(
        default=None,
        description=(
            "Línea de transporte utilizada sólo para simulación, evaluación "
            "técnica o pruebas controladas."
        ),
        examples=["60"],
    )
    unidad: Optional[str] = Field(
        default=None,
        description=(
            "Unidad, interno o identificador técnico utilizado sólo para "
            "simulación, evaluación técnica o pruebas controladas."
        ),
        examples=["1234"],
    )


class VerificacionPrioridadResponse(BaseModel):
    prioridad_activa: bool = Field(
        ...,
        description="Indica si existe un atributo técnico de prioridad activo en la simulación.",
    )
    perfil_ux: str = Field(
        ...,
        description="Modalidad conceptual de experiencia de usuario o asistencia.",
    )
    fecha_caducidad: Optional[str] = Field(
        default=None,
        description="Fecha conceptual de caducidad del atributo técnico, si corresponde.",
    )
    motivo: str = Field(
        ...,
        description="Explicación conceptual del resultado de la verificación.",
    )
    entorno: str = Field(
        ...,
        description="Entorno de ejecución declarado por el MVP.",
    )
    datos_sensibles_procesados: bool = Field(
        ...,
        description="Debe permanecer en false dentro del MVP conceptual.",
    )
    integracion_real_con_organismos: bool = Field(
        ...,
        description="Debe permanecer en false mientras no exista autorización institucional real.",
    )


@app.get("/")
def root():
    """
    Endpoint raíz del MVP.

    Declara expresamente la naturaleza conceptual y demostrativa del proyecto.
    """

    return {
        "proyecto": "SUBE Prioridad",
        "estado": "MVP conceptual, técnico y demostrativo",
        "descripcion": (
            "Propuesta ciudadana de innovación pública para asistencia preventiva, "
            "accesibilidad efectiva, privacidad por diseño y convivencia en el "
            "transporte público."
        ),
        "implementacion_productiva": False,
        "integracion_real_con_organismos": False,
        "modificacion_sistema_sube": False,
        "procesa_datos_medicos": False,
        "procesa_datos_identificatorios": False,
        "documentacion": "/docs",
        "health": "/health",
        "guardrails": "/project/guardrails",
    }


@app.get("/health")
def health():
    """
    Endpoint simple de salud del servicio demostrativo.
    """

    return {
        "status": "ok",
        "service": "sube-prioridad-api",
        "environment": "mvp-conceptual",
        "datos_sensibles_procesados": False,
        "integracion_real_con_organismos": False,
        "implementacion_productiva": False,
    }


@app.get("/project/guardrails")
def project_guardrails():
    """
    Endpoint público de guardrails institucionales y técnicos.

    Sirve para que cualquier persona, autoridad, desarrollador o evaluador
    pueda verificar los límites declarados del MVP.
    """

    return {
        "naturaleza": "MVP conceptual, técnico y demostrativo",
        "implementacion_productiva": False,
        "integracion_real_con_organismos": False,
        "modificacion_sistema_sube": False,
        "procesamiento_datos_medicos": False,
        "procesamiento_datos_identificatorios": False,
        "principios": [
            "privacidad por diseño",
            "minimización de datos",
            "no exposición de diagnósticos",
            "atributo técnico de prioridad",
            "separación entre acreditación institucional y operación técnica",
            "interoperabilidad simulada",
            "gradualidad",
            "reversibilidad",
            "auditabilidad",
            "neutralidad tecnológica",
            "accesibilidad efectiva",
            "asistencia preventiva",
            "no discriminación",
            "no sustitución de asientos prioritarios",
            "no imposición de nuevas cargas al chofer",
        ],
        "datos_no_procesados_en_core": [
            "DNI",
            "nombre",
            "apellido",
            "domicilio",
            "diagnóstico médico",
            "historia clínica",
            "certificado médico en texto plano",
            "datos de salud identificables",
            "condición médica específica",
            "documentación sanitaria",
        ],
        "integraciones": {
            "sube": "no integrada en este MVP",
            "mi_argentina": "no integrada en este MVP",
            "nacion_servicios": "no integrada en este MVP",
            "cnrt": "no integrada en este MVP",
            "andis": "no integrada en este MVP",
            "renaper": "no integrada en este MVP",
            "sisa": "no integrada en este MVP",
        },
        "modelo_conceptual": [
            "necesidad previamente acreditada",
            "atributo técnico de prioridad",
            "preferencia de asistencia",
            "validación operativa",
            "alerta genérica o asistencia preventiva",
            "evaluación institucional",
        ],
    }


@app.post(
    "/api/v1/prioridad/verificar",
    response_model=VerificacionPrioridadResponse,
)
def verificar_prioridad(request: VerificacionPrioridadRequest):
    """
    Verificación conceptual de prioridad.

    La lógica es deliberadamente simple porque el endpoint pertenece a un MVP
    conceptual. No consulta organismos reales, no valida certificados médicos,
    no procesa identidad real y no modifica ningún sistema de transporte.

    Regla demostrativa:
    - Si el token contiene la palabra "activa", y no contiene "inactiva" ni
      "inactive", se devuelve prioridad activa.
    - En cualquier otro caso, se devuelve prioridad inactiva.
    """

    token_normalizado = request.token_prioridad.strip().lower()

    prioridad_activa = (
        "activa" in token_normalizado
        and "inactiva" not in token_normalizado
        and "inactive" not in token_normalizado
    )

    if prioridad_activa:
        return VerificacionPrioridadResponse(
            prioridad_activa=True,
            perfil_ux="preventiva",
            fecha_caducidad=str(date.today().replace(year=date.today().year + 1)),
            motivo="Atributo técnico de prioridad activo en entorno MVP conceptual.",
            entorno="mvp-conceptual",
            datos_sensibles_procesados=False,
            integracion_real_con_organismos=False,
        )

    return VerificacionPrioridadResponse(
        prioridad_activa=False,
        perfil_ux="sin_prioridad_operativa",
        fecha_caducidad=None,
        motivo="No se registra atributo técnico activo en la simulación del MVP.",
        entorno="mvp-conceptual",
        datos_sensibles_procesados=False,
        integracion_real_con_organismos=False,
    )
