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

# %%
plt.figure(figsize=(9, 7))

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
plt.show()
