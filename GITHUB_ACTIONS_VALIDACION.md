# Validación de SonarQube en GitHub Actions con IS_COVERAGE

## Descripción

El workflow de GitHub Actions ahora soporta dos modos de validación mediante el flag `IS_COVERAGE`:

- **IS_COVERAGE=TRUE**: Valida que el coverage sea ≥ 90%
- **IS_COVERAGE=FALSE**: Valida que los issues por severidad estén dentro de los límites permitidos

## Modos de Validación

### Modo 1: Validación de Coverage (IS_COVERAGE=TRUE)

**Umbral requerido:** Coverage ≥ 90%

Si el coverage es menor a 90%, el workflow fallará.

### Modo 2: Validación de Severidad (IS_COVERAGE=FALSE)

**Umbrales permitidos:**

| Severidad | Máximo Permitido | Acción si excede |
|-----------|------------------|------------------|
| Blocker | 1 | ❌ Fails |
| Critical | 1 | ❌ Fails |
| Major | 2 | ❌ Fails |
| Minor | 0 | ⚠️ Warning |
| Info | 0 | ℹ️ Info (no bloqueante) |

Si Blocker, Critical o Major exceden los límites, el workflow fallará.

## Ejecutar el Workflow Manualmente

### Desde GitHub UI

1. Ve a tu repositorio en GitHub
2. Clic en la pestaña **Actions**
3. Selecciona el workflow **SonarQube Scan**
4. Clic en **Run workflow** (botón azul arriba a la derecha)
5. Configura los inputs:
   - **is_coverage**: Selecciona `TRUE` o `FALSE`
   - **project_key**: Ingresa el key de tu proyecto en SonarQube (ej: `pruebas-sonarqube`)
6. Clic en **Run workflow** (botón verde)

### Desde Git (Trigger Automático)

El workflow también se ejecuta automáticamente en:
- Push a las ramas `main` o `develop`
- Pull requests a estas ramas

Para ejecutar en modo automático con diferentes modos, puedes:

**Opción A: Usar workflow_dispatch con variables**

```bash
# Usar GitHub CLI
gh workflow run sonarqube-scan.yml \
  -f is_coverage=FALSE \
  -f project_key=pruebas-sonarqube
```

**Opción B: Modificar el workflow para leer de un archivo**

Crea un archivo `.github/workflows/config.yml`:

```yaml
is_coverage: "FALSE"
project_key: "pruebas-sonarqube"
```

Luego en el workflow, lee este archivo:

```yaml
- name: Load config
  id: config
  run: |
    if [ -f .github/workflows/config.yml ]; then
      echo "is_coverage=$(yq -r '.is_coverage' .github/workflows/config.yml)" >> $GITHUB_OUTPUT
      echo "project_key=$(yq -r '.project_key' .github/workflows/config.yml)" >> $GITHUB_OUTPUT
    else
      echo "is_coverage=TRUE" >> $GITHUB_OUTPUT
      echo "project_key=pruebas-sonarqube" >> $GITHUB_OUTPUT
    fi

env:
  IS_COVERAGE: ${{ steps.config.outputs.is_coverage }}
  PROJECT_KEY: ${{ steps.config.outputs.project_key }}
```

## Ver Resultados del Workflow

### En GitHub Actions

1. Ve a la pestaña **Actions**
2. Selecciona la ejecución del workflow
3. Verás los logs con:
   - Paso "Check Coverage" o "Check Severity" según el modo
   - Resumen de métricas
   - ✅ PASS o ❌ FAIL

### En SonarQube

1. Ve a tu SonarQube (local o cloud)
2. Busca el proyecto
3. Verás el análisis del workflow

## API de SonarQube Usada

El workflow usa la API de SonarQube para obtener métricas:

### Obtener Coverage
```
GET /api/measures/component?component={projectKey}&metricKeys=coverage
```

### Obtener Issues por Severidad
```
GET /api/issues/search?componentKeys={projectKey}&severities={SEVERITY}&ps=500
```

Severidades disponibles:
- BLOCKER
- CRITICAL
- MAJOR
- MINOR
- INFO

## Modificar Umbrales

