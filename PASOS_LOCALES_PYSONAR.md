# Pasos para Ejecutar Análisis Local con pysonar

Guía paso a paso para ejecutar el análisis de SonarQube localmente usando `pysonar` con un entorno virtual.

## Paso 1: Crear y Activar Entorno Virtual

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual (macOS/Linux)
source venv/bin/activate

# Verificar que está activado (deberías ver (venv) en el prompt)
which python
# Debe mostrar: /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube/venv/bin/python
```

## Paso 2: Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Instalar pysonar
pip install pysonar
```

## Paso 3: Verificar Instalación

```bash
# Verificar versión de pysonar
pysonar --version

# Verificar que Python funciona
python test_cleaning.py
```

## Paso 4: Asegurar que SonarQube esté Corriendo

```bash
# Verificar que SonarQube esté accesible
curl http://localhost:9000/api/server/version

# Debería devolver algo como: {"version":"9.9.0.65466"}
```

Si SonarQube no está corriendo, inicia Docker Compose:
```bash
docker-compose up -d
```

## Paso 5: Crear Proyecto en SonarQube (si no existe)

1. Abre http://localhost:9000 en tu navegador
2. Inicia sesión (admin/admin)
3. Clic en "Create Project"
4. Project name: `prueba`
5. Project key: `prueba`
6. Selecciona "Manually"
7. Genera y copia el token

## Paso 6: Ejecutar Análisis con pysonar

### Opción A: Usando parámetros en línea de comandos

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
source venv/bin/activate

pysonar \
  --sonar-host-url=http://localhost:9000 \
  --sonar-token=sqp_e422142e9e11a8fa9d3dbb500e2310af76b50068 \
  --sonar-project-key=prueba \
  --sonar-sources=data_cleaning.py \
  --sonar-tests=test_data_cleaning.py \
  --sonar-exclusions=venv/**,*.csv,*.md,.git/**,.github/**,pytest.ini,coverage.xml,.coverage
```

**Importante:**
- `--sonar-sources=data_cleaning.py` - Solo analiza el código principal
- `--sonar-tests=test_data_cleaning.py` - Solo analiza los tests
- `--sonar-exclusions` excluye:
  - `venv/**` - Todo el entorno virtual
  - `*.csv` - Archivos CSV
  - `*.md` - Archivos Markdown
  - `.git/**` - Directorio .git
  - `.github/**` - Workflows de GitHub
  - `pytest.ini` - Configuración de pytest
  - `coverage.xml` - Reporte de coverage
  - `.coverage` - Archivo de coverage

### Opción B: Usando archivo de configuración

Crea un archivo `.pysonar.yaml`:

```yaml
sonar:
  host-url: http://localhost:9000
  token: sqp_e422142e9e11a8fa9d3dbb500e2310af76b50068
  project-key: prueba
  project-name: Prueba SonarQube
  project-version: 1.0
  sources: .
  exclusions:
    - "venv/**"
    - "**/*.csv"
    - "**/*.md"
    - ".git/**"
    - ".github/**"
  source-encoding: UTF-8
  python-version: "3.9"
```

Luego ejecuta:
```bash
pysonar
```

### Opción C: Usando variables de entorno

```bash
export SONAR_HOST_URL=http://localhost:9000
export SONAR_TOKEN=sqp_e422142e9e11a8fa9d3dbb500e2310af76b50068
export SONAR_PROJECT_KEY=prueba

pysonar
```

## Paso 7: Ver Resultados

1. Ve a http://localhost:9000/projects
2. Busca el proyecto `prueba`
3. Verás el dashboard con:
   - Quality Gate (Pasó/Falló)
   - Bugs
   - Code Smells
   - Vulnerabilities
   - Duplications

## Paso 8: Ver Issues Detectados

En SonarQube:
1. Clic en el proyecto `prueba`
2. Clic en la pestaña **Issues**
3. Filtra por:
   - **Type**: Code Smell (verás las malas prácticas)
   - **Severity**: Critical, Major, Minor

Deberías ver issues como:
- "Refactor this function to reduce its Cognitive Complexity"
- "Remove this unused import"
- "Remove this unused variable"
- "Remove this commented out code"
- "Define a constant instead of duplicating this literal"

## Paso 9: Desactivar Entorno Virtual

Cuando termines:

```bash
deactivate
```

## Script Automatizado

Crea un script `run_analysis.sh` para automatizar el proceso:

```bash
#!/bin/bash

# Activar entorno virtual
source venv/bin/activate

# Ejecutar análisis
pysonar \
  --sonar-host-url=http://localhost:9000 \
  --sonar-token=sqp_e422142e9e11a8fa9d3dbb500e2310af76b50068 \
  --sonar-project-key=prueba

# Desactivar entorno virtual
deactivate
```

Hazlo ejecutable:
```bash
chmod +x run_analysis.sh
```

Ejecuta:
```bash
./run_analysis.sh
```

## Troubleshooting

### Error: "pysonar: command not found"

```bash
# Asegúrate de estar en el entorno virtual
source venv/bin/activate

# Reinstalar pysonar
pip install pysonar
```

### Error: "Connection refused"

```bash
# Verificar que SonarQube esté corriendo
curl http://localhost:9000/api/server/version

# Si no responde, inicia SonarQube
docker-compose up -d
```

### Error: "Invalid token"

```bash
# Verifica que el token sea correcto
# Debe comenzar con "sqp_"
# Genera un nuevo token en SonarQube si es necesario
```

### Error: "Project key not found"

```bash
# Asegúrate de que el proyecto exista en SonarQube
# El project key debe coincidir exactamente
# Ve a http://localhost:9000/projects para verificar
```

## Alternativa: Usar sonar-scanner (Opcional)

Si pysonar no funciona, puedes usar sonar-scanner:

```bash
# Instalar sonar-scanner
brew install sonar-scanner

# Ejecutar análisis
sonar-scanner \
  -Dsonar.projectKey=prueba \
  -Dsonar.projectName=Prueba SonarQube \
  -Dsonar.projectVersion=1.0 \
  -Dsonar.sources=. \
  -Dsonar.sourceEncoding=UTF-8 \
  -Dsonar.exclusions=**/*.csv,**/*.md \
  -Dsonar.python.version=3.9 \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=sqp_e422142e9e11a8fa9d3dbb500e2310af76b50068
```

## Resumen de Comandos

```bash
# 1. Crear entorno virtual
python3 -m venv venv

# 2. Activar entorno virtual
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
pip install pysonar

# 4. Ejecutar análisis
pysonar \
  --sonar-host-url=http://localhost:9000 \
  --sonar-token=sqp_e422142e9e11a8fa9d3dbb500e2310af76b50068 \
  --sonar-project-key=prueba

# 5. Ver resultados en http://localhost:9000/projects

# 6. Desactivar entorno virtual
deactivate
```

## Notas Importantes

- **pysonar** es un wrapper simplificado de SonarScanner para Python
- Si encuentras problemas, considera usar **sonar-scanner** directamente
- El token que proporcionaste (`sqp_e422142e9e11a8fa9d3dbb500e2310af76b50068`) debe ser válido
- Asegúrate de que el project key `prueba` exista en SonarQube
- El análisis puede tomar 1-2 minutos dependiendo del tamaño del proyecto
