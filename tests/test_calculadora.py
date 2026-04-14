"""
Suite de Pruebas Unitarias - Calculadora de Métricas
Cobertura intencional: ~65% (para demostrar Quality Gate fallido/ajustado)
Curso: Especialidad I - Calidad de Software
"""

import pytest
from src.calculadora import Calculadora, GestorHistorial, ProcesadorMetricas


# ─── FIXTURES ───────────────────────────────────────────────────────────────

@pytest.fixture
def calc():
    """Instancia de Calculadora para cada test."""
    return Calculadora()


@pytest.fixture
def historial():
    """Instancia de GestorHistorial para cada test."""
    return GestorHistorial()


@pytest.fixture
def procesador():
    """Instancia de ProcesadorMetricas para cada test."""
    return ProcesadorMetricas()


# ─── TESTS: CALCULADORA ─────────────────────────────────────────────────────

class TestCalculadora:
    """Pruebas unitarias para la clase Calculadora."""

    def test_sumar_positivos(self, calc):
        """Verifica suma de números positivos."""
        assert calc.sumar(3, 5) == 8

    def test_sumar_negativos(self, calc):
        """Verifica suma con números negativos."""
        assert calc.sumar(-2, -3) == -5

    def test_sumar_cero(self, calc):
        """Verifica suma con cero (identidad aditiva)."""
        assert calc.sumar(7, 0) == 7

    def test_restar_positivos(self, calc):
        """Verifica resta básica."""
        assert calc.restar(10, 4) == 6

    def test_restar_resultado_negativo(self, calc):
        """Verifica resta que produce resultado negativo."""
        assert calc.restar(2, 8) == -6

    def test_multiplicar_positivos(self, calc):
        """Verifica multiplicación básica."""
        assert calc.multiplicar(4, 5) == 20

    def test_multiplicar_por_cero(self, calc):
        """Verifica propiedad del cero en multiplicación."""
        assert calc.multiplicar(99, 0) == 0

    def test_multiplicar_negativos(self, calc):
        """Verifica multiplicación de negativos → positivo."""
        assert calc.multiplicar(-3, -4) == 12

    def test_dividir_normal(self, calc):
        """Verifica división básica."""
        assert calc.dividir(10, 2) == 5

    def test_dividir_resultado_decimal(self, calc):
        """Verifica división con resultado decimal."""
        assert calc.dividir(7, 2) == 3.5

    # ❌ TEST FALTANTE INTENCIONAL: No hay test para dividir(x, 0)
    # Esto es parte de la demostración pedagógica:
    # SonarQube mostrará que la rama de error no está cubierta.

    def test_potencia_cuadrado(self, calc):
        """Verifica potencia al cuadrado."""
        assert calc.potencia(3, 2) == 9

    def test_potencia_cubo(self, calc):
        """Verifica potencia al cubo."""
        assert calc.potencia(2, 3) == 8

    # ❌ TEST FALTANTE: raiz_cuadrada() → cobertura incompleta intencional


# ─── TESTS: GESTOR HISTORIAL ─────────────────────────────────────────────────

class TestGestorHistorial:
    """Pruebas unitarias para GestorHistorial."""

    def test_agregar_operacion(self, historial):
        """Verifica que se agrega correctamente una operación."""
        historial.agregar("sumar(3,5)", 8.0)
        assert len(historial.obtener_historial()) == 1

    def test_agregar_multiples_operaciones(self, historial):
        """Verifica múltiples adiciones al historial."""
        historial.agregar("sumar(1,1)", 2.0)
        historial.agregar("restar(5,3)", 2.0)
        historial.agregar("multiplicar(2,4)", 8.0)
        assert len(historial.obtener_historial()) == 3

    def test_limpiar_historial(self, historial):
        """Verifica que limpiar() vacía el historial."""
        historial.agregar("sumar(1,2)", 3.0)
        historial.limpiar()
        assert len(historial.obtener_historial()) == 0

    def test_promedio_resultados(self, historial):
        """Verifica cálculo de promedio del historial."""
        historial.agregar("op1", 10.0)
        historial.agregar("op2", 20.0)
        historial.agregar("op3", 30.0)
        assert historial.calcular_promedio_resultados() == 20.0

    def test_promedio_historial_vacio(self, historial):
        """Verifica que historial vacío retorna 0."""
        assert historial.calcular_promedio_resultados() == 0.0


# ─── TESTS: PROCESADOR DE MÉTRICAS ──────────────────────────────────────────

class TestProcesadorMetricas:
    """Pruebas unitarias para ProcesadorMetricas."""

    def test_clasificar_cobertura_excelente(self, procesador):
        """Verifica clasificación EXCELENTE (≥ 90%)."""
        assert procesador.clasificar_cobertura(95) == "EXCELENTE"

    def test_clasificar_cobertura_buena(self, procesador):
        """Verifica clasificación BUENO (80–89%)."""
        assert procesador.clasificar_cobertura(85) == "BUENO"

    def test_clasificar_cobertura_aceptable(self, procesador):
        """Verifica clasificación ACEPTABLE (60–79%)."""
        assert procesador.clasificar_cobertura(70) == "ACEPTABLE"

    def test_clasificar_cobertura_baja(self, procesador):
        """Verifica clasificación BAJO (40–59%)."""
        assert procesador.clasificar_cobertura(50) == "BAJO"

    def test_clasificar_cobertura_critica(self, procesador):
        """Verifica clasificación CRITICO (< 20%)."""
        assert procesador.clasificar_cobertura(10) == "CRITICO"

    def test_clasificar_cobertura_invalida(self, procesador):
        """Verifica clasificación INVALIDO (negativo)."""
        assert procesador.clasificar_cobertura(-5) == "INVALIDO"

    def test_deuda_tecnica_baja(self, procesador):
        """Verifica evaluación de deuda técnica baja (≤ 30 min)."""
        resultado = procesador.evaluar_deuda_tecnica(15)
        assert resultado["nivel"] == "BAJO"
        assert resultado["horas"] == 0

    def test_deuda_tecnica_media(self, procesador):
        """Verifica evaluación de deuda técnica media."""
        resultado = procesador.evaluar_deuda_tecnica(90)
        assert resultado["nivel"] == "MEDIO"
        assert resultado["horas"] == 1
        assert resultado["minutos"] == 30

    def test_deuda_tecnica_alta(self, procesador):
        """Verifica evaluación de deuda técnica alta (> 120 min)."""
        resultado = procesador.evaluar_deuda_tecnica(200)
        assert resultado["nivel"] == "ALTO"

    def test_generar_reporte_con_datos(self, procesador):
        """Verifica generación de reporte con historial."""
        historial = [
            {"operacion": "sumar", "resultado": 10.0},
            {"operacion": "restar", "resultado": 20.0},
        ]
        reporte = procesador.generar_reporte(historial)
        assert reporte["total_operaciones"] == 2
        assert reporte["promedio_resultados"] == 15.0

    def test_generar_reporte_vacio(self, procesador):
        """Verifica reporte con historial vacío."""
        reporte = procesador.generar_reporte([])
        assert reporte["total"] == 0
