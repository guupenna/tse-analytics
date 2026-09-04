import os

import pandas as pd
import streamlit as st

from utils import METRICAS, make_clusters, make_scatterplot

app_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.dirname(app_path)
base_path = os.path.dirname(src_path)
data_path = os.path.join(base_path, "data")
parquet_path = os.path.join(data_path, "data_partidos.parquet")

st.set_page_config(page_title="Perfil das candidaturas - TSE 2024", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 2.5rem; max-width: 1400px; }
    h1 { font-size: 2.1rem !important; font-weight: 700; letter-spacing: -0.02em;
         margin-bottom: 0.2rem; }
    .subtitulo { color: #6b7280; font-size: 1.02rem; margin-bottom: 1.8rem; }
    .rodape { color: #9aa2b1; font-size: 0.82rem; border-top: 1px solid #e4e8ef;
              padding-top: 1rem; margin-top: 2.5rem; }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=60 * 60 * 24)
def create_df(mtime):
    return pd.read_parquet(parquet_path)


df = create_df(os.path.getmtime(parquet_path))

st.markdown("# Quem se candidatou em 2024")
st.markdown('<p class="subtitulo">Perfil de gênero e cor/raça das candidaturas '
            'por partido, a partir dos dados abertos do TSE.</p>',
            unsafe_allow_html=True)

uf_options = ["BR"] + sorted(u for u in df["SG_UF"].unique() if u != "BR")
cargo_options = ["GERAL"] + sorted(c for c in df["DS_CARGO"].unique() if c != "GERAL")
metrica_options = list(METRICAS)


def rotulo(m):
    return METRICAS[m][0]


with st.container(border=True):
    c1, c2, c3, c4 = st.columns([1, 1.4, 1.7, 1.7])
    estado = c1.selectbox("Estado", uf_options,
                          help="BR agrega todas as unidades da federação.")
    cargo = c2.selectbox("Cargo", cargo_options,
                         help="GERAL soma os três cargos em disputa.")
    x = c3.selectbox("Eixo horizontal", metrica_options,
                     format_func=rotulo, index=0)
    y = c4.selectbox("Eixo vertical", metrica_options,
                     format_func=rotulo, index=1)

    t1, t2, _ = st.columns([1.2, 1.2, 3])
    size = t1.toggle("Dimensionar por volume",
                     help="O tamanho da bolha reflete o número de candidaturas.")
    cluster = t2.toggle("Agrupar por perfil",
                        help="Agrupa partidos com perfis semelhantes.")

data = df[(df["SG_UF"] == estado) & (df["DS_CARGO"] == cargo)]

if data.empty:
    st.warning(f"Não há candidaturas de {cargo.lower()} em {estado}.")
    st.stop()

if cluster:
    data = make_clusters(data)

col_grafico, col_leitura = st.columns([3, 1], gap="large")

with col_grafico:
    st.pyplot(make_scatterplot(data, x, y, estado, cargo, size, cluster))

with col_leitura:
    st.markdown("#### Como ler")
    st.markdown(
        f"Cada ponto é um partido. As linhas tracejadas marcam a taxa do "
        f"recorte selecionado (**{estado} - {cargo.lower()}**), então elas se "
        f"movem quando você troca o filtro.\n\n"
        f"Partidos no **canto inferior esquerdo** ficam abaixo da média nos "
        f"dois indicadores e partidos no **superior direito**, acima nos dois."
    )
    if size:
        st.info("Bolhas maiores = mais candidaturas.", icon="⬤")
    if cluster:
        st.info("Cores agrupam partidos de perfil semelhante.", icon="◆")

st.markdown('<p class="rodape">Dados: Tribunal Superior Eleitoral', unsafe_allow_html=True)
