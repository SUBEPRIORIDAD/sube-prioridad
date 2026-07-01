from datetime import datetime, timezone
from enum import IntEnum
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field, model_validator

from bono_solidario_simulator import (
    DEFAULT_EVENT_TTL_MINUTES,
    DemoRecognitionLedger,
    SeatType,
    create_demo_solidary_event,
    create_demo_transport_context,
    result_to_dict as bono_result_to_dict,
    simulate_solidary_recognition,
)


APP_NAME = "SUBE Prioridad"
APP_VERSION = "0.3.0"
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
    "demo-priority-attribute-001",
    "demo-priority-attribute-preventive",
    "demo-priority-attribute-visible",
}


DEMO_BONO_SOLIDARIO_LEDGER = DemoRecognitionLedger()


class AssistancePreference(IntEnum):
    """
    Preferencia demostrativa de asistencia.

    No representa clasificación médica.
    No representa diagnóstico.
    No representa CUD.
    """

    SILENCIOSA = 1
    DISCRETA = 2
    PREVENTIVA = 3
    VISIBLE = 4


class VerificationStatus(str):
    VALID = "valid"
    INVALID = "invalid"


class VerificationRequest(BaseModel):
    """
    Solicitud demostrativa de verificación de prioridad.

    El endpoint no acepta DNI, nombre, diagnóstico, CUD ni documentación médica.
    """

    token_prioridad: str = Field(
        ...,
        description=(
            "Token técnico demostrativo de prioridad. "
            "No debe contener DNI, nombre, diagnóstico, CUD ni texto libre."
        ),
        examples=["demo-priority-attribute-001"],
    )
    preferencia_asistencia: Optional[AssistancePreference] = Field(
        default=AssistancePreference.PREVENTIVA,
        description="Preferencia demostrativa de asistencia configurada por el usuario.",
    )
    linea: Optional[str] = Field(
        default=None,
        description="Identificador demostrativo de línea o recorrido.",
        examples=["demo-linea-001"],
    )
    unidad: Optional[str] = Field(
        default=None,
        description="Identificador demostrativo de unidad de transporte.",
        examples=["demo-unidad-001"],
    )

    @model_validator(mode="before")
    @classmethod
    def reject_sensitive_fields(cls, values: Any) -> Any:
        if isinstance(values, dict):
            _assert_no_prohibited_fields(values)
        return values


class VerificationResponse(BaseModel):
    project: str
    version: str
    demo_mode: bool
    status: str
    prioridad_activa: bool
    token_verificado: bool
    motivo: str
    preferencia_asistencia: Optional[AssistancePreference]
    alerta: str
    privacidad: str
    rol_chofer: str
    linea: Optional[str]
    unidad: Optional[str]
    timestamp_utc: str
    advertencias: List[str]


class BonoSolidarioSimulationRequest(BaseModel):
    """
    Solicitud demostrativa del Bono Solidario.

    Este endpoint está separado del core de prioridad.
    No acredita puntos reales.
    No sincroniza con Red SUBE real.
    No otorga beneficios reales.
    """

    event_demo_id: str = Field(
        ...,
        description="Identificador demostrativo único del evento solidario.",
        examples=["demo-solidary-event-api-001"],
    )
    priority_user_token: str = Field(
        ...,
        description="Token demostrativo no sensible del usuario SUBE Prioridad.",
        examples=["demo-priority-user-001"],
    )
    collaborator_token: str = Field(
        ...,
        description="Token demostrativo no sensible del pasajero colaborador.",
        examples=["demo-collaborator-001"],
    )
    priority_user_decides_to_recognize: bool = Field(
        ...,
        description=(
            "Decisión voluntaria del usuario SUBE Prioridad. "
            "Sin esta decisión no hay Bono Solidario."
        ),
        examples=[True],
    )
    seat_type: SeatType = Field(
        default=SeatType.GENERAL_USE,
        description=(
            "Tipo de asiento. El Bono Solidario sólo aplica conceptualmente "
            "a asientos de uso general."
        ),
    )
    voluntary_seat_yield: bool = Field(
        default=True,
        description="Indica si existió una cesión voluntaria de asiento.",
    )
    country: str = Field(
        default="Argentina",
        description="País del contexto demostrativo.",
    )
    vehicle_demo_id: str = Field(
        default="demo-bus-001",
        description="Unidad demostrativa del transporte.",
    )
    route_demo_id: str = Field(
        default="demo-route-001",
        description="Ruta o línea demostrativa.",
    )
    trip_demo_id: str = Field(
        default="demo-trip-001",
        description="Viaje demostrativo.",
    )
    time_window_demo_id: str = Field(
        default="demo-window-001",
        description="Ventana temporal demostrativa.",
    )
    expected_vehicle_demo_id: Optional[str] = Field(
        default=None,
        description="Unidad esperada para validar coincidencia demostrativa.",
    )
    expected_route_demo_id: Optional[str] = Field(
        default=None,
        description="Ruta esperada para validar coincidencia demostrativa.",
    )
    expected_trip_demo_id: Optional[str] = Field(
        default=None,
        description="Viaje esperado para validar coincidencia demostrativa.",
    )
    expected_time_window_demo_id: Optional[str] = Field(
        default=None,
        description="Ventana temporal esperada para validar coincidencia demostrativa.",
    )
    ttl_minutes: int = Field(
        default=DEFAULT_EVENT_TTL_MINUTES,
        ge=1,
        le=60,
        description="Tiempo de vida demostrativo del evento en minutos.",
    )

    @model_validator(mode="before")
    @classmethod
    def reject_sensitive_fields(cls, values: Any) -> Any:
        if isinstance(values, dict):
            _assert_no_prohibited_fields(values)
        return values


