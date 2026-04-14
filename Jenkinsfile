// ─────────────────────────────────────────────────────────────────────────────
// Jenkinsfile
// Pipeline declarativo: Python + pytest + SonarQube local
//
// PROPÓSITO PEDAGÓGICO: Demuestra cómo Jenkins orquesta el pipeline completo:
//   Stage 1 → Checkout    : Clonar el código
//   Stage 2 → Instalar    : Instalar dependencias Python
//   Stage 3 → Pruebas     : Ejecutar pytest con cobertura
//   Stage 4 → SonarQube   : Enviar análisis al servidor local
//   Stage 5 → Quality Gate: Verificar si el código aprueba o falla
//   Stage 6 → Notificar   : Resumen del resultado
// ─────────────────────────────────────────────────────────────────────────────

pipeline {

    agent any

    // ── HERRAMIENTAS (configuradas en Jenkins → Global Tool Configuration) ──
    // No se requieren herramientas adicionales para Python (se usa pip directo)

    // ── VARIABLES DE ENTORNO ─────────────────────────────────────────────────
    environment {
        // Nombre del servidor SonarQube configurado en Jenkins
        // (Jenkins → Manage → Configure System → SonarQube servers)
        SONARQUBE_SERVER = 'SonarQube-Local'

        // Token de SonarQube guardado como credencial en Jenkins
        // (Jenkins → Manage → Credentials → sonar-token)
        SONAR_TOKEN = credentials('sonar-token')

        // Nombre del proyecto en SonarQube
        PROJECT_KEY = 'calidad-software-demo'

        // Directorio del entorno virtual Python
        VENV_DIR = '.venv'
    }

    // ── OPCIONES DEL PIPELINE ────────────────────────────────────────────────
    options {
        // Tiempo máximo de ejecución del pipeline completo
        timeout(time: 30, unit: 'MINUTES')
        // Conservar solo los últimos 10 builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        // No ejecutar builds concurrentes del mismo branch
        disableConcurrentBuilds()
        // Mostrar timestamps en los logs
        timestamps()
    }

    // ── STAGES ───────────────────────────────────────────────────────────────
    stages {

        // ── STAGE 1: CHECKOUT ─────────────────────────────────────────────────
        stage('📥 Checkout') {
            steps {
                echo '=== Clonando repositorio ==='
                checkout scm
                sh 'git log --oneline -5'  // Mostrar últimos 5 commits
            }
        }

        // ── STAGE 2: CONFIGURAR ENTORNO ───────────────────────────────────────
        stage('🐍 Configurar Python') {
            steps {
                echo '=== Configurando entorno virtual Python ==='
                sh '''
                    python3 --version
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements-dev.txt
                    pip list
                '''
            }
        }

        // ── STAGE 3: PRUEBAS Y COBERTURA ──────────────────────────────────────
        stage('🧪 Pruebas Unitarias') {
            steps {
                echo '=== Ejecutando suite de pruebas con pytest ==='
                sh '''
                    . ${VENV_DIR}/bin/activate
                    python -m pytest \
                        --cov=src \
                        --cov-report=xml:coverage.xml \
                        --cov-report=html:htmlcov \
                        --junitxml=test-results.xml \
                        -v \
                        --tb=short
                '''
            }
            post {
                always {
                    // Publicar resultados de pruebas en Jenkins
                    junit 'test-results.xml'
                    // Publicar reporte HTML de cobertura
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }

        // ── STAGE 4: ANÁLISIS SONARQUBE ────────────────────────────────────────
        stage('🔍 Análisis SonarQube') {
            steps {
                echo '=== Enviando análisis a SonarQube ==='
                // withSonarQubeEnv inyecta SONAR_HOST_URL y SONAR_AUTH_TOKEN
                withSonarQubeEnv("${SONARQUBE_SERVER}") {
                    sh '''
                        . ${VENV_DIR}/bin/activate
                        pip install sonar-scanner-cli 2>/dev/null || true

                        # Ejecutar sonar-scanner con parámetros explícitos
                        sonar-scanner \
                            -Dsonar.projectKey=${PROJECT_KEY} \
                            -Dsonar.projectName="Demo CI/CD - Calidad de Software" \
                            -Dsonar.projectVersion=1.0 \
                            -Dsonar.sources=src \
                            -Dsonar.tests=tests \
                            -Dsonar.python.version=3.11 \
                            -Dsonar.python.coverage.reportPaths=coverage.xml \
                            -Dsonar.sourceEncoding=UTF-8 \
                            -Dsonar.login=${SONAR_TOKEN}
                    '''
                }
            }
        }

        // ── STAGE 5: QUALITY GATE ──────────────────────────────────────────────
        stage('✅ Quality Gate') {
            steps {
                echo '=== Verificando Quality Gate de SonarQube ==='
                // Espera hasta 5 minutos que SonarQube termine el análisis
                // abortPipeline: true → el build FALLA si el QG falla
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        // ── STAGE 6: RESUMEN ───────────────────────────────────────────────────
        stage('📋 Resumen') {
            steps {
                echo '=== Pipeline completado exitosamente ==='
                sh '''
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo "  PIPELINE CI/CD - RESULTADO FINAL"
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                    echo "  Branch:    ${GIT_BRANCH}"
                    echo "  Commit:    ${GIT_COMMIT}"
                    echo "  SonarQube: http://localhost:9000"
                    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
                '''
            }
        }
    }

    // ── POST-ACTIONS (se ejecutan siempre, independiente del resultado) ──────
    post {
        success {
            echo '✅ Pipeline EXITOSO — Quality Gate aprobado'
        }
        failure {
            echo '❌ Pipeline FALLIDO — Revisar Quality Gate en SonarQube'
            echo 'Dashboard: http://localhost:9000/dashboard?id=calidad-software-demo'
        }
        always {
            echo '🧹 Limpiando workspace...'
            sh 'rm -rf ${VENV_DIR} || true'
            cleanWs()
        }
    }
}
