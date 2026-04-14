"""
Módulo: Calculadora de Métricas de Calidad de Software
Propósito: Ejemplo pedagógico con defectos intencionales para SonarQube
Curso: Especialidad I - Calidad de Software
"""

import math


# ─── CLASE PRINCIPAL ────────────────────────────────────────────────────────

class Calculadora:
    """
    Calculadora básica para demostración de CI/CD + SonarQube.
    NOTA PEDAGÓGICA: Este archivo contiene defectos intencionales
    que SonarQube detectará durante el análisis estático.
    """

    def sumar(self, a: float, b: float) -> float:
        """Retorna la suma de dos números."""
        return a + b

    def restar(self, a: float, b: float) -> float:
        """Retorna la diferencia entre dos números."""
        return a - b

    def multiplicar(self, a: float, b: float) -> float:
        """Retorna el producto de dos números."""
        return a * b

    def dividir(self, a: float, b: float) -> float:
        """
        Retorna el cociente de dos números.
        DEFECTO INTENCIONAL #1 (Bug): No valida divisor igual a cero.
        SonarQube lo reportará como Bug de severidad MAJOR.
        """
        # ❌ BUG: Falta validar b == 0 → lanzará ZeroDivisionError en runtime
        return a / b

    def raiz_cuadrada(self, numero: float) -> float:
        """
        Calcula la raíz cuadrada de un número.
        DEFECTO INTENCIONAL #2 (Bug): No valida números negativos.
        """
        # ❌ BUG: math.sqrt(-1) lanza ValueError en runtime
        return math.sqrt(numero)

    def potencia(self, base: float, exponente: float) -> float:
        """Retorna base elevada al exponente."""
        return base ** exponente


# ─── GESTOR DE HISTORIAL ────────────────────────────────────────────────────

class GestorHistorial:
    """
    Mantiene un registro de operaciones realizadas.
    DEFECTO INTENCIONAL #3 (Code Smell): Contraseña hardcodeada.
    SonarQube lo reportará como Security Hotspot crítico.
    """

    # ❌ SECURITY HOTSPOT: Credencial en texto plano en el código fuente
    DB_PASSWORD = "admin123"  # noqa

    def __init__(self):
        self.historial = []
        self.max_registros = 100

    def agregar(self, operacion: str, resultado: float) -> None:
        """Agrega una operación al historial."""
        entrada = {
            "operacion": operacion,
            "resultado": resultado
        }
        self.historial.append(entrada)

    def obtener_historial(self) -> list:
        """Retorna todo el historial de operaciones."""
        return self.historial

    def limpiar(self) -> None:
        """Limpia el historial completo."""
        self.historial = []

    def calcular_promedio_resultados(self) -> float:
        """
        Calcula el promedio de todos los resultados del historial.
        DEFECTO INTENCIONAL #4 (Code Smell): Código duplicado.
        Esta lógica también aparece en reporte.py (duplicación > 3%).
        """
        if not self.historial:
            return 0.0
        total = sum(entrada["resultado"] for entrada in self.historial)
        promedio = total / len(self.historial)
        return promedio


# ─── PROCESADOR DE MÉTRICAS ─────────────────────────────────────────────────

class ProcesadorMetricas:
    """
    Procesa y clasifica métricas de calidad.
    DEFECTO INTENCIONAL #5 (Code Smell): Complejidad ciclomática alta.
    SonarQube lo reportará cuando la función tenga > 10 caminos.
    """

    def clasificar_cobertura(self, porcentaje: float) -> str:
        """
        Clasifica el nivel de cobertura de pruebas.
        ❌ CODE SMELL: Complejidad ciclomática = 7 (debería refactorizarse).
        """
        if porcentaje < 0:
            return "INVALIDO"
        elif porcentaje < 20:
            return "CRITICO"
        elif porcentaje < 40:
            return "MUY_BAJO"
        elif porcentaje < 60:
            return "BAJO"
        elif porcentaje < 80:
            return "ACEPTABLE"
        elif porcentaje < 90:
            return "BUENO"
        else:
            return "EXCELENTE"

    def evaluar_deuda_tecnica(self, minutos: int) -> dict:
        """Evalúa la deuda técnica y retorna un resumen."""
        horas = minutos // 60
        mins_restantes = minutos % 60

        if minutos <= 30:
            nivel = "BAJO"
            accion = "Monitorear en próxima iteración"
        elif minutos <= 120:
            nivel = "MEDIO"
            accion = "Planificar refactoring en sprint actual"
        else:
            nivel = "ALTO"
            accion = "Refactoring urgente requerido"

        return {
            "minutos_totales": minutos,
            "horas": horas,
            "minutos": mins_restantes,
            "nivel": nivel,
            "accion_recomendada": accion
        }

    def generar_reporte(self, historial: list) -> dict:
        """
        Genera un reporte de métricas.
        DEFECTO INTENCIONAL #4b (duplicación): misma lógica que en GestorHistorial.
        """
        if not historial:
            return {"total": 0, "promedio": 0.0}

        # ❌ DUPLICACIÓN: misma lógica de promedio que en GestorHistorial
        total = sum(entrada["resultado"] for entrada in historial)
        promedio = total / len(historial)

        return {
            "total_operaciones": len(historial),
            "promedio_resultados": promedio,
            "ultimo_resultado": historial[-1]["resultado"]
        }
