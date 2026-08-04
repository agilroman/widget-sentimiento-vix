from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import yfinance as yf
import time

app = FastAPI(title="API Indicador de Sentimiento VIX")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caché en memoria: guardamos los datos y cuándo se pidieron por última vez
cache = {
    "datos": None,
    "ultima_actualizacion": 0
}
DURACION_CACHE = 300  # 5 minutos, en segundos

def clasificar_sentimiento(vix):
    if vix < 15:
        return "Calma"
    elif vix < 20:
        return "Normal"
    elif vix < 30:
        return "Nervioso"
    else:
        return "Pánico"

def obtener_datos_vix():
    """Descarga datos de Yahoo Finance solo si el caché ha caducado."""
    ahora = time.time()
    if cache["datos"] is None or (ahora - cache["ultima_actualizacion"]) > DURACION_CACHE:
        vix = yf.Ticker("^VIX")
        datos = vix.history(period="6mo")
        cache["datos"] = datos
        cache["ultima_actualizacion"] = ahora
    return cache["datos"]

@app.get("/api/sentimiento")
def obtener_sentimiento():
    datos = obtener_datos_vix()

    valor_actual = float(datos["Close"].iloc[-1])
    media_movil_20 = float(datos["Close"].rolling(window=20).mean().iloc[-1])
    nivel = clasificar_sentimiento(valor_actual)

    return {
        "valor_actual": round(valor_actual, 2),
        "media_movil_20d": round(media_movil_20, 2),
        "nivel_sentimiento": nivel,
        "fecha_ultimo_dato": str(datos.index[-1].date())
    }

@app.get("/api/historico")
def obtener_historico():
    datos = obtener_datos_vix()

    fechas = [str(fecha.date()) for fecha in datos.index]
    valores = [round(float(v), 2) for v in datos["Close"]]

    return {
        "fechas": fechas,
        "valores": valores
    }