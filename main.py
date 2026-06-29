from datetime import date
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
title="SUBE Prioridad API",
description=(
"MVP conceptual y demostrativo para asistencia preventiva, "
"accesibilidad efectiva y privacidad por diseño en transporte público."
),
version="0.1.0",
)

class VerificacionPrioridadRequest(BaseModel):
"""
Solicitud conceptual de verificación.

```
Este MVP no recibe DNI, nombre, apellido, diagnóstico médico,
historia clínica ni certificados médicos en texto plano.

El campo token_prioridad representa un identificador técnico,
pseudoanonimizado o simulado para fines demostrativos.
"""

token_prioridad: str = Field(
    ...,
    description="Token técnico o identificador pseudoanonimizado de prioridad.",
    examples=["demo-prioridad-activa"],
)

linea: Optional[str] = Field(
    default=None,
    description="Línea de transporte, sólo para simulación o evaluación técnica.",
    examples=["60"],
)

unidad: Optional[str] = Field(
    default=None,
    description="Unidad o interno, sólo para simulación o evaluación técnica.",
    examples=["1234"],
)
```

class VerificacionPrioridadResponse(BaseModel):
"""
Respuesta conceptual de verificación.

```
La respuesta no informa diagnósticos, condiciones médicas,
datos personales identificables ni motivos sensibles.
"""

prioridad_activa: bool
perfil_ux: str
fecha_caducidad: Optional[str]
motivo: str
entorno: str
datos_sensibles_procesados: bool
integracion_real_con_organismos: bool
```

@app.get("/")
def root():
"""
Endpoint raíz del MVP.

```
Expone el estado conceptual del proyecto sin afirmar implementación
productiva ni integración real con sistemas externos.
"""

return {
    "proyecto": "SUBE Prioridad",
    "estado": "MVP conceptual y demostrativo",
    "descripcion": (
        "Propuesta ciudadana de innovación pública para asistencia preventiva, "
        "accesibilidad efectiva y convivencia en el transporte público."
    ),
    "implementacion_productiva": False,
    "integracion_real_con_organismos": False,
    "procesa_datos_medicos": False,
    "documentacion": "/docs",
}
```

@app.get("/health")
def health():
"""
Endpoint de salud del servicio.

```
Se utiliza para verificación técnica básica del MVP.
"""

return {
    "status": "ok",
    "service": "sube-prioridad-api",
    "environment": "mvp-conceptual",
    "datos_sensibles_procesados": False,
    "integracion_real_con_organismos": False,
}
```

@app.get("/project/guardrails")
def project_guardrails():
"""
Devuelve límites conceptuales y técnicos del MVP.

```
Este endpoint ayuda a mantener alineado el código con la documentación
institucional del proyecto.
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
    ],
}
```

@app.post("/api/v1/prioridad/verificar", response_model=VerificacionPrioridadResponse)
def verificar_prioridad(request: VerificacionPrioridadRequest):
"""
Verificación conceptual de prioridad.

```
Este endpoint no consulta organismos reales, no accede al sistema SUBE,
no procesa datos médicos y no representa una implementación productiva.

Para fines demostrativos:
- tokens que contengan "activa" devuelven prioridad activa;
- tokens que contengan "inactive" o "inactiva" devuelven prioridad inactiva;
- cualquier otro token se considera no activo en el MVP.
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
```
