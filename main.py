import sys # importa la librería para leer argumentos desde la terminal

tareas = [] # lista donde se guardarán las tareas
with open("tareas.txt") as f: # abre el archivo de tareas
    for linea in f.readlines(): # recorre cada línea del archivo
        partes = linea.strip().split(",") # separa por comas (ID, duración, categoría)
        tareas.append((partes[0], int(partes[1]), partes[2]))  # guarda la tarea como tupla

recursos = [] # lista donde se guardarán los recursos
with open("recursos.txt") as f: # abre el archivo de recursos
    for linea in f.readlines(): # recorre cada línea
        partes = linea.strip().split(",") # separa por comas
        recursos.append((partes[0], set(partes[1:]))) # guarda el recurso y sus categorías 

tareas = sorted(tareas, key=lambda t: t[1], reverse=True) # ordena las tareas por duración de mayor a menor 

tiempo_libre = {}  # diccionario que guarda cuándo queda libre cada recurso
for rid, cats in recursos: # recorre los recursos
    tiempo_libre[rid] = 0 # inicialmente todos están libres en tiempo 0

resultado = [] # lista donde se guardará la solución final

for tarea_id, duracion, categoria in tareas: # recorre cada tarea
    mejor_recurso = None # variable para guardar el mejor recurso encontrado
    menor_tiempo = 999999 # inicializa con un número grande

    for rid, cats in recursos:  # recorre todos los recursos
        if categoria in cats: # verifica si el recurso puede hacer esa tarea
            if tiempo_libre[rid] < menor_tiempo: # busca el recurso más disponible
                menor_tiempo = tiempo_libre[rid]  # actualiza el menor tiempo encontrado
                mejor_recurso = rid # guarda el mejor recurso

    inicio = tiempo_libre[mejor_recurso] # guarda el mejor recurso
    fin = inicio + duracion # el fin es inicio + duración de la tarea
    tiempo_libre[mejor_recurso] = fin # actualiza el tiempo en que el recurso queda libre
    resultado.append((tarea_id, mejor_recurso, inicio, fin)) # guarda la asignación de la tarea

with open("output.txt", "w") as f: # guarda la asignación de la tarea
    for tarea_id, rid, inicio, fin in resultado: # recorre los resultados
      f.write(f"{tarea_id},{rid},{inicio},{fin}\n")  # escribe cada línea en formato requerido
      