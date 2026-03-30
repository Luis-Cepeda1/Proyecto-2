import sys
import heapq

tareas = []
with open("tareas.txt", "r", encoding="utf-8") as archivo_tareas:
    for linea in archivo_tareas:
        linea = linea.rstrip("\n")
        if not linea:
            continue
        id_tarea, duracion, categoria = linea.split(",")
        tareas.append((id_tarea, int(duracion), categoria))

recursos_raw = []
with open("recursos.txt", "r", encoding="utf-8") as archivo_recursos:
    for linea in archivo_recursos:
        linea = linea.rstrip("\n")
        if not linea:
            continue
        partes = linea.split(",")
        id_recurso = partes[0]
        categorias = partes[1:]
        recursos_raw.append((id_recurso, categorias))

categoria_a_indice = {}
siguiente_indice = 0

for _, _, categoria in tareas:
    if categoria not in categoria_a_indice:
        categoria_a_indice[categoria] = siguiente_indice
        siguiente_indice += 1

for _, categorias in recursos_raw:
    for categoria in categorias:
        if categoria not in categoria_a_indice:
            categoria_a_indice[categoria] = siguiente_indice
            siguiente_indice += 1

cantidad_categorias = siguiente_indice
cantidad_recursos = len(recursos_raw)

ids_recursos = [None] * cantidad_recursos
categorias_por_recurso = [None] * cantidad_recursos
heaps_base = [[] for _ in range(cantidad_categorias)]

for indice_recurso, (id_recurso, categorias) in enumerate(recursos_raw):
    ids_recursos[indice_recurso] = id_recurso
    categorias_indices = [categoria_a_indice[c] for c in categorias]
    categorias_por_recurso[indice_recurso] = categorias_indices

    for indice_categoria in categorias_indices:
        heaps_base[indice_categoria].append((0, indice_recurso))

for heap_categoria in heaps_base:
    heapq.heapify(heap_categoria)

tareas_convertidas = []
for id_tarea, duracion, categoria in tareas:
    tareas_convertidas.append((id_tarea, duracion, categoria_a_indice[categoria]))

def asignar_tareas(tareas_ordenadas):
    heaps = [heap_categoria.copy() for heap_categoria in heaps_base]
    tiempo_libre = [0] * cantidad_recursos
    asignaciones = []
    makespan = 0

    heappop = heapq.heappop
    heappush = heapq.heappush

    for id_tarea, duracion, indice_categoria in tareas_ordenadas:
        heap_categoria = heaps[indice_categoria]

        while True:
            tiempo, indice_recurso = heappop(heap_categoria)
            if tiempo == tiempo_libre[indice_recurso]:
                break

        inicio = tiempo
        fin = inicio + duracion
        tiempo_libre[indice_recurso] = fin
        asignaciones.append((id_tarea, indice_recurso, inicio, fin))

        if fin > makespan:
            makespan = fin

        for otra_categoria in categorias_por_recurso[indice_recurso]:
            heappush(heaps[otra_categoria], (fin, indice_recurso))

    return asignaciones, makespan

makespan_objetivo = int(sys.argv[1]) if len(sys.argv) > 1 else 0

criterios = [
    sorted(tareas_convertidas, key=lambda t: t[1], reverse=True),
    sorted(tareas_convertidas, key=lambda t: t[1]),
    sorted(tareas_convertidas, key=lambda t: (t[2], -t[1])),
    sorted(tareas_convertidas, key=lambda t: (-t[1], t[2])),
]

mejor_asignacion = None
mejor_makespan = 10**18

for tareas_ordenadas in criterios:
    asignaciones, makespan = asignar_tareas(tareas_ordenadas)

    if makespan < mejor_makespan:
        mejor_makespan = makespan
        mejor_asignacion = asignaciones

    if mejor_makespan <= makespan_objetivo:
        break

with open("output.txt", "w", encoding="utf-8") as salida:
    salida.writelines(
        f"{id_tarea},{ids_recursos[indice_recurso]},{inicio},{fin}\n"
        for id_tarea, indice_recurso, inicio, fin in mejor_asignacion
    )

print("Makespan obtenido:", mejor_makespan)