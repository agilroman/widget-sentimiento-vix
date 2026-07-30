import yfinance as yf

# Descargamos el histórico del VIX (índice de volatilidad)
vix = yf.Ticker("^VIX")
datos = vix.history(period="6mo")  # últimos 6 meses

# Mostramos las primeras y últimas filas
print(datos.head())
print(datos.tail())

# Guardamos en un CSV para no tener que descargarlo cada vez
datos.to_csv("vix_historico.csv")
print("\n✅ Datos guardados en vix_historico.csv")