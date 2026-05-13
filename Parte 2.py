"""


IVAN DAVID AGUDELO DEL RIO
Docente : María Camila Espinosa Cuartas
Fecha   : Abril 29 de 2026

LA TRANSITIVIDAD PUEDE EN SER CIERTOS CASOS VACUA PORQUE NO HAY ELEMENTOS QUE CONTRADIGAN LA PROPIEDAD,
TENER EN CUENTA ESTO, Y CONTINUE EJECUTANDO EL CODIGO
"""

LINEA  = "─" * 65
DOBLE  = "═" * 65
TITULO = "  ANÁLISIS DE RELACIONES Y FUNCIONES   "


#  ENTRADA Y VALIDACIÓN DE CONJUNTOS

def ingresar_conjunto(nombre_conjunto: str) -> list:
    print(f"\n  Ingrese los elementos del conjunto {nombre_conjunto}.")
    print("  Sepárelos por comas.  Ejemplo:  1, 2, 3  ó  a, b, c")

    while True:
        entrada = input(f"  Conjunto {nombre_conjunto} = {{ ").strip()

        if not entrada:
            print("  ✗ El conjunto no puede estar vacío. Intente de nuevo.\n")
            continue

        elementos = [e.strip() for e in entrada.split(",") if e.strip()]

        if len(elementos) == 0:
            print("  ✗ No se detectaron elementos válidos. Intente de nuevo.\n")
            continue

        if len(elementos) > 10:
            print(f"  ✗ Se ingresaron {len(elementos)} elementos. "
                  "El máximo permitido es 10. Intente de nuevo.\n")
            continue

        if len(elementos) != len(set(elementos)):
            duplicados = sorted({e for e in elementos if elementos.count(e) > 1})
            print(f"  ✗ Elementos duplicados detectados: {duplicados}. "
                  "Cada elemento debe ser único. Intente de nuevo.\n")
            continue

        print(f"  ✓ Conjunto {nombre_conjunto} = {{ {', '.join(elementos)} }}"
              f"  ({len(elementos)} elemento(s))")
        return elementos


# CONSTRUCCIÓN DE LA RELACIÓN (PARES ORDENADOS)

def ingresar_relacion(conjunto_a: list, conjunto_b: list) -> list:
    set_a = set(conjunto_a)
    set_b = set(conjunto_b)

    while True:
        print(f"\n  Ingrese los pares ordenados de la relación.")
        print("  Formato: x,y    — escriba uno por línea.")
        print("  Cuando termine, deje la línea vacía y presione ENTER.")
        print(f"  Dominio válido    : {conjunto_a}")
        print(f"  Codominio válido  : {conjunto_b}")
        print("  (Una relación vacía R = ∅ es matemáticamente válida.)\n")

        relacion     = []
        set_relacion = set()

        while True:
            entrada = input("  Par ordenado (x,y): ").strip()

            if entrada == "":
                break

            partes = [p.strip() for p in entrada.split(",")]
            if len(partes) != 2:
                print("  ✗ Formato incorrecto. Use exactamente: x,y\n")
                continue

            x, y = partes[0], partes[1]

            if x not in set_a:
                print(f"  ✗ '{x}' no pertenece al dominio {conjunto_a}.\n")
                continue
            if y not in set_b:
                print(f"  ✗ '{y}' no pertenece al codominio {conjunto_b}.\n")
                continue

            par = (x, y)
            if par in set_relacion:
                print(f"  ✗ El par {par} ya fue ingresado. Se omite.\n")
                continue

            relacion.append(par)
            set_relacion.add(par)
            print(f"  ✓ Par {par} agregado.")

        print(f"\n  Relación ingresada: R = {_formatear_relacion(relacion)}")
        print(f"  Total de pares   : {len(relacion)}")

        while True:
            resp = input("\n  ¿Confirma esta relación? (s = sí / n = reingresar): ").strip().lower()
            if resp in ("s", "si", "sí", "y", "yes"):
                return relacion
            elif resp in ("n", "no"):
                print("\n  ── Reingresando la relación desde cero ──")
                break
            else:
                print("  ✗ Respuesta no reconocida. Escriba 's' o 'n'.")


# DIAGNÓSTICO DE PROPIEDADES

def es_reflexiva(relacion: list, conjunto_a: list) -> tuple:
    set_r = set(relacion)
    pares_faltantes = [(a, a) for a in conjunto_a if (a, a) not in set_r]
    return (len(pares_faltantes) == 0), pares_faltantes


