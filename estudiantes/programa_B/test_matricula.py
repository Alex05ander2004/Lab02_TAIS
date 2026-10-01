"""
Plantilla de pruebas - Programa B (motor de matricula y promedios).

Ejecute con:

    python3 -m pytest test_matricula.py -q

Recuerde: la ESPECIFICACION es el oraculo. No modifique matricula.py.
"""

from decimal import Decimal

import pytest

import matricula as mat


@pytest.fixture
def catalogo():
    """Catalogo de referencia de la seccion 3 de la especificacion."""
    cursos = [
        mat.Curso("IS101", "Algoritmica", 4, []),
        mat.Curso("IS201", "Estructuras de Datos", 4, ["IS101"]),
        mat.Curso("IS301", "Base de Datos", 3, ["IS201"]),
        mat.Curso("IS401", "Ingenieria de Software", 4, []),
        mat.Curso("IS402", "Pruebas de Software", 3, ["IS401"]),
        mat.Curso("IS403", "Redes", 3, []),
        mat.Curso("IS404", "Sistemas Operativos", 4, []),
        mat.Curso("IS405", "Compiladores", 4, []),
        mat.Curso("IS406", "Inteligencia Artificial", 3, []),
        mat.Curso("IS407", "Seminario de Tesis", 1, []),
    ]
    return {c.codigo: c for c in cursos}


def test_ejemplo_de_la_especificacion(catalogo):
    """Caso 5 de la tabla de ejemplos: (20*4 + 10*3) / 7 = 15.71."""
    promedio = mat.calcular_promedio_ponderado({"IS101": 20, "IS403": 10}, catalogo)
    assert promedio == Decimal("15.71")


# --- Escriba sus pruebas a partir de aqui ---------------------------------
# Cada prueba lleva el numero de caso (CP) de la Tabla 3 de la Hoja de Trabajo.
# Todos los resultados esperados se dedujeron de especificacion_B.md.

# Matricula base de 12 creditos sin prerrequisitos: IS101(4) + IS401(4) + IS404(4)
BASE_12 = ["IS101", "IS401", "IS404"]
# Caso 9 de la especificacion: 22 creditos
CASO_9 = ["IS101", "IS401", "IS404", "IS405", "IS403", "IS406"]


def reg(codigo, nota, intentos=1):
    return mat.RegistroHistorial(codigo, nota, intentos)


# ===================== R1 - Nota final de un curso ======================

def test_cp01_r1_nota_10_5_redondea_a_11():
    assert mat.calcular_nota_final([(10.5, 1)]) == 11


def test_cp02_r1_nota_12_5_redondea_a_13():
    assert mat.calcular_nota_final([(12.5, 1)]) == 13


def test_cp03_r1_nota_10_51_redondea_a_11():
    assert mat.calcular_nota_final([(10.51, 1)]) == 11


def test_cp04_r1_nota_10_49_redondea_a_10():
    assert mat.calcular_nota_final([(10.49, 1)]) == 10


def test_cp05_r1_ejemplo_ponderado_12_y_16_da_14():
    assert mat.calcular_nota_final([(12, 0.4), (16, 0.6)]) == 14


def test_cp06_r1_lista_vacia_lanza_sin_creditos():
    with pytest.raises(mat.SinCreditosError):
        mat.calcular_nota_final([])


def test_cp07_r1_suma_de_pesos_cero_lanza_sin_creditos():
    with pytest.raises(mat.SinCreditosError):
        mat.calcular_nota_final([(15, 0)])


def test_cp08_r1_evaluacion_con_nota_21_lanza_fuera_de_rango():
    with pytest.raises(mat.NotaFueraDeRangoError):
        mat.calcular_nota_final([(21, 1)])


# ===================== R2 - Aprobacion de un curso ======================

def test_cp09_r2_nota_10_no_aprueba():
    assert mat.esta_aprobado(10) is False


def test_cp10_r2_nota_11_aprueba():
    assert mat.esta_aprobado(11) is True


def test_cp11_r2_nota_12_aprueba():
    assert mat.esta_aprobado(12) is True


# ===================== R3 - Promedio ponderado ==========================

