import os

class SubePrioridadConfig:
    """Centralización de variables de entorno y parámetros de hardware de la validadora."""
    
    # Parámetros del Algoritmo del Bono Solidario (Sección XV del Pliego)
    BONO_WINDOW_SECONDS: float = float(os.getenv("SUBE_BONO_WINDOW", 60.0))
    
    # Configuración de Seguridad y Cifrado (Cumplimiento Ley 25.326)
    CRYPTO_ALGORITHM: str = os.getenv("SUBE_CRYPTO_ALGO", "AES-128-CBC")
    TOKEN_SECRET_SALT: str = os.getenv("SUBE_SECRET_SALT", "NacionServiciosCriptoSalt2026")
    
    # Endpoints del Bus de Interoperabilidad Federal (Decreto 1273/16)
    ANDIS_API_URL: str = os.getenv("ANDIS_API_ENDPOINT", "
