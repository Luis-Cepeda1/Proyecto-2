import sys
import pickle
import bisect
import math
from typing import Any


def truncar(valor: float) -> str:
    """Trunca a 1 decimal y devuelve string con exactamente 1 decimal."""
    t = int(valor * 10) / 10
    return f"{t:.1f}"


# ────────────────────────────────────────────────────────────────
# Helpers de búsqueda binaria sobre listas (ts, valor) ordenadas por ts
# ────────────────────────────────────────────────────────────────

class _KeyWrapper:
    """Permite usar bisect sobre lista de tuplas comparando solo el primer elemento."""
    __slots__ = ("lst",)

    def __init__(self, lst: list[tuple[str, float]]) -> None:
        self.lst = lst

    def __getitem__(self, idx: int) -> str:
        return self.lst[idx][0]

    def __len__(self) -> int:
        return len(self.lst)


def indice_izq(lista: list[tuple[str, float]], ts: str) -> int:
    """Primer índice con timestamp >= ts."""
    return bisect.bisect_left(_KeyWrapper(lista), ts)


def indice_der(lista: list[tuple[str, float]], ts: str) -> int:
    """Primer índice con timestamp > ts."""
    return bisect.bisect_right(_KeyWrapper(lista), ts)


# ────────────────────────────────────────────────────────────────
# Implementación de cada tipo de consulta
# ────────────────────────────────────────────────────────────────

def max_vib_rango(
    por_sector: dict[str, dict[str, list[tuple[str, float]]]],
    sector: str,
    ts_ini: str,
    ts_fin: str,
) -> str:
    sector_data = por_sector.get(sector)
    if not sector_data:
        return "NODATA"
    lista = sector_data.get("VIB")
    if not lista:
        return "NODATA"
    lo = indice_izq(lista, ts_ini)
    hi = indice_der(lista, ts_fin)
    if lo >= hi:
        return "NODATA"
    maximo = max(v for _, v in lista[lo:hi])
    return truncar(maximo)


def prom_temp(
    por_sector: dict[str, dict[str, list[tuple[str, float]]]],
    sector: str,
    fecha: str,
) -> str:
    # Rango del día: fecha + "T00:00:00" a fecha + "T23:59:59"
    ts_ini = fecha + "T00:00:00"
    ts_fin = fecha + "T23:59:59"
    sector_data = por_sector.get(sector)
    if not sector_data:
        return "NODATA"
    lista = sector_data.get("TEMP")
    if not lista:
        return "NODATA"
    lo = indice_izq(lista, ts_ini)
    hi = indice_der(lista, ts_fin)
    if lo >= hi:
        return "NODATA"
    valores = [v for _, v in lista[lo:hi]]
    prom = sum(valores) / len(valores)
    return truncar(prom)


def picos_vib(
    por_sensor: dict[str, dict[str, list[tuple[str, float]]]],
    sensor: str,
    umbral: float,
) -> str:
    sensor_data = por_sensor.get(sensor)
    if not sensor_data:
        return "NODATA"
    lista = sensor_data.get("VIB")
    if not lista:
        return "NODATA"
    picos = [ts for ts, v in lista if v > umbral]
    if not picos:
        return "NONE"
    return ",".join(picos)


def rango_temp_ts(
    por_sector: dict[str, dict[str, list[tuple[str, float]]]],
    sector: str,
    ts_ini: str,
    ts_fin: str,
) -> str:
    sector_data = por_sector.get(sector)
    if not sector_data:
        return "NODATA"
    lista = sector_data.get("TEMP")
    if not lista:
        return "NODATA"
    lo = indice_izq(lista, ts_ini)
    hi = indice_der(lista, ts_fin)
    if lo >= hi:
        return "NODATA"
    valores = [v for _, v in lista[lo:hi]]
    minimo = min(valores)
    maximo = max(valores)
    prom = sum(valores) / len(valores)
    return f"{truncar(minimo)},{truncar(maximo)},{truncar(prom)}"


