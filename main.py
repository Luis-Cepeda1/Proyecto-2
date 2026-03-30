import sys
import heapq

tareas = []
with open("tareas.txt") as f:
    for linea in f.readlines():
        partes = linea.strip().split(",")
        tareas.append((partes[0], int(partes[1]), partes[2]))

recursos = []
with open("recursos.txt") as f:
    for linea in f.readlines():
        partes = linea.strip().split(",")
        recursos.append((partes[0], set(partes[1:])))

def asignar(tareas_ordenadas):
    cats_por_recurso = {}
    heaps = {}
    tiempo_libre = {}

    for rid, cats in recursos:
        tiempo_libre[rid] = 0
        cats_por_recurso[rid] = cats
        for cat in cats:
            if cat not in heaps:
                heaps[cat] = []
            heapq.heappush(heaps[cat], (0, rid))

    resultado = []

    for tarea_id, duracion, categoria in tareas_ordenadas:
        while True:
            tiempo, rid = heapq.heappop(heaps[categoria])
            if tiempo == tiempo_libre[rid]:
                break

        inicio = tiempo_libre[rid]
        fin = inicio + duracion
        tiempo_libre[rid] = fin
        resultado.append((tarea_id, rid, inicio, fin))

        for cat in cats_por_recurso[rid]:
            heapq.heappush(heaps[cat], (fin, rid))

    return resultado

makespan_objetivo = int(sys.argv[1]) if len(sys.argv) > 1 else 0

criterios = [
    sorted(tareas, key=lambda t: t[1], reverse=True),
    sorted(tareas, key=lambda t: t[1], reverse=False),
    sorted(tareas, key=lambda t: (t[2], -t[1])),
    sorted(tareas, key=lambda t: (-t[1], t[2])),
]

mejor_resultado = None
mejor_makespan = 999999999

for tareas_ordenadas in criterios:
    resultado = asignar(tareas_ordenadas)
    makespan = max(fin for _, _, _, fin in resultado)

    if makespan < mejor_makespan:
        mejor_makespan = makespan
        mejor_resultado = resultado

    if mejor_makespan <= makespan_objetivo:
        break

with open("output.txt", "w") as f:
    for tarea_id, rid, inicio, fin in mejor_resultado:
        f.write(f"{tarea_id},{rid},{inicio},{fin}\n")

print("Makespan obtenido: " + str(mejor_makespan))