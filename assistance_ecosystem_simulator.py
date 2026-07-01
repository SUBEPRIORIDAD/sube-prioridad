"""
SUBE Prioridad — Puente conceptual de ecosistema de asistencia.

Este archivo queda como módulo estable de compatibilidad para CI.

La lógica principal de blindaje entre usuario SUBE Prioridad y pasajero que
cede asiento se desarrolla en módulos separados, más específicos y auditables.

No representa implementación oficial.
No integra SUBE real.
No integra Red SUBE real.
No procesa datos sensibles.
No impone cargas al chofer.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List


PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Ecosistema de Asistencia"
SIMULATOR_VERSION = "0.1.1"
DEMO_MODE = True


def run_demo() -> Dict[str, Any]:
    """
    Ejecuta una demostración mínima y estable del ecosistema conceptual.

    La finalidad de este módulo es no romper CI mientras la lógica de seguridad
    se desarrolla en flujos separados.
    """
    return {
        "project": PROJECT_NAME,
        "module": MODULE_NAME,
        "version": SIMULATOR_VERSION,
        "demo_mode": DEMO_MODE,
        "priority_active": True,
        "previously_accredited_need": True,
        "sequence_status": "ready",
        "assistance_mode": "passive",
        "alert_plan": {
            "visibility": "passive",
            "message": (
                "Alerta pasiva demostrativa: asistencia preventiva sin revelar "
                "diagnóstico, DNI, CUD ni datos médicos."
            ),
            "luminous_enabled": False,
            "driver_action_required": False,
            "passenger_action_required": False,
            "accessibility_resource_ping": False,
        },
        "sync_result": {
            "sync_status": "simulated_sync",
            "synchronized_nodes": [
                "priority_attribute",
                "user_preferences",
                "validator_edge",
                "transport_unit",
            ],
            "degraded_nodes": [],
            "reason": (
                "Sincronización conceptual mínima. No existe integración real "
                "con SUBE ni Red SUBE."
            ),
        },
        "privacy_notice": (
            "La secuencia no revela DNI, nombre, domicilio, diagnóstico, CUD, "
            "historia clínica ni certificado médico."
        ),
        "driver_burden": (
            "El personal de conducción no diagnostica, no valida documentación, "
            "no administra beneficios y no decide la prioridad."
        ),
        "warnings": _common_warnings(),
        "timestamp_utc": _now_utc(),
    }


def _common_warnings() -> List[str]:
    return [
        "Módulo conceptual y demostrativo.",
        "Sin implementación oficial vigente.",
        "Sin integración real con SUBE.",
        "Sin integración real con Red SUBE.",
        "Sin integración real con organismos públicos.",
        "Sin modificación de validadoras reales.",
        "Sin geolocalización real.",
        "Sin procesamiento de datos sensibles.",
        "Sin diagnóstico médico.",
        "Sin CUD real.",
        "Sin sanciones.",
        "Sin ranking.",
        "Sin vigilancia.",
        "Sin obligación para pasajeros.",
        "Sin carga operativa para el chofer.",
        "El usuario conserva control sobre el modo de asistencia.",
    ]


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    import json

    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
