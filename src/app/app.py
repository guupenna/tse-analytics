# %%
import pandas as pd
import sqlalchemy
import streamlit as st
from utils import make_scatterplot, make_clusters

engine = sqlalchemy.create_engine("sqlite:///../../data/database.db")

with open("etl_partidos.sql", "r") as open_file:
    query = open_file.read()

df = pd.read_sql(query, engine)
df.head()

# %%

text = """
# Análise de dados abertos do TSE das Eleições de 2024.
"""
st.markdown(text)

uf_options = df["SG_UF"].unique().tolist()
uf_options.remove("BR")
uf_options = ["BR"] + uf_options

estado = st.sidebar.selectbox(label="Estado", placeholder="Selecione o estado para filtro", options=uf_options)
size = st.sidebar.checkbox(label="Tamanho dos partidos")
cluster = st.sidebar.checkbox(label="Definir cluster")

data = df[df["SG_UF"] == estado]

if cluster:
    data = make_clusters(data)

fig = make_scatterplot(data, estado, size=size, cluster=cluster)
st.pyplot(fig)