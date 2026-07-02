from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

# --- GLOSARIO DE HARDWARE Y ENTORNOS OPERATIVOS ADICIONADO ---
class HardwareTargetKind(str, Enum):
    COLECTIVO_EDGE_OFFLINE = "colectivo_edge_offline"
    TREN_DE_LA_COSTA_EDGE_MIXED = "tren_costa_edge_mixed"
    TREN_METROPOLITANO_MOLINETE = "tren_central_online"
    SUBTE_MOLINETE = "subte_central_online"

@dataclass
class EventoValidacion:
    """
    Representa un evento conceptual de validación para el módulo futuro
    de Bono Solidario.
    Este modelo no pertenece al núcleo inicial de asistencia preventiva.
    Se conserva como componente experimental y demostrativo para evaluar
    reglas antifraude en escenarios futuros.
    No debe contener DNI, nombre, apellido, diagnóstico médico, historia
    clínica, certificados médicos ni datos de salud identificables.
    """
    tarjeta_id: str
    linea: str
    unidad: str
    timestamp: datetime
    tipo_evento: str = "validacion"
    # Extensión de contexto físico sin romper compatibilidad (Opcional con default)
    hardware_origen: HardwareTargetKind = HardwareTargetKind.COLECTIVO_EDGE_OFFLINE

@dataclass
class ResultadoAntifraude:
    """
    Resultado conceptual del análisis antifraude.
    permitido:
        Indica si el evento supera las reglas demostrativas.
    motivo:
        Explica la razón principal del resultado.
    alertas:
        Lista de alertas no sensibles detectadas.
    score_riesgo:
        Puntaje conceptual de riesgo, entre 0 y 100.
    """
    permitido: bool
    motivo: str
    alertas: List[str]
    score_riesgo: int
    # Campos de modulación de interfaz agregados de forma segura
    hardware_action: str = "standard_fare_deduction"
    open_solidary_window: bool = False
    latency_estimation_ms: int = 120

