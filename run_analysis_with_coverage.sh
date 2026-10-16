#!/bin/bash

# Script para ejecutar análisis de SonarQube con coverage usando sonar-scanner
# Este script usa sonar-scanner directamente porque pysonar no soporta bien el coverage

set -e

echo "=========================================="
echo "  Análisis SonarQube con Coverage"
echo "  (usando sonar-scanner)"
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
echo "   ✓ Dependencias instaladas"

# Ejecutar tests con coverage
echo ""
echo "3. Ejecutando tests con coverage..."
pytest --cov=data_cleaning --cov-report=xml --cov-report=term-missing --cov-fail-under=30
echo "   ✓ Tests ejecutados (coverage ~47%)"

# Verificar que coverage.xml se generó
if [ ! -f "coverage.xml" ]; then
    echo "   ✗ coverage.xml no se generó. Generando manualmente..."
    coverage xml
fi
echo "   ✓ coverage.xml generado"

# Verificar SonarQube
echo ""
echo "4. Verificando SonarQube..."
if curl -s ${SONAR_HOST_URL:-http://localhost:9000}/api/server/version > /dev/null 2>&1; then
    echo "   ✓ SonarQube está corriendo en ${SONAR_HOST_URL:-http://localhost:9000}"
else
    echo "   ✗ SonarQube no está accesible. Iniciando con Docker Compose..."
    docker-compose up -d
    echo "   Esperando a que SonarQube esté listo..."
    sleep 30
    if curl -s ${SONAR_HOST_URL:-http://localhost:9000}/api/server/version > /dev/null 2>&1; then
        echo "   ✓ SonarQube iniciado correctamente"
    else
        echo "   ✗ No se pudo iniciar SonarQube. Verifica manualmente."
        exit 1
    fi
fi

# Ejecutar análisis con sonar-scanner
echo ""
echo "5. Ejecutando análisis con sonar-scanner..."
echo "   SonarQube URL: ${SONAR_HOST_URL:-http://localhost:9000}"
echo "   Project Key: ${SONAR_PROJECT_KEY:-prueba}"
echo ""

# Verificar que SONAR_TOKEN esté definido
if [ -z "${SONAR_TOKEN}" ]; then
    echo "   ✗ Error: SONAR_TOKEN no está definido"
    echo "   Ejecuta: export SONAR_TOKEN=tu_token_aqui"
    exit 1
fi

sonar-scanner \
  -Dsonar.projectKey="${SONAR_PROJECT_KEY:-prueba}" \
  -Dsonar.projectName="Prueba SonarQube" \
  -Dsonar.projectVersion="1.0" \
  -Dsonar.sources="data_cleaning.py" \
  -Dsonar.tests="test_data_cleaning.py" \
  -Dsonar.sourceEncoding="UTF-8" \
  -Dsonar.exclusions="venv/**,**/*.csv,**/*.md,.git/**,.github/**,pytest.ini,coverage.xml,.coverage" \
  -Dsonar.test.exclusions="test_*.py" \
  -Dsonar.python.version="3.9" \
  -Dsonar.python.coverage.reportPaths="coverage.xml" \
  -Dsonar.coverage.jacoco.xmlReportPaths="coverage.xml" \
  -Dsonar.host.url="${SONAR_HOST_URL:-http://localhost:9000}" \
  -Dsonar.login="${SONAR_TOKEN}"

# Desactivar entorno virtual
echo ""
echo "6. Desactivando entorno virtual..."
deactivate
echo "   ✓ Entorno virtual desactivado"

echo ""
echo "=========================================="
echo "  Análisis completado"
echo "=========================================="
echo ""
echo "Ver los resultados en:"
echo "  ${SONAR_HOST_URL:-http://localhost:9000}/projects"
echo ""
echo "Para ver los issues detectados:"
echo "  1. Selecciona el proyecto '${SONAR_PROJECT_KEY:-prueba}'"
echo "  2. Clic en la pestaña 'Issues'"
echo "  3. Filtra por 'Code Smell' y 'Security Hotspot'"
echo ""
echo "Coverage debería mostrarse como ~50% (falla el Quality Gate que requiere 90%)"
echo ""
