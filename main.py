from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta

app = FastAPI(
    title="Core Backend SUBE Prioridad",
    description="Motor de microservicios para la tokenización y gobernanza de atributos de movilidad segura."
)

# Modelo de datos de entrada (Cumplimiento de la Capa de Confianza de Entrada)
class VerificationRequest(BaseModel):
    token_tramite_hash: str
    firma_digital_medico: str

# Modelo de datos de salida (Principio de Abstracción Médica - Cero diagnósticos clínicos)
class VerificationResponse(BaseModel):
    atributo_prioridad_activo: bool
    perfil_alertas_ux: int  # 1: Visible, 2: Discreto, 3: Pasivo
    fecha_caducidad: datetime

@app.post(
    "/api/v1/prioridad/verificar", 
    response_model=VerificationResponse, 
    status_code=status.HTTP_200_OK,
    summary="Endpoint de Homologación de Atributo Binario"
)
async def verificar_prioridad(payload: VerificationRequest):
    # Simulación de auditoría criptográfica del origen de confianza (ANDIS/SISA)
    if not payload.token_tramite_hash or len(payload.token_tramite_hash) != 64:
        raise HTTPException(
            status_code=400, 
            detail="Formato de token transaccional inválido. Se requiere hash SHA-256."
        )
    
    # Simulación de regla de negocio: Retorna el atributo binario puro disociado del DNI
    return VerificationResponse(
        atributo_prioridad_activo=True,
        perfil_alertas_ux=2, # Por defecto: Perfil discreto orientado al panel de conducción
        fecha_caducidad=datetime.utcnow() + timedelta(days=180) # Atributo transitorio mutable
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
