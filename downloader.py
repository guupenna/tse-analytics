# %%
import requests
import os
import http
import argparse

from rich.progress import track

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-ch-ua": '"Chromium";v="126", "Not.A/Brand";v="24", "Google Chrome";v="126"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}

DATA_PATH = './data'

class DownloadTSE:

    def __init__(self):
        if not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)


    def download_candidatos(self, ano: int, base_path:str = DATA_PATH):

        url = f"https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_cand/consulta_cand_{ano}.zip"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == http.HTTPStatus.OK:
            path = os.path.join(base_path, f"consulta_cand_{ano}.zip")
            with open(path, "wb") as f:
                f.write(response.content)
            print(f"Arquivo consulta_cand_{ano}.zip baixado com sucesso.")
            return True

        print(f"Falha ao baixar arquivo consulta_cand_{ano}.zip. Status code: {response.status_code}")
        return False


    def download_bens_candidatos(self, ano: int, base_path:str = DATA_PATH):
        url = f"https://cdn.tse.jus.br/estatistica/sead/odsele/bem_candidato/bem_candidato_{ano}.zip"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == http.HTTPStatus.OK:
            path = os.path.join(base_path, f"bem_candidato_{ano}.zip")
            with open(path, "wb") as f:
                f.write(response.content)
            print(f"Arquivo bem_candidato_{ano}.zip baixado com sucesso.")
            return True

        print(f"Falha ao baixar arquivo bem_candidato_{ano}.zip. Status code: {response.status_code}")
        return False


    def download_coligacoes(self, ano: int, base_path:str = DATA_PATH):
            url = f"https://cdn.tse.jus.br/estatistica/sead/odsele/consulta_coligacao/consulta_coligacao_{ano}.zip"
            response = requests.get(url, headers=HEADERS)
    
            if response.status_code == http.HTTPStatus.OK:
                path = os.path.join(base_path, f"consulta_coligacao_{ano}.zip")
                with open(path, "wb") as f:
                    f.write(response.content)
                print(f"Arquivo consulta_coligacao_{ano}.zip baixado com sucesso.")
                return True
    
            print(f"Falha ao baixar arquivo consulta_coligacao_{ano}.zip. Status code: {response.status_code}")
            return False


    def download_motivo_cassacao(self, ano: int, base_path:str = DATA_PATH):
        url = f"https://cdn.tse.jus.br/estatistica/sead/odsele/motivo_cassacao/motivo_cassacao_{ano}.zip"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == http.HTTPStatus.OK:
            path = os.path.join(base_path, f"motivo_cassacao_{ano}.zip")
            with open(path, "wb") as f:
                f.write(response.content)
            print(f"Arquivo motivo_cassacao_{ano}.zip baixado com sucesso.")
            return True

        print(f"Falha ao baixar arquivo motivo_cassacao_{ano}.zip. Status code: {response.status_code}")
        return False


    def download_votacao_candidato_munzona(self, ano: int, base_path:str = DATA_PATH):
        url = f"https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_candidato_munzona/votacao_candidato_munzona_{ano}.zip"
        response = requests.get(url, headers=HEADERS)

        if response.status_code == http.HTTPStatus.OK:
            path = os.path.join(base_path, f"votacao_candidato_munzona_{ano}.zip")            
            with open(path, "wb") as f:
                f.write(response.content)
            print(f"Arquivo votacao_candidato_munzona_{ano}.zip baixado com sucesso.")
            return True

        print(f"Falha ao baixar arquivo votacao_candidato_munzona_{ano}.zip. Status code: {response.status_code}")
        return False


    def download_por_ano(self, ano:int):

        if not os.path.exists(os.path.join(DATA_PATH, str(ano))):
            os.makedirs(os.path.join(DATA_PATH, str(ano)))

        self.download_candidatos(ano, os.path.join(DATA_PATH, str(ano)))
        self.download_bens_candidatos(ano, os.path.join(DATA_PATH, str(ano)))
        self.download_coligacoes(ano, os.path.join(DATA_PATH, str(ano)))
        self.download_motivo_cassacao(ano, os.path.join(DATA_PATH, str(ano)))
        self.download_votacao_candidato_munzona(ano, os.path.join(DATA_PATH, str(ano)))


    def download_por_anos(self, anos:list):
        for ano in track(anos, description="Baixando dados dos anos..."):
            self.download_por_ano(ano)


# %%
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Baixar dados do TSE")
    parser.add_argument("--inicio", "-i", type=int, help="Primeiro ano a ser baixado")
    parser.add_argument("--fim", "-f", type=int, help="Último ano a ser baixado")
    parser.add_argument("--intervalo", type=int, default=2, help="Interavalo entre os anos a serem baixados")
    args= parser.parse_args()

    downloader = DownloadTSE()
    downloader.download_por_anos(range(args.inicio, args.fim + 1, args.intervalo))