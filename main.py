<<<<<<< HEAD
import sys

tareas = []
with open("tareas_2.txt") as f:
    for linea in f.readlines():
        partes = linea.strip().split(",")
        tareas.append((partes[0], int(partes[1]), partes[2]))

recursos = []
with open("recursos_2.txt") as f:
    for linea in f.readlines():
        partes = linea.strip().split(",")
        recursos.append((partes[0], set(partes[1:])))

tareas = sorted(tareas, key=lambda t: t[1], reverse=True)

tiempo_libre = {}
for rid, cats in recursos:
    tiempo_libre[rid] = 0

resultado = []

for tarea_id, duracion, categoria in tareas:
    mejor_recurso = None
    menor_tiempo = 999999
=======
from typing import List, Dict, Set, Tuple  # Tipos para mejorar claridad y estructura del código
import sys  # Permite leer argumentos desde la terminal

tareas = []  # Lista donde se almacenarán las tareas leídas desde el archivo
with open("tareas.txt") as f:  # Abre el archivo tareas.txt en modo lectura
    for linea in f.readlines():  # Recorre cada línea del archivo
        partes = linea.strip().split(",")  # Elimina saltos de línea y separa por comas
        tareas.append((partes[0], int(partes[1]), partes[2]))  
        # Guarda la tarea como tupla: (id, duración, categoría)

recursos = []  # Lista donde se almacenarán los recursos
with open("recursos.txt") as f:  # Abre el archivo recursos.txt
    for linea in f.readlines():  # Recorre cada línea
        partes = linea.strip().split(",")  # Limpia y separa por comas
        recursos.append((partes[0], set(partes[1:])))  
        # Guarda el recurso como tupla: (id, conjunto de categorías que puede hacer)

tareas_ordenadas = sorted(tareas, key=lambda t: t[1], reverse=True)  
# Ordena las tareas de mayor a menor duración (estrategia greedy)

tiempo_recurso = {}  # Diccionario que indica cuándo queda libre cada recurso
for rid, cats in recursos:  # Recorre todos los recursos
    tiempo_recurso[rid] = 0  # Inicializa todos los recursos como disponibles en tiempo 0

resultado = []  # Lista donde se guardará la planificación final

for tarea_id, duracion, categoria in tareas_ordenadas:  
# Recorre cada tarea ya ordenada

    mejor_recurso = None  # Guardará el recurso más adecuado
    menor_tiempo = 999999  # Valor inicial grande para buscar el mínimo

    for rid, cats in recursos:  # Recorre todos los recursos
        if categoria in cats:  # Verifica si el recurso puede realizar la tarea
            if tiempo_recurso[rid] < menor_tiempo:  # Si este recurso queda libre antes
                menor_tiempo = tiempo_recurso[rid]  # Actualiza el menor tiempo encontrado
                mejor_recurso = rid  # Guarda este recurso como el mejor

    inicio = tiempo_recurso[mejor_recurso]  # La tarea inicia cuando el recurso queda libre
    fin = inicio + duracion  # El tiempo de término es inicio + duración
    tiempo_recurso[mejor_recurso] = fin  # Actualiza cuándo el recurso vuelve a estar disponible

    resultado.append((tarea_id, mejor_recurso, inicio, fin))  
    # Guarda la asignación: (tarea, recurso, inicio, fin)

with open("output.txt", "w") as f:  # Abre el archivo de salida en modo escritura
    for tarea_id, rid, inicio, fin in resultado:  # Recorre cada asignación
        f.write(tarea_id + "," + rid + "," + str(inicio) + "," + str(fin) + "\n")  
        # Escribe cada asignación en formato requerido (CSV)

# ========================= DEFINICIÓN DE TIPOS =========================

Tarea = Tuple[str, int, str]  # (id, duración, categoría)
Recurso = Tuple[str, Set[str]]  # (id, conjunto de categorías)
Asignacion = Tuple[str, str, int, int]  # (tarea, recurso, inicio, fin)

# ========================= FUNCIONES =========================

def leer_tareas(nombre_archivo: str) -> List[Tarea]:
    tareas: List[Tarea] = []  # Lista tipada de tareas

    with open(nombre_archivo, "r") as archivo:  # Abre archivo
        for linea in archivo:  # Recorre cada línea
            partes = linea.strip().split(",")  # Limpia y separa
            tarea_id = partes[0]  # ID de la tarea
            duracion = int(partes[1])  # Duración convertida a entero
            categoria = partes[2]  # Categoría de la tarea
            tareas.append((tarea_id, duracion, categoria))  # Guarda la tarea

    return tareas  # Retorna la lista de tareas
