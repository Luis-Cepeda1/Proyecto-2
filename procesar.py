import sys
import pickle
from bisect import insort
from collections import defaultdict
from typing import Any


RANGOS: dict[str, tuple[float, float]] = {
    "VIB": (0.0, 50.0),
    "TEMP": (-10.0, 60.0),
}


def es_valido(tipo: str, valor: float) -> bool:
    if tipo not in RANGOS:
        return False
    minimo, maximo = RANGOS[tipo]
    return minimo <= valor <= maximo


def numero_sensor(sensor: str) -> int:
    return int(sensor[1:])


def procesar_archivo(ruta_datos: str) -> None:
    por_sector: dict[str, dict[str, list[tuple[str, float]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    por_sensor: dict[str, dict[str, list[tuple[str, float]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    sensores_sector: dict[str, set[str]] = defaultdict(set)
    temp_por_fecha: dict[str, dict[str, dict[str, float]]] = defaultdict(dict)

    with open(ruta_datos, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue

            partes = linea.split("|")
            if len(partes) != 5:
                continue

            timestamp, sensor, tipo, valor_str, sector = partes

            try:
                valor = float(valor_str)
            except ValueError:
                continue

            if not es_valido(tipo, valor):
                continue

            por_sector[sector][tipo].append((timestamp, valor))
            por_sensor[sensor][tipo].append((timestamp, valor))
            sensores_sector[sector].add(sensor)

            if tipo == "TEMP":
                fecha = timestamp[:10]
                if fecha not in temp_por_fecha[sector]:
                    temp_por_fecha[sector][fecha] = {"sum": 0.0, "count": 0.0}
                temp_por_fecha[sector][fecha]["sum"] += valor
                temp_por_fecha[sector][fecha]["count"] += 1.0

    for sector in por_sector:
        for tipo in por_sector[sector]:
            por_sector[sector][tipo].sort(key=lambda par: par[0])

    for sensor in por_sensor:
        for tipo in por_sensor[sensor]:
            por_sensor[sensor][tipo].sort(key=lambda par: par[0])

    sensores_ordenados: dict[str, list[str]] = {}
    for sector, sensores in sensores_sector.items():
        sensores_ordenados[sector] = sorted(sensores, key=numero_sensor)

    estructura: dict[str, Any] = {
        "por_sector": dict(por_sector),
        "por_sensor": dict(por_sensor),
        "sensores_sector": sensores_ordenados,
        "temp_por_fecha": dict(temp_por_fecha),
    }

    with open("datos.bin", "wb") as archivo_salida:
        pickle.dump(estructura, archivo_salida, protocol=pickle.HIGHEST_PROTOCOL)

    print("Preprocesamiento completado -> datos.bin")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: py procesar.py datos.txt")
        sys.exit(1)

    procesar_archivo(sys.argv[1])