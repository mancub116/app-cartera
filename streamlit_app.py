
# streamlit_app.py
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime

st.set_page_config(page_title="Análisis de Acciones", layout="centered")
st.title("📈 Calculadora de Rentabilidad y Volatilidad")

st.write("Introduce los tickers (símbolos) de las acciones separados por comas (ej. AAPL, TSLA, MSFT)")

tickers_input = st.text_input("Tickers", "AAPL, MSFT, TSLA")

if tickers_input:
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(",")]

    end_date = datetime.datetime.today()
    start_date = end_date - datetime.timedelta(days=365)

    data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]

    if len(tickers) == 1:
        data = data.to_frame()

    st.subheader("Resultados")

    results = []
    for ticker in tickers:
        prices = data[ticker].dropna()

        if len(prices) < 60:
            st.warning(f"No hay suficientes datos para {ticker}")
            continue

        # Rentabilidades
        ret_1m = (prices[-1] - prices[-21]) / prices[-21] * 100
        ret_6m = (prices[-1] - prices[-126]) / prices[-126] * 100
        ret_1y = (prices[-1] - prices[0]) / prices[0] * 100

        # Volatilidad (desviación estándar anualizada)
        daily_returns = prices.pct_change().dropna()
        vol = np.std(daily_returns) * np.sqrt(252) * 100

        results.append({
            "Activo": ticker,
            "Rentabilidad 1M": f"{ret_1m:.2f}%",
            "Rentabilidad 6M": f"{ret_6m:.2f}%",
            "Rentabilidad 1A": f"{ret_1y:.2f}%",
            "Volatilidad Anualizada": f"{vol:.2f}%"
        })

    if results:
        st.dataframe(pd.DataFrame(results))

        st.subheader("📉 Evolución de precios")
        st.line_chart(data)
