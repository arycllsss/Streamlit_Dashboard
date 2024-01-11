import folium
import streamlit as st
import pandas as pd
from api.service import get_data
from streamlit_folium import st_folium

st.image('img/ifpi.png', width=150)
st.title('Cruviana Dashboard')
st.subheader('Estação Meteorológica: UAPP IFPI Oeiras')
st.write('---')
dicionario_dados = """
• Datetime: Tempo preciso em que a leitura ocorreu em formato americano.
• id: Identificador único da leitura.
• Data_add: Data em que a leitura ocorreu em formato americano.
• BarTrend: Tendência da pressão para 3h.
• Barometer: Pressão barométrica.
• TempOut: Temperatura do ar em grau em (⁰C).
• WindSpeed: Velocidade do vento em (km/h).
• WindSpeed10Min: Média de velocidade do vento nos últimos 10 minutos em (km/h).
• WindDir: Direção do vento em (⁰).
• HumOut: Umidade relativa do ar em (%).
• RainRate: Volume de chuva por hora (mm).
• SolarRad: Radiação solar em (W/m²).
• RainDay: Volume de chuva acumulado no dia em (mm).
• RainMonth: Volume de chuva acumulado no Mês em (mm).
• RainYear: Volume de chuva acumulado no ano em (mm).
• ETDay: Volume de evapotranspiração acumulado no dia em (mm).
• ETMonth: Volume de evapotranspiração acumulado no mês em (mm).
• ETYear: Volume de evapotranspiração acumulado no ano em (mm).
• RainStorm: Volume de chuva considerada tempestade (mm).
• HeatIndex: Índice de calor em (⁰C).
• WindChill: Sensação térmica considerando vento (⁰C).
• THSWIndex: Sensação térmica considerando umidade, radiação solar, vento e temperatura.
• Station: Identificador da estação meteorológica.
"""
st.subheader('📒 Dicionário de Dados')
st.text(dicionario_dados)
st.write('---')
st.header("🌦️ Leituras")
data = st.date_input('Data')


def load_data():
    df = pd.DataFrame(get_data(data))

    df = df.drop(columns=['Data_add', 'Data', 'WindSpeed',
                          'WindSpeed10Min', 'RainRate', 'ETMonth',
                          'RainStorm', 'Station',
                          ])

    df = df.set_index('id')
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['Datetime'] = df['Datetime'].dt.strftime('%d/%m/%y %H:%M')

    return df


leituras = load_data()
st.write(leituras)
st.write('---')
st.subheader('🌡 Temperatura️')
st.line_chart(data=leituras, x='Datetime', y='TempOut', color='#F00')
st.write(f'Temperatura mínima: {leituras.TempOut.min()} °C')
st.write(f'Temperatura maxima: {leituras.TempOut.max()} °C')
st.write('---')
st.subheader('☀️ Radiação Solar')
st.line_chart(data=leituras, x='Datetime', y='SolarRad', color='#FFA500')
st.write(f'Índise maximo de de Radiação: {leituras.SolarRad.max()} W/m²')
st.write('---')
st.subheader('🌧️ Precipitações')
st.line_chart(data=leituras, x='Datetime', y='RainDay')
st.write(f'Volume total acumulado: {leituras.RainDay.max()} mm')
st.write('---')
st.subheader('🌬︎ Umidade do Ar')
st.line_chart(data=leituras, x='Datetime', y='HumOut', color='#A020F0')
st.write(f'A umiade máxima no ar é de {leituras.HumOut.max()} %')
st.write('---')
st.subheader('🧭 Localização')
m = folium.Map(
    location=[-7.000322480023738, -42.10099404281391],
    zoom_star=20)

folium.Marker(
    [-7.000322480023738, -42.10099404281391],
    popup='Estação Meteorológica UAPP - IFPI',
    tooltip='Estação Meteorológica UAPP - IFPI'
).add_to(m)

mapa = st_folium(m, width=700)
