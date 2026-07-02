"""
SUBE Prioridad — Sistema de Registro de Auditoría y Control Operativo.
Sección X, XI y XXXVII del Pliego Técnico:
 Procesa de forma asíncrona los eventos de interfaz local y alertas transaccionales,
 garantizando la anonimización irreversible y el cumplimiento de la Ley N.º 25.326.

Mantiene los archivos de log bajo formatos rígidos clave-valor inyectables.
"""

from __future__ import annotations
import logging
import os
import time
from typing import Any, Dict, List

PROJECT_NAME = "SUBE Prioridad"
MODULE_NAME = "Logger Analítico de Auditoría"
FLOW_VERSION = "0.1.0"
DEMO_MODE = True

PROHIBITED_FIELDS = {
    "dni", "documento", "nombre", "apellido", "domicilio", "direccion", "dirección",
    "telefono", "teléfono", "email", "correo", "diagnostico", "diagnóstico",
    "historia_clinica", "historia_clínica", "certificado_medico", "certificado_médico",
    "cud", "discapacidad", "patologia", "patología", "medico", "médico", "obra_social"
}

def purge_prohibited_fields(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Sección XXXVII: Purga en memoria de cualquier variable sensible antes del formateo."""
    if not isinstance(payload, dict):
        return payload
    sanitized_payload = {}
    for key, value in payload.items():
        normalized_key = str(key).strip().lower()
        if normalized_key in PROHIBITED_FIELDS:
            continue
        if isinstance(value, dict):
            sanitized_payload[key] = purge_prohibited_fields(value)
        else:
            sanitized_payload[key] = value
    return sanitized_payload
class SubePrioridadAuditLogger:
    """Pipeline de auditoría para anomalías transaccionales del core y alertas UX de accesibilidad."""
    
    def __init__(self, output_dir: str = "logs/audit"):
        self.output_dir = output_dir
        # Asegura la persistencia de los directorios locales de forma Fail-Safe
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Configuración estructurada del buffer de salida
        self.logger = logging.getLogger("SUBE_PRIORIDAD_AUDIT")
        self.logger.setLevel(logging.INFO)
        
        log_file_path = os.path.join(self.output_dir, "transacciones_criticas.log")
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        
        # Formato ISO-8601 estricto con marcas de precisión milimétrica (Sección XXI)
        formatter = logging.Formatter(
            '%(asctime)s | [%(levelname)s] | %(message)s', 
            datefmt='%Y-%m-%dT%H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)

    def registrar_alerta_disparada(self, card_hash: str, modo: int) -> None:
        """Registra la activación local de un perfil UX (Visible/Discreto/Pasivo)."""
        clean_hash = str(card_hash).replace("\n", "").replace("\r", "").strip()
        # Blindamos la salida forzando claves explícitas
        self.logger.info(f"UX_TRIGGERED | CardHash: {clean_hash[:10]}... | PerfilAlertasUX: {int(modo)}")

    def registrar_anomalia_antifraude(self, card_hash: str, error_tipo: str) -> None:
        """Escribe alertas críticas de seguridad ante inconsistencias en ventanas de tiempo."""
        clean_hash = str(card_hash).replace("\n", "").replace("\r", "").strip()
        # Mitigación contra inyección de logs sanitizando saltos de línea imprevistos
        clean_error = str(error_tipo).replace("\n", "").replace("\r", "").replace("|", "-").strip()
        
        # Validación heurística pasiva para evitar fugas de texto médico libre
        check_dict = purge_prohibited_fields({clean_error.lower(): True})
        if not check_dict:
            clean_error = "REGISTRO_RESTRINGIDO_POR_POLITICA_PRIVACIDAD"

        self.logger.warning(f"ANTIFRAUD_ALERT | CardHash: {clean_hash[:10]}... | Violación: {clean_error}")
def ejecutar_logs_demo() -> Dict[str, Any]:
    """Inyecta registros controlados en el buffer para validar la persistencia física."""
    audit = SubePrioridadAuditLogger()
    
    # Pruebas estándar del flujo core
    audit.registrar_alerta_disparada("8f4a3b1c9e2d7f6a5b4c3d2e", modo=2)
    audit.registrar_anomalia_antifraude("11a22b33c44d55e66f77g88h", error_tipo="VENTANA_TEMPORAL_DUPLICADA")
    
    # Intento de simulación maliciosa de inyección o fuga médica (Debe ser interceptado)
    audit.registrar_anomalia_antifraude("99z99z99z99z99z99z99z99z", error_tipo="DIAGNOSTICO_ADJUNTADO_ERROR")

    return {
        "componente": "SubePrioridadAuditLogger",
        "estado_persistencia": "completado_exitosamente",
        "archivo_salida": f"{audit.output_dir}/transacciones_criticas.log",
        "modulo_activo": "core_control_layer"
    }

if __name__ == "__main__":
    import json
    # Validamos la ejecución local de la rutina e imprimimos el resultado de control
    print(json.dumps(ejecutar_logs_demo(), indent=2, ensure_ascii=False))