def es_simetrica(relacion: list) -> tuple:
    set_r = set(relacion)
    pares_faltantes = [(y, x) for (x, y) in relacion if (y, x) not in set_r]
    return (len(pares_faltantes) == 0), pares_faltantes


def _calcular_cierre_transitivo(relacion: list) -> list:
    relacion_ampliada = list(relacion)
    set_ampliada      = set(relacion)
    hubo_cambio       = True

    while hubo_cambio:
        hubo_cambio = False
        snapshot    = list(relacion_ampliada)

        for (a, b) in snapshot:
            for (c, d) in snapshot:
                if b == c:
                    par_nuevo = (a, d)
                    if par_nuevo not in set_ampliada:
                        relacion_ampliada.append(par_nuevo)
                        set_ampliada.add(par_nuevo)
                        hubo_cambio = True

    set_original = set(relacion)
    return [p for p in relacion_ampliada if p not in set_original]


def es_transitiva(relacion: list) -> tuple:
    pares_nuevos = _calcular_cierre_transitivo(relacion)
    return (len(pares_nuevos) == 0), pares_nuevos


# EVALUACIÓN DE FUNCIONES


def evaluar_funcion(relacion: list, conjunto_a: list, conjunto_b: list) -> dict:
    resultado = {
        "es_funcion"               : False,
        "razon_no_funcion"         : "",
        "es_inyectiva"             : False,
        "es_sobreyectiva"          : False,
        "es_biyectiva"             : False,
        "razon_inyectiva"          : "",
        "razon_sobreyectiva"       : "",
        "elementos_sin_imagen"     : [],
        "elementos_imagen_multiple": [],
        "elementos_codominio_libre": [],
    }

    imagenes_por_elemento = {a: [y for (x, y) in relacion if x == a]
                             for a in conjunto_a}

    sin_imagen    = [a for a, imgs in imagenes_por_elemento.items() if len(imgs) == 0]
    multiples_imgs = [a for a, imgs in imagenes_por_elemento.items() if len(imgs) > 1]

    resultado["elementos_sin_imagen"]      = sin_imagen
    resultado["elementos_imagen_multiple"] = multiples_imgs

    if sin_imagen:
        resultado["razon_no_funcion"] = (
            f"Los elementos {sin_imagen} del dominio no tienen imagen en B. "
            "Una función exige que TODOS los elementos del dominio tengan imagen."
        )
        return resultado

    if multiples_imgs:
        detalles = {a: imagenes_por_elemento[a] for a in multiples_imgs}
        resultado["razon_no_funcion"] = (
            f"Los elementos {multiples_imgs} tienen más de una imagen "
            f"(detalle: {detalles}), violando la unicidad de la función."
        )
        return resultado

    resultado["es_funcion"] = True

    todas_las_imagenes = [y for (_, y) in relacion]
    imagenes_repetidas = sorted({y for y in todas_las_imagenes
                                 if todas_las_imagenes.count(y) > 1})

    if not imagenes_repetidas:
        resultado["es_inyectiva"]    = True
        resultado["razon_inyectiva"] = (
            "Todos los elementos del dominio tienen imágenes distintas "
            "(no hay dos elementos de A que compartan la misma imagen)."
        )
    else:
        resultado["razon_inyectiva"] = (
            f"Las imágenes {imagenes_repetidas} corresponden a más de un elemento "
            "del dominio, por lo tanto NO es inyectiva."
        )

    imagenes_usadas = set(todas_las_imagenes)
    codominio_libre = [b for b in conjunto_b if b not in imagenes_usadas]
    resultado["elementos_codominio_libre"] = codominio_libre

    if not codominio_libre:
        resultado["es_sobreyectiva"]    = True
        resultado["razon_sobreyectiva"] = (
            "Todo elemento del codominio B tiene al menos una preimagen en A."
        )
    else:
        resultado["razon_sobreyectiva"] = (
            f"Los elementos {codominio_libre} del codominio no tienen preimagen "
            "en A, por lo tanto NO es sobreyectiva."
        )

    resultado["es_biyectiva"] = resultado["es_inyectiva"] and resultado["es_sobreyectiva"]

    return resultado


# UTILIDADES DE PRESENTACIÓN

def _formatear_relacion(relacion: list) -> str:
    if not relacion:
        return "∅  (relación vacía)"
    return "{ " + ", ".join(str(p) for p in relacion) + " }"


