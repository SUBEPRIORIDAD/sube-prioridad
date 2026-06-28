#!/bin/sh

# =====================================================================
# SCRIPT DE DIAGNÓSTICO EN TIEMPO DE EJECUCIÓN (DOCKER HEALTHCHECK)
# =====================================================================

# Realiza una petición de baja latencia al endpoint local de la API core
RESPONSE_STATUS=$(wget --quiet --spider --server-response http://localhost:8000/api/v1/prioridad/verificar 2>&1 | awk '/HTTP\// {print $2}')

# Verifica que el código de respuesta del servidor FastAPI sea un estándar de red válido
if [ "$RESPONSE_STATUS" = "405" ] || [ "$RESPONSE_STATUS" = "200" ]; then
    # Un código 405 (Método no permitido) o 200 confirma que el puerto y el loop de eventos están activos
    echo "🍏 [HEALTHCHECK PASSED]: El nodo del backend responde de forma óptima."
    exit 0
else
    echo "🍎 [HEALTHCHECK FAILED]: Nodo sin respuesta o en condición de desbordamiento de memoria."
    exit 1
fi
