from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import yfinance as yf

app = FastAPI(title="API Indicador de Sentimiento VIX")

# Permitimos que cualquier página web (nuestro HTML) pueda consultar esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def clasificar_sentimiento(vix):
    if vix < 15:
        return "Calma"
    elif vix < 20:
        return "Normal"
    elif vix < 30:
        return "Nervioso"
    else:
        return "Pánico"

@app.get("/api/sentimiento")
def obtener_sentimiento():
    # Descargamos datos frescos del VIX cada vez que se llama a la API
    vix = yf.Ticker("^VIX")
    datos = vix.history(period="6mo")

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
    vix = yf.Ticker("^VIX")
    datos = vix.history(period="6mo")

    fechas = [str(fecha.date()) for fecha in datos.index]
    valores = [round(float(v), 2) for v in datos["Close"]]

    return {
        "fechas": fechas,
        "valores": valores
    }