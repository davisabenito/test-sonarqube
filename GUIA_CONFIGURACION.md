# Guía de Configuración - SonarQube + GitHub Actions

## Paso 1: Iniciar SonarQube Local

### Opción A: Usar Docker Compose (Recomendado)

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube
docker-compose up -d
```

Espera unos minutos mientras SonarQube se inicia. Verifica con:
```bash
docker logs -f sonarqube
```

Cuando veas "SonarQube is up", presiona Ctrl+C.

### Opción B: Usar Docker directamente

```bash
docker run -d \
  --name sonarqube \
  -p 9000:9000 \
  -e SONAR_JDBC_URL=jdbc:postgresql://db:5432/sonar \
  -e SONAR_JDBC_USERNAME=sonar \
  -e SONAR_JDBC_PASSWORD=sonar \
  sonarqube:lts-community
```

## Paso 2: Configurar SonarQube

1. Abre http://localhost:9000 en tu navegador
2. Inicia sesión:
   - Usuario: `admin`
   - Contraseña: `admin`
3. Cambia la contraseña cuando se te pida (anótala)

## Paso 3: Crear el Proyecto en SonarQube

1. Clic en **"Create Project"** (botón grande arriba a la derecha)
2. **Project name**: `pruebas-sonarqube`
3. **Project key**: `pruebas-sonarqube` (se autocompleta)
4. **Main branch**: `main`
5. Clic en **"Set up"**
6. Selecciona **"Manually"** (para analizar localmente)
7. Clic en **"Continue"**
8. Clic en **"Locally"**
9. Clic en **"Generate"** para crear un token
10. **IMPORTANTE**: Copia el token generado (ej: `sqa_1234567890abcdef`)
    - Solo se muestra una vez
    - Guárdalo en un lugar seguro

## Paso 4: Probar el Análisis Local

### Instalar SonarScanner

```bash
# macOS
brew install sonar-scanner

# Verificar instalación
sonar-scanner --version
```

### Ejecutar el primer análisis

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

Reemplaza `TU_TOKEN_AQUI` con el token que copiaste en el Paso 3.

### Ver resultados

1. Ve a http://localhost:9000/projects
2. Busca el proyecto `pruebas-sonarqube`
3. Verás el dashboard con:
   - Quality Gate
   - Bugs, Code Smells, Vulnerabilities
   - Duplications
   - Coverage

## Paso 5: Configurar GitHub (Opcional - para GitHub Actions)

### 5.1 Crear repositorio en GitHub

```bash
cd /Users/davisbenito/Develop/BCP/web-dataops/pruebas-sonarqube

# Inicializar git
git init

# Agregar archivos
git add .

# Commit inicial
git commit -m "Initial commit with SonarQube test code"

# Crear repositorio en GitHub
gh repo create pruebas-sonarqube --public --source=.

# Push a GitHub
git push -u origin main
```

### 5.2 Configurar SonarQube para acceso externo

**IMPORTANTE**: GitHub Actions no puede acceder a `localhost:9000`. Tienes 3 opciones:

#### Opción 1: Usar ngrok (Más fácil para pruebas)

```bash
# Instalar ngrok
brew install ngrok

# Iniciar túnel para SonarQube
ngrok http 9000

# Copia la URL generada (ej: https://abc123.ngrok.io)
```

Luego, en SonarQube:
1. Ve a **Administration** → **Configuration** → **Server URL**
2. Cambia la URL base a la de ngrok (ej: `https://abc123.ngrok.io`)
3. Guarda los cambios

#### Opción 2: Usar SonarCloud (Recomendado para producción)

1. Ve a https://sonarcloud.io
2. Crea una cuenta gratuita
3. Conecta tu cuenta de GitHub
4. Crea el proyecto desde SonarCloud
5. SonarCloud se integrará automáticamente con GitHub Actions

#### Opción 3: Servidor SonarQube accesible públicamente

Si tienes un servidor en la nube o VPS, instala SonarQube allí y usa su URL pública.

### 5.3 Configurar Secrets en GitHub

