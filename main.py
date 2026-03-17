from typing import List, Dict, Set, Tuple
import sys


Tarea = Tuple[str, int, str]
Recurso = Tuple[str, Set[str]]
Asignacion = Tuple[str, str, int, int]


def leer_tareas(nombre_archivo: str) -> List[Tarea]:
    tareas: List[Tarea] = []

    with open(nombre_archivo, "r") as archivo:
        for linea in archivo:
            partes = linea.strip().split(",")
            tarea_id = partes[0]
            duracion = int(partes[1])
            categoria = partes[2]
            tareas.append((tarea_id, duracion, categoria))

    return tareas


def leer_recursos(nombre_archivo: str) -> List[Recurso]:
    recursos: List[Recurso] = []

    with open(nombre_archivo, "r") as archivo:
        for linea in archivo:
            partes = linea.strip().split(",")
            recurso_id = partes[0]
            categorias = set(partes[1:])
            recursos.append((recurso_id, categorias))

    return recursos


def planificar_tareas(tareas: List[Tarea], recursos: List[Recurso]) -> List[Asignacion]:
    tareas_ordenadas = sorted(tareas, key=lambda tarea: tarea[1], reverse=True)

    tiempo_recurso: Dict[str, int] = {}
    for recurso_id, _ in recursos:
        tiempo_recurso[recurso_id] = 0

    resultado: List[Asignacion] = []

    for tarea_id, duracion, categoria in tareas_ordenadas:
        mejor_recurso = None
        menor_tiempo = float("inf")

        for recurso_id, categorias in recursos:
            if categoria in categorias and tiempo_recurso[recurso_id] < menor_tiempo:
                menor_tiempo = tiempo_recurso[recurso_id]
                mejor_recurso = recurso_id

        if mejor_recurso is None:
            raise ValueError(f"No existe recurso compatible para la tarea {tarea_id}")

        inicio = tiempo_recurso[mejor_recurso]
        fin = inicio + duracion
        tiempo_recurso[mejor_recurso] = fin

        resultado.append((tarea_id, mejor_recurso, inicio, fin))

    return resultado


def escribir_salida(nombre_archivo: str, resultado: List[Asignacion]) -> None:
    with open(nombre_archivo, "w") as archivo:
        for tarea_id, recurso_id, inicio, fin in resultado:
            archivo.write(f"{tarea_id},{recurso_id},{inicio},{fin}\n")


def calcular_makespan(resultado: List[Asignacion]) -> int:
    if not resultado:
        return 0
    return max(fin for _, _, _, fin in resultado)


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python main.py <makespan_objetivo>")
        return

    makespan_objetivo = int(sys.argv[1])

    tareas = leer_tareas("tareas.txt")
    recursos = leer_recursos("recursos.txt")
    resultado = planificar_tareas(tareas, recursos)
    escribir_salida("output.txt", resultado)

    makespan_obtenido = calcular_makespan(resultado)

    print(f"Makespan objetivo: {makespan_objetivo}")
    print(f"Makespan obtenido: {makespan_obtenido}")

    if makespan_obtenido <= makespan_objetivo:
        print("Se cumplió o mejoró el makespan objetivo.")
    else:
        print("No se alcanzó el makespan objetivo, pero se generó una solución válida.")


if __name__ == "__main__":
    main()