def sensores_sector(
    sensores_sector_idx: dict[str, list[str]],
    sector: str,
) -> str:
    sensores = sensores_sector_idx.get(sector)
    if not sensores:
        return "NODATA"
    return ",".join(sensores)


def siguiente_medicion(
    por_sensor: dict[str, dict[str, list[tuple[str, float]]]],
    sensor: str,
    tipo: str,
    ts: str,
) -> str:
    sensor_data = por_sensor.get(sensor)
    if not sensor_data:
        return "NODATA"
    lista = sensor_data.get(tipo)
    if not lista:
        return "NODATA"
    # Buscar primer elemento estrictamente posterior a ts
    idx = indice_der(lista, ts)
    if idx >= len(lista):
        return "NONE"
    ts_sig, val_sig = lista[idx]
    return f"{ts_sig},{truncar(val_sig)}"


# ────────────────────────────────────────────────────────────────
# Procesamiento principal
# ────────────────────────────────────────────────────────────────

HANDLERS: dict[str, Any] = {
    "MAX_VIB_RANGO": max_vib_rango,
    "PROM_TEMP": prom_temp,
    "PICOS_VIB": picos_vib,
    "RANGO_TEMP_TS": rango_temp_ts,
    "SENSORES_SECTOR": sensores_sector,
    "SIGUIENTE_MEDICION": siguiente_medicion,
}


def procesar_consultas(ruta_consultas: str, ruta_resultados: str) -> None:
    # Cargar estructura serializada
    with open("datos.bin", "rb") as f:
        datos = pickle.load(f)

    por_sector: dict[str, dict[str, list[tuple[str, float]]]] = datos["por_sector"]
    por_sensor: dict[str, dict[str, list[tuple[str, float]]]] = datos["por_sensor"]
    sensores_idx: dict[str, list[str]] = datos["sensores_sector"]

    resultados: list[str] = []

    with open(ruta_consultas, "r", encoding="utf-8") as f_consultas:
        for linea in f_consultas:
            linea = linea.strip()
            if not linea:
                resultados.append("")
                continue

            partes = linea.split()
            tipo_consulta = partes[0]

            try:
                if tipo_consulta == "MAX_VIB_RANGO":
                    # MAX_VIB_RANGO <sector> <ts_ini> <ts_fin>
                    resp = max_vib_rango(por_sector, partes[1], partes[2], partes[3])

                elif tipo_consulta == "PROM_TEMP":
                    # PROM_TEMP <sector> <fecha>
                    resp = prom_temp(por_sector, partes[1], partes[2])

                elif tipo_consulta == "PICOS_VIB":
                    # PICOS_VIB <sensor> <umbral>
                    resp = picos_vib(por_sensor, partes[1], float(partes[2]))

                elif tipo_consulta == "RANGO_TEMP_TS":
                    # RANGO_TEMP_TS <sector> <ts_ini> <ts_fin>
                    resp = rango_temp_ts(por_sector, partes[1], partes[2], partes[3])

                elif tipo_consulta == "SENSORES_SECTOR":
                    # SENSORES_SECTOR <sector>
                    resp = sensores_sector(sensores_idx, partes[1])

                elif tipo_consulta == "SIGUIENTE_MEDICION":
                    # SIGUIENTE_MEDICION <sensor> <tipo> <timestamp>
                    resp = siguiente_medicion(por_sensor, partes[1], partes[2], partes[3])

                else:
                    resp = "NODATA"

            except (IndexError, ValueError):
                resp = "NODATA"

            resultados.append(resp)

    with open(ruta_resultados, "w", encoding="utf-8") as f_out:
        f_out.write("\n".join(resultados) + "\n")

    print(f"Consultas procesadas → {ruta_resultados}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python consultas.py consultas.txt resultados.txt")
        sys.exit(1)
    procesar_consultas(sys.argv[1], sys.argv[2])