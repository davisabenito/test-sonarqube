# SonarCloud Analysis with GitHub Actions

Este proyecto utiliza SonarCloud para análisis de calidad de código integrado con GitHub Actions.

## 📋 Requisitos Previos

1. **Cuenta en SonarCloud**
   - Regístrate en https://sonarcloud.io
   - Conecta tu cuenta de GitHub

2. **Proyecto en SonarCloud**
   - Crea un nuevo proyecto en SonarCloud
   - Conecta tu repositorio de GitHub
   - Anota el **Project Key** y **Organization Key**

3. **Token de SonarCloud**
   - Ve a My Account → Security
   - Genera un nuevo token
   - Anota el token (solo se muestra una vez)

## 🔧 Configuración en GitHub

### Paso 1: Configurar Secrets

Ve a tu repositorio en GitHub → Settings → Secrets and variables → Actions → New repository secret

Agrega el siguiente secret:

| Nombre del Secret | Descripción |
|------------------|-------------|
| `SONAR_TOKEN` | Token de autenticación de SonarCloud |

**Importante:** No incluyas el token directamente en el código o en archivos públicos.

### Paso 2: Configurar el Workflow

El workflow `.github/workflows/sonarqube-scan.yml` ya está configurado con:

- **Organization Key**: Configurado en el workflow
- **Project Key**: Configurado en el workflow
- **Modos de validación**: Coverage o Severidad

## 🚀 Ejecutar el Análisis

### Automático (Push o Pull Request)

El análisis se ejecuta automáticamente en:
- Push a las ramas `main` o `develop`
- Pull requests a estas ramas

### Manual (Workflow Dispatch)

1. Ve a tu repositorio en GitHub
2. Clic en la pestaña **Actions**
3. Selecciona el workflow **SonarCloud Scan**
4. Clic en **Run workflow** (botón azul arriba a la derecha)
5. Selecciona el modo:
   - **is_coverage**: `TRUE` (valida coverage) o `FALSE` (valida severidad)
6. Clic en **Run workflow** (botón verde)

## 📊 Modos de Validación

### Modo 1: Validación de Coverage (IS_COVERAGE=TRUE)

Valida que el coverage de código sea ≥ 90%.

Si el coverage es menor a 90%, el workflow fallará.

**Steps ejecutados:**
- Run tests with coverage
- Verify coverage.xml
- SonarCloud Scan
- Debug SonarCloud API Response
- Check coverage from SonarCloud
- SonarCloud Quality Gate

### Modo 2: Validación de Severidad (IS_COVERAGE=FALSE)

Valida que los issues por severidad estén dentro de los límites usando **dos herramientas**:

#### A. Validación de SonarCloud (Validate SonarCloud severity thresholds)

Usa las severidades nativas de SonarCloud:

| Severidad SonarCloud | Máximo Permitido | Acción si excede |
|---------------------|------------------|------------------|
| BLOCKER | 1 | ❌ Fails |
| CRITICAL | 1 | ❌ Fails |
| MAJOR | 2 | ❌ Fails |
| MINOR | 0 | ⚠️ Warning |
| INFO | 0 | ℹ️ Info (no bloqueante) |

**Nota:** SonarCloud usa severidades BLOCKER/CRITICAL/MAJOR/MINOR/INFO, mientras que Bandit usa HIGH/MEDIUM/LOW.

#### B. Validación de Bandit (Validate Bandit thresholds)

Usa las severidades de Bandit (security scanner):

| Severidad Bandit | Máximo Permitido | Acción si excede |
|------------------|------------------|------------------|
| HIGH | 2 | ❌ Fails |
| MEDIUM | 5 | ❌ Fails |
| LOW | Sin límite | ℹ️ Info |

**Steps ejecutados:**
- Run Bandit Security Scan
- SonarCloud Scan
- Debug SonarCloud API Response
- Validate SonarCloud severity thresholds
- Validate Bandit thresholds
- SonarCloud Quality Gate

## 📈 Ver Resultados

### En GitHub Actions