1. Ve a tu repositorio en GitHub
2. Clic en **Settings** → **Secrets and variables** → **Actions**
3. Clic en **New repository secret**
4. Agrega:

**Secret 1: SONAR_HOST_URL**
- Name: `SONAR_HOST_URL`
- Value: `https://tu-url-ngrok.ngrok.io` (o tu URL pública de SonarQube)

**Secret 2: SONAR_TOKEN**
- Name: `SONAR_TOKEN`
- Value: El token que generaste en SonarQube (Paso 3)

### 5.4 Ejecutar GitHub Actions

1. Haz un push al repositorio:
```bash
git add .
git commit -m "Trigger SonarQube scan"
git push
```

2. Ve a la pestaña **Actions** en tu repositorio de GitHub
3. Verás el workflow "SonarQube Scan" ejecutándose
4. Espera a que termine (toma 1-2 minutos)

### 5.5 Ver resultados del análisis

1. Ve a SonarQube (http://localhost:9000 o tu URL pública)
2. Selecciona el proyecto `pruebas-sonarqube`
3. Verás los resultados del análisis desde GitHub Actions

## Paso 6: Configurar Quality Gate (Opcional)

El Quality Gate define si el código es aceptable. Por defecto, SonarQube tiene uno estándar.

### Ver el Quality Gate actual

1. En SonarQube, ve a **Quality Gates**
2. Verás el "Sonar way" (Quality Gate por defecto)

### Crear un Quality Gate personalizado (Opcional)

1. Clic en **Create Quality Gate**
2. Nombre: `Pruebas SonarQube`
3. Agrega condiciones:
   - Coverage on New Code: > 0% (más relajado)
   - Rating on New Code: A (bugs)
   - Rating on New Code: A (vulnerabilities)
   - Rating on New Code: D (code smells) - más relajado
4. Clic en **Save**
5. Asigna este Quality Gate a tu proyecto:
   - Ve a **Projects** → **pruebas-sonarqube**
   - Clic en **Project Settings** → **Quality Gate**
   - Selecciona `Pruebas SonarQube`
   - Clic en **Save**

## Paso 7: Ver Malas Prácticas Detectadas

En SonarQube, ve a:
- **Issues**: Ver todos los problemas detectados
- **Code Smells**: Malas prácticas de código
- **Bugs**: Errores potenciales
- **Vulnerabilities**: Problemas de seguridad

Filtra por:
- Severidad: Critical, Major, Minor
- Tipo: Code Smell, Bug, Vulnerability
- Estado: Open, Closed

Este proyecto debería mostrar múltiples issues de tipo Code Smell debido a las malas prácticas intencionales.

## Troubleshooting

### SonarQube no inicia

```bash
# Ver logs
docker logs sonarqube

# Reiniciar
docker-compose restart
```

### Error de conexión a PostgreSQL

Asegúrate de que el contenedor de la base de datos está corriendo:
```bash
docker ps
```

### SonarScanner no encuentra el token

Verifica que el token sea correcto y que SonarQube esté accesible:
```bash
curl http://localhost:9000/api/server/version
```

### GitHub Actions falla con "Connection refused"

- Verifica que `SONAR_HOST_URL` sea accesible públicamente
- Usa ngrok si SonarQube está en localhost
- Verifica que el token sea correcto

### El análisis no muestra resultados

- Verifica que el project key sea correcto
- Asegúrate de que el archivo `sonar-project.properties` esté configurado
- Revisa los logs del análisis

## Resumen

✅ **SonarQube Local**: http://localhost:9000
✅ **Proyecto Key**: `pruebas-sonarqube`
✅ **Token**: Guardado en un lugar seguro
✅ **SonarScanner**: Instalado y configurado
✅ **GitHub Actions**: Configurado con secrets (opcional)
✅ **Prueba**: Ejecutar análisis local y ver resultados

## Próximos pasos

1. Mejorar el código `data_cleaning.py` para resolver los issues
2. Re-ejecutar el análisis para ver mejoras
3. Configurar Quality Gate más estricto para producción
4. Integrar con CI/CD de tu proyecto real
