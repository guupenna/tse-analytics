import matplotlib.pyplot as plt
import seaborn as sns
from adjustText import adjust_text
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

METRICAS = {
    "txGeneroFeminino": {
        "rotulo": "Candidaturas de pessoas do gênero feminino",
        "coluna": "totalGeneroFeminino",
        "media": True,
        "formato": "percentual",
    },
    "txCorRacaPreta": {
        "rotulo": "Candidaturas de pessoas pretas",
        "coluna": "totalCorRacaPreta",
        "media": True,
        "formato": "percentual",
    },
    "txCorRacaNaoBranca": {
        "rotulo": "Candidaturas de pessoas não brancas",
        "coluna": "totalCorRacaNaoBranca",
        "media": True,
        "formato": "percentual",
    },
    "avgIdade": {
        "rotulo": "Idade média",
        "coluna": "totalIdade",
        "media": True,
        "formato": "anos",
    },
    "avgBens": {
        "rotulo": "Patrimônio por candidatura",
        "coluna": "totalBens",
        "media": True,
        "formato": "reais",
    },
    "avgBensNotZero": {
        "rotulo": "Patrimônio de quem declarou bens",
        "coluna": "totalBensNotZero",
        "denominador": "totalCandidatosNotZero",
        "media": True,
        "formato": "reais",
    },
    "totalBens": {
        "rotulo": "Patrimônio declarado (total)",
        "coluna": "totalBens",
        "media": False,
        "formato": "reais",
    },
}

TINTA = "#1d2433"
SUAVE = "#8b95a7"
PONTO = "#2a6f97"
DESTAQUE = "#c1666b"
MALHA = "#e4e8ef"


def rotulo(metrica):
    return METRICAS[metrica]["rotulo"]


def agregar(data, metrica):
    soma = data[METRICAS[metrica]["coluna"]].sum()
    if not METRICAS[metrica]["media"]:
        return soma
    total = data[METRICAS[metrica].get("denominador", "totalCandidatos")].sum()
    if total == 0:
        return float("nan")
    return soma / total


def formatar(valor, metrica, eixo=False):
    formato = METRICAS[metrica]["formato"]

    if formato == "percentual":
        texto = f"{valor:.0%}" if eixo else f"{valor:.1%}"
    elif formato == "anos":
        texto = f"{valor:.0f}" if eixo else f"{valor:.1f} anos"
    else:
        if abs(valor) >= 1e9:
            valor, unidade = valor / 1e9, " bi"
        elif abs(valor) >= 1e6:
            valor, unidade = valor / 1e6, " mi"
        elif abs(valor) >= 1e3:
            valor, unidade = valor / 1e3, " mil"
        else:
            unidade = ""
        if eixo:
            casas = 1 if 0 < abs(valor) < 10 else 0
        else:
            casas = 1
        texto = f"R$ {valor:.{casas}f}{unidade}"

    return texto.replace(".", ",")


def make_scatterplot(data, x, y, estado="BR", cargo="GERAL", size=False, cluster=False):
    tx_x, tx_y = agregar(data, x), agregar(data, y)

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

    ax.axhspan(ax.get_ylim()[0],
               tx_y,
               xmin=0,
               xmax=1,
               color=SUAVE,
               alpha=0.05,
               zorder=0)

    texts = [
        ax.text(row[x],
                row[y],
                row["SG_PARTIDO"],
                fontsize=9,
                color=TINTA,
                zorder=5)
        for _, row in data.iterrows()
    ]

    ax.axhline(y=tx_y,
               color=TINTA,
               alpha=0.55,
               linestyle=(0, (6, 4)),
               linewidth=1.2,
               label=f"{rotulo(y)} ({estado}): {formatar(tx_y, y)}")
    ax.axvline(x=tx_x,
               color=DESTAQUE,
               alpha=0.75,
               linestyle=(0, (6, 4)),
               linewidth=1.2,
               label=f"{rotulo(x)} ({estado}): {formatar(tx_x, x)}")

    ax.set_xlabel(rotulo(x), fontsize=11, color=SUAVE, labelpad=12)
    ax.set_ylabel(rotulo(y), fontsize=11, color=SUAVE, labelpad=12)
    ax.xaxis.set_major_formatter(lambda v, _: formatar(v, x, eixo=True))
    ax.yaxis.set_major_formatter(lambda v, _: formatar(v, y, eixo=True))

    ax.grid(True, color=MALHA, linewidth=0.9)
    ax.set_axisbelow(True)
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(MALHA)
    ax.tick_params(colors=SUAVE, labelsize=10, length=0)

    legenda = ax.legend(loc="upper center",
                        bbox_to_anchor=(0.5, -0.13),
                        ncol=2,
                        frameon=False,
                        fontsize=9.5)
    for texto in legenda.get_texts():
        texto.set_color(TINTA)

    fig.tight_layout()

    adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle="-", color=SUAVE, lw=0.7, alpha=0.8))

    plt.close(fig)
    return fig


def make_clusters(data, x, y, n=6):
    n = min(n, len(data))
    X = StandardScaler().fit_transform(data[[x, y]])
    model = KMeans(n_clusters=n, random_state=42, n_init=10)
    data = data.copy()
    data["cluster"] = model.fit_predict(X)
    return data
