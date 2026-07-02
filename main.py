
APP_NAME = "SUBE Prioridad"
PROJECT_NAME = APP_NAME
APP_VERSION = "0.4.1"
APP_VERSION = "0.4.2"
DEMO_MODE = True


@@ -51,23 +51,24 @@

class PriorityVerificationRequest(BaseModel):
"""
    Payload flexible de verificación demo.
    Payload de verificación demo.

    No debe contener DNI, diagnóstico, CUD, certificado médico ni datos sensibles.
    Los campos centrales son requeridos para mantener compatibilidad con tests
    y evitar que un payload vacío sea aceptado como válido.
   """

    priority_attribute_active: bool = Field(default=True)
    previously_accredited_need: bool = Field(default=True)
    validation_paid: bool = Field(default=True)
    priority_attribute_active: bool = Field(...)
    previously_accredited_need: bool = Field(...)
    validation_paid: bool = Field(...)
user_token: Optional[str] = Field(default="demo-priority-user-001")
priority_attribute_token: Optional[str] = Field(default="demo-priority-attribute-001")


class SolidaryBonusSimulationRequest(BaseModel):
"""
    Payload flexible para simulación simple del Bono Solidario.
    Payload para simulación simple del Bono Solidario.

    La simulación base no aplica beneficios reales.
    Se conserva compatibilidad con el endpoint previo.
   """

priority_user_token: str = Field(default="demo-priority-user-001")
@@ -117,7 +118,7 @@ def health() -> Dict[str, Any]:
"project": PROJECT_NAME,
"version": APP_VERSION,
"demo_mode": DEMO_MODE,
        "status": "healthy",
        "status": "ok",
}


@@ -126,7 +127,9 @@ def project_guardrails() -> Dict[str, Any]:
return {
"app_name": APP_NAME,
"project": PROJECT_NAME,
        "version": APP_VERSION,
"demo_mode": DEMO_MODE,
        "status": "ok",
"guardrails": [
"Sin integración real con SUBE.",
"Sin integración real con Red SUBE.",
@@ -222,7 +225,7 @@ def simular_bono_solidario(

event = create_demo_solidary_event(
priority_user_token=request.priority_user_token,
        collaborator_user_token=request.collaborator_user_token,
        collaborator_token=request.collaborator_user_token,
voluntary_seat_yield=request.voluntary_seat_yield,
priority_user_confirms=request.priority_user_confirms,
same_transport_context=request.same_transport_context,
