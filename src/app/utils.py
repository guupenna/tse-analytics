import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
from sklearn.cluster import KMeans

def make_scatterplot(data, estado="BR", cargo="GERAL", size=False, cluster=False):
    txGeneroFeminino = data["totalGeneroFeminino"].sum() / data["totalCandidatos"].sum()
    txCorRacaPreta = data["totalCorRacaPreta"].sum() / data["totalCandidatos"].sum()

    fig, ax = plt.subplots(figsize=(9, 7))

    config = {
        "data": data,
        "x": "txGeneroFeminino",
        "y": "txCorRacaPreta",
        "size": "totalCandidatos",
        "sizes": (5, 300),
        "hue": "cluster",
        "palette": "viridis",
        "alpha": 0.6,
        "legend": False,
        "ax": ax
    }

    if not cluster:
        del config["hue"]

    if not size:
        del config["size"]
        del config["sizes"]

    sns.scatterplot(**config)

    texts = []
    for _, row in data.iterrows():
        texts.append(ax.text(row["txGeneroFeminino"],
                            row["txCorRacaPreta"],
                            row["SG_PARTIDO"],
                            fontsize=9))

    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Taxa de Pessoas do Gênero Feminino")
    ax.set_ylabel("Taxa de Pessoas Pretas")
    ax.axhline(y=txCorRacaPreta,
            color="black",
            alpha=0.6,
            linestyle="--",
            label=f"Taxa {estado} Cor/Raça Preta: {txCorRacaPreta:.1%}")
    ax.axvline(x=txGeneroFeminino,
            color="tomato",
            alpha=0.6,
            linestyle="--",
            label=f"Taxa {estado} Gênero Feminino: {txGeneroFeminino:.1%}")
    ax.legend(loc="lower right")

    fig.suptitle(f"Partidos: Cor/Raça vs Gênero - Eleições 2024 ({estado} · {cargo})")
    if size:
        ax.set_title("Quanto maior a bolha, maior o número de candidaturas", fontsize=9)
    fig.tight_layout()

    adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle="-", color="gray", lw=0.6))

    plt.close(fig)
    return fig


def make_clusters(data, n=6):
    model = KMeans(n_clusters=n, random_state=42)
    model.fit(data[["txGeneroFeminino", "txCorRacaPreta"]])

    data["cluster"] = model.labels_

    return data