# Solución: Excluir venv del Análisis de SonarQube

## Problema
pysonar estaba analizando también el directorio `venv`, lo cual generaba muchos issues falsos de las librerías instaladas.

## Solución

### Opción 1: Ejecutar con exclusiones directamente (Recomendado)

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

### Opción 2: Usar el script actualizado

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
./run_analysis.sh
```

El script ya tiene las exclusiones configuradas.

### Opción 3: Usar sonar-scanner con exclusiones

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
source venv/bin/activate

sonar-scanner \
  -Dsonar.projectKey=prueba \
  -Dsonar.projectName=Prueba SonarQube \
  -Dsonar.projectVersion=1.0 \
  -Dsonar.sources=. \
  -Dsonar.sourceEncoding=UTF-8 \
  -Dsonar.exclusions=venv/**,**/*.csv,**/*.md,.git/**,.github/** \
  -Dsonar.python.version=3.9 \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=sqp_e422142e9e11a8fa9d3dbb500e2310af76b50068
```

## Exclusiones Configuradas

Los siguientes directorios y archivos están excluidos del análisis:

- ✅ `venv/**` - Entorno virtual completo
- ✅ `*.csv` - Archivos CSV (datos de prueba)
- ✅ `*.md` - Archivos Markdown (documentación)
- ✅ `.git/**` - Directorio de Git
- ✅ `.github/**` - Workflows de GitHub Actions

## Archivos Analizados

Solo se analizarán estos archivos de tu código:

- ✅ `data_cleaning.py` - Código con malas prácticas
- ✅ `test_cleaning.py` - Script de prueba

## Verificar que las exclusiones funcionaron

Después de ejecutar el análisis:

1. Ve a http://localhost:9000/projects
2. Selecciona el proyecto `prueba`
3. Clic en la pestaña **Code**
4. Verifica que solo aparezcan tus archivos Python, no los de venv

## Si sigues viendo archivos de venv

### Opción A: Borrar análisis anterior en SonarQube

1. Ve a http://localhost:9000/projects
2. Selecciona el proyecto `prueba`
3. Clic en **Project Settings** → **Deletion**
4. Clic en **Delete Project**
5. Crea el proyecto nuevamente con el mismo key `prueba`
6. Ejecuta el análisis nuevamente con las exclusiones

### Opción B: Usar un directorio src separado

Crea una estructura más limpia:

```bash
mkdir src
mv data_cleaning.py src/
mv test_cleaning.py src/
```

Luego especifica solo el directorio src:

```bash
pysonar \
  --sonar-host-url=http://localhost:9000 \
  --sonar-token=sqp_e422142e9e11a8fa9d3dbb500e2310af76b50068 \
  --sonar-project-key=prueba \
  --sonar-sources=src \
  --sonar-exclusions=*.csv,*.md
```

## Comando rápido para ejecutar ahora

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
source venv/bin/activate
pysonar --sonar-host-url=http://localhost:9000 --sonar-token=sqp_e422142e9e11a8fa9d3dbb500e2310af76b50068 --sonar-project-key=prueba --sonar-sources=. --sonar-exclusions=venv/**,*.csv,*.md,.git/**,.github/**
deactivate
```

O simplemente:

```bash
./run_analysis.sh
```
