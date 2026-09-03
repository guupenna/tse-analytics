# %%
import pandas as pd
import sqlalchemy
import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text

with open("partidos.sql", "r") as open_file:
    query = open_file.read()

engine = sqlalchemy.create_engine("sqlite:///../data/database.db")

df = pd.read_sql_query(query, engine)
df.head()

totalCandidatos = df["totalCandidatos"].sum()

txGeneroFeminino = df["totalGeneroFeminino"].sum() / totalCandidatos
txCorRacaPreta = df["totalCorRacaPreta"].sum() / totalCandidatos
txCorRacaNaoBranca = df["totalCorRacaNaoBranca"].sum() / totalCandidatos

# %%
plt.figure(figsize=(9, 7), dpi=500)

sns.scatterplot(data=df,
                x="txGeneroFemininoBR",
                y="txCorRacaPretaBR",
                s=60)

texts = []
for _, row in df.iterrows():
    texts.append(plt.text(row["txGeneroFemininoBR"],
                          row["txCorRacaPretaBR"],
                          row["SG_PARTIDO"],
                          fontsize=9))

adjust_text(texts, arrowprops=dict(arrowstyle="-", color="gray", lw=0.6))

plt.grid(True, alpha=0.3)
plt.title("Partidos: Cor/Raça vs Gênero - Eleições 2024")
plt.xlabel("Taxa de Pessoas do Gênero Feminino")
plt.ylabel("Taxa de Pessoas Pretas")
plt.axhline(y=txCorRacaPreta,
            color="black",
            alpha=0.6,
            linestyle="--",
            label=f"Taxa nacional Cor/Raça Preta: {txCorRacaPreta:.1%}")
plt.axvline(x=txGeneroFeminino,
            color="tomato",
            alpha=0.6,
            linestyle="--",
            label=f"Taxa nacional Gênero Feminino: {txGeneroFeminino:.1%}")
plt.legend(loc="lower right")
plt.savefig("../img/partidos_cor_raca_genero.png")
plt.show()

# %%
plt.figure(figsize=(9, 7), dpi=500)

sns.scatterplot(data=df,
                x="txGeneroFemininoBR",
                y="txCorRacaPretaBR",
                size="totalCandidatos",
                sizes=(5, 300),
                legend=False)

texts = []
for _, row in df.iterrows():
    texts.append(plt.text(row["txGeneroFemininoBR"],
                          row["txCorRacaPretaBR"],
                          row["SG_PARTIDO"],
                          fontsize=9))

adjust_text(texts, arrowprops=dict(arrowstyle="-", color="gray", lw=0.6))

plt.grid(True, alpha=0.3)
plt.title("Partidos: Cor/Raça vs Gênero - Eleições 2024")
plt.xlabel("Taxa de Pessoas do Gênero Feminino")
plt.ylabel("Taxa de Pessoas Pretas")
plt.axhline(y=txCorRacaPreta,
            color="black",
            alpha=0.6,
            linestyle="--",
            label=f"Taxa nacional Cor/Raça Preta: {txCorRacaPreta:.1%}")
plt.axvline(x=txGeneroFeminino,
            color="tomato",
            alpha=0.6,
            linestyle="--",
            label=f"Taxa nacional Gênero Feminino: {txGeneroFeminino:.1%}")
plt.legend(loc="lower right")
plt.savefig("../img/partidos_cor_raca_genero_bolha_size.png")
plt.show()

# %%
from sklearn import cluster

X = df[["txGeneroFemininoBR", "txCorRacaPretaBR"]]
model = cluster.KMeans(n_clusters=5)
model.fit(X)

df["clusterBR"] = model.labels_
df.groupby(["clusterBR"])["txGeneroFemininoBR"].count()
# %%

plt.figure(figsize=(9, 7), dpi=500)

sns.scatterplot(data=df,
                x="txGeneroFemininoBR",
                y="txCorRacaPretaBR",
                hue="clusterBR",
                palette="viridis",
                s=60,
                size="totalCandidatos",
                sizes=(5, 300),
                alpha=0.6,
                legend=False)

texts = []
for _, row in df.iterrows():
    texts.append(plt.text(row["txGeneroFemininoBR"],
                          row["txCorRacaPretaBR"],
                          row["SG_PARTIDO"],
                          fontsize=9))

adjust_text(texts, arrowprops=dict(arrowstyle="-", color="gray", lw=0.6))

plt.grid(True, alpha=0.3)
plt.suptitle("Partidos: Cor/Raça vs Gênero - Eleições 2024")
plt.title("Maior a bolha, maior a quantidade de partidos", fontdict={"size":9})
plt.xlabel("Taxa de Pessoas do Gênero Feminino")
plt.ylabel("Taxa de Pessoas Pretas")
plt.axhline(y=txCorRacaPreta,
            color="black",
            alpha=0.6,
            linestyle="--",
            label=f"Taxa nacional Cor/Raça Preta: {txCorRacaPreta:.1%}")
plt.axvline(x=txGeneroFeminino,
            color="tomato",
            alpha=0.6,
            linestyle="--",
            label=f"Taxa nacional Gênero Feminino: {txGeneroFeminino:.1%}")
plt.legend(loc="lower right")
plt.savefig("../img/partidos_cluster.png")
plt.show()
