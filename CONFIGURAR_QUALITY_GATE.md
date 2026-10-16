# Configurar Quality Gate para que Falle

## ¿Por qué el Quality Gate está Passed?

El Quality Gate por defecto de SonarQube ("Sonar way") se basa en **New Code** (código nuevo desde el último análisis). Como este es un proyecto nuevo, casi todo es "New Code" pero las condiciones por defecto son:

| Condición | Umbral | Estado actual |
|-----------|--------|--------------|
| Coverage on New Code | No configurado por defecto | 59.4% - No se evalúa |
| Rating on New Code (Bugs) | A | A - ✅ Passed |
| Rating on New Code (Vulnerabilities) | A | A - ✅ Passed |
| Rating on New Code (Code Smells) | A | A - ✅ Passed |
| Reliability Rating on New Code | A | A - ✅ Passed |
| Security Rating on New Code | A | A - ✅ Passed |
| Maintainability Rating on New Code | A | A - ✅ Passed |

Por eso muestra **Passed** aunque el coverage sea 59.4%.

## Solución: Crear un Quality Gate Personalizado

### Paso 1: Crear un Quality Gate Personalizado

1. Ve a http://localhost:9000
2. Clic en **Quality Gates** (menú superior)
3. Clic en **Create** (botón azul arriba a la derecha)
4. Nombre: `Pruebas SonarQube - Strict`
5. Clic en **Create**

### Paso 2: Configurar Condiciones del Quality Gate

En el Quality Gate recién creado, clic en **Add Condition** y agrega:

#### Condición 1: Coverage en New Code
- **Condition**: Coverage on New Code
- **Operator**: < (menor que)
- **Threshold**: 90.0
- **Error**: When threshold is not met
- Clic en **Add Condition**

#### Condición 2: Code Smells en New Code
- **Condition**: Rating on New Code
- **Metric**: Code Smells
- **Operator**: Worse than
- **Threshold**: B
- **Error**: When threshold is not met
- Clic en **Add Condition**

#### Condición 3: Security Hotspots Reviewed
- **Condition**: Security Hotspots Reviewed
- **Operator**: < (menor que)
- **Threshold**: 100
- **Error**: When threshold is not met
- Clic en **Add Condition**

### Paso 3: Asignar el Quality Gate al Proyecto

1. Ve a **Quality Gates**
2. Clic en **Pruebas SonarQube - Strict** (tu Quality Gate)
3. Clic en **Set as Default** (opcional, para todos los proyectos)
4. O específicamente para tu proyecto:
   - Ve a **Projects** → **test-sonar**
   - Clic en **Project Settings** → **Quality Gate**
   - Selecciona `Pruebas SonarQube - Strict`
   - Clic en **Save**