def test_cp12_r3_pondera_por_creditos_no_por_cursos(catalogo):
    # (20*4 + 10*1) / 5 = 18.00
    promedio = mat.calcular_promedio_ponderado({"IS401": 20, "IS407": 10}, catalogo)
    assert promedio == Decimal("18.00")


def test_cp13_r3_redondeo_dos_decimales_medio_hacia_arriba(catalogo):
    # (11*4 + 11*3 + 12*1) / 8 = 89/8 = 11.125 -> 11.13
    promedio = mat.calcular_promedio_ponderado(
        {"IS101": 11, "IS403": 11, "IS407": 12}, catalogo)
    assert promedio == Decimal("11.13")


def test_cp14_r3_sin_creditos_lanza_sin_creditos(catalogo):
    with pytest.raises(mat.SinCreditosError):
        mat.calcular_promedio_ponderado({}, catalogo)


# ===================== R4 - Estado academico ============================

def test_cp15_r4_tres_desaprobados_es_desaprobado():
    assert mat.determinar_estado(Decimal("15.00"), 3) == "DESAPROBADO"
    assert mat.determinar_estado(Decimal("15.00"), 4) == "DESAPROBADO"


def test_cp16_r4_dos_desaprobados_promedio_alto_es_observado():
    assert mat.determinar_estado(Decimal("15.00"), 2) == "OBSERVADO"


def test_cp17_r4_promedio_9_99_es_desaprobado():
    assert mat.determinar_estado(Decimal("9.99"), 0) == "DESAPROBADO"


def test_cp18_r4_promedio_10_00_es_observado():
    assert mat.determinar_estado(Decimal("10.00"), 0) == "OBSERVADO"


def test_cp19_r4_promedio_10_01_y_10_99_es_observado():
    assert mat.determinar_estado(Decimal("10.01"), 0) == "OBSERVADO"
    assert mat.determinar_estado(Decimal("10.99"), 0) == "OBSERVADO"


def test_cp20_r4_promedio_11_00_sin_desaprobados_es_aprobado():
    assert mat.determinar_estado(Decimal("11.00"), 0) == "APROBADO"


def test_cp21_r4_promedio_11_01_sin_desaprobados_es_aprobado():
    assert mat.determinar_estado(Decimal("11.01"), 0) == "APROBADO"


def test_cp22_r4_promedio_11_00_con_un_desaprobado_es_observado():
    assert mat.determinar_estado(Decimal("11.00"), 1) == "OBSERVADO"


def test_cp23_r4_ejemplo6_promedio_11_es_aprobado(catalogo):
    r = mat.evaluar_semestre({"IS401": 11, "IS403": 11}, catalogo)
    assert r.promedio_ponderado == Decimal("11.00")
    assert r.estado == "APROBADO"


def test_cp24_r4_ejemplo7_un_desaprobado_es_observado(catalogo):
    r = mat.evaluar_semestre({"IS101": 20, "IS401": 20, "IS403": 5}, catalogo)
    assert r.cursos_desaprobados == 1
    assert r.estado == "OBSERVADO"


def test_cp25_r4_ejemplo8_promedio_10_43_es_observado(catalogo):
    r = mat.evaluar_semestre({"IS401": 10, "IS403": 11}, catalogo)
    assert r.promedio_ponderado == Decimal("10.43")
    assert r.estado == "OBSERVADO"


def test_cp26_r4_cuenta_cursos_desaprobados_no_creditos(catalogo):
    r = mat.evaluar_semestre({"IS101": 5, "IS401": 15}, catalogo)
    assert r.cursos_desaprobados == 1
    assert r.cursos_aprobados == 1


# ===================== R5 - Prerrequisitos ==============================

def test_cp27_r5_prerrequisito_aprobado_con_12_permite(catalogo):
    mat.verificar_prerrequisitos(catalogo["IS201"], {"IS101": reg("IS101", 12)})


def test_cp28_r5_prerrequisito_aprobado_con_11_permite(catalogo):
    mat.verificar_prerrequisitos(catalogo["IS201"], {"IS101": reg("IS101", 11)})


def test_cp29_r5_prerrequisito_con_10_lanza_error(catalogo):
    with pytest.raises(mat.PrerrequisitoNoCumplidoError):
        mat.verificar_prerrequisitos(catalogo["IS201"], {"IS101": reg("IS101", 10)})


