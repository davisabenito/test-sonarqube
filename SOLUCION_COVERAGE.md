# Solución: Coverage 0% en SonarQube

## Problema
SonarQube muestra 0% de coverage aunque pytest genera el reporte `coverage.xml`. Esto ocurre porque:
1. `pysonar` no soporta bien el parámetro de coverage
2. El archivo `coverage.xml` no se está leyendo correctamente

## Solución: Usar sonar-scanner en lugar de pysonar

pysonar es un wrapper simplificado pero no soporta todas las opciones de SonarQube, especialmente el coverage. La solución es usar `sonar-scanner` directamente.

## Paso 1: Instalar sonar-scanner

```bash
# macOS
brew install sonar-scanner

# Verificar instalación
sonar-scanner --version
```

## Paso 2: Usar el script con variables de entorno

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube

# Configurar variables de entorno
export SONAR_HOST_URL=http://localhost:9000
export SONAR_TOKEN=sqp_35ac38bccff8c00b4916273e59ab8c7e8da1f2f2
export SONAR_PROJECT_KEY=test-sonar

# Ejecutar el análisis con coverage
./run_analysis_with_coverage.sh
```

## Paso 3: O ejecutar manualmente con sonar-scanner

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
source venv/bin/activate

# Ejecutar tests para generar coverage.xml
pytest --cov=data_cleaning --cov-report=xml --cov-report=term-missing

# Ejecutar análisis con sonar-scanner
sonar-scanner \
  -Dsonar.projectKey=test-sonar \
  -Dsonar.projectName=Test SonarQube \
  -Dsonar.projectVersion=1.0 \
  -Dsonar.sources=data_cleaning.py \
  -Dsonar.tests=test_data_cleaning.py \
  -Dsonar.sourceEncoding=UTF-8 \
  -Dsonar.exclusions=venv/**,**/*.csv,**/*.md,.git/**,.github/**,pytest.ini,coverage.xml,.coverage \
  -Dsonar.test.exclusions=test_*.py \
  -Dsonar.python.version=3.9 \
  -Dsonar.python.coverage.reportPaths=coverage.xml \
  -Dsonar.coverage.jacoco.xmlReportPaths=coverage.xml \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=sqp_35ac38bccff8c00b4916273e59ab8c7e8da1f2f2

deactivate
```

## Parámetros Clave para Coverage

Estos son los parámetros que hacen que SonarQube lea el coverage:

```properties
-Dsonar.python.coverage.reportPaths=coverage.xml
-Dsonar.coverage.jacoco.xmlReportPaths=coverage.xml
```

SonarQube usa el formato XML de JaCoCo para leer el coverage, incluso para Python.

## Verificar que coverage.xml se genera

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
source venv/bin/activate

# Ejecutar tests
pytest --cov=data_cleaning --cov-report=xml

# Verificar que el archivo existe
ls -la coverage.xml

# Ver el contenido (opcional)
head -20 coverage.xml

deactivate
```

El archivo `coverage.xml` debería tener una estructura similar a:

```xml
<?xml version="1.0" ?>
<coverage version="6.0" timestamp="...">
  <packages>
    <package name="." line-rate="0.5" branch-rate="0.5">
      <classes>
        <class name="data_cleaning.py" filename="data_cleaning.py" line-rate="0.5">
          ...
        </class>
      </classes>
    </package>
  </packages>
</coverage>
```

## Variables de Entorno Soportadas

El script `run_analysis_with_coverage.sh` soporta estas variables de entorno:

| Variable | Valor por defecto | Descripción |
|----------|-------------------|-------------|
| `SONAR_HOST_URL` | `http://localhost:9000` | URL de SonarQube |
| `SONAR_TOKEN` | (requerido) | Token de autenticación |
| `SONAR_PROJECT_KEY` | `prueba` | Key del proyecto en SonarQube |

## Ejemplo Completo con tus Variables

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube

# Configurar tus variables
export SONAR_HOST_URL=http://localhost:9000
export SONAR_TOKEN=sqp_35ac38bccff8c00b4916273e59ab8c7e8da1f2f2
export SONAR_PROJECT_KEY=test-sonar

# Ejecutar análisis
./run_analysis_with_coverage.sh
```

## Resultados Esperados

Después de ejecutar el análisis con sonar-scanner, deberías ver en SonarQube:

- **Coverage**: ~50% (rojo, porque el Quality Gate requiere 90%)
- **Quality Gate**: ❌ FAILED (por coverage < 90%)
- **Code Smells**: 30+ issues
- **Security Hotspots**: 5+ issues

## Si el Coverage Sigue en 0%

### Opción 1: Verificar el proyecto en SonarQube

1. Ve a http://localhost:9000/projects
2. Selecciona `test-sonar`
3. Clic en **Project Settings** → **Analysis Scope**
4. Verifica que `data_cleaning.py` esté en la lista de fuentes
5. Verifica que `test_data_cleaning.py` esté en la lista de tests

### Opción 2: Regenerar coverage.xml

```bash
source venv/bin/activate
# Limpiar coverage anterior
coverage erase
# Ejecutar tests nuevamente
pytest --cov=data_cleaning --cov-report=xml
# Verificar
ls -la coverage.xml
deactivate
```

### Opción 3: Usar el parámetro de coverage de pytest

```bash
source venv/bin/activate
coverage run -m pytest
coverage xml
coverage report
deactivate
```

### Opción 4: Verificar que sonar-scanner lea el archivo

```bash
# Ejecutar sonar-scanner con modo verbose
sonar-scanner \
  -Dsonar.projectKey=test-sonar \
  -Dsonar.projectName=Test SonarQube \
  -Dsonar.sources=data_cleaning.py \
  -Dsonar.tests=test_data_cleaning.py \
  -Dsonar.python.coverage.reportPaths=coverage.xml \
  -Dsonar.coverage.jacoco.xmlReportPaths=coverage.xml \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=sqp_35ac38bccff8c00b4916273e59ab8c7e8da1f2f2 \
  -X  # Modo verbose para ver qué archivos se están leyendo
```

## Diferencia entre pysonar y sonar-scanner

| Característica | pysonar | sonar-scanner |
|----------------|---------|---------------|
| Coverage | ❌ No soportado bien | ✅ Soportado |
| Facilidad de uso | ✅ Simple | ⚠️ Más verboso |
| Parámetros | Limitados | Completo |
| Recomendado para | Análisis básico | Análisis con coverage |

## Comando Rápido

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
export SONAR_HOST_URL=http://localhost:9000
export SONAR_TOKEN=sqp_35ac38bccff8c00b4916273e59ab8c7e8da1f2f2
export SONAR_PROJECT_KEY=test-sonar
./run_analysis_with_coverage.sh
```

## Verificar en SonarQube

1. Ve a http://localhost:9000/projects
2. Busca `test-sonar`
3. Verás:
   - Coverage: ~50% (rojo)
   - Quality Gate: FAILED
   - Code Smells: 30+
   - Security Hotspots: 5+

El Quality Gate fallará porque coverage es 50% y requiere 90%.
