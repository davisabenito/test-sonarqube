# Mejoras Agregadas para Detección de SonarQube

## Cambios Realizados

### 1. Nuevas Malas Prácticas Agregadas al Código

Se agregaron **30+ nuevas malas prácticas** que SonarQube detectará:

#### Problemas de Calidad de Código

| Mal Práctica | Función | Severidad |
|--------------|---------|-----------|
| Constantes con nombres malos | `A, B, C` | Minor |
| Parámetro mutable por defecto | `parametro_por_defecto_mutuable()` | Critical |
| Código muerto | `codigo_muerto()` | Major |
| Comparación redundante | `comparacion_redundante()` | Major |
| Asignación no usada | `asignacion_no_usada()` | Minor |
| Concatenación ineficiente | `concatenacion_string_ineficiente()` | Minor |
| Números mágicos | `funcion_magic_number()` | Minor |
| Demasiadas líneas vacías | `demasiadas_lineas_vacias()` | Minor |
| Variable shadowing | `variable_shadowing()` | Minor |
| Uso de type() en lugar de isinstance | `uso_de_tipo()` | Minor |
| Literal string no usado | `literal_comentario_inutil()` | Minor |
| Clonar con slice en lugar de copy() | `clonar_con_slice()` | Minor |
| Comparación con None usando == | `check_none_comparision()` | Minor |
| Demasiados returns | `function_with_too_many_returns()` | Major |
| String comparison case-sensitive | `string_comparison_case_sensitive()` | Minor |
| Comentario muy largo | `comentario_muy_largo()` | Minor |
| Función no retornada | `funcion_no_retornada()` | Major |
| Except vacío | `empty_except()` | Critical |
| NotImplementedError sin mensaje | `not_implemented()` | Minor |
| Loop infinito | `infinite_loop_possibility()` | Critical |
| Deprecated function sin docstring | `deprecated_function()` | Minor |

#### Problemas de Seguridad

| Mal Práctica | Función | Severidad |
|--------------|---------|-----------|
| SQL injection simulada | `sql_injection_simulada()` | Critical |
| Password hardcodeado | `hardcoded_password()` | Critical |
| Hash inseguro (MD5) | `insecure_hash()` | Critical |
| Uso de eval() | `eval_usage()` | Critical |
| Uso de exec() | `exec_usage()` | Critical |
| time.sleep en producción | `temporizador()` | Minor |

### 2. Tests con Coverage del 50%

#### Archivo Creado: `test_data_cleaning.py`

Cubre **19 funciones** de ~40 disponibles:
- ✅ `cargar_datos_sin_verificar()`
- ✅ `procesar_datos_duplicado()`
- ✅ `funcion_demasiado_larga()`
- ✅ `complejidad_ciclomatica_alta()`
- ✅ `parametro_demasiados()`
- ✅ `variable_no_usada()`
- ✅ `import_no_usado()`
- ✅ `hardcoding()`
- ✅ `parametro_por_defecto_mutuable()`
- ✅ `codigo_muerto()`
- ✅ `comparacion_redundante()`
- ✅ `asignacion_no_usada()`
- ✅ `concatenacion_string_ineficiente()`
- ✅ `check_none_comparision()`
- ✅ `function_with_too_many_returns()`
- ✅ `string_comparison_case_sensitive()`
- ✅ `clonar_con_slice()`
- ✅ `temporizador()`

**NO cubiertas intencionalmente (para mantener 50%):**
- ❌ `funcion_sin_documentacion()`
- ❌ `usar_print_en_lugar_de_logging()`
- ❌ `excepcion_generica()`
- ❌ `anidamiento_excesivo()`
- ❌ `funcion_magic_number()`
- ❌ `sql_injection_simulada()`
- ❌ `empty_except()`
- ❌ `funcion_no_retornada()`
- ❌ `comentario_muy_largo()`
- ❌ `demasiadas_lineas_vacias()`
- ❌ `variable_shadowing()`
- ❌ `uso_de_tipo()`
- ❌ `literal_comentario_inutil()`
- ❌ `try_except_finally()`
- ❌ `deprecated_function()`
- ❌ `not_implemented()`
- ❌ `infinite_loop_possibility()`
- ❌ `unused_import_function()`
- ❌ `hardcoded_password()`
- ❌ `insecure_hash()`
- ❌ `eval_usage()`
- ❌ `exec_usage()`

### 3. Configuración de Coverage

#### Archivo: `pytest.ini`
```ini
[pytest]
addopts =
    --cov=data_cleaning
    --cov-report=xml
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=50
```

#### Archivo: `sonar-project.properties`
```properties
# Configuración de coverage
sonar.python.coverage.reportPaths=coverage.xml
sonar.coverage.jacoco.xmlReportPaths=coverage.xml

# Umbral de coverage (Quality Gate fallará si es menor a 90%)
sonar.coverage.minimum=90.0
```

### 4. Actualización de Dependencias