Para cambiar los umbrales de validación, edita el archivo `.github/workflows/sonarqube-scan.yml`:

### Cambiar Umbral de Coverage

```yaml
# En el step "Check Coverage"
if (( $(echo "$COVERAGE < 90" | bc -l) )); then  # Cambia 90 por tu umbral
```

### Cambiar Umbrales de Severidad

```yaml
# En el step "Check Severity"
if [ "$BLOCKER" -gt 1 ]; then  # Cambia 1 por tu umbral
if [ "$CRITICAL" -gt 1 ]; then  # Cambia 1 por tu umbral
if [ "$MAJOR" -gt 2 ]; then  # Cambia 2 por tu umbral
```

## Ejemplo de Salida

### IS_COVERAGE=TRUE

```
Validando coverage en SonarQube...
Coverage actual: 47.45%
❌ Coverage 47.45% es menor al 90% requerido
Error: Process completed with exit code 1
```

### IS_COVERAGE=FALSE

```
Validando severidad de issues en SonarQube...
Fetching severity metrics...

=== Resumen de Issues por Severidad ===
Blocker: 0
Critical: 5
Major: 15
Minor: 10
Info: 3

✅ PASS: Blocker (0) dentro del límite (≤1)
❌ FAIL: Critical (5) excede el máximo permitido (1)
✅ PASS: Major (15) dentro del límite (≤2)
⚠️  WARNING: Minor (10) debería ser 0
ℹ️  INFO: Info (3) presente (no bloqueante)

❌ El Quality Gate falló por severidad
Error: Process completed with exit code 1
```

## Configurar Secrets en GitHub

Necesitas estos secrets en tu repositorio:

| Secret | Valor |
|--------|-------|
| `SONAR_HOST_URL` | URL de SonarQube (ej: https://tu-ngrok.ngrok.io) |
| `SONAR_TOKEN` | Token de autenticación de SonarQube |

## Integración con Pull Requests

Para validar automáticamente en PRs con diferentes modos:

### Opción 1: Validar Coverage en PRs a `main`

```yaml
on:
  pull_request:
    branches: [ main ]
env:
  IS_COVERAGE: 'TRUE'  # Validar coverage en PRs a main
```

### Opción 2: Validar Severidad en PRs a `develop`

```yaml
on:
  pull_request:
    branches: [ develop ]
env:
  IS_COVERAGE: 'FALSE'  # Validar severidad en PRs a develop
```

### Opción 3: Validar ambos

Agrega dos jobs separados en el workflow:

```yaml
jobs:
  sonarqube-coverage:
    name: SonarQube Scan (Coverage)
    env:
      IS_COVERAGE: 'TRUE'
    # ... steps ...

  sonarqube-severity:
    name: SonarQube Scan (Severity)
    env:
      IS_COVERAGE: 'FALSE'
    # ... steps ...
```

## Troubleshooting

### Error: "bc: command not found"

El workflow usa `bc` para comparaciones numéricas. Si falla, instala:

```yaml
- name: Install bc
  run: sudo apt-get install -y bc
```

### Error: "jq: command not found"

El workflow usa `jq` para procesar JSON. Si falla, instala:

```yaml
- name: Install jq
  run: sudo apt-get install -y jq
```

### Error: API Authentication

Verifica que:
1. El token sea correcto
2. El token tenga permisos suficientes
3. La URL de SonarQube sea accesible desde GitHub Actions

### Coverage muestra 0%

Verifica que:
1. Los tests se ejecuten si IS_COVERAGE=TRUE
2. El archivo `coverage.xml` se genere
3. El parámetro `sonar.python.coverage.reportPaths=coverage.xml` esté configurado

## Resumen

| Modo | Validación | Umbral |
|------|------------|--------|
| IS_COVERAGE=TRUE | Coverage | ≥ 90% |
| IS_COVERAGE=FALSE | Blocker | ≤ 1 |
| IS_COVERAGE=FALSE | Critical | ≤ 1 |
| IS_COVERAGE=FALSE | Major | ≤ 2 |
| IS_COVERAGE=FALSE | Minor | = 0 (warning) |
| IS_COVERAGE=FALSE | Info | = 0 (info) |
