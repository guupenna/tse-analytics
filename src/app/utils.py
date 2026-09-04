import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
from sklearn.cluster import KMeans

METRICAS = {
    "txGeneroFeminino": ("Candidaturas de mulheres", "totalGeneroFeminino"),
    "txCorRacaPreta": ("Candidaturas de pessoas pretas", "totalCorRacaPreta"),
    "txCorRacaNaoBranca": ("Candidaturas de pessoas não brancas", "totalCorRacaNaoBranca"),
}

TINTA = "#1d2433"
SUAVE = "#8b95a7"
PONTO = "#2a6f97"
DESTAQUE = "#c1666b"
MALHA = "#e4e8ef"


def taxa(data, metrica):
    total = data["totalCandidatos"].sum()
    if total == 0:
        return float("nan")
    return data[METRICAS[metrica][1]].sum() / total


def make_scatterplot(data, x, y, estado="BR", cargo="GERAL", size=False, cluster=False):
    tx_x, tx_y = taxa(data, x), taxa(data, y)

    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    config = {
        "data": data,
        "x": x,
        "y": y,
        "size": "totalCandidatos",
        "sizes": (25, 450),
        "hue": "cluster",
        "palette": "viridis",
        "color": PONTO,
        "alpha": 0.75,
        "linewidth": 0.8,
        "edgecolor": "white",
        "legend": False,
        "ax": ax,
    }

    if not cluster:
        del config["hue"]
        del config["palette"]
    else:
        del config["color"]

    if not size:
        del config["size"]
        del config["sizes"]
        config["s"] = 110

    sns.scatterplot(**config)

    ax.axhspan(ax.get_ylim()[0], tx_y, xmin=0, xmax=1, color=SUAVE, alpha=0.05, zorder=0)

    texts = [
        ax.text(row[x], row[y], row["SG_PARTIDO"],
                fontsize=9, color=TINTA, zorder=5)
        for _, row in data.iterrows()
    ]

    ax.axhline(y=tx_y, color=TINTA, alpha=0.55, linestyle=(0, (6, 4)), linewidth=1.2,
               label=f"{METRICAS[y][0]} ({estado}): {tx_y:.1%}")
    ax.axvline(x=tx_x, color=DESTAQUE, alpha=0.75, linestyle=(0, (6, 4)), linewidth=1.2,
               label=f"{METRICAS[x][0]} ({estado}): {tx_x:.1%}")

    ax.set_xlabel(METRICAS[x][0], fontsize=11, color=SUAVE, labelpad=12)
    ax.set_ylabel(METRICAS[y][0], fontsize=11, color=SUAVE, labelpad=12)
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")

    ax.grid(True, color=MALHA, linewidth=0.9)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(MALHA)
    ax.tick_params(colors=SUAVE, labelsize=10, length=0)

    legenda = ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13),
                        ncol=2, frameon=False, fontsize=9.5)
    for texto in legenda.get_texts():
        texto.set_color(TINTA)

    fig.tight_layout()

    adjust_text(texts, ax=ax,
                arrowprops=dict(arrowstyle="-", color=SUAVE, lw=0.7, alpha=0.8))

    plt.close(fig)
    return fig


def make_clusters(data, n=6):
    n = min(n, len(data))
    model = KMeans(n_clusters=n, random_state=42, n_init=10)
    data = data.copy()
    data["cluster"] = model.fit_predict(data[["txGeneroFeminino", "txCorRacaPreta"]])
    return data
