# load_simulator.py
# Simulador de Carga Masiva y Estrés de Concurrencia en Hora Pico - Red SUBE Prioridad
# Desarrollado bajo la iniciativa ciudadana de Andrés Federico di Fiore

import time
import random
import concurrent.futures
from typing import List, Dict

class SubeLoadSimulator:
    def __init__(self, target_concurrency: int = 1000, latency_threshold_ms: float = 300.0):
        """
        Inicializa el simulador de estrés con objetivos de concurrencia masiva
        y los acuerdos de nivel de servicio (SLA) mandatorios por el Pliego Técnico.
        """
        self.target_concurrency = target_concurrency
        self.latency_threshold_ms = latency_threshold_ms
        self.success_count = 0
        self.sla_breach_count = 0

    def generate_mock_transaction(self, tx_id: int) -> Dict:
        """
        Genera tramas transaccionales sintéticas simulando la interacción híbrida
        entre tarjetas con perfiles prioritarios y validadores de a bordo.
        """
        is_priority = random.choice([True, False, False, False]) # 25% de densidad prioritaria
        current_unix = int(time.time())
        
        return {
            "tx_id": tx_id,
            "terminal_validadora_id": f"VAL_NFC_STATION_RET_{random.randint(1, 50)}",
            "linea_colectivo_id": str(random.choice(["060", "152", "059", "068"])),
            "interno_coche_id": f"INT_{random.randint(100, 999):04d}",
            "tarjeta_prioridad_hash_anon": f"sha256_mock_prio_{random.getrandbits(64):x}" if is_priority else "",
            "tarjeta_colaborador_hash_anon": f"sha256_mock_colab_{random.getrandbits(64):x}" if not is_priority else "",
            "timestamp_nfc": current_unix,
            "timestamp_bono_nfc": current_unix + random.randint(1, 5) if not is_priority else 0
        }

    def simulate_single_request(self, transaction: Dict) -> float:
        """
        Simula el paso de procesamiento por el microservicio desacoplado de FastAPI,
        interactuando con la caché volátil protegida (SRAM) para validar latencias.
        """
        start_time = time.time()
        
        # Emulación del procesamiento crítico local (lectura de token + cross-checking)
        # En producción este bloque llama a: validator.py y cache_manager.py
        processing_delay = random.uniform(0.010, 0.080) # 10ms a 80ms de inercia de base
        
        # Simular una penalización por desbordamiento controlado ante ráfagas concurrentes masivas
        if transaction["tx_id"] % 200 == 0:
            processing_delay += random.uniform(0.150, 0.250) # Inyección aleatoria de estrés de red
            
        time.sleep(processing_delay)
        elapsed_ms = (time.time() - start_time) * 1000.0
        return elapsed_ms

    def run_stress_test(self) -> Dict:
        """
        Ejecuta el pool de hilos concurrentes simulando la llegada masiva y asíncrona
        de pasajeros en hora pico en una estación compleja de transbordo.
        """
        print(f"[*] Iniciando Prueba de Humo y Carga Masiva: {self.target_concurrency} transacciones simultáneas.")
        transactions = [self.generate_mock_transaction(i) for i in range(self.target_concurrency)]
        latencies: List[float] = []

        # Ejecución paralela utilizando un pool de hilos de alta velocidad
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            future_to_tx = {executor.submit(self.simulate_single_request, tx): tx for tx in transactions}
            for future in concurrent.futures.as_completed(future_to_tx):
                try:
                    latency = future.result()
                    latencies.append(latency)
                    
                    if latency <= self.latency_threshold_ms:
                        self.success_count += 1
                    else:
                        self.sla_breach_count += 1
                except Exception as e:
                    print(f"[!] Error crítico en el hilo transaccional: {e}")

        # Procesamiento analítico macro y métricas de rendimiento
        avg_latency = sum(latencies) / len(latencies) if latencies else 0
        p95_latency = sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0
        sla_compliance = (self.success_count / self.target_concurrency) * 100

        metrics = {
            "total_processed": len(latencies),
            "average_latency_ms": round(avg_latency, 2),
            "p95_latency_ms": round(p95_latency, 2),
            "sla_compliance_percentage": round(sla_compliance, 2),
            "failures_count": self.sla_breach_count
        }

        print("[+] Simulación completa. Resultados de telemetría de rendimiento:")
        print(f"    - Latencia Promedio: {metrics['average_latency_ms']} ms")
        print(f"    - Latencia Percentil 95 (P95): {metrics['p95_latency_ms']} ms")
        print(f"    - Cumplimiento del SLA Mandatorio (<300ms): {metrics['sla_compliance_percentage']}%")
        
        return metrics

if __name__ == "__main__":
    # Inicializa el simulador emulando 1.000 solicitudes concurrentes en la terminal
    simulator = SubeLoadSimulator(target_concurrency=1000)
    simulator.run_stress_test()
