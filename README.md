# Pruebas SonarQube

Proyecto de ejemplo para probar SonarQube con código Python que contiene malas prácticas intencionales para que SonarQube las detecte.

## Propósito

Este proyecto contiene código Python con múltiples malas prácticas diseñadas específicamente para que SonarQube las detecte:
- Variables globales
- Código duplicado
- Funciones demasiado largas
- Falta de documentación
- Uso de print en lugar de logging
- Excepciones genéricas
- Anidamiento excesivo
- Alta complejidad ciclomática
- Demasiados parámetros
- Variables no usadas
- Imports no utilizados
- Valores hardcodeados

## Configuración de SonarQube Local

### 1. Iniciar SonarQube con Docker

```bash
docker run -d \
  --name sonarqube \
  -p 9000:9000 \
  -e SONAR_JDBC_URL=jdbc:postgresql://db:5432/sonar \
  -e SONAR_JDBC_USERNAME=sonar \
  -e SONAR_JDBC_PASSWORD=sonar \
  sonarqube:lts-community
```

O usando docker-compose:

```yaml
version: "3"
services:
  sonarqube:
    image: sonarqube:lts-community
    container_name: sonarqube
    ports:
      - "9000:9000"
    environment:
      - SONAR_JDBC_URL=jdbc:postgresql://db:5432/sonar
      - SONAR_JDBC_USERNAME=sonar
      - SONAR_JDBC_PASSWORD=sonar
    volumes:
      - sonarqube_data:/opt/sonarqube/data
      - sonarqube_logs:/opt/sonarqube/logs
      - sonarqube_extensions:/opt/sonarqube/extensions

  db:
    image: postgres:13
    container_name: sonarqube_db
    environment:
      - POSTGRES_USER=sonar
      - POSTGRES_PASSWORD=sonar
      - POSTGRES_DB=sonar
    volumes:
      - postgresql_data:/var/lib/postgresql/data

volumes:
  sonarqube_data:
  sonarqube_logs:
  sonarqube_extensions:
  postgresql_data:
```

### 2. Acceder a SonarQube

1. Abre http://localhost:9000 en tu navegador
2. Inicia sesión con:
   - Usuario: `admin`
   - Contraseña: `admin`
3. Cambia la contraseña cuando se te solicite

### 3. Crear el proyecto en SonarQube

1. Clic en "Create Project"
2. Nombre del proyecto: `pruebas-sonarqube`
3. Key del proyecto: `pruebas-sonarqube`
4. Selecciona "Manually"
5. Anota el **token** que se genera (se mostrará una sola vez)

## Configuración de GitHub

### 1. Crear el repositorio en GitHub

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
git init
git add .
git commit -m "Initial commit with SonarQube test code"
gh repo create pruebas-sonarqube --public --source=.
git push -u origin main
```

### 2. Configurar Secrets en GitHub

Ve a tu repositorio en GitHub → Settings → Secrets and variables → Actions → New repository secret

Agrega los siguientes secrets:

| Nombre del Secret | Valor |
|-------------------|-------|
| `SONAR_HOST_URL` | `http://localhost:9000` (o tu URL de SonarQube) |
| `SONAR_TOKEN` | El token que generaste en SonarQube |

**Nota:** Si SonarQube está en tu máquina local, GitHub Actions no podrá acceder a `localhost:9000`. Necesitas:
- Usar SonarQube Cloud (sonarcloud.io), o
- Exponer SonarQube a través de un túnel (ngrok, localtunnel), o
- Usar un servidor SonarQube accesible públicamente

### 3. Exponer SonarQube localmente (opcional)

Si quieres usar SonarQube local con GitHub Actions, usa ngrok:

```bash
# Instala ngrok
brew install ngrok  # macOS
# o descarga desde https://ngrok.com/

# Inicia ngrok
ngrok http 9000

# Copia la URL generada (ej: https://abc123.ngrok.io)
# Usa esa URL como SONAR_HOST_URL en GitHub
```

