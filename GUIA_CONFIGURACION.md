# Demo CI/CD + SonarQube — Guía de Configuración
## Especialidad I: Calidad de Software | Semana 4

---

## Descripción del Proyecto

Este repositorio es un **ejemplo pedagógico completo** para demostrar CI/CD con análisis de calidad estática usando SonarQube/SonarCloud.

### Estructura del Proyecto

```
cicd-demo/
├── src/
│   └── calculadora.py          ← Código fuente (con defectos intencionales)
├── tests/
│   └── test_calculadora.py     ← Suite de pruebas (cobertura ~65%)
├── .github/
│   └── workflows/
│       └── ci-sonarcloud.yml   ← Pipeline GitHub Actions + SonarCloud
├── jenkins/
│   └── init.groovy.d/          ← Scripts de configuración inicial Jenkins
├── docker-compose.yml          ← Stack Jenkins + SonarQube local
├── Jenkinsfile                 ← Pipeline declarativo para Jenkins
├── sonar-project.properties    ← Configuración del proyecto para SonarQube
├── pyproject.toml              ← Configuración de pytest y cobertura
└── requirements-dev.txt        ← Dependencias de desarrollo
```

### Defectos Intencionales para Demostración

| # | Tipo | Ubicación | SonarQube lo reporta como |
|---|------|-----------|---------------------------|
| 1 | Bug | `dividir()` sin validar divisor = 0 | Bug MAJOR |
| 2 | Bug | `raiz_cuadrada()` sin validar negativos | Bug MAJOR |
| 3 | Security Hotspot | Contraseña hardcodeada en `GestorHistorial` | Security Hotspot CRITICAL |
| 4 | Code Smell | Código duplicado entre `GestorHistorial` y `ProcesadorMetricas` | Code Smell MINOR |
| 5 | Code Smell | Complejidad ciclomática alta en `clasificar_cobertura()` | Code Smell MAJOR |

---

## OPCIÓN A: GitHub Actions + SonarCloud (Nube)

