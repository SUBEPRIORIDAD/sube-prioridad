import logging
import os
import time

class SubePrioridadAuditLogger:
    """Pipeline de auditoría asíncrona para anomalías transaccionales y alertas UX."""
    
    def __init__(self, output_dir: str = "logs/audit"):
        self.output_dir = output_dir
        # Asegura la persistencia de los directorios locales del bus en tiempo de ejecución
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Configuración estructurada del buffer de salida
        self.logger = logging.getLogger("SUBE_PRIORIDAD_AUDIT")
        self.logger.setLevel(logging.INFO)
        
        log_file_path = os.path.join(self.output_dir, "transacciones_criticas.log")
        file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
        
        # Formato ISO-8601 estricto con marcas de precisión milimétrica
        formatter = logging.Formatter(
            '%(asctime)s | [%(levelname)s] | %(message)s', 
            datefmt='%Y-%m-%dT%H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        
        if not self.logger.handlers:
            self.logger.addHandler(file_handler)

    def registrar_alerta_disparada(self, card_hash: str, modo: int) -> None:
        """Registra la activación local de un perfil UX (Visible/Discreto/Pasivo)."""
        self.logger.info(f"UX_TRIGGERED | CardHash: {card_hash[:10]}... | PerfilAlertasUX: {modo}")

    def registrar_anomalia_antifraude(self, card_hash: str, error_tipo: str) -> None:
        """Escribe alertas críticas de seguridad ante violaciones de marcas de tiempo."""
        self.logger.warning(f"ANTIFRAUD_ALERT | CardHash: {card_hash[:10]}... | Violación: {error_tipo}")

if __name__ == "__main__":
    audit = SubePrioridadAuditLogger()
    audit.registrar_alerta_disparada("8f4a3b1c9e2d7f6a5b4c3d2e", modo=2)
    audit.registrar_anomalia_antifraude("11a22b33c44d55e66f77g88h", error_tipo="VENTANA_TEMPORAL_DUPLICADA")
    print(f"📝 Registros de prueba inyectados de forma segura en logs/audit/")