class BonoSolidarioSimulationResponse(BaseModel):
    project: str
    module: str
    version: str
    demo_mode: bool
    status: str
    solidary_point_demo: int
    recognition_enabled_by_priority_user: bool
    same_transport_context: bool
    review_required: bool
    risk_flags: List[str]
    reason: str
    privacy_notice: str
    driver_burden: str
    warnings: List[str]
    timestamp_utc: str


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "MVP conceptual y demostrativo de SUBE Prioridad. "
        "No es una implementación oficial. "
        "No integra SUBE real. "
        "No procesa datos sensibles reales."
    ),
)


@app.get("/")
def root() -> Dict[str, Any]:
    return {
        "project": APP_NAME,
        "version": APP_VERSION,
        "demo_mode": DEMO_MODE,
        "status": "ok",
        "description": (
            "Propuesta ciudadana de innovación pública para asistencia preventiva "
            "en transporte público."
        ),
        "core": {
            "priority_verification": "/api/v1/prioridad/verificar",
            "bono_solidario_future_module": "/api/v1/bono-solidario/simular",
        },
        "guardrails": [
            "No implementación oficial vigente.",
            "No integración real con SUBE.",
            "No conexión real con organismos públicos.",
            "No procesamiento de DNI, diagnóstico, CUD ni datos médicos.",
            "Bono Solidario separado del token de prioridad.",
        ],
    }


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "project": APP_NAME,
        "version": APP_VERSION,
        "demo_mode": DEMO_MODE,
        "timestamp_utc": _now_utc(),
    }


@app.get("/project/guardrails")
def project_guardrails() -> Dict[str, Any]:
    return {
        "project": APP_NAME,
        "version": APP_VERSION,
        "demo_mode": DEMO_MODE,
        "guardrails": [
            "SUBE Prioridad es una propuesta conceptual y demostrativa.",
            "No es una implementación oficial vigente.",
            "No modifica el sistema SUBE real.",
            "No modifica validadoras reales.",
            "No procesa DNI.",
            "No procesa nombre ni apellido.",
            "No procesa domicilio.",
            "No procesa diagnóstico.",
            "No procesa historia clínica.",
            "No procesa CUD.",
            "No procesa certificados médicos.",
            "No reemplaza los asientos prioritarios legales.",
            "No traslada cargas operativas al chofer.",
            "No genera vigilancia.",
            "No genera rankings de pasajeros.",
            "No genera sanciones.",
            "El Bono Solidario es un módulo futuro, opcional y separado.",
            "El Bono Solidario queda en manos del usuario SUBE Prioridad.",
        ],
    }


@app.post(
    "/api/v1/prioridad/verificar",
    response_model=VerificationResponse,
)
def verificar_prioridad(request: VerificationRequest) -> VerificationResponse:
    """
    Verifica un atributo técnico demostrativo de prioridad.

    Este endpoint no interpreta texto libre.
    Este endpoint no activa prioridad por frases como bono solidario,
    tarifa social, beneficio vigente o viajar gratis.
    """
    token = request.token_prioridad.strip()

    if _looks_like_free_text_or_benefit(token):
        return _invalid_priority_response(
            request=request,
            motivo=(
                "El valor recibido parece texto libre, beneficio tarifario o frase descriptiva. "
                "La prioridad no se activa por palabras mágicas ni por menciones a Bono Solidario, "
                "tarifa social o beneficios. Debe utilizarse un atributo técnico demostrativo "
                "previamente emitido."
            ),
        )

    if token not in DEMO_PRIORITY_REGISTRY:
        return _invalid_priority_response(
            request=request,
            motivo=(
                "No se registra un atributo técnico demostrativo de prioridad para el token informado. "
                "El MVP evita falsos positivos y no presume prioridad por texto libre."
            ),
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
            "La prioridad activa no revela diagnóstico ni documentación sensible."
        ),
        preferencia_asistencia=request.preferencia_asistencia,
        alerta=_build_priority_alert(request.preferencia_asistencia),
        privacidad=(
            "El transporte sólo recibe una señal genérica de asistencia. "
            "No recibe DNI, nombre, diagnóstico, CUD, historia clínica ni certificado médico."
        ),
        rol_chofer=(
            "El personal de conducción no debe diagnosticar, validar documentación médica "
            "ni administrar beneficios."
        ),
        linea=request.linea,
        unidad=request.unidad,
        timestamp_utc=_now_utc(),
        advertencias=_common_priority_warnings(),
    )