def _mostrar_cerradura(nombre: str, pares_nuevos: list, relacion: list) -> None:
    rel_ampliada = sorted(set(relacion) | set(pares_nuevos))
    print(f"\n  ► Cerradura {nombre}")
    print(f"    Pares a agregar      : {pares_nuevos}")
    print(f"    Relación resultante  : {_formatear_relacion(rel_ampliada)}")


#  PRESENTACIÓN DE RESULTADOS

def mostrar_diagnostico(relacion: list, conjunto_a: list, conjunto_b: list,
                        es_relacion_en_a: bool) -> None:

    print(f"\n{DOBLE}")
    print("  DIAGNÓSTICO DE PROPIEDADES DE LA RELACIÓN")
    print(DOBLE)
    print(f"  R = {_formatear_relacion(relacion)}")
    print(f"  |R| = {len(relacion)} par(es) ordenado(s)\n")

    # ── REFLEXIVIDAD ──────────────────────────────────────────────
    print(LINEA)
    print("  1. REFLEXIVIDAD")
    print(LINEA)

    if es_relacion_en_a:
        reflexiva, cerradura_ref = es_reflexiva(relacion, conjunto_a)
        icono = "✓" if reflexiva else "✗"
        print(f"  [{icono}] La relación {'ES' if reflexiva else 'NO ES'} reflexiva.")

        if reflexiva:
            print("      ∀a ∈ A, (a, a) ∈ R  →  condición cumplida.")
        else:
            print(f"      Pares diagonales faltantes: {cerradura_ref}")
            _mostrar_cerradura("reflexiva", cerradura_ref, relacion)
    else:
        reflexiva = False
        print("  [—] Reflexividad NO aplica  (A ≠ B).")
        print("      La reflexividad requiere R ⊆ A×A; con A≠B no está garantizada.")

    # ── SIMETRÍA ──────────────────────────────────────────────────
    print(f"\n{LINEA}")
    print("  2. SIMETRÍA")
    print(LINEA)

    if es_relacion_en_a:
        simetrica, cerradura_sim = es_simetrica(relacion)
        icono = "✓" if simetrica else "✗"
        print(f"  [{icono}] La relación {'ES' if simetrica else 'NO ES'} simétrica.")

        if simetrica:
            print("      ∀(a,b) ∈ R, (b,a) ∈ R  →  condición cumplida.")
        else:
            print(f"      Pares sin su inverso: {cerradura_sim}")
            _mostrar_cerradura("simétrica", cerradura_sim, relacion)
    else:
        simetrica = False
        print("  [—] Simetría NO aplica  (A ≠ B).")
        print("      El inverso (b,a) de un par (a,b) ∈ A×B no está garantizado en A×B.")

    # ── TRANSITIVIDAD ─────────────────────────────────────────────
    print(f"\n{LINEA}")
    print("  3. TRANSITIVIDAD")
    print(LINEA)

    if not es_relacion_en_a:
        print("  (Con A y B disjuntos, la transitividad puede ser vacuamente verdadera.)\n")

    transitiva, cerradura_trans = es_transitiva(relacion)
    icono = "✓" if transitiva else "✗"
    print(f"  [{icono}] La relación {'ES' if transitiva else 'NO ES'} transitiva.")

    if transitiva:
        print("      ∀(a,b),(b,c) ∈ R → (a,c) ∈ R  →  condición cumplida.")
    else:
        print(f"      Cerradura transitiva completa (todos los pares): {cerradura_trans}")
        _mostrar_cerradura("transitiva", cerradura_trans, relacion)

    # ── RELACIÓN DE EQUIVALENCIA ──────────────────────────────────
    print(f"\n{DOBLE}")
    print("  VEREDICTO: ¿ES RELACIÓN DE EQUIVALENCIA?")
    print(DOBLE)

    ref_txt = ("✓" if reflexiva  else "✗") if es_relacion_en_a else "—"
    sim_txt = ("✓" if simetrica  else "✗") if es_relacion_en_a else "—"
    tra_txt = "✓" if transitiva else "✗"

    print(f"  Reflexiva [{ref_txt}]  |  Simétrica [{sim_txt}]  |  Transitiva [{tra_txt}]")
    print()

    if es_relacion_en_a and reflexiva and simetrica and transitiva:
        print("  ✓  SÍ es una RELACIÓN DE EQUIVALENCIA.")
        print("     Cumple las tres propiedades simultáneamente:")
        print("     Reflexiva ✓  |  Simétrica ✓  |  Transitiva ✓")
    else:
        print("  ✗  NO es una relación de equivalencia.")
        razones = []
        if not es_relacion_en_a:
            razones.append("R ⊆ A×B con A≠B (requiere R ⊆ A×A)")
        else:
            if not reflexiva:
                razones.append("no es reflexiva")
            if not simetrica:
                razones.append("no es simétrica")
        if not transitiva:
            razones.append("no es transitiva")
        print(f"     Motivo(s): {' | '.join(razones)}.")