def test_cp30_r5_prerrequisito_ausente_lanza_error(catalogo):
    with pytest.raises(mat.PrerrequisitoNoCumplidoError):
        mat.verificar_prerrequisitos(catalogo["IS201"], {})


# ===================== R6 - Carga de creditos ===========================

def test_cp31_r6_carga_11_creditos_lanza_error(catalogo):
    with pytest.raises(mat.CreditosInvalidosError):
        mat.validar_matricula(["IS101", "IS401", "IS403"], catalogo, [], 12.0)


def test_cp32_r6_carga_12_creditos_es_valida(catalogo):
    assert mat.validar_matricula(BASE_12, catalogo, [], 12.0) == 12


def test_cp33_r6_carga_13_creditos_es_valida(catalogo):
    assert mat.validar_matricula(BASE_12 + ["IS407"], catalogo, [], 12.0) == 13


def test_cp34_r6_ejemplo9_carga_22_es_valida(catalogo):
    assert mat.validar_matricula(CASO_9, catalogo, [], 12.0) == 22


def test_cp35_r6_ejemplo10_carga_23_con_12_lanza_error(catalogo):
    with pytest.raises(mat.CreditosInvalidosError):
        mat.validar_matricula(CASO_9 + ["IS407"], catalogo, [], 12.0)


def test_cp36_r6_ejemplo11_carga_23_con_15_es_valida(catalogo):
    assert mat.validar_matricula(CASO_9 + ["IS407"], catalogo, [], 15.0) == 23


def test_cp37_r6_carga_23_con_promedio_14_99_lanza_error(catalogo):
    with pytest.raises(mat.CreditosInvalidosError):
        mat.validar_matricula(CASO_9 + ["IS407"], catalogo, [], 14.99)


def test_cp38_r6_ejemplo12_carga_6_lanza_error(catalogo):
    with pytest.raises(mat.CreditosInvalidosError):
        mat.validar_matricula(["IS403", "IS406"], catalogo, [], 12.0)


def test_cp39_r6_limite_ampliado_desde_15_00():
    assert mat.limite_creditos(Decimal("14.99")) == 22
    assert mat.limite_creditos(Decimal("15.00")) == 26
    assert mat.limite_creditos(Decimal("15.01")) == 26


def test_cp40_r6_carga_25_y_26_con_promedio_15_es_valida():
    mat.validar_carga(25, Decimal("15.00"))
    mat.validar_carga(26, Decimal("15.00"))


def test_cp41_r6_carga_27_con_promedio_15_lanza_error():
    with pytest.raises(mat.CreditosInvalidosError):
        mat.validar_carga(27, Decimal("15.00"))


def test_cp42_r6_carga_11_en_validar_carga_lanza_error():
    with pytest.raises(mat.CreditosInvalidosError):
        mat.validar_carga(11, Decimal("12.00"))


# ===================== R7 - Tope de cursos ==============================

def test_cp43_r7_siete_cursos_es_valido(catalogo):
    siete = CASO_9 + ["IS407"]
    assert mat.validar_matricula(siete, catalogo, [], 15.0) == 23


def test_cp44_r7_ocho_cursos_lanza_matricula_error(catalogo):
    ocho = CASO_9 + ["IS407", "IS402"]
    with pytest.raises(mat.MatriculaError):
        mat.validar_matricula(ocho, catalogo, [], 15.0)


# ===================== R8 - Curso ya aprobado ===========================

def test_cp45_r8_curso_aprobado_con_12_lanza_error(catalogo):
    with pytest.raises(mat.CursoYaAprobadoError):
        mat.validar_matricula(BASE_12, catalogo, [reg("IS101", 12)], 12.0)


def test_cp46_r8_curso_aprobado_con_11_lanza_error(catalogo):
    with pytest.raises(mat.CursoYaAprobadoError):
        mat.validar_matricula(BASE_12, catalogo, [reg("IS101", 11)], 12.0)


def test_cp47_r8_curso_desaprobado_con_10_se_puede_matricular(catalogo):
    assert mat.validar_matricula(BASE_12, catalogo, [reg("IS101", 10)], 12.0) == 12


# ===================== R9 - Reprobacion reiterada =======================