@app.post(
    "/api/v1/bono-solidario/simular",
    response_model=BonoSolidarioSimulationResponse,
)
def simular_bono_solidario(
    request: BonoSolidarioSimulationRequest,
) -> BonoSolidarioSimulationResponse:
    """
    Simula el módulo futuro de Bono Solidario.

    El Bono Solidario está separado de la prioridad.
    No activa prioridad.
    No otorga puntos reales.
    No sincroniza con Red SUBE real.
    """
    actual_context = create_demo_transport_context(
        country=request.country,
        vehicle_demo_id=request.vehicle_demo_id,
        route_demo_id=request.route_demo_id,
        trip_demo_id=request.trip_demo_id,
        time_window_demo_id=request.time_window_demo_id,
    )

    expected_context = create_demo_transport_context(
        country=request.country,
        vehicle_demo_id=request.expected_vehicle_demo_id or request.vehicle_demo_id,
        route_demo_id=request.expected_route_demo_id or request.route_demo_id,
        trip_demo_id=request.expected_trip_demo_id or request.trip_demo_id,
        time_window_demo_id=(
            request.expected_time_window_demo_id or request.time_window_demo_id
        ),
    )

    event = create_demo_solidary_event(
        event_demo_id=request.event_demo_id,
        priority_user_token=request.priority_user_token,
        collaborator_token=request.collaborator_token,
        priority_user_decides_to_recognize=request.priority_user_decides_to_recognize,
        seat_type=request.seat_type,
        voluntary_seat_yield=request.voluntary_seat_yield,
        transport_context=actual_context,
        ttl_minutes=request.ttl_minutes,
    )

    result = simulate_solidary_recognition(
        event=event,
        expected_context=expected_context,
        ledger=DEMO_BONO_SOLIDARIO_LEDGER,
    )

    return BonoSolidarioSimulationResponse(**bono_result_to_dict(result))


def _invalid_priority_response(
    request: VerificationRequest,
    motivo: str,
) -> VerificationResponse:
    return VerificationResponse(
        project=APP_NAME,
        version=APP_VERSION,
        demo_mode=DEMO_MODE,
        status=VerificationStatus.INVALID,
        prioridad_activa=False,
        token_verificado=False,
        motivo=motivo,
        preferencia_asistencia=request.preferencia_asistencia,
        alerta=(
            "No se emite alerta de prioridad porque el atributo técnico demostrativo "
            "no fue verificado."
        ),
        privacidad=(
            "No se procesa información sensible. "
            "No se infiere diagnóstico ni condición personal."
        ),
        rol_chofer=(
            "El personal de conducción no debe resolver la validez de tokens, "
            "beneficios o condiciones personales."
        ),
        linea=request.linea,
        unidad=request.unidad,
        timestamp_utc=_now_utc(),
        advertencias=_common_priority_warnings(),
    )


def _build_priority_alert(
    preference: Optional[AssistancePreference],
) -> str:
    if preference == AssistancePreference.SILENCIOSA:
        return (
            "Registro interno demostrativo sin alerta visible. "
            "La asistencia queda limitada a la preferencia silenciosa del usuario."
        )

    if preference == AssistancePreference.DISCRETA:
        return (
            "Alerta discreta demostrativa: podría requerirse asistencia preventiva "
            "sin exponer datos personales."
        )

    if preference == AssistancePreference.VISIBLE:
        return (
            "Alerta visible demostrativa: solicitud genérica de colaboración preventiva "
            "sin revelar diagnóstico."
        )

    return (
        "Alerta preventiva demostrativa: una persona podría requerir viajar sentada "
        "o recibir colaboración voluntaria."
    )


def _looks_like_free_text_or_benefit(token: str) -> bool:
    normalized = token.lower().strip()

    suspicious_terms = {
        "bono",
        "solidario",
        "tarifa",
        "social",
        "beneficio",
        "vigente",
        "gratis",
        "viajar",
        "cud",
        "andis",
        "medico",
        "médico",
        "diagnostico",
        "diagnóstico",
        "certificado",
        "sancion",
        "sanción",
        "ranking",
    }

    if any(term in normalized for term in suspicious_terms):
        return True

    if len(normalized.split()) > 1:
        return True

    return False


def _assert_no_prohibited_fields(payload: Dict[str, Any]) -> None:
    normalized_keys = {str(key).strip().lower() for key in payload.keys()}
    forbidden = sorted(normalized_keys.intersection(PROHIBITED_FIELDS))

    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para SUBE Prioridad: "
            + ", ".join(forbidden)
        )


def _common_priority_warnings() -> List[str]:
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
        "Bono Solidario separado del token de prioridad.",
    ]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()
