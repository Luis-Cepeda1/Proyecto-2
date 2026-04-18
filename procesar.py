import sys
import pickle
from collections import defaultdict
from typing import Any


def truncar_1_decimal(valor: float) -> float:
    return int(valor * 10) / 10


def es_registro_valido(tipo: str, valor: float) -> bool:
    if tipo == "VIB":
        return 0.0 <= valor <= 50.0
    if tipo == "TEMP":
        return -10.0 <= valor <= 60.0
    return False

def convertir_a_dict(obj: Any) -> Any:
    if isinstance(obj, defaultdict):
        obj = dict(obj)
    if isinstance(obj, dict):
        return {k: convertir_a_dict(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [convertir_a_dict(x) for x in obj]
    if isinstance(obj, set):
        return sorted(obj, key=lambda s: int(s[1:]))
    return obj

def main() -> None:
    if len(sys.argv) != 2:
        print("Uso: python procesar.py datos.txt")
        sys.exit(1)

    archivo_entrada = sys.argv[1]

    sector_tipo: dict[str, dict[str, dict[str, list[Any]]]] = defaultdict(
        lambda: defaultdict(lambda: {"timestamps": [], "values": []})
    )
    sensor_tipo: dict[str, dict[str, dict[str, list[Any]]]] = defaultdict(
        lambda: defaultdict(lambda: {"timestamps": [], "values": []})
    )
    sector_sensores: dict[str, set[str]] = defaultdict(set)
    sector_fecha_temp: dict[str, dict[str, dict[str, float]]] = defaultdict(
        lambda: defaultdict(lambda: {"sum": 0.0, "count": 0.0})
    )

    with open(archivo_entrada, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue

            timestamp, sensor_id, tipo, valor_str, sector = linea.split("|")

            if tipo not in {"VIB", "TEMP"}:
                continue

            valor = float(valor_str)
            if not es_registro_valido(tipo, valor):
                continue

            sector_tipo[sector][tipo]["timestamps"].append(timestamp)
            sector_tipo[sector][tipo]["values"].append(valor)

            sensor_tipo[sensor_id][tipo]["timestamps"].append(timestamp)
            sensor_tipo[sensor_id][tipo]["values"].append(valor)

            sector_sensores[sector].add(sensor_id)

            if tipo == "TEMP":
                fecha = timestamp[:10]
                sector_fecha_temp[sector][fecha]["sum"] += valor
                sector_fecha_temp[sector][fecha]["count"] += 1.0

    # ordenar listas por timestamp
    for sector in sector_tipo:
        for tipo in sector_tipo[sector]:
            pares = list(zip(
                sector_tipo[sector][tipo]["timestamps"],
                sector_tipo[sector][tipo]["values"]
            ))
            pares.sort(key=lambda x: x[0])
            sector_tipo[sector][tipo]["timestamps"] = [p[0] for p in pares]
            sector_tipo[sector][tipo]["values"] = [p[1] for p in pares]

    for sensor in sensor_tipo:
        for tipo in sensor_tipo[sensor]:
            pares = list(zip(
                sensor_tipo[sensor][tipo]["timestamps"],
                sensor_tipo[sensor][tipo]["values"]
            ))
            pares.sort(key=lambda x: x[0])
            sensor_tipo[sensor][tipo]["timestamps"] = [p[0] for p in pares]
            sensor_tipo[sensor][tipo]["values"] = [p[1] for p in pares]

    estructura = {
        "sector_tipo": convertir_a_dict(sector_tipo),
        "sensor_tipo": convertir_a_dict(sensor_tipo),
        "sector_sensores": convertir_a_dict(sector_sensores),
        "sector_fecha_temp": convertir_a_dict(sector_fecha_temp),}

    with open("datos_serializados.pkl", "wb") as archivo_salida:
        pickle.dump(estructura, archivo_salida)


if __name__ == "__main__":
    main()
