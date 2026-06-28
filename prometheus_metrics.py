import time

class SubeMetricsCollector:
    """Instrumentación estandarizada para la auditoría y telemetría pública de latencias."""
    
    def __init__(self):
        # Contadores y métricas simuladas basados en el formato de OpenMetrics
        self.metrics_store = {
            "sube_prioridad_transactions_total": 0,
            "sube_prioridad_bonos_assigned_total": 0,
            "sube_prioridad_latency_seconds_sum": 0.0
        }

    def registrar_transaccion(self, duracion_ns: int, bono_otorgado: bool) -> None:
        """Incrementa los vectores de telemetría de forma atómica en el bus local."""
        duracion_segundos = duracion_ns / 1_000_000_000.0
        self.metrics_store["sube_prioridad_transactions_total"] += 1
        self.metrics_store["sube_prioridad_latency_seconds_sum"] += duracion_segundos
        
        if bono_otorgado:
            self.metrics_store["sube_prioridad_bonos_assigned_total"] += 1

    def exportar_formato_prometheus(self) -> str:
        """Formatea las métricas internas bajo el estándar plano de la W3C/Prometheus."""
        avg_latency = 0.0
        if self.metrics_store["sube_prioridad_transactions_total"] > 0:
            avg_latency = self.metrics_store["sube_prioridad_latency_seconds_sum"] / self.metrics_store["sube_prioridad_transactions_total"]
            
        return (
            f"# HELP sube_prioridad_transactions_total Pasajes totales evaluados.\n"
            f"# TYPE sube_prioridad_transactions_total counter\n"
            f"sube_prioridad_transactions_total {self.metrics_store['sube_prioridad_transactions_total']}\n"
            f"# HELP sube_prioridad_avg_latency_seconds Promedio de latencia en validación de borde.\n"
            f"# TYPE sube_prioridad_avg_latency_seconds gauge\n"
            f"sube_prioridad_avg_latency_seconds {avg_latency:.6f}\n"
        )

if __name__ == "__main__":
    collector = SubeMetricsCollector()
    collector.registrar_transaccion(duracion_ns=45_000_000, bono_otorgado=True)
    collector.registrar_transaccion(duracion_ns=12_000_000, bono_otorgado=False)
    print("📈 [TELEMETRÍA PÚBLICA]: Formato estructurado expuesto para dashboards de control:")
    print(collector.exportar_formato_prometheus())
