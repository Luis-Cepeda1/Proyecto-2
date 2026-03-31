import sys
import heapq

# Se leen las tareas del archivo y se guardan como: (id_tarea, duracion, categoria)
tareas = []
with open("tareas.txt", "r", encoding="utf-8") as archivo_tareas:
    for linea in archivo_tareas:
        linea = linea.rstrip("\n")
        if not linea:
            continue
        id_tarea, duracion, categoria = linea.split(",")
        tareas.append((id_tarea, int(duracion), categoria))

# Se leen los recursos y las categorías que pueden ejecutar
recursos_raw = []
with open("recursos.txt", "r", encoding="utf-8") as archivo_recursos:
    for linea in archivo_recursos:
        linea = linea.rstrip("\n")
        if not linea:
            continue
        partes = linea.split(",")
        recursos_raw.append((partes[0], partes[1:]))

# Se convierten las categorías (strings) a índices numéricos para hacer el algoritmo más eficiente
categoria_a_indice = {}
siguiente_indice = 0

# Se asigna índice a cada categoría de tareas
for _, _, categoria in tareas:
    if categoria not in categoria_a_indice:
        categoria_a_indice[categoria] = siguiente_indice
        siguiente_indice += 1

# Se asegura que todas las categorías de recursos también estén incluidas
for _, categorias in recursos_raw:
    for categoria in categorias:
        if categoria not in categoria_a_indice:
            categoria_a_indice[categoria] = siguiente_indice
            siguiente_indice += 1

cantidad_categorias = siguiente_indice
cantidad_recursos = len(recursos_raw)

# Arreglos optimizados para acceso rápido
ids_recursos = [None] * cantidad_recursos
categorias_por_recurso = [None] * cantidad_recursos

# Heaps por categoría que permiten obtener rápido el recurso más disponible
heaps_base = [[] for _ in range(cantidad_categorias)]

# Se construyen los heaps iniciales
for indice_recurso, (id_recurso, categorias) in enumerate(recursos_raw):
    ids_recursos[indice_recurso] = id_recurso
    categorias_indices = [categoria_a_indice[c] for c in categorias]
    categorias_por_recurso[indice_recurso] = categorias_indices
    # Cada recurso se agrega a los heaps de sus categorías
    for indice_categoria in categorias_indices:
        heaps_base[indice_categoria].append((0, indice_recurso))

# Se ordenan los heaps por prioridad
for heap_categoria in heaps_base:
    heapq.heapify(heap_categoria)

# Se reemplazan las categorías por sus índices numéricos
tareas_convertidas = []
for id_tarea, duracion, categoria in tareas:
    tareas_convertidas.append((id_tarea, duracion, categoria_a_indice[categoria]))

# Asigna las tareas a recursos usando heaps 
def asignar_tareas(tareas_ordenadas):
    heaps = [heap[:] for heap in heaps_base]
    tiempo_libre = [0] * cantidad_recursos
    asignaciones = []
    makespan = 0

    heappop = heapq.heappop
    heappush = heapq.heappush

    # Se recorren las tareas en un orden heurístico
    for id_tarea, duracion, indice_categoria in tareas_ordenadas:
        heap_categoria = heaps[indice_categoria]

        # Se obtiene el mejor recurso disponible 
        while True:
            tiempo, indice_recurso = heappop(heap_categoria)
            if tiempo == tiempo_libre[indice_recurso]:
                break

        # Se asigna la tarea
        inicio = tiempo
        fin = inicio + duracion
        tiempo_libre[indice_recurso] = fin
        asignaciones.append((id_tarea, indice_recurso, inicio, fin))

        # Se actualiza el makespan
        if fin > makespan:
            makespan = fin

        # Se actualizan todos los heaps donde participa ese recurso
        for otra_categoria in categorias_por_recurso[indice_recurso]:
            heappush(heaps[otra_categoria], (fin, indice_recurso))

    return asignaciones, makespan

makespan_objetivo = int(sys.argv[1]) if len(sys.argv) > 1 else 0

# Se prueban distintos órdenes de tareas para mejorar el resultado
criterios = [
    sorted(tareas_convertidas, key=lambda t: t[1], reverse=True), # tareas largas primero
    sorted(tareas_convertidas, key=lambda t: (t[2], -t[1])), # por categoría y su duración
    sorted(tareas_convertidas, key=lambda t: t[1]), # tareas cortas primero
]

mejor_asignacion = None
mejor_makespan = 10**18

for tareas_ordenadas in criterios:
    asignaciones, makespan = asignar_tareas(tareas_ordenadas)

    # Se guarda la mejor solución encontrada
    if makespan < mejor_makespan:
        mejor_makespan = makespan
        mejor_asignacion = asignaciones

    # Break si se cumple el objetivo
    if mejor_makespan <= makespan_objetivo:
        break

# Se guarda el resultado en un output
with open("output.txt", "w", encoding="utf-8") as salida:
    salida.writelines(
        f"{id_tarea},{ids_recursos[indice_recurso]},{inicio},{fin}\n"
        for id_tarea, indice_recurso, inicio, fin in mejor_asignacion)
    
print("Makespan obtenido:", mejor_makespan)

