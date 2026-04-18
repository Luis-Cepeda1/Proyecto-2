import sys
import pickle
from bisect import bisect_left, bisect_right
from typing import Any


def truncar_str_1_decimal(valor: float) -> str:
    truncado = int(valor * 10) / 10
    return f"{truncado:.1f}"


def cargar_datos() -> dict[str, Any]:
    with open("datos_serializados.pkl", "rb") as archivo:
        return pickle.load(archivo)


def resolver_max_vib_rango(datos: dict[str, Any], sector: str, ts_ini: str, ts_fin: str) -> str:
    sector_tipo = datos["sector_tipo"]
    if sector not in sector_tipo or "VIB" not in sector_tipo[sector]:
        return "NODATA"

    timestamps = sector_tipo[sector]["VIB"]["timestamps"]
    values = sector_tipo[sector]["VIB"]["values"]

    i = bisect_left(timestamps, ts_ini)
    j = bisect_right(timestamps, ts_fin)

    if i == j:
        return "NODATA"

    return truncar_str_1_decimal(max(values[i:j]))


def resolver_prom_temp(datos: dict[str, Any], sector: str, fecha: str) -> str:
    sector_fecha_temp = datos["sector_fecha_temp"]
    if sector not in sector_fecha_temp or fecha not in sector_fecha_temp[sector]:
        return "NODATA"

    suma = sector_fecha_temp[sector][fecha]["sum"]
    count = sector_fecha_temp[sector][fecha]["count"]

    if count == 0:
        return "NODATA"

    return truncar_str_1_decimal(suma / count)


def resolver_picos_vib(datos: dict[str, Any], sensor: str, umbral: float) -> str:
    sensor_tipo = datos["sensor_tipo"]
    if sensor not in sensor_tipo or "VIB" not in sensor_tipo[sensor]:
        return "NODATA"

    timestamps = sensor_tipo[sensor]["VIB"]["timestamps"]
    values = sensor_tipo[sensor]["VIB"]["values"]

    respuesta = [timestamps[i] for i in range(len(values)) if values[i] > umbral]

    if not respuesta:
        return "NONE"

    return ",".join(respuesta)


def resolver_rango_temp_ts(datos: dict[str, Any], sector: str, ts_ini: str, ts_fin: str) -> str:
    sector_tipo = datos["sector_tipo"]
    if sector not in sector_tipo or "TEMP" not in sector_tipo[sector]:
        return "NODATA"

    timestamps = sector_tipo[sector]["TEMP"]["timestamps"]
    values = sector_tipo[sector]["TEMP"]["values"]

    i = bisect_left(timestamps, ts_ini)
    j = bisect_right(timestamps, ts_fin)

    if i == j:
        return "NODATA"

    sub = values[i:j]
    minimo = min(sub)
    maximo = max(sub)
    promedio = sum(sub) / len(sub)

    return f"{truncar_str_1_decimal(minimo)},{truncar_str_1_decimal(maximo)},{truncar_str_1_decimal(promedio)}"


def resolver_sensores_sector(datos: dict[str, Any], sector: str) -> str:
    sector_sensores = datos["sector_sensores"]
    if sector not in sector_sensores or not sector_sensores[sector]:
        return "NODATA"

    return ",".join(sector_sensores[sector])


def resolver_siguiente_medicion(datos: dict[str, Any], sensor: str, tipo: str, timestamp: str) -> str:
    sensor_tipo = datos["sensor_tipo"]
    if sensor not in sensor_tipo or tipo not in sensor_tipo[sensor]:
        return "NODATA"

    timestamps = sensor_tipo[sensor][tipo]["timestamps"]
    values = sensor_tipo[sensor][tipo]["values"]

    i = bisect_right(timestamps, timestamp)

    if i >= len(timestamps):
        return "NONE"

    return f"{timestamps[i]},{truncar_str_1_decimal(values[i])}"


def resolver_consulta(datos: dict[str, Any], consulta: str) -> str:
    partes = consulta.strip().split()
    tipo = partes[0]

    if tipo == "MAX_VIB_RANGO":
        return resolver_max_vib_rango(datos, partes[1], partes[2], partes[3])

    if tipo == "PROM_TEMP":
        return resolver_prom_temp(datos, partes[1], partes[2])

    if tipo == "PICOS_VIB":
        return resolver_picos_vib(datos, partes[1], float(partes[2]))

    if tipo == "RANGO_TEMP_TS":
        return resolver_rango_temp_ts(datos, partes[1], partes[2], partes[3])

    if tipo == "SENSORES_SECTOR":
        return resolver_sensores_sector(datos, partes[1])

    if tipo == "SIGUIENTE_MEDICION":
        return resolver_siguiente_medicion(datos, partes[1], partes[2], partes[3])

    return "NODATA"


def main() -> None:
    if len(sys.argv) != 3:
        print("Uso: python consultas.py consultas.txt resultados.txt")
        sys.exit(1)

    archivo_consultas = sys.argv[1]
    archivo_resultados = sys.argv[2]

    datos = cargar_datos()

    respuestas: list[str] = []
    with open(archivo_consultas, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            respuestas.append(resolver_consulta(datos, linea))

    with open(archivo_resultados, "w", encoding="utf-8") as archivo:
        for respuesta in respuestas:
            archivo.write(respuesta + "\n")


if __name__ == "__main__":
    main()
    