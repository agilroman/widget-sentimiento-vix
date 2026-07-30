import pandas as pd

# Cargamos los datos guardados en el paso anterior
datos = pd.read_csv("vix_historico.csv", index_col=0, parse_dates=True)

# Cogemos el último valor de cierre del VIX (el más reciente)
valor_actual = datos["Close"].iloc[-1]

# Calculamos la media móvil de los últimos 20 días (tendencia)
media_movil_20 = datos["Close"].rolling(window=20).mean().iloc[-1]

# Función para clasificar el nivel de sentimiento según el valor del VIX
def clasificar_sentimiento(vix):
    if vix < 15:
        return "Calma"
    elif vix < 20:
        return "Normal"
    elif vix < 30:
        return "Nervioso"
    else:
        return "Pánico"

nivel = clasificar_sentimiento(valor_actual)

# Mostramos el resultado por pantalla
print(f"Valor actual del VIX: {valor_actual:.2f}")
print(f"Media móvil (20 días): {media_movil_20:.2f}")
print(f"Nivel de sentimiento: {nivel}")