### Paso 4: Re-ejecutar el Análisis

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
export SONAR_HOST_URL=http://localhost:9000
export SONAR_TOKEN=sqp_35ac38bccff8c00b4916273e59ab8c7e8da1f2f2
export SONAR_PROJECT_KEY=test-sonar
./run_analysis_with_coverage.sh
```

### Paso 5: Ver el Quality Gate Failed

Ahora deberías ver:
- **Quality Gate Status**: ❌ FAILED
- **Reason**: Coverage on New Code is 59.4% but should be ≥ 90.0%

## Alternativa: Modificar el Quality Gate "Sonar way"

Si no quieres crear uno nuevo, puedes modificar el "Sonar way":

1. Ve a **Quality Gates**
2. Clic en **Sonar way**
3. Clic en **Copy** para crear una copia
4. Renómbrala a `Sonar way - Custom`
5. Agrega las condiciones mencionadas arriba
6. Asigna esta copia a tu proyecto

## Código Duplicado Agregado

He agregado **6 bloques de código duplicado** para aumentar el porcentaje de duplicaciones:

| Bloque | Funciones | Líneas duplicadas |
|--------|-----------|-------------------|
| 1 | `duplicado_1()`, `duplicado_2()`, `duplicado_3()` | ~12 líneas × 3 |
| 2 | `procesar_datos_v1()`, `procesar_datos_v2()`, `procesar_datos_v3()` | ~8 líneas × 3 |
| 3 | `validar_datos_v1()`, `validar_datos_v2()`, `validar_datos_v3()` | ~12 líneas × 3 |
| 4 | `limpiar_texto_v1()`, `limpiar_texto_v2()`, `limpiar_texto_v3()` | ~8 líneas × 3 |
| 5 | `calcular_estadisticas_v1()`, `calcular_estadisticas_v2()`, `calcular_estadisticas_v3()` | ~10 líneas × 3 |

**Total**: ~150 líneas de código duplicado

## Agregar Condición de Duplicaciones al Quality Gate

Si quieres que también falle por duplicaciones:

### Agregar Condición de Duplicaciones

En tu Quality Gate personalizado, agrega:

#### Condición 4: Duplications en New Code
- **Condition**: Duplicated Lines on New Code
- **Operator**: > (mayor que)
- **Threshold**: 3.0
- **Error**: When threshold is not met
- Clic en **Add Condition**

Esto hará que el Quality Gate falle si hay más del 3% de duplicaciones.

## Resumen de Condiciones Recomendadas

Para un Quality Gate estricto que falle con tu código actual:

| Condición | Operador | Umbral | Estado actual | Resultado |
|-----------|----------|---------|--------------|-----------|
| Coverage on New Code | < | 90.0% | 59.4% | ❌ Failed |
| Rating on New Code (Code Smells) | Worse than | B | A | ✅ Passed |
| Security Hotspots Reviewed | < | 100% | 0% | ❌ Failed |
| Duplicated Lines on New Code | > | 3.0% | 0.0% | ✅ Passed |

## Ver Condiciones del Quality Gate

1. Ve a http://localhost:9000/quality_gates
2. Clic en tu Quality Gate
3. Verás todas las condiciones configuradas

## Re-ejecutar después de agregar código duplicado

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
export SONAR_HOST_URL=http://localhost:9000
export SONAR_TOKEN=sqp_35ac38bccff8c00b4916273e59ab8c7e8da1f2f2
export SONAR_PROJECT_KEY=test-sonar
./run_analysis_with_coverage.sh
```

Ahora deberías ver:
- **Coverage**: ~59.4% (sin cambios significativos)
- **Duplications**: ~5-10% (por el código duplicado agregado)
- **Quality Gate**: ❌ FAILED (por coverage < 90%)

## Nota sobre "New Code" vs "Overall Code"

SonarQube evalúa principalmente el **New Code** (código nuevo desde el último análisis). Si quieres evaluar todo el código:

1. Ve a **Quality Gates**
2. Clic en tu Quality Gate
3. Agrega condiciones para **Overall Code** (no solo New Code)

Ejemplo:
- **Condition**: Coverage on Overall Code
- **Operator**: <
- **Threshold**: 90.0

## Quality Gate Default en sonar-project.properties

También puedes configurar el Quality Gate en el archivo de propiedades:

```properties
# Configurar un Quality Gate específico
sonar.qualitygate=gates:Pruebas SonarQube - Strict
```

Sin embargo, el Quality Gate debe existir en SonarQube primero.

## Verificar el Quality Gate Asignado

1. Ve a http://localhost:9000/projects
2. Clic en `test-sonar`
3. Clic en **Project Settings** → **Quality Gate**
4. Verás qué Quality Gate está asignado

## Quick Reference

### Para que el Quality Gate falle con tu código actual:

1. ✅ Crear Quality Gate personalizado
2. ✅ Agregar condición: Coverage on New Code < 90%
3. ✅ Asignar Quality Gate al proyecto
4. ✅ Re-ejecutar análisis
5. ✅ Ver Quality Gate FAILED en SonarQube

### Ver duplicaciones:

1. ✅ Ya agregué 6 bloques de código duplicado
2. ✅ Re-ejecutar análisis
3. ✅ Ver "Duplications" en el dashboard (debería ser ~5-10%)
