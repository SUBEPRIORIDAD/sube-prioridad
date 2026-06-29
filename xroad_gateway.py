import time
import uuid
from typing import Dict, Optional


SIMULATED_EXTERNAL_SERVICES = {
    "ANDIS",
    "SISA",
    "RENAPER",
    "Mi Argentina",
    "Nacion Servicios",
    "Nación Servicios",
    "CNRT",
}


class XRoadRequest:
    def __init__(
        self,
        token_hash: str,
        service_name: str,
        correlation_id: str,
    ) -> None:
        self.token_hash = token_hash
        self.service_name = service_name
        self.correlation_id = correlation_id


class XRoadResponse:
    def __init__(
        self,
        success: bool,
        service_name: str,
        correlation_id: str,
        payload: Dict[str, object],
        elapsed_ms: int,
        simulated: bool,
    ) -> None:
        self.success = success
        self.service_name = service_name
        self.correlation_id = correlation_id
        self.payload = payload
        self.elapsed_ms = elapsed_ms
        self.simulated = simulated


class XRoadGateway:
    """
    Simulador de gateway de interoperabilidad.

    No contiene DNI, nombre, diagnóstico, domicilio ni historia clínica.
    No representa una conexión real con organismos públicos.
    """

    def __init__(self, simulated_latency_ms: int = 50) -> None:
        self.simulated_latency_ms = simulated_latency_ms

    def build_request(
        self,
        token_hash: str,
        service_name: str,
        correlation_id: Optional[str] = None,
    ) -> XRoadRequest:
        if not token_hash:
            raise ValueError("token_hash es obligatorio.")

        if not service_name:
            raise ValueError("service_name es obligatorio.")

        return XRoadRequest(
            token_hash=token_hash,
            service_name=service_name,
            correlation_id=correlation_id or str(uuid.uuid4()),
        )

    def verify_priority_attribute(self, request: XRoadRequest) -> XRoadResponse:
        start = time.time()

        time.sleep(self.simulated_latency_ms / 1000)

        elapsed_ms = int((time.time() - start) * 1000)

        return XRoadResponse(
            success=True,
            service_name=request.service_name,
            correlation_id=request.correlation_id,
            elapsed_ms=elapsed_ms,
            simulated=is_simulated_external_service(request.service_name),
            payload={
                "atributo_prioridad_activo": True,
                "perfil_alertas_ux": 2,
                "fuente": "simulador_xroad_mvp",
                "datos_sensibles_procesados": False,
                "integracion_real": False,
            },
        )


def is_simulated_external_service(service_name: str) -> bool:
    normalized = service_name.strip().lower()

    return any(
        service.lower() == normalized
        for service in SIMULATED_EXTERNAL_SERVICES
    )
