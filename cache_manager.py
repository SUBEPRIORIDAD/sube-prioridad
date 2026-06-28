import time
from typing import Dict, Optional

class SubePrioridadCacheManager:
    """Simulador de capa de caché en memoria de alto rendimiento para validaciones en microsegundos."""
    
    def __init__(self):
        # Estructura en memoria local para almacenar tokens médicos validados temporalmente
        self._cache_store: Dict[str, dict] = {}
        # Tiempo de vida por defecto de los datos en caché: 1 hora (3600 segundos)
        self.TTL_SECONDS = 3600.0

    def set_token_status(self, token_hash: str, is_active: bool) -> None:
        """Escribe el estado del atributo disociado en la capa de memoria rápida."""
        self._cache_store[token_hash] = {
            "status": is_active,
            "expires_at": time.time() + self.TTL_SECONDS
        }

    def get_token_status(self, token_hash: str) -> Optional[bool]:
        """Recupera de forma inmediata el estado binario del beneficio (<5ms)."""
        current_time = time.time()
        cached_item = self._cache_store.get(token_hash)
        
        if not cached_item:
            return None  # Cache Miss: Se debe requerir consulta al bus centralizado
            
        # Validación de caducidad cronológica de la caché
        if current_time > cached_item["expires_at"]:
            del self._cache_store[token_hash]  # Purga por expiración de TTL
            return None
            
        return cached_item["status"]  # Cache Hit: Retorno fluido del atributo

# --- PRUEBA UNITARIA DE CONSOLA ---
if __name__ == "__main__":
    cache = SubePrioridadCacheManager()
    sample_hash = "8f4a3b1c9e2d7f6a5b4c3d2e1f0a9b8c7d6e5f4a3b2c1d0e9f8a7b6c5d4e3f2a"
    
    cache.set_token_status(sample_hash, is_active=True)
    print(f"[Caché de Borde]: Estado recuperado para validación rápida: {cache.get_token_status(sample_hash)}")
