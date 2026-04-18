
import sys
import pickle
from collections import defaultdict
from typing import Any

# Rangos válidos por tipo
RANGOS: dict[str, tuple[float, float]] = {
    "VIB":  (0.0, 50.0),
    "TEMP": (-10.0, 60.0),
}


def truncar(valor: float) -> float:
    """Trunca a 1 decimal (no redondea)."""
    return int(valor * 10) / 10


def procesar(ruta_datos: str) -> None:
    # Índice 1: sector -> tipo -> lista de (timestamp_str, valor)
    # ordenada por timestamp al final
    por_sector: dict[str, dict[str, list[tuple[str, float]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    # Índice 2: sensor -> tipo -> lista de (timestamp_str, valor)
    por_sensor: dict[str, dict[str, list[tuple[str, float]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    # Índice 3: sector -> set de sensores
    sensores_sector: dict[str, set[str]] = defaultdict(set)

    with open(ruta_datos, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            partes = linea.split("|")
            if len(partes) != 5:
                continue

            ts, sensor, tipo, valor_str, sector = partes

            # Filtrar tipos no reconocidos
            if tipo not in RANGOS:
                continue

            # Parsear valor
            try:
                valor = float(valor_str)
            except ValueError:
                continue

            # Filtrar por rango válido
            lo, hi = RANGOS[tipo]
            if valor < lo or valor > hi:
                continue

            valor_t = truncar(valor)

            por_sector[sector][tipo].append((ts, valor_t))
            por_sensor[sensor][tipo].append((ts, valor_t))
            sensores_sector[sector].add(sensor)

    # Ordenar todas las listas por timestamp (son strings ISO 8601, orden lexicográfico = orden cronológico)
    for sector_data in por_sector.values():
        for tipo_lista in sector_data.values():
            tipo_lista.sort(key=lambda x: x[0])

    for sensor_data in por_sensor.values():
        for tipo_lista in sensor_data.values():
            tipo_lista.sort(key=lambda x: x[0])

    # Convertir sets a listas ordenadas numéricamente para SENSORES_SECTOR
    sensores_ordenados: dict[str, list[str]] = {}
    for sector, sensores in sensores_sector.items():
        sensores_ordenados[sector] = sorted(sensores, key=lambda s: int(s[1:]))

    # Empaquetar en una sola estructura
    datos: dict[str, Any] = {
        "por_sector": dict(por_sector),
        "por_sensor": dict(por_sensor),
        "sensores_sector": sensores_ordenados,
    }

    with open("datos.bin", "wb") as f_out:
        pickle.dump(datos, f_out, protocol=pickle.HIGHEST_PROTOCOL)

    print("Preprocesamiento completado → datos.bin")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python procesar.py datos.txt")
        sys.exit(1)
    procesar(sys.argv[1])