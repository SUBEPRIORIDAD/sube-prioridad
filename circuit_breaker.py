import time

class SubeCircuitBreaker:
    """Implementación del patrón Circuit Breaker para evitar parálisis transaccional por caídas de red."""
    
    def __init__(self):
        self.state = "CLOSED"  # CLOSED (Operación Normal), OPEN (Falla - Modo Contingencia Local)
        self.failure_count = 0
        self.FAILURE_THRESHOLD = 3
        self.cooldown_seconds = 10
        self.last_failure_time = 0.0

    def registrar_intento(self, exito_conexion: bool) -> str:
        """Evalúa dinámicamente el estado del enlace con los buses del Ministerio de Salud."""
        current_time = time.time()

        # Si el circuito está abierto, verifica si expiró el tiempo de enfriamiento
        if self.state == "OPEN":
            if current_time - self.last_failure_time > self.cooldown_seconds:
                self.state = "HALF-OPEN"
                print("🔄 [CIRCUIT BREAKER]: Enlace en modo HALF-OPEN. Intentando reconexión pasiva...")
            else:
                return "CONTINGENCIA_LOCAL_OFFLINE_FORCE"

        if exito_conexion:
            self.failure_count = 0
            self.state = "CLOSED"
            return "INTEGRACION_ONLINE_ESTATAL"
        else:
            self.failure_count += 1
            self.last_failure_time = current_time
            if self.failure_count >= self.FAILURE_THRESHOLD or self.state == "HALF-OPEN":
                self.state = "OPEN"
                print("🚨 [CIRCUIT BREAKER]: Abierto por fallas consecutivas del Bus Central. Modo Aislado Activado.")
                return "CONTINGENCIA_LOCAL_OFFLINE_FORCE"
            return "REINTENTO_EN_PROGRESO"

if __name__ == "__main__":
    breaker = SubeCircuitBreaker()
    print("🛡️ [FILTRO DE CONTROL DE INERCIA]: Probando aislamiento automático ante tres caídas del backend:")
    print(f" Intento 1 (Falla): {breaker.registrar_intento(exito_conexion=False)}")
    print(f" Intento 2 (Falla): {breaker.registrar_intento(exito_conexion=False)}")
    print(f" Intento 3 (Falla): {breaker.registrar_intento(exito_conexion=False)}")
    print(f" Intento 4 (Servidor caído): {breaker.registrar_intento(exito_conexion=False)}")
