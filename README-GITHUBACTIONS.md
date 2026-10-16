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

### Modo 2: Validación de Severidad (IS_COVERAGE=FALSE)

Valida que los issues por severidad estén dentro de los límites:

| Severidad | Máximo Permitido | Acción si excede |
|-----------|------------------|------------------|
| Blocker | 1 | ❌ Fails |
| Critical | 1 | ❌ Fails |
| Major | 2 | ❌ Fails |
| Minor | 0 | ⚠️ Warning |
| Info | 0 | ℹ️ Info (no bloqueante) |

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

```
Validando severidad de issues en SonarCloud...
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
```

## 🛠️ Modificar Umbrales

Para cambiar los umbrales de validación, edita `.github/workflows/sonarqube-scan.yml`:

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
