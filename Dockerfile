# Estándar de la industria: Imagen base ligera de Python basada en Linux Alpine
FROM python:3.10-alpine

# Establece el directorio de trabajo seguro dentro del contenedor (Sandbox)
WORKDIR /app

# Copia los archivos lógicos y scripts del validador al contenedor
COPY validator.py test_antifraud.py ./

# Variable de entorno para asegurar que los logs se emitan en tiempo real sin búfer
ENV PYTHONUNBUFFERED=1

# Comando por defecto: Ejecuta la suite de pruebas unitarias automatizadas antifraude
CMD ["python", "-m", "unittest", "test_antifraud.py", "-v"]
