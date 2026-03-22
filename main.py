<<<<<<< HEAD
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
=======
from typing import List, Dict, Set, Tuple  
import sys  
# Librerias para poder leer el codigo de buena manera
>>>>>>> afed660 (Agrega comentarios explicativos al codigo final, cambios)

tareas = []
with open("tareas.txt") as f:
    for linea in f.readlines():
        partes = linea.strip().split(",")
        tareas.append((partes[0], int(partes[1]), partes[2]))  
# Guarda la tarea como tupla

recursos = []
with open("recursos.txt") as f:
    for linea in f.readlines():
        partes = linea.strip().split(",")
        recursos.append((partes[0], set(partes[1:])))  
# Guarda el recurso como tupla


tareas_ordenadas = sorted(tareas, key=lambda t: t[1], reverse=True)  
# Ordena tareas por duración (mayor a menor)

tiempo_recurso = {}
for rid, cats in recursos:
    tiempo_recurso[rid] = 0  
# Guarda cuándo queda libre cada recurso

resultado = []   
# Lista donde se guardará la planificación final


for tarea_id, duracion, categoria in tareas_ordenadas:

    mejor_recurso = None
    menor_tiempo = 999999

    for rid, cats in recursos:
        if categoria in cats:  
# Verifica si el recurso puede realizar la tarea
            if tiempo_recurso[rid] < menor_tiempo:
                menor_tiempo = tiempo_recurso[rid]
                mejor_recurso = rid  
# Elegimos el recurso que queda libre antes

    inicio = tiempo_recurso[mejor_recurso]  
    fin = inicio + duracion
    tiempo_recurso[mejor_recurso] = fin  
# Actualiza cuándo el recurso vuelve a estar disponible

    resultado.append((tarea_id, mejor_recurso, inicio, fin))  
# Guarda asignación


with open("output.txt", "w") as f:
    for tarea_id, rid, inicio, fin in resultado:
        f.write(f"{tarea_id},{rid},{inicio},{fin}\n")  
# Ordenando el formato 


Tarea = Tuple[str, int, str]
Recurso = Tuple[str, Set[str]]
Asignacion = Tuple[str, str, int, int]


def leer_tareas(nombre_archivo: str) -> List[Tarea]:
<<<<<<< HEAD
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
=======
    tareas: List[Tarea] = []
    with open(nombre_archivo, "r") as archivo:
        for linea in archivo:
            partes = linea.strip().split(",")
            tareas.append((partes[0], int(partes[1]), partes[2]))
    return tareas
>>>>>>> afed660 (Agrega comentarios explicativos al codigo final, cambios)

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
    recursos: List[Recurso] = []
    with open(nombre_archivo, "r") as archivo: # Abre el archivo
        for linea in archivo:
            partes = linea.strip().split(",")
            recursos.append((partes[0], set(partes[1:])))
    return recursos


def planificar_tareas(tareas: List[Tarea], recursos: List[Recurso]) -> List[Asignacion]:
    tareas_ordenadas = sorted(tareas, key=lambda tarea: tarea[1], reverse=True)
# Ordena tareas por duración
    tiempo_recurso: Dict[str, int] = {r: 0 for r, _ in recursos}
# Inicializa disponibilidad de recursos

    resultado: List[Asignacion] = []

    for tarea_id, duracion, categoria in tareas_ordenadas:
        mejor_recurso = None
        menor_tiempo = float("inf")

        for recurso_id, categorias in recursos:
            if categoria in categorias and tiempo_recurso[recurso_id] < menor_tiempo:
                menor_tiempo = tiempo_recurso[recurso_id]
                mejor_recurso = recurso_id  
# Selecciona recurso disponible más temprano

        if mejor_recurso is None:
            raise ValueError("No hay recurso compatible")

        inicio = tiempo_recurso[mejor_recurso]
        fin = inicio + duracion
        tiempo_recurso[mejor_recurso] = fin

        resultado.append((tarea_id, mejor_recurso, inicio, fin))

    return resultado


def escribir_salida(nombre_archivo: str, resultado: List[Asignacion]) -> None:
    with open(nombre_archivo, "w") as archivo:
        for t, r, i, f in resultado:
            archivo.write(f"{t},{r},{i},{f}\n")
# Escribe cada línea en formato requerido


def calcular_makespan(resultado: List[Asignacion]) -> int:
    return max(fin for _, _, _, fin in resultado) if resultado else 0
# Devuelve el mayor tiempo de finalización (makespan)


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
        print("Se cumplió el objetivo")
    else:
        print("Solución válida pero no óptima")


<<<<<<< HEAD
if __name__ == "__main__":  # Punto de entrada del programa
    main()  # Ejecuta el programa principal
>>>>>>> eec8332 (Agrega comentarios explicativos al codigo final)
=======
if __name__ == "__main__":
    main()
>>>>>>> afed660 (Agrega comentarios explicativos al codigo final, cambios)
