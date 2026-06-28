import concurrent.futures
import random
import time
from validator import SubePrioridadValidator

class SubeLoadSimulator:
    """Motor de simulación de carga estocástica para validación de concurrencia y paralelismo."""
    
    def __init__(self, total_usuarios: int = 50):
        self.validator = SubePrioridadValidator()
        self.total_usuarios = total_usuarios

    def _simular_pasajero(self, user_index: int) -> dict:
        """Genera un evento de pasaje sintético con atributos aleatorios de prioridad."""
        card_id = f"SUBE_SIM_CARD_{1000 + user_index}"
        # Simula de forma probabilística un 15% de usuarios prioritarios en el flujo
        is_priority = random.random() < 0.15
        
        # Ejecuta la transacción a través de la lógica del firmware
        return self.validator.process_transaction(card_id, is_priority_user=is_priority)

    def ejecutar_estres_hora_pico(self):
        """Dispara hilos concurrentes simulando molinetes y validadoras operando en paralelo."""
        print(f"⚡ Iniciando prueba de estrés: {self.total_usuarios} transacciones concurrentes...")
        
        exitos = 0
        bonos_encolados = 0
        
        # Utiliza un pool de hilos para simular concurrencia real sobre la memoria del sistema
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futuros = [executor.submit(self._simular_pasajero, i) for i in range(self.total_usuarios)]
            
            for futuro in concurrent.futures.as_completed(futuros):
                try:
                    resultado = futuro.result()
                    exitos += 1
                    if resultado["bono_eligible"]:
                        bonos_encolados += 1
                except Exception as e:
                    print(f"❌ Error en hilo de simulación: {e}")
                    
        print(f"📊 [STRESS TEST COMPLETED]: {exitos}/{self.total_usuarios} pasajes procesados de forma segura.")
        print(f"🎮 Ventanas causales del Bono Solidario abiertas y consolidadas: {bonos_encolados}")

if __name__ == "__main__":
    simulador = SubeLoadSimulator(total_usuarios=100)
    simulador.ejecutar_estres_hora_pico()