1. Ve a la pestaña **Actions**
2. Selecciona la ejecución del workflow
3. Expande los steps para ver:
   - Resumen de coverage o severidad
   - ✅ PASS o ❌ FAIL
   - Métricas detalladas

### En SonarCloud

1. Ve a https://sonarcloud.io
2. Busca tu proyecto
3. Verás:
   - Quality Gate status
   - Coverage
   - Bugs, Vulnerabilities, Code Smells
   - Duplications
   - Security Hotspots

## 🔍 Ejemplo de Salida

### IS_COVERAGE=TRUE

```
Validando coverage en SonarCloud...
Coverage actual: 47.45%
❌ Coverage 47.45% es menor al 90% requerido
Error: Process completed with exit code 1
```

### IS_COVERAGE=FALSE

#### Validación de SonarCloud Severities

```
=== Validando umbrales de severidad de SonarCloud ===
Umbrales configurados:
  BLOCKER ≤ 1
  CRITICAL ≤ 1
  MAJOR ≤ 2
  MINOR = 0 (warning)
  INFO = 0 (info)

=== Issues por severidad ===
BLOCKER: 0 (máximo: 1)
CRITICAL: 5 (máximo: 1)
MAJOR: 15 (máximo: 2)
MINOR: 10 (esperado: 0)
INFO: 3 (esperado: 0)

✅ BLOCKER: 0 dentro del límite (≤1)
❌ CRITICAL: 5 excede el máximo permitido (1)
❌ MAJOR: 15 excede el máximo permitido (2)
⚠️  MINOR: 10 debería ser 0
ℹ️  INFO: 3 presente (no bloqueante)

❌ Los umbrales de severidad de SonarCloud no cumplen los requisitos
```

#### Validación de Bandit

```
Bandit total: 8
HIGH: 1 (máximo permitido: 2)
MEDIUM: 7 (máximo permitido: 5)

❌ Bandit excede los umbrales de severidad.
```

## 🛠️ Modificar Umbrales

Para cambiar los umbrales de validación, edita `.github/workflows/sonarqube-scan.yml`:

### Cambiar Umbral de Coverage

```yaml
# En el step "Check coverage from SonarCloud"
if awk -v c="$COVERAGE" 'BEGIN { exit !(c < 90) }'; then  # Cambia 90 por tu umbral
```

### Cambiar Umbrales de Severidad SonarCloud

```yaml
# En el step "Validate SonarCloud severity thresholds"
if [ "$BLOCKER" -gt 1 ]; then  # Cambia 1 por tu umbral
if [ "$CRITICAL" -gt 1 ]; then  # Cambia 1 por tu umbral
if [ "$MAJOR" -gt 2 ]; then  # Cambia 2 por tu umbral
```

### Cambiar Umbrales de Severidad Bandit

```yaml
# En el step "Validate Bandit thresholds"
if [ "$HIGH" -gt 2 ]; then  # Cambia 2 por tu umbral
if [ "$MEDIUM" -gt 5 ]; then  # Cambia 5 por tu umbral
```

## 📁 Estructura del Proyecto

```
pruebas-sonarqube/
├── .github/
│   └── workflows/
│       └── sonarqube-scan.yml    # Workflow de GitHub Actions
├── data_cleaning.py              # Código con malas prácticas
├── test_data_cleaning.py         # Tests (coverage ~47%)
├── requirements.txt               # Dependencias Python
├── sonar-project.properties      # Configuración SonarQube (local)
└── README-GITHUBACTIONS.md       # Este archivo
```

## 🔐 Seguridad

- El token de SonarCloud se almacena como un secret en GitHub
- Nunca compartas el token en el código o en archivos públicos
- Los secrets están encriptados y solo son accesibles por los workflows del repositorio

## 📚 Recursos

