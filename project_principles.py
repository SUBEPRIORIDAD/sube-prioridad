"""
Principios rectores del MVP SUBE Prioridad.

Este módulo centraliza definiciones institucionales y técnicas para evitar
que los distintos componentes del repositorio se aparten de la naturaleza
conceptual, gradual, auditable y no definitiva de la propuesta.

No contiene datos personales, diagnósticos, DNI ni información sensible.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Final, Tuple


PROJECT_NAME: Final[str] = "SUBE Prioridad"
PROJECT_STAGE: Final[str] = "MVP conceptual y demostrativo"
PROJECT_SCOPE: Final[str] = (
    "Herramienta de asistencia preventiva para facilitar el acceso respetuoso "
    "a un asiento a personas con necesidad acreditada de viajar sentadas."
)


class ModuleStatus(str, Enum):
    MVP_CORE = "mvp_core"
    FUTURE_EVOLUTION = "future_evolution"
    SIMULATED_INTEGRATION = "simulated_integration"
    DOCUMENTATION_ONLY = "documentation_only"


@dataclass(frozen=True)
class ProjectGuardrails:
    no_personal_data_in_core: bool = True
    no_medical_diagnosis_in_core: bool = True
    no_driver_operational_burden: bool = True
    no_passenger_sanctions: bool = True
    no_revenue_system_modification: bool = True
    no_priority_seat_regime_modification: bool = True
    voluntary_solidarity_only: bool = True
    progressive_implementation: bool = True
    authority_driven_feasibility: bool = True


GUARDRAILS: Final[ProjectGuardrails] = ProjectGuardrails()
PROHIBITED_CORE_DATA: Final[Tuple[str, ...]] = (
    "dni",
    "nombre",
    "apellido",
    "domicilio",
    "historia_clinica",
    "diagnostico_medico",
    "certificado_medico_texto_plano",
    "identidad_real_pasajero_colaborador",
)


MVP_CORE_MODULES: Final[Tuple[str, ...]] = (
    "priority_attribute",
    "privacy_preserving_validation",
    "user_assistance_preferences",
    "health_check",
    "audit_without_personal_data",
)


FUTURE_EVOLUTION_MODULES: Final[Tuple[str, ...]] = (
    "bono_solidario",
    "symbolic_recognition",
    "fare_discount_experiment",
    "predictive_antifraud",
    "geofencing_contextual_validation",
)


SIMULATED_EXTERNAL_SERVICES: Final[Tuple[str, ...]] = (
    "ANDIS",
    "SISA",
    "RENAPER",
    "Mi Argentina",
    "Nacion Servicios",
    "CNRT",
)


# Rutas de gobernanza e infraestructura incorporadas para la Fase II de Homologación
DOCUMENTACION_GOBERNANZA_CORE: Final[Tuple[str, ...]] = (
    "./DOC_INTEROPERABILIDAD.md",
    "./TECHNICAL_ROADMAP_NACION_SERVICIOS.md",
)
def assert_safe_payload(payload: dict) -> None:
    """
    Verifica que un payload técnico no incluya campos prohibidos en el core.

    Esta función no reemplaza una auditoría de seguridad real.
    Sirve como control defensivo mínimo para el MVP.
    """

    normalized_keys = {str(key).lower() for key in payload.keys()}

    forbidden = [
        field for field in PROHIBITED_CORE_DATA if field.lower() in normalized_keys
    ]

    if forbidden:
        raise ValueError(
            "El payload contiene campos prohibidos para el core del MVP: "
            + ", ".join(forbidden)
        )


def describe_project() -> dict:
    return {
        "name": PROJECT_NAME,
        "stage": PROJECT_STAGE,
        "scope": PROJECT_SCOPE,
        "guardrails": GUARDRAILS.__dict__,
        "mvp_core_modules": MVP_CORE_MODULES,
        "future_evolution_modules": FUTURE_EVOLUTION_MODULES,
        "simulated_external_services": SIMULATED_EXTERNAL_SERVICES,
        "documentacion_gobernanza_core": DOCUMENTACION_GOBERNANZA_CORE,
    }


def is_future_evolution_module(module_name: str) -> bool:
    return module_name in FUTURE_EVOLUTION_MODULES


def is_simulated_external_service(service_name: str) -> bool:
    normalized = service_name.strip().lower()
    return any(service.lower() == normalized for service in SIMULATED_EXTERNAL_SERVICES)