### Prerrequisitos
- Cuenta en [github.com](https://github.com) (gratuita)
- Cuenta en [sonarcloud.io](https://sonarcloud.io) vinculada a GitHub (gratuita para repos públicos)

### Paso 1: Crear el Repositorio en GitHub

```bash
# Clonar este demo y subir a tu cuenta
git init
git add .
git commit -m "feat: demo inicial CI/CD + SonarQube"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/cicd-demo.git
git push -u origin main
```

### Paso 2: Configurar SonarCloud

1. Entrar a [sonarcloud.io](https://sonarcloud.io) → **Log in with GitHub**
2. Clic en **"+"** → **"Analyze new project"**
3. Seleccionar tu repositorio `cicd-demo`
4. Elegir **"With GitHub Actions"** como método de análisis
5. SonarCloud te entregará:
   - Tu `SONAR_TOKEN`
   - El nombre de tu organización (`sonar.organization`)

### Paso 3: Configurar el Secreto en GitHub

```
GitHub Repo → Settings → Secrets and variables → Actions → New repository secret

Name:  SONAR_TOKEN
Value: (el token que entregó SonarCloud)
```

### Paso 4: Actualizar sonar-project.properties

```properties
# Descomentar y completar con tu organización de SonarCloud
sonar.organization=TU_ORGANIZACION_SONARCLOUD
sonar.projectKey=TU_USUARIO_cicd-demo
```

### Paso 5: Activar el Pipeline

```bash
# Hacer un commit cualquiera para disparar el workflow
git add sonar-project.properties
git commit -m "config: agregar organización SonarCloud"
git push
```

### Paso 6: Ver Resultados

- **GitHub Actions**: `github.com/TU_USUARIO/cicd-demo/actions`
- **SonarCloud Dashboard**: `sonarcloud.io/project/overview?id=TU_PROJECT_KEY`

---

## OPCIÓN B: Docker Compose Local (Jenkins + SonarQube)

### Prerrequisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado
- Al menos **6 GB de RAM** disponible para Docker
- Puertos **8080** y **9000** libres

### Paso 1: Ajuste del Kernel (Linux/Mac con Linux VM)

```bash
# Necesario para ElasticSearch (motor interno de SonarQube)
sudo sysctl -w vm.max_map_count=262144

# Para que persista entre reinicios:
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

> **Windows**: Docker Desktop aplica este ajuste automáticamente.

### Paso 2: Levantar el Stack

```bash
# Clonar / posicionarse en el directorio del proyecto
cd cicd-demo

# Levantar todos los servicios en segundo plano
docker compose up -d

# Ver progreso de inicialización (esperar ~2-3 minutos)
docker compose logs -f
```

### Paso 3: Configurar SonarQube

1. Abrir [http://localhost:9000](http://localhost:9000)
2. Login inicial: `admin` / `admin`
3. **Cambiar contraseña** (obligatorio al primer ingreso)
4. Ir a **My Account → Security → Generate Tokens**
5. Crear token: nombre `jenkins-token`, tipo `Global Analysis Token`
6. **Copiar el token** (solo se muestra una vez)

```
Crear proyecto manualmente:
  Projects → Create Project → Manually
  Project key:  calidad-software-demo
  Display name: Demo CI/CD - Calidad de Software
```

### Paso 4: Configurar Jenkins

1. Abrir [http://localhost:8080](http://localhost:8080)
2. Obtener contraseña inicial:
   ```bash
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. Instalar plugins sugeridos
4. Instalar plugin adicional:
   - **Manage Jenkins → Plugins → Available**
   - Buscar: `SonarQube Scanner` → Install

5. Configurar servidor SonarQube:
   - **Manage Jenkins → Configure System → SonarQube servers**
   - Name: `SonarQube-Local`
   - URL: `http://sonarqube:9000` ← usar nombre del contenedor, no localhost
   - Authentication token: agregar el token generado en el paso anterior

6. Instalar SonarScanner:
   - **Manage Jenkins → Global Tool Configuration → SonarQube Scanner**
   - Name: `SonarScanner`
   - ✅ Install automatically

### Paso 5: Crear Pipeline en Jenkins

```
New Item → Pipeline
  Name: cicd-demo-pipeline
  
Definition: Pipeline script from SCM
  SCM: Git
  Repository URL: (URL de tu repositorio o ruta local)
  Script Path: Jenkinsfile
```

### Paso 6: Ejecutar y Ver Resultados

```
Jenkins: http://localhost:8080/job/cicd-demo-pipeline/
Build Now → Ver Console Output en tiempo real

SonarQube: http://localhost:9000/dashboard?id=calidad-software-demo
```

---

## Ejecutar Pruebas Localmente (sin Docker)

```bash
# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# Instalar dependencias
pip install -r requirements-dev.txt

# Ejecutar pruebas con cobertura
python -m pytest -v

# Ver reporte HTML de cobertura
open htmlcov/index.html     # Mac
xdg-open htmlcov/index.html # Linux
```

---

## Guión para la Demostración en Clase

### Fase 1 — Estado Inicial (5 min)
```bash
# Mostrar el código con defectos
cat src/calculadora.py

# Ejecutar pruebas → ver que pasan pero con cobertura ~65%
python -m pytest -v
```

### Fase 2 — Activar Pipeline (3 min)
```bash
git add .
git commit -m "demo: pipeline inicial con defectos intencionales"
git push
```
→ Mostrar el pipeline ejecutándose en GitHub Actions / Jenkins

### Fase 3 — Ver Resultados en SonarQube (5 min)
- Mostrar el **Quality Gate** (debería pasar con threshold en 60%)
- Mostrar los **Bugs detectados** (dividir/0, raiz negativa)
- Mostrar el **Security Hotspot** (contraseña hardcodeada)
- Mostrar la **duplicación de código**

### Fase 4 — Subir el Umbral del Quality Gate (3 min)
```
SonarQube → Quality Gates → Create → Agregar condición:
  Coverage < 80% → FAILED
```
→ Reejecutar el pipeline → El Quality Gate ahora FALLA

### Fase 5 — Corregir y Volver a Pasar (5 min)
```python
# En calculadora.py, corregir el método dividir:
def dividir(self, a: float, b: float) -> float:
    if b == 0:
        raise ValueError("El divisor no puede ser cero")
    return a / b
```
```bash
git add src/calculadora.py
git commit -m "fix: validar divisor cero en método dividir"
git push
```
→ Mostrar que el bug desaparece en SonarQube tras el nuevo análisis

---

## Recursos Adicionales

- [Documentación SonarCloud](https://docs.sonarcloud.io/)
- [Documentación SonarQube](https://docs.sonarsource.com/sonarqube/)
- [GitHub Actions Marketplace](https://github.com/marketplace/actions/official-sonarqube-scan)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [pytest-cov documentación](https://pytest-cov.readthedocs.io/)