def mostrar_evaluacion_funcion(resultado: dict) -> None:
    print(f"\n{DOBLE}")
    print("  EVALUACIÓN: ¿ES FUNCIÓN?")
    print(DOBLE)

    if not resultado["es_funcion"]:
        print("  ✗  La relación NO es una función.")
        print(f"     {resultado['razon_no_funcion']}")
        if resultado["elementos_sin_imagen"]:
            print(f"     Elementos sin imagen         : {resultado['elementos_sin_imagen']}")
        if resultado["elementos_imagen_multiple"]:
            print(f"     Elementos con más de 1 imagen: {resultado['elementos_imagen_multiple']}")
        return

    print("  ✓  La relación SÍ es una FUNCIÓN  f : A → B.")
    print("     Cada elemento de A tiene exactamente una imagen en B.")
    print(f"\n  Clasificación de la función:")
    print(f"  {'─'*50}")

    icono_i = "✓" if resultado["es_inyectiva"] else "✗"
    print(f"\n  [{icono_i}] INYECTIVA  (función uno a uno)")
    print(f"      {resultado['razon_inyectiva']}")

    icono_s = "✓" if resultado["es_sobreyectiva"] else "✗"
    print(f"\n  [{icono_s}] SOBREYECTIVA  (función sobre)")
    print(f"      {resultado['razon_sobreyectiva']}")
    if resultado["elementos_codominio_libre"]:
        print(f"      Elementos del codominio sin preimagen: "
              f"{resultado['elementos_codominio_libre']}")

    icono_b = "✓" if resultado["es_biyectiva"] else "✗"
    print(f"\n  [{icono_b}] BIYECTIVA  (correspondencia uno a uno perfecta)")
    if resultado["es_biyectiva"]:
        print("      Es simultáneamente inyectiva y sobreyectiva.")
        print("      Existe una correspondencia perfecta (1 a 1) entre A y B.")
    else:
        faltantes = []
        if not resultado["es_inyectiva"]:
            faltantes.append("inyectividad")
        if not resultado["es_sobreyectiva"]:
            faltantes.append("sobreyectividad")
        print(f"      No cumple: {' y '.join(faltantes)}.")

#  PROGRAMA PRINCIPAL

def main():
    print(f"\n{DOBLE}")
    print(f"{TITULO}")
    print(DOBLE)
    print("  Parte 2 · Taller Evaluativo · Matemática Discreta")
    print(f"{LINEA}\n")

    print("  ¿Con cuántos conjuntos desea trabajar?")
    print("    [1]  Un solo conjunto A  →  Relación en A   (R ⊆ A×A)")
    print("    [2]  Dos conjuntos A y B →  Relación de A en B  (R ⊆ A×B)")

    while True:
        opcion = input("\n  Ingrese su opción (1 ó 2): ").strip()
        if opcion in ("1", "2"):
            break
        print("  ✗ Opción inválida. Escriba 1 ó 2.")

    es_relacion_en_a = (opcion == "1")

    print(f"\n{LINEA}")
    print("  DEFINICIÓN DE CONJUNTOS")
    print(LINEA)

    conjunto_a = ingresar_conjunto("A")

    if es_relacion_en_a:
        conjunto_b = conjunto_a
        print("\n  (Relación en A: el codominio es el mismo conjunto A)")
    else:
        conjunto_b = ingresar_conjunto("B")

    print(f"\n{LINEA}")
    print("  DEFINICIÓN DE LA RELACIÓN R")
    print(LINEA)

    relacion = ingresar_relacion(conjunto_a, conjunto_b)

    print(f"\n  ✓ Relación confirmada: R = {_formatear_relacion(relacion)}")

    mostrar_diagnostico(relacion, conjunto_a, conjunto_b, es_relacion_en_a)

    resultado_funcion = evaluar_funcion(relacion, conjunto_a, conjunto_b)
    mostrar_evaluacion_funcion(resultado_funcion)

    print(f"\n{DOBLE}")
    print("  Análisis finalizado.  ¡Hasta pronto!")
    print(f"{DOBLE}\n")


if __name__ == "__main__":
    main()