## Ejecutar el análisis localmente

### Instalar SonarScanner

```bash
# macOS con Homebrew
brew install sonar-scanner

# Linux
wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-4.8.0.2856-linux.zip
unzip sonar-scanner-cli-*.zip
export PATH=$PATH:$(pwd)/sonar-scanner-*/bin
```

### Ejecutar el análisis

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
sonar-scanner \
  -Dsonar.projectKey=pruebas-sonarqube \
  -Dsonar.projectName=Pruebas SonarQube \
  -Dsonar.projectVersion=1.0 \
  -Dsonar.sources=. \
  -Dsonar.sourceEncoding=UTF-8 \
  -Dsonar.exclusions=**/*.csv,**/*.md \
  -Dsonar.python.version=3.9 \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=TU_TOKEN_AQUI
```

## Ejecutar el análisis con GitHub Actions

1. Push de cambios al repositorio:
```bash
git add .
git commit -m "Trigger SonarQube scan"
git push
```

2. Ve a la pestaña "Actions" en tu repositorio de GitHub
3. Verás el workflow "SonarQube Scan" ejecutándose
4. Una vez completado, ve a SonarQube para ver los resultados

## Ver resultados en SonarQube

1. Accede a http://localhost:9000/projects
2. Selecciona el proyecto `pruebas-sonarqube`
3. Verás:
   - **Quality Gate**: Pasó/Falló
   - **Bugs**: Problemas de código
   - **Code Smells**: Malas prácticas
   - **Vulnerabilities**: Problemas de seguridad
   - **Coverage**: Cobertura de código (si se configura)
   - **Duplications**: Código duplicado

## Malas prácticas detectadas

Este código debería generar los siguientes issues en SonarQube:

| Issue | Tipo | Severidad |
|-------|------|-----------|
| Variables globales | Code Smell | Major |
| Código duplicado | Code Smell | Major |
| Función demasiado larga (>50 líneas) | Code Smell | Major |
| Falta de documentación | Code Smell | Minor |
| Uso de print en lugar de logging | Code Smell | Minor |
| Excepción genérica (Exception) | Code Smell | Critical |
| Anidamiento excesivo (>3 niveles) | Code Smell | Major |
| Alta complejidad ciclomática (>15) | Code Smell | Critical |
| Demasiados parámetros (>7) | Code Smell | Major |
| Variable no usada | Code Smell | Minor |
| Import no utilizado | Code Smell | Minor |
| Valores hardcodeados | Code Smell | Minor |

## Solución del Quality Gate

Por defecto, SonarQube tiene un Quality Gate que puede fallar si:
- La cobertura de código es < 80%
- Hay nuevos bugs
- Hay nuevas vulnerabilidades
- Hay nuevas code smells

Para que este proyecto pase el Quality Gate inicialmente, puedes:
1. Crear un Quality Gate personalizado más relajado
2. O simplemente observar los issues sin bloquear el pipeline

## Script de prueba local

```bash
# Ejecutar el script Python
python data_cleaning.py
```

## Estructura del proyecto

```
pruebas-sonarqube/
├── .github/
│   └── workflows/
│       └── sonarqube-scan.yml    # Workflow de GitHub Actions
├── data_cleaning.py               # Código con malas prácticas
├── datos.csv                      # Datos de prueba
├── sonar-project.properties      # Configuración de SonarQube
├── sonar-scanner.properties       # Configuración del scanner
├── requirements.txt               # Dependencias Python
└── README.md                      # Este archivo
```

## Recursos

- [Documentación de SonarQube](https://docs.sonarqube.org/)
- [SonarScanner CLI](https://docs.sonarqube.org/latest/analyzing-source-code/sonarscanner/)
- [GitHub Actions para SonarQube](https://github.com/marketplace/actions/sonarqube-scan)
- [Python Quality Profile](https://docs.sonarqube.org/latest/analyzing-source-code/languages/python/)
