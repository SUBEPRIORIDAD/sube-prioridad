import time
from typing import Dict, Optional

class SubePrioridadValidator:
    def __init__(self):
        # Almacena el último evento de prioridad activo localmente en la validadora
        self.active_priority_event: Optional[Dict[str, float]] = None
        self.WINDOW_THRESHOLD_SECONDS = 60.0

    def process_transaction(self, card_id: str, is_priority_user: bool) -> dict:
        current_timestamp = time.time()
        
        # CASO A: El usuario posee el atributo de prioridad activo en su tarjeta MIFARE
        if is_priority_user:
            self.active_priority_event = {
                "priority_card_id": card_id,
                "timestamp": current_timestamp
            }
            return {
                "status": "APPROVED",
                "action": "TRIGGER_DISCRET_ALERT",
                "msg": "Alerta de asiento prioritario enviada de forma local al habitáculo.",
                "bono_eligible": False
            }
        
        # CASO B: Transacción ordinaria. Se evalúa la ventana temporal previa
        if self.active_priority_event:
            time_delta = current_timestamp - self.active_priority_event["timestamp"]
            
            if time_delta <= self.WINDOW_THRESHOLD_SECONDS:
                priority_id = self.active_priority_event["priority_card_id"]
                self.active_priority_event = None # Reset de la ventana temporal local
                
                return {
                    "status": "APPROVED",
                    "action": "QUEUE_FOR_CLEARING",
                    "msg": f"Boleto común procesado dentro de delta t ({time_delta:.2f}s).",
                    "bono_eligible": True,
                    "meta": {"cooperating_card": card_id, "associated_priority_card": priority_id}
                }
        
        # CASO C: Transacción común fuera de la ventana de prioridad
        return {
            "status": "APPROVED",
            "action": "STANDARD_FLUID_TRANSACTION",
            "msg": "Transacción base procesada de forma regular.",
            "bono_eligible": False
        }

# --- EJECUCIÓN SIMULADA DE LABORATORIO ---
if __name__ == "__main__":
    validator = SubePrioridadValidator()
    
    print("--- Simulación de Procesamiento Local de Firmware ---")
    # 1. Pasa tarjeta prioritaria por el bus local
    print(f"[Evento 1]: {validator.process_transaction('SUBE_PRO_9982', is_priority_user=True)['msg']}")
    
    # 2. Pasajero común cede asiento y paga 3 segundos después
    time.sleep(3) 
    resultado = validator.process_transaction("SUBE_COM_1143", is_priority_user=False)
    print(f"[Evento 2]: {resultado['msg']}")
    print(f" > ¿Elegible para Bono Solidario en el clearing diario?: {resultado['bono_eligible']}")
    print(f" > Acción en cola de transacciones (Batch): {resultado['action']}")