- [Documentación de SonarCloud](https://docs.sonarcloud.io/)
- [GitHub Actions para SonarQube](https://github.com/marketplace/actions/sonarqube-scan)
- [SonarScanner CLI](https://docs.sonarcloud.io/latest/analyzing-source-code/sonarscanner/)
- [Python Quality Profile](https://docs.sonarcloud.io/latest/analyzing-source-code/languages/python/)

## ❓ Preguntas Frecuentes

### ¿Por qué el workflow falla con "Unrecognized option"?

Este error ocurrió en versiones anteriores cuando se usaba SonarQube local con SonarCloud. El workflow actual está configurado para SonarCloud y debería funcionar correctamente.

### ¿Cómo cambiar de SonarCloud a SonarQube local?

Si deseas usar SonarQube local en lugar de SonarCloud:

1. Modifica `.github/workflows/sonarqube-scan.yml`
2. Agrega el secret `SONAR_HOST_URL` en GitHub
3. Cambia la URL de la API de `https://sonarcloud.io` a tu URL local
4. Elimina el parámetro `-Dsonar.organization`

### ¿Cómo aumentar el coverage actual?

El código actual tiene un coverage de ~47%. Para aumentarlo:

1. Agrega más tests en `test_data_cleaning.py`
2. Cubre las funciones que actualmente no están probadas
3. Re-ejecuta el análisis para ver el nuevo coverage

### ¿El workflow consume cuota de SonarCloud?

SonarCloud tiene límites de análisis según tu plan:
- Free: 1 proyecto público, análisis ilimitado
- Team: Proyectos privados, análisis ilimitado

Verifica tu plan en SonarCloud para más detalles.

## 🆘 Troubleshooting

### Error: "SONAR_TOKEN not found"

Verifica que:
1. El secret `SONAR_TOKEN` esté configurado en tu repositorio
2. El nombre del secret sea exactamente `SONAR_TOKEN` (mayúsculas)
3. El token sea válido y no haya expirado

### Error: "Project not found"

Verifica que:
1. El Project Key en el workflow coincida con el de SonarCloud
2. El proyecto exista en tu organización de SonarCloud
3. Tu cuenta de GitHub esté conectada a SonarCloud

### Coverage muestra 0%

Verifica que:
1. Los tests se ejecuten si IS_COVERAGE=TRUE
2. El archivo `coverage.xml` se genere
3. El parámetro `sonar.python.coverage.reportPaths=coverage.xml` esté configurado

## 📝 Notas

- Este proyecto está diseñado para probar SonarCloud con código que contiene malas prácticas intencionales
- El coverage actual es ~47%, por debajo del 90% requerido
- El Quality Gate está configurado para fail cuando no cumple los umbrales
- Puedes ajustar los umbrales según tus necesidades

## 🔀 Diferencia entre SonarCloud y Bandit Severities

El workflow valida severidades de **dos herramientas diferentes** cuando `IS_COVERAGE=FALSE`:

### SonarCloud Severities (Quality/Code Smells/Security)

| SonarCloud | Equivalente Genérico | Descripción |
|------------|---------------------|-------------|
| BLOCKER | Critical | Debe corregirse inmediatamente |
| CRITICAL | High | Problema grave |
| MAJOR | Medium | Problema importante |
| MINOR | Low | Problema menor |
| INFO | Info | Informativo |

SonarCloud analiza:
- Code Smells (mantenibilidad)
- Bugs (funcionalidad)
- Vulnerabilities (seguridad)
- Security Hotspots (seguridad)

### Bandit Severities (Security Only)

| Bandit | Equivalente Genérico | Descripción |
|--------|---------------------|-------------|
| HIGH | Critical | Vulnerabilidad crítica |
| MEDIUM | Medium | Vulnerabilidad media |
| LOW | Low | Vulnerabilidad menor |

Bandit analiza **solo** vulnerabilidades de seguridad en Python.

### ¿Por qué dos validaciones?

1. **SonarCloud**: Análisis completo de calidad (code smells, bugs, duplications, coverage, seguridad)
2. **Bandit**: Análisis especializado en seguridad Python, más estricto para vulnerabilidades

Puedes configurar umbrales diferentes para cada herramienta según tus políticas de calidad y seguridad.
