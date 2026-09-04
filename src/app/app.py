# %%
import pandas as pd
import streamlit as st
import os

from utils import make_scatterplot, make_clusters

app_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(app_path)
base_path = os.path.dirname(src_path)
data_path = os.path.join(base_path, "data")

parquet_path = os.path.join(data_path, "data_partidos.parquet")


@st.cache_data(ttl=60*60*24)
def create_df(mtime):
    return pd.read_parquet(parquet_path)

# %%

df = create_df(os.path.getmtime(parquet_path))

text = """
# Análise de dados abertos do TSE das Eleições de 2024
"""
st.markdown(text)

uf_options = df["SG_UF"].unique().tolist()
uf_options.remove("BR")
uf_options = ["BR"] + uf_options

cargo_options = df["DS_CARGO"].unique().tolist()
cargo_options.remove("GERAL")
cargo_options = ["GERAL"] + cargo_options

estado = st.sidebar.selectbox(label="Estado", placeholder="Selecione o estado para filtro", options=uf_options)
cargo = st.sidebar.selectbox(label="Cargo", options=cargo_options)
size = st.sidebar.checkbox(label="Tamanho dos partidos")
cluster = st.sidebar.checkbox(label="Definir cluster")

data = df[(df["SG_UF"] == estado) & (df["DS_CARGO"] == cargo)]

if cluster:
    data = make_clusters(data)

fig = make_scatterplot(data, estado, cargo, size, cluster)
st.pyplot(fig)