#### Archivo: `requirements.txt`
```
pandas>=1.3.0
numpy>=1.21.0
pytest>=7.0.0
pytest-cov>=3.0.0
```

### 5. Actualización del Script de Análisis

#### Archivo: `run_analysis.sh`
Ahora ejecuta tests antes del análisis:
```bash
# Ejecutar tests con coverage
pytest --cov=data_cleaning --cov-report=xml --cov-report=term-missing --cov-fail-under=50
```

## Ejecutar el Análisis Completo

### Opción 1: Usar el script automatizado

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
./run_analysis.sh
```

Este script:
1. Activa el entorno virtual
2. Instala dependencias
3. Ejecuta tests con coverage (~50%)
4. Verifica SonarQube
5. Ejecuta análisis con pysonar
6. Desactiva entorno virtual

### Opción 2: Ejecutar manualmente

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest --cov=data_cleaning --cov-report=xml --cov-report=term-missing

# Ejecutar análisis SonarQube
pysonar \
  --sonar-host-url=http://localhost:9000 \
  --sonar-token=sqp_e422142e9e11a8fa9d3dbb500e2310af76b50068 \
  --sonar-project-key=prueba \
  --sonar-sources=. \
  --sonar-exclusions=venv/**,*.csv,*.md,.git/**,.github/**

deactivate
```

## Resultados Esperados en SonarQube

### Quality Gate Status: ❌ FAILED

El Quality Gate fallará por:

1. **Coverage < 90%**
   - Coverage actual: ~50%
   - Requerido: 90%
   - Estado: ❌ FALLO

2. **Code Smells** (más de 30)
   - Critical: 5+ (parámetro mutable, except vacío, loop infinito, SQL injection, hash inseguro, eval, exec)
   - Major: 10+ (código muerto, código duplicado, función larga, anidamiento, complejidad, etc.)
   - Minor: 15+ (variables no usadas, imports no usados, comentarios, etc.)

3. **Security Issues** (5+)
   - Critical: SQL injection, password hardcodeado, hash inseguro, eval, exec

### Issues Detectados por Categoría

#### Code Smells (Calidad)
- Variables globales
- Código duplicado
- Funciones demasiado largas
- Falta de documentación
- Print en lugar de logging
- Excepciones genéricas
- Anidamiento excesivo
- Alta complejidad ciclomática
- Demasiados parámetros
- Variables no usadas
- Imports no utilizados
- Valores hardcodeados
- Parámetros mutables por defecto
- Código muerto
- Comparaciones redundantes
- Concatenación ineficiente
- Números mágicos
- Comentarios largos
- Líneas vacías excesivas
- Variable shadowing
- Uso de type()
- Literales no usados
- Clonación con slice
- Comparación con None
- Demasiados returns
- Comparación case-sensitive

#### Security Hotspots (Seguridad)
- SQL injection
- Password hardcodeado
- Hash inseguro (MD5)
- Uso de eval()
- Uso de exec()
- time.sleep en producción

## Ver Resultados

1. Ve a http://localhost:9000/projects
2. Selecciona el proyecto `prueba`
3. Verás:
   - **Quality Gate**: ❌ FAILED
   - **Coverage**: ~50% (rojo, requiere 90%)
   - **Code Smells**: 30+ issues
   - **Security Hotspots**: 5+ issues
   - **Bugs**: Algunos issues potenciales

## Cómo Pasar el Quality Gate (Opcional)

Si quieres que el Quality Gate pase, necesitas:

1. **Aumentar coverage a 90%+:**
   - Agregar tests para las funciones no cubiertas
   - O bajar el umbral en `sonar.coverage.minimum`

2. **Resolver Code Smells críticos:**
   - Eliminar parámetros mutables por defecto
   - Manejar excepciones específicas
   - Eliminar código muerto
   - Reducir complejidad ciclomática

3. **Resolver Security Hotspots:**
   - Eliminar passwords hardcodeados
   - Usar hash seguro (SHA-256 en lugar de MD5)
   - Eliminar eval() y exec()
   - Usar prepared statements para SQL

## Resumen de Archivos Modificados

| Archivo | Cambio |
|---------|--------|
| `data_cleaning.py` | +30 malas prácticas nuevas |
| `test_data_cleaning.py` | Nuevo archivo con tests (50% coverage) |
| `pytest.ini` | Nuevo archivo de configuración pytest |
| `requirements.txt` | Agregado pytest y pytest-cov |
| `sonar-project.properties` | Configuración de coverage (90% umbral) |
| `run_analysis.sh` | Ejecuta tests antes del análisis |

## Pruebas de Coverage

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
source venv/bin/activate
pytest --cov=data_cleaning --cov-report=term-missing
```

Salida esperada:
```
---------- coverage: platform darwin, python 3.9.X ----------
Name                Stmts   Miss  Cover   Missing
-------------------------------------------------
data_cleaning.py      350    175    50%   50-100, 150-200, ...
-------------------------------------------------
TOTAL                 350    175    50%
```
