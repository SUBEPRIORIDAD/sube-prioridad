#!/bin/bash

# =====================================================================
# SCRIPT DE CONFIGURACIÓN AUTOMATIZADA - ECOSESTEMA SUBE PRIORIDAD
# =====================================================================

echo "🚀 Iniciando inicialización del entorno SUBE Prioridad..."

# 1. Crear estructura de directorios requerida para la arquitectura limpia
echo "📁 Creando directorios del sistema..."
mkdir -p .github/workflows
mkdir -p logs/audit

# 2. Verificar dependencias base del entorno local
echo "🔍 Verificando intérprete de Python..."
if ! command -v python3 &> /dev/null
then
    echo "❌ Error: Python3 no se encuentra instalado en el sistema operativo."
    exit 1
fi

# 3. Compilación estática de verificación sintáctica
echo "⚙️ Ejecutando auditoría de compilación del firmware de borde..."
python3 -m py_compile validator.py
python3 -m py_compile main.py

if [ $? -eq 0 ]; then
    echo "✅ Compilación exitosa. Sintaxis de código libre de anomalías."
else
    echo "❌ Error de compilación en los módulos centrales de Python."
    exit 1
fi

# 4. Ejecución del marco de pruebas unitarias del motor antifraude
echo "🧪 Ejecutando suite de testeo automático (Consistencia Temporal)..."
python3 -m unittest test_antifraud.py -v

if [ $? -eq 0 ]; then
    echo "🎉 [ENTORNO LISTO]: Todos los filtros lógicos y criptográficos han pasado las pruebas."
else
    echo "⚠️ Alerta: El marco de pruebas reportó fallas en la lógica transaccional."
    exit 1
fi
