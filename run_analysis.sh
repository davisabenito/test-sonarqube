#!/bin/bash

# Script para ejecutar análisis de SonarQube con pysonar
# Uso: ./run_analysis.sh

set -e

echo "=========================================="
echo "  Análisis SonarQube con pysonar"
echo "=========================================="
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "data_cleaning.py" ]; then
    echo "Error: Ejecuta este script desde el directorio raíz del proyecto"
    exit 1
fi

# Activar entorno virtual
echo "1. Activando entorno virtual..."
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "   ✓ Entorno virtual activado"
else
    echo "   ✗ Entorno virtual no encontrado. Creándolo..."
    python3 -m venv venv
    source venv/bin/activate
    echo "   ✓ Entorno virtual creado y activado"
fi

# Instalar dependencias
echo ""
echo "2. Instalando dependencias..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
pip install pysonar -q
echo "   ✓ Dependencias instaladas"

# Ejecutar tests con coverage
echo ""
echo "3. Ejecutando tests con coverage..."
pytest --cov=data_cleaning --cov-report=xml --cov-report=term-missing --cov-fail-under=50
echo "   ✓ Tests ejecutados (coverage ~50%)"

# Verificar que coverage.xml se generó
if [ ! -f "coverage.xml" ]; then
    echo "   ✗ coverage.xml no se generó. Generando manualmente..."
    coverage xml
fi
echo "   ✓ coverage.xml generado"

# Verificar SonarQube
echo ""
echo "4. Verificando SonarQube..."
if curl -s http://localhost:9000/api/server/version > /dev/null 2>&1; then
    echo "   ✓ SonarQube está corriendo en http://localhost:9000"
else
    echo "   ✗ SonarQube no está accesible. Iniciando con Docker Compose..."
    docker-compose up -d
    echo "   Esperando a que SonarQube esté listo..."
    sleep 30
    if curl -s http://localhost:9000/api/server/version > /dev/null 2>&1; then
        echo "   ✓ SonarQube iniciado correctamente"
    else
        echo "   ✗ No se pudo iniciar SonarQube. Verifica manualmente."
        exit 1
    fi
fi

# Ejecutar análisis
echo ""
echo "5. Ejecutando análisis con pysonar..."
echo "   SonarQube URL: ${SONAR_HOST_URL:-http://localhost:9000}"
echo "   Project Key: ${SONAR_PROJECT_KEY:-prueba}"
echo ""

pysonar \
  --sonar-host-url=${SONAR_HOST_URL:-http://localhost:9000} \
  --sonar-token=${SONAR_TOKEN} \
  --sonar-project-key=${SONAR_PROJECT_KEY:-prueba} \
  --sonar-sources=data_cleaning.py \
  --sonar-tests=test_data_cleaning.py \
  --sonar-exclusions=venv/**,*.csv,*.md,.git/**,.github/**,pytest.ini,coverage.xml,.coverage \
  --sonar-python-coverage-reportPaths=coverage.xml

# Desactivar entorno virtual
echo ""
echo "5. Desactivando entorno virtual..."
deactivate
echo "   ✓ Entorno virtual desactivado"

echo ""
echo "=========================================="
echo "  Análisis completado"
echo "=========================================="
echo ""
echo "Ver los resultados en:"
echo "  http://localhost:9000/projects"
echo ""
echo "Para ver los issues detectados:"
echo "  1. Selecciona el proyecto 'prueba'"
echo "  2. Clic en la pestaña 'Issues'"
echo "  3. Filtra por 'Code Smell'"
echo ""