class AntifraudValidator:
    """
    Motor antifraude conceptual para escenarios futuros de Bono Solidario.
    Este componente no forma parte del core inicial de SUBE Prioridad.
    No se conecta con SUBE real.
    No se conecta con Mi Argentina.
    No se conecta con organismos públicos.
    No procesa identidad real ni datos médicos.
    Su finalidad actual es demostrar cómo podrían evaluarse reglas técnicas
    no sensibles en un entorno de simulación.
    """
    def __init__(
        self,
        ventana_minutos: int = 10,
        max_eventos_por_ventana: int = 3,
        max_score_permitido: int = 70,
    ) -> None:
        self.ventana_minutos = ventana_minutos
        self.max_eventos_por_ventana = max_eventos_por_ventana
        self.max_score_permitido = max_score_permitido
        self._eventos: List[EventoValidacion] = []

    def registrar_evento(self, evento: EventoValidacion) -> None:
        """
        Registra un evento conceptual en memoria.
        Este registro es sólo demostrativo. No debe usarse como almacenamiento
        productivo ni como base de auditoría real.
        """
        self._eventos.append(evento)
        self._limpiar_eventos_antiguos(evento.timestamp)

    def validar_evento(self, evento: EventoValidacion) -> ResultadoAntifraude:
        """
        Evalúa un evento conceptual con reglas simples antifraude.
        Reglas demostrativas:
        - tarjeta_id no vacío;
        - línea no vacía;
        - unidad no vacía;
        - timestamp válido;
        - exceso de validaciones en ventana temporal;
        - validaciones repetidas en la misma línea y unidad;
        - validaciones simultáneas en unidades distintas.
        Ninguna regla utiliza datos personales, médicos o identificatorios reales.
        """
        alertas: List[str] = []
        score = 0
        
        errores_basicos = self._validar_campos_basicos(evento)
        if errores_basicos:
            return ResultadoAntifraude(
                permitido=False,
                motivo="Evento inválido por campos básicos incompletos.",
                alertas=errores_basicos,
                score_riesgo=100,
                hardware_action="fail_fast_block",
                open_solidary_window=False,
                latency_estimation_ms=50
            )

        eventos_recientes = self._eventos_en_ventana(evento)
        if len(eventos_recientes) >= self.max_eventos_por_ventana:
            alertas.append("exceso_de_eventos_en_ventana_temporal")
            score += 35

        if self._hay_repeticion_misma_linea_unidad(evento, eventos_recientes):
            alertas.append("repeticion_misma_linea_y_unidad")
            score += 25

        if self._hay_unidades_distintas_en_ventana(evento, eventos_recientes):
            alertas.append("validaciones_en_unidades_distintas")
            score += 30

        if self._hay_timestamp_futuro(evento):
            alertas.append("timestamp_futuro")
            score += 40

        score = min(score, 100)
        permitido = score < self.max_score_permitido
        
        # --- FILTRO DE ARQUITECTURA: DISCRIMINACIÓN FÍSICA DE ENTORNO ---
        # Comportamiento exclusivo para Validación Descentralizada de Borde (Colectivos y Tren de la Costa)
        if evento.hardware_origen in [HardwareTargetKind.COLECTIVO_EDGE_OFFLINE, HardwareTargetKind.TREN_DE_LA_COSTA_EDGE_MIXED]:
            hardware_action = "execute_immediate_edge_habitaculo_alert"
            open_solidary_window = True if permitido else False
            latency_estimation_ms = 240  # Latencia controlada en microcontroladores locales offline
        
        # Comportamiento exclusivo para Validación Centralizada Pre-Bordo (Molinetes Ferroviarios)
        else:
            hardware_action = "route_async_signal_to_platform_displays"
            open_solidary_window = False  # No se abre re-validación cívica en molinetes transitados
            latency_estimation_ms = 380  # Tránsito WAN hacia el backend centralizado

        motivo = (
            "Evento permitido en entorno demostrativo."
            if permitido
            else "Evento observado por reglas antifraude conceptuales."
        )

        return ResultadoAntifraude(
            permitido=permitido,
            motivo=motivo,
            alertas=alertas,
            score_riesgo=score,
            hardware_action=hardware_action,
            open_solidary_window=open_solidary_window,
            latency_estimation_ms=latency_estimation_ms
        )

    def validar_y_registrar(self, evento: EventoValidacion) -> ResultadoAntifraude:
        """
        Evalúa el evento y, si corresponde, lo registra.
        En este MVP demostrativo se registra tanto si está permitido como si
        genera alertas, para poder simular comportamiento histórico.
        """
        resultado = self.validar_evento(evento)
        self.registrar_evento(evento)
        return resultado

    def reset(self) -> None:
        """
        Limpia los eventos registrados en memoria.
        """
        self._eventos.clear()

    def estado(self) -> Dict[str, Any]:
        """
        Devuelve un estado conceptual del validador.
        """
        return {
            "componente": "AntifraudValidator",
            "entorno": "mvp-conceptual",
            "eventos_en_memoria": len(self._eventos),
            "ventana_minutos": self.ventana_minutos,
            "max_eventos_por_ventana": self.max_eventos_por_ventana,
            "max_score_permitido": self.max_score_permitido,
            "procesa_datos_sensibles": False,
            "integracion_real_con_organismos": False,
            "integracion_real_sube": False,
            "modulo": "bono_solidario_futuro_experimental",
        }

    def _validar_campos_basicos(self, evento: EventoValidacion) -> List[str]:
        errores: List[str] = []
        if not evento.tarjeta_id or not evento.tarjeta_id.strip():
            errores.append("tarjeta_id_requerido")
        if not evento.linea or not evento.linea.strip():
            errores.append("linea_requerida")
        if not evento.unidad or not evento.unidad.strip():
            errores.append("unidad_requerida")
        if not isinstance(evento.timestamp, datetime):
            errores.append("timestamp_invalido")
        return errores

    def _eventos_en_ventana(self, evento: EventoValidacion) -> List[EventoValidacion]:
        inicio_ventana = evento.timestamp - timedelta(minutes=self.ventana_minutos)
        return [
            existente
            for existente in self._eventos
            if existente.tarjeta_id == evento.tarjeta_id
            and inicio_ventana <= existente.timestamp <= evento.timestamp
        ]

    def _hay_repeticion_misma_linea_unidad(
        self,
        evento: EventoValidacion,
        eventos_recientes: List[EventoValidacion],
    ) -> bool:
        return any(
            existente.linea == evento.linea and existente.unidad == evento.unidad
            for existente in eventos_recientes
        )

    def _hay_unidades_distintas_en_ventana(
        self,
        evento: EventoValidacion,
        eventos_recientes: List[EventoValidacion],
    ) -> bool:
        return any(
            existente.linea == evento.linea and existente.unidad != evento.unidad
            for existente in eventos_recientes
        )

    def _hay_timestamp_futuro(self, evento: EventoValidacion) -> bool:
        ahora = datetime.now(timezone.utc)
        timestamp = evento.timestamp
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        return timestamp > ahora + timedelta(minutes=5)

    def _limpiar_eventos_antiguos(self, referencia: datetime) -> None:
        limite = referencia - timedelta(minutes=self.ventana_minutos * 3)
        self._eventos = [
            evento for evento in self._eventos if evento.timestamp >= limite
        ]

def crear_evento_demo(
    tarjeta_id: str = "token-demo",
    linea: str = "60",
    unidad: str = "1234",
    timestamp: Optional[datetime] = None,