def test_cp48_r9_dos_intentos_no_requiere_autorizacion(catalogo):
    historial = [reg("IS101", 8, intentos=2)]
    assert mat.validar_matricula(BASE_12, catalogo, historial, 12.0) == 12


def test_cp49_r9_tres_o_cuatro_intentos_sin_autorizacion_lanza_error(catalogo):
    for intentos in (3, 4):
        historial = [reg("IS101", 8, intentos=intentos)]
        with pytest.raises(mat.AutorizacionRequeridaError):
            mat.validar_matricula(BASE_12, catalogo, historial, 12.0)


def test_cp50_r9_tres_intentos_con_autorizacion_es_valido(catalogo):
    historial = [reg("IS101", 8, intentos=3)]
    assert mat.validar_matricula(
        BASE_12, catalogo, historial, 12.0, autorizaciones=("IS101",)) == 12


# ===================== R10 - Validaciones de entrada ====================

def test_cp51_r10_nota_menos_1_lanza_fuera_de_rango():
    with pytest.raises(mat.NotaFueraDeRangoError):
        mat.validar_nota(-1)


def test_cp52_r10_nota_0_y_1_son_validas():
    assert mat.validar_nota(0) == Decimal("0")
    assert mat.validar_nota(1) == Decimal("1")


def test_cp53_r10_nota_19_y_20_son_validas():
    assert mat.validar_nota(19) == Decimal("19")
    assert mat.validar_nota(20) == Decimal("20")


def test_cp54_r10_nota_21_lanza_fuera_de_rango():
    with pytest.raises(mat.NotaFueraDeRangoError):
        mat.validar_nota(21)


def test_cp55_r10_ejemplo13_nota_25_lanza_fuera_de_rango():
    with pytest.raises(mat.NotaFueraDeRangoError):
        mat.validar_nota(25)


def test_cp56_r10_promedio_con_nota_21_lanza_fuera_de_rango(catalogo):
    with pytest.raises(mat.NotaFueraDeRangoError):
        mat.calcular_promedio_ponderado({"IS101": 21}, catalogo)


def test_cp57_r10_obtener_curso_inexistente_lanza_error(catalogo):
    with pytest.raises(mat.CursoInexistenteError):
        mat.obtener_curso(catalogo, "XX999")


def test_cp58_r10_matricula_con_curso_inexistente_lanza_error(catalogo):
    with pytest.raises(mat.CursoInexistenteError):
        mat.validar_matricula(BASE_12 + ["XX999"], catalogo, [], 12.0)


def test_cp59_r10_promedio_con_curso_inexistente_lanza_error(catalogo):
    with pytest.raises(mat.CursoInexistenteError):
        mat.calcular_promedio_ponderado({"XX999": 15}, catalogo)


def test_cp60_r10_excepciones_son_subclases_de_matricula_error():
    for exc in (mat.CursoInexistenteError, mat.NotaFueraDeRangoError,
                mat.PrerrequisitoNoCumplidoError, mat.CreditosInvalidosError,
                mat.CursoYaAprobadoError, mat.AutorizacionRequeridaError,
                mat.SinCreditosError):
        assert issubclass(exc, mat.MatriculaError)


# ===================== Orden de verificacion ============================

def test_cp61_orden_tope_de_cursos_antes_que_existencia(catalogo):
    ocho = CASO_9 + ["IS407", "XX999"]
    with pytest.raises(mat.MatriculaError) as exc:
        mat.validar_matricula(ocho, catalogo, [], 15.0)
    assert type(exc.value) is mat.MatriculaError


def test_cp62_orden_ya_aprobado_antes_que_autorizacion(catalogo):
    historial = [reg("IS101", 15, intentos=3)]
    with pytest.raises(mat.CursoYaAprobadoError):
        mat.validar_matricula(BASE_12, catalogo, historial, 12.0)


def test_cp63_orden_prerrequisito_antes_que_carga(catalogo):
    # IS201 sin IS101 aprobado y carga de 4 creditos: debe fallar por R5, no por R6
    with pytest.raises(mat.PrerrequisitoNoCumplidoError):
        mat.validar_matricula(["IS201"], catalogo, [], 12.0)


def test_cp64_r6_carga_21_con_promedio_12_es_valida():
    mat.validar_carga(21, Decimal("12.00"))
