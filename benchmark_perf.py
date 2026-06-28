import time
from validator import SubePrioridadValidator
from cache_manager import SubePrioridadCacheManager

class SubePerformanceBenchmark:
    """Módulo de auditoría técnica de tiempos y profiling micro-transaccional."""
    
    def __init__(self):
        self.validator = SubePrioridadValidator()
        self.cache = SubePrioridadCacheManager()

    def ejecutar_benchmarks(self):
        print("⏱️ Iniciando perfiles de rendimiento del ecosistema...")
        
        # BENCHMARK 1: Velocidad de respuesta de la lógica de firmware local
        t_start = time.perf_counter_ns()
        self.validator.process_transaction("SUBE_BENCH_01", is_priority_user=True)
        t_end = time.perf_counter_ns()
        latency_firmware_ms = (t_end - t_start) / 1_000_000
        
        # BENCHMARK 2: Recuperación desde el gestor de caché de alta velocidad
        sample_hash = "8f4a3b1c9e2d7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a"
        self.cache.set_token_status(sample_hash, is_active=True)
        
        t_start_cache = time.perf_counter_ns()
        self.cache.get_token_status(sample_hash)
        t_end_cache = time.perf_counter_ns()
        latency_cache_ms = (t_end_cache - t_start_cache) / 1_000_000
        
        # REPORTE DE AUDITORÍA FINAL
        print("\n=======================================================")
        print("🏛️ REPORTES DE REQUERIMIENTOS DE NACIÓN SERVICIOS S.A.")
        print("=======================================================")
        print(f"1. Latencia Motor Lógico (Borde): {latency_firmware_ms:.4f} ms")
        print(f"2. Latencia Capa de Caché (Memoria): {latency_cache_ms:.4f} ms")
        
        CRITICAL_THRESHOLD_MS = 300.0
        if latency_firmware_ms < CRITICAL_THRESHOLD_MS:
            print(f"✅ [DESEMPEÑO HOMOLOGADO]: Latencia inferior al límite duro de {CRITICAL_THRESHOLD_MS}ms.")
        else:
            print("⚠️ Alerta: El procesamiento supera el umbral crítico de velocidad requerido.")
        print("=======================================================\n")

if __name__ == "__main__":
    bench = SubePerformanceBenchmark()
    bench.ejecutar_benchmarks()