>>>>>>> eec8332 (Agrega comentarios explicativos al codigo final)

    for rid, cats in recursos:
        if categoria in cats:
            if tiempo_libre[rid] < menor_tiempo:
                menor_tiempo = tiempo_libre[rid]
                mejor_recurso = rid

<<<<<<< HEAD
    inicio = tiempo_libre[mejor_recurso]
    fin = inicio + duracion
    tiempo_libre[mejor_recurso] = fin
    resultado.append((tarea_id, mejor_recurso, inicio, fin))

with open("output.txt", "w") as f:
    for tarea_id, rid, inicio, fin in resultado:
      f.write(f"{tarea_id},{rid},{inicio},{fin}\n")
      
=======
def leer_recursos(nombre_archivo: str) -> List[Recurso]:
    recursos: List[Recurso] = []  # Lista tipada de recursos

    with open(nombre_archivo, "r") as archivo:  # Abre archivo
        for linea in archivo:  # Recorre líneas
            partes = linea.strip().split(",")  # Limpia y separa
            recurso_id = partes[0]  # ID del recurso
            categorias = set(partes[1:])  # Categorías como conjunto
            recursos.append((recurso_id, categorias))  # Guarda el recurso

    return recursos  # Retorna lista de recursos


def planificar_tareas(tareas: List[Tarea], recursos: List[Recurso]) -> List[Asignacion]:
    tareas_ordenadas = sorted(tareas, key=lambda tarea: tarea[1], reverse=True)  
    # Ordena tareas por duración (greedy)

    tiempo_recurso: Dict[str, int] = {}  # Diccionario de disponibilidad
    for recurso_id, _ in recursos:
        tiempo_recurso[recurso_id] = 0  # Inicializa todos en 0

    resultado: List[Asignacion] = []  # Lista de asignaciones

    for tarea_id, duracion, categoria in tareas_ordenadas:
        mejor_recurso = None  # Mejor recurso encontrado
        menor_tiempo = float("inf")  # Inicializa con infinito

        for recurso_id, categorias in recursos:
            if categoria in categorias and tiempo_recurso[recurso_id] < menor_tiempo:
                # Si el recurso es compatible y queda libre antes
                menor_tiempo = tiempo_recurso[recurso_id]
                mejor_recurso = recurso_id

        if mejor_recurso is None:
            # Si no hay recurso compatible
            raise ValueError(f"No existe recurso compatible para la tarea {tarea_id}")

        inicio = tiempo_recurso[mejor_recurso]  # Inicio de la tarea
        fin = inicio + duracion  # Fin de la tarea
        tiempo_recurso[mejor_recurso] = fin  # Actualiza disponibilidad

        resultado.append((tarea_id, mejor_recurso, inicio, fin))  
        # Guarda asignación

    return resultado  # Retorna planificación completa


def escribir_salida(nombre_archivo: str, resultado: List[Asignacion]) -> None:
    with open(nombre_archivo, "w") as archivo:  # Abre archivo de salida
        for tarea_id, recurso_id, inicio, fin in resultado:
            archivo.write(f"{tarea_id},{recurso_id},{inicio},{fin}\n")  
            # Escribe cada línea en formato requerido


def calcular_makespan(resultado: List[Asignacion]) -> int:
    if not resultado:  # Si no hay tareas
        return 0
    return max(fin for _, _, _, fin in resultado)  
    # Devuelve el mayor tiempo de finalización (makespan)


def main() -> None:
    if len(sys.argv) < 2:  # Verifica si se entregó argumento
        print("Uso: python main.py <makespan_objetivo>")  # Mensaje de uso
        return

    makespan_objetivo = int(sys.argv[1])  # Lee el argumento desde la terminal

    tareas = leer_tareas("tareas.txt")  # Carga tareas desde archivo
    recursos = leer_recursos("recursos.txt")  # Carga recursos
    resultado = planificar_tareas(tareas, recursos)  # Genera planificación
    escribir_salida("output.txt", resultado)  # Guarda resultado en archivo

    makespan_obtenido = calcular_makespan(resultado)  # Calcula makespan final

    print(f"Makespan objetivo: {makespan_objetivo}")  # Muestra objetivo
    print(f"Makespan obtenido: {makespan_obtenido}")  # Muestra resultado

    if makespan_obtenido <= makespan_objetivo:
        print("Se cumplió o mejoró el makespan objetivo.")  # Caso exitoso
    else:
        print("No se alcanzó el makespan objetivo, pero se generó una solución válida.")  
        # Caso no óptimo pero válido


if __name__ == "__main__":  # Punto de entrada del programa
    main()  # Ejecuta el programa principal
>>>>>>> eec8332 (Agrega comentarios explicativos al codigo final)
