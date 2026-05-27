import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Dashboard Energetico", layout="wide")

diretorio = os.path.dirname(os.path.abspath(__file__))
caminho = os.path.join(diretorio, 'simulacao_producao_energia_brasil.csv')

@st.cache_data
def carregar_dados(c):
    if not os.path.exists(c):
        st.error(f"Arquivo nao encontrado: {c}")
        return None
    dados = pd.read_csv(c)
    dados['data'] = pd.to_datetime(dados['data'])
    dados['eficiencia'] = (dados['producao_mwh'] / dados['capacidade_instalada']) * 100
    dados['tipo'] = dados['percentual_renovavel'].apply(lambda x: 'Renovavel' if x > 50 else 'Fossil')
    return dados

df = carregar_dados(caminho)

if df is not None:
    st.title("⚡ Matriz Energetica Brasileira")
    st.sidebar.header("Filtros")
    reg = st.sidebar.multiselect("Regiao", options=df['regiao'].unique(), default=df['regiao'].unique())
    fnt = st.sidebar.multiselect("Fonte", options=df['fonte_energia'].unique(), default=df['fonte_energia'].unique())
    
    df_f = df[(df['regiao'].isin(reg)) & (df['fonte_energia'].isin(fnt))]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Producao Total", f"{df_f['producao_mwh'].sum()/1e6:.2f} GWh")
    c2.metric("Custo Medio", f"R$ {df_f['custo_medio_mwh'].mean():.2f}")
    c3.metric("Emissoes", f"{df_f['emissao_co2'].sum()/1e3:.2f}k Ton")
    
    st.plotly_chart(px.line(df_f, x='data', y='producao_mwh', color='tipo'), use_container_width=True)
    st.plotly_chart(px.bar(df_f, x='uf', y='producao_mwh', color='fonte_energia'), use_container_width=True)
    st.subheader("Dados")
    st.dataframe(df_f.head(50))