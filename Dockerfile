# Dockerfile
# Entorno de producción inmutable y liviano basado en Linux Alpine
# Diseñado bajo el esquema federal del Programa SUBE Prioridad por Andrés Federico di Fiore

FROM python:3.11-alpine

# Instalar dependencias del sistema mínimas para compilar y asegurar capas
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev \
    && apk add --no-cache bash curl

WORKDIR /app

# Copiar requerimientos e instalar de forma aislada
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Eliminar herramientas de compilación para endurecimiento (Hardening) de la imagen
RUN apk del .build-deps

# Copiar el core del código fuente y scripts de inicialización
COPY . .

# Crear un usuario no-privilegiado para mitigar riesgos de ejecución como root
RUN adduser -D subeuser && chown -R subeuser:subeuser /app
USER subeuser

EXPOSE 8000

# Script duro de control de salud embebido
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD ["./health_check.sh"]

CMD ["uvicorn", "main.py:app", "--host", "0.0.0.0", "--port", "8000"]
