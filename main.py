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

    for rid, cats in recursos:
        if categoria in cats:
            if tiempo_libre[rid] < menor_tiempo:
                menor_tiempo = tiempo_libre[rid]
                mejor_recurso = rid

    inicio = tiempo_libre[mejor_recurso]
    fin = inicio + duracion
    tiempo_libre[mejor_recurso] = fin
    resultado.append((tarea_id, mejor_recurso, inicio, fin))

with open("output.txt", "w") as f:
    for tarea_id, rid, inicio, fin in resultado:
      f.write(f"{tarea_id},{rid},{inicio},{fin}\n")
      