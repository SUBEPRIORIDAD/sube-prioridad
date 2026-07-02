import time
from datetime import datetime, timedelta, timezone
from validator import AntifraudValidator, EventoValidacion, HardwareTargetKind

class SubeCompletePerformanceSuite:
    """Suite integralizada de control de latencia, stress, clonación y cross-checking."""
    
    def __init__(self):
        # Inicialización del motor core analítico real bajo especificaciones del pliego
        self.validator = AntifraudValidator(
            ventana_minutos=10,
            max_eventos_por_ventana=3,
            max_score_permitido=70
        )

    def verificar_cross_checking(self, ev_prioritario: EventoValidacion, ev_colaborador: EventoValidacion) -> dict:
        """Aplica la regla del Art 99: Compara metadatos de ambas tarjetas para mitigar fraudes."""
        alertas = []
        score = 0
        permitido = True
        
        # 1. Validación de infraestructura idéntica
        if ev_prioritario.linea != ev_colaborador.linea or ev_prioritario.unidad != ev_colaborador.unidad:
            alertas.append("falso_registro_coincidencia_infraestructura")
            score = 50
            permitido = False
            
        # 2. Validación de ventana cronológica de co-presencia física (< 10 minutos)
        delta_tiempo = abs((ev_prioritario.timestamp - ev_colaborador.timestamp).total_seconds())
        if delta_tiempo > 600:
            alertas.append("violacion_ventana_simultaneidad_temporal")
            score = 60
            permitido = False
            
        return {"alertas": alertas, "score_riesgo": score, "permitido": permitido}
    def probar_latencia_basica(self):
        """PRUEBA 1: Mide la velocidad de respuesta en una transacción feliz estándar."""
        print("\n⏱️  [PRUEBA 1] Evaluando velocidad base del motor lógico...")
        print("=" * 75)
        evento = EventoValidacion(
            tarjeta_id="token-bench-card-normal", linea="60", unidad="2415",
            timestamp=datetime.now(timezone.utc), tipo_evento="validacion",
            hardware_origen=HardwareTargetKind.COLECTIVO_EDGE_OFFLINE
        )
        t_start = time.perf_counter_ns()
        resultado = self.validator.validar_evento(evento)
        t_end = time.perf_counter_ns()
        latency_ms = (t_end - t_start) / 1_000_000.0
        print(f"Latencia Motor Lógico (Borde): {latency_ms:.4f} ms")
        print(f"Acción de Hardware Registrada: {resultado.hardware_action}")
        print("=" * 75)

    def probar_stress_temporal(self):
        """PRUEBA 2: Simula una ráfaga de 5 pasadas consecutivas para saturar la ventana."""
        print("\n⚡ [PRUEBA 2] Iniciando stress analítico por saturación de ventana...")
        print("=" * 75)
        ahora = datetime.now(timezone.utc)
        tarjeta_id_prueba = "stress-test-card-999"
        for i in range(1, 6):
            evento = EventoValidacion(
                tarjeta_id=tarjeta_id_prueba, linea="60", unidad="2415",
                timestamp=ahora + timedelta(seconds=i * 2), tipo_evento="validacion",
                hardware_origen=HardwareTargetKind.COLECTIVO_EDGE_OFFLINE
            )
            resultado = self.validator.validar_y_registrar(evento)
            print(f"Pasada #{i} | Score Riesgo: {resultado.score_riesgo} | Permitido: {resultado.permitido}")
            if resultado.alertas:
                print(f"   ⚠️  Alertas: {resultado.alertas} | ⚙️  Acción: {resultado.hardware_action}")
        print("=" * 75)

    def probar_tarjeta_clonada_imposible(self):
        """PRUEBA 3: Simula la misma tarjeta en dos colectivos distintos en un delta de 3 segundos."""
        print("\n🚨 [PRUEBA 3] Ejecutando detección de Tarjeta Clonada (Viaje Imposible)...")
        print("=" * 75)
        ahora = datetime.now(timezone.utc)
        tarjeta_clon = "clone-fraud-card-111"
        evento_legal = EventoValidacion(
            tarjeta_id=tarjeta_clon, linea="60", unidad="2415",
            timestamp=ahora, tipo_evento="validacion", hardware_origen=HardwareTargetKind.COLECTIVO_EDGE_OFFLINE
        )
        self.validator.validar_y_registrar(evento_legal)
        evento_ataque = EventoValidacion(
            tarjeta_id=tarjeta_clon, linea="60", unidad="8888",
            timestamp=ahora + timedelta(seconds=3), tipo_evento="validacion", hardware_origen=HardwareTargetKind.COLECTIVO_EDGE_OFFLINE
        )
        resultado_ataque = self.validator.validar_y_registrar(evento_ataque)
        print(f"Pasada B | Coche 8888 | Score Riesgo: {resultado_ataque.score_riesgo} | Permitido: {resultado_ataque.permitido}")
        print(f"   ⚠️  Alertas de Red: {resultado_ataque.alertas}")
        print("=" * 75)
    def probar_cross_checking_coincidencia(self):
        """PRUEBA 4 VITAL: Sección XLVIII, Art 99. Validación cruzada de infraestructura y tiempo."""
        print("\n📡 [PRUEBA 4 VITAL] Ejecutando Cross-Checking de Coincidencia Transaccional...")
        print("=" * 75)
        ahora = datetime.now(timezone.utc)
        
        # Escenario A: Intento Fraudulento - Coincidencia de tiempo pero en UNIDADES DISTINTAS
        print("Sub-test 4.A: Mismo tiempo, diferentes colectivos (Inconsistencia física)...")
        ev_pasajero_a = EventoValidacion(
            tarjeta_id="prioridad-user-aaa", linea="60", unidad="2415",
            timestamp=ahora, tipo_evento="validacion", hardware_origen=HardwareTargetKind.COLECTIVO_EDGE_OFFLINE
        )
        ev_colaborador_falso = EventoValidacion(
            tarjeta_id="colaborador-fake-bbb", linea="60", unidad="7777", # Intento de hackeo
            timestamp=ahora + timedelta(seconds=4), tipo_evento="validacion", hardware_origen=HardwareTargetKind.COLECTIVO_EDGE_OFFLINE
        )
        
        res_cross_falso = self.verificar_cross_checking(ev_pasajero_a, ev_colaborador_falso)
        print(f"   Resultado Auditoría Falso -> Alertas: {res_cross_falso['alertas']} | Score: {res_cross_falso['score_riesgo']} | Permitido: {res_cross_falso['permitido']}")
        print("-" * 75)

        # Escenario B: Validación Exitosa - Coincidencia de Línea, Unidad y ventana cronológica lógica a bordo
        print("Sub-test 4.B: Simultaneidad verificada (Línea 60, Unidad 2415, delta < 10s)...")
        ev_pasajero_b = EventoValidacion(
            tarjeta_id="prioridad-user-ccc", linea="60", unidad="2415",
            timestamp=ahora + timedelta(minutes=2), tipo_evento="validacion", hardware_origen=HardwareTargetKind.COLECTIVO_EDGE_OFFLINE
        )
        ev_colaborador_real = EventoValidacion(
            tarjeta_id="colaborador-real-ddd", linea="60", unidad="2415", # Misma unidad exacta
            timestamp=ahora + timedelta(minutes=2, seconds=5), # Delta de 5 segundos
            tipo_evento="validacion", hardware_origen=HardwareTargetKind.COLECTIVO_EDGE_OFFLINE
        )
        
        t_start = time.perf_counter_ns()
        res_cross_real = self.verificar_cross_checking(ev_pasajero_b, ev_colaborador_real)
        t_end = time.perf_counter_ns()
        latency_ms = (t_end - t_start) / 1_000_000.0
        
        print(f"   Procesamiento Cross-Checking Exitoso en: {latency_ms:.4f} ms")
        print(f"   Resultado Auditoría Real -> Alertas: {res_cross_real['alertas']} | Score: {res_cross_real['score_riesgo']} | Permitido: {res_cross_real['permitido']}")
        print("=======================================================================\n")

if __name__ == "__main__":
    suite = SubeCompletePerformanceSuite()
    suite.probar_latencia_basica()
    suite.probar_stress_temporal()
    suite.probar_tarjeta_clonada_imposible()
    suite.probar_cross_checking_coincidencia()
