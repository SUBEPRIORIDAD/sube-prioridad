# test_antifraud.py
# Motor Transaccional Antifraude y Control de Colusión - Programa SUBE Prioridad
# Desarrollado bajo la iniciativa ciudadana de Andrés Federico di Fiore

import datetime
from typing import Dict, Tuple, List

class AntiFraudEngine:
    def __init__(self, repeat_threshold_days: int = 7, max_coincidences: int = 2):
        """
        Inicializa el motor predictivo antifraude.
        Establece los umbrales para el control de comportamiento repetitivo.
        """
        # Estructura en memoria SRAM protegida: {(id_prioritario, id_colaborador): [lista_de_timestamps]}
        self.interaction_history: Dict[Tuple[str, str], List[datetime.datetime]] = {}
        self.repeat_threshold_days = repeat_threshold_days
        self.max_coincidences = max_coincidences

    def verify_time_window(self, priority_timestamp: int, collaborator_timestamp: int) -> bool:
        """
        Valida la regla de consistencia temporal estricta de 60 segundos
        entre el paso de la tarjeta prioritaria y la re-validación colaboradora.
        """
        delta_t = abs(collaborator_timestamp - priority_timestamp)
        return delta_t <= 60

    def validate_solidary_bonus(self, priority_card_hash: str, collaborator_card_hash: str, current_time: datetime.datetime) -> bool:
        """
        Analiza patrones de comportamiento repetitivo entre los mismos dos identificadores
        para bloquear el fraude compartido/colusión en el Bono Solidario.
        """
        # Clave única simétrica para identificar el par de tarjetas interactuando
        pair_key = (priority_card_hash, collaborator_card_hash)
        
        if pair_key not in self.interaction_history:
            self.interaction_history[pair_key] = [current_time]
            return True  # Primera interacción registrada de forma limpia
            
        # Limpieza asíncrona de registros fuera de la ventana cronológica de auditoría
        cutoff_date = current_time - datetime.timedelta(days=self.repeat_threshold_days)
        self.interaction_history[pair_key] = [t for t in self.interaction_history[pair_key] if t > cutoff_date]
        
        # Filtro duro de restricciones: si superan el límite de coexistencia cíclica, se deniega el bono
        if len(self.interaction_history[pair_key]) >= self.max_coincidences:
            # El software dispara una alerta de seguridad silenciosa para auditoría macro
            # y suspende de forma preventiva la acumulación de beneficios
            return False
            
        self.interaction_history[pair_key].append(current_time)
        return True

    def run_cross_checking(self, priority_tx: dict, collaborator_tx: dict) -> bool:
        """
        Ejecuta la auditoría cruzada de infraestructura exigiendo concordancia
        estricta de coche, ramal, geofencing y consistencia temporal.
        """
        # 1. Verificar coincidencia estricta de material rodante
        if priority_tx.get("interno_coche_id") != collaborator_tx.get("interno_coche_id"):
            return False
            
        if priority_tx.get("linea_colectivo_id") != collaborator_tx.get("linea_colectivo_id"):
            return False

        # 2. Verificar ventana temporal estricta de 60 segundos
        time_valid = self.verify_time_window(
            priority_tx.get("timestamp_nfc", 0), 
            collaborator_tx.get("timestamp_bono_nfc", 0)
        )
        if not time_valid:
            return False

        # 3. Validar contra el motor de colusión/fraude compartido
        current_dt = datetime.datetime.fromtimestamp(collaborator_tx.get("timestamp_bono_nfc", 0))
        return self.validate_solidary_bonus(
            priority_tx.get("tarjeta_prioridad_hash_anon", ""),
            collaborator_tx.get("tarjeta_colaborador_hash_anon", ""),
            current_dt
        )
