# %%
import zipfile
import os
import argparse

from rich.progress import track

DATA_PATH = './data'

class ExtractFromZip:

    def __init__(self):
        pass

    def extract_zip(self, zip_file_path, extract_to):

        if not os.path.exists(zip_file_path):
            raise FileNotFoundError(f"O arquivo {zip_file_path} não existe.")

        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)


    def extract_por_ano(self, ano):

        folder = f"{DATA_PATH}/{ano}"

        files = [i for i in os.listdir(folder) if i.endswith(".zip")]
        for file in files:
            extract_to = os.path.join(folder, file.replace(".zip", ''))
            zip_file_path = os.path.join(folder, file)
            self.extract_zip(zip_file_path, extract_to)

        print(f"Arquivo do ano {ano} extraído com sucesso.")


    def extract_por_anos(self, anos):

        for ano in track(anos, description="Extraindo arquivos..."):
            self.extract_por_ano(ano)


# %%
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extrair dados")
    parser.add_argument("--inicio", "-i", type=int, help="Primeiro ano a ser extraído")
    parser.add_argument("--fim", "-f", type=int, help="Último ano a ser extraído")
    parser.add_argument("--intervalo", type=int, default=2, help="Interavalo entre os anos a serem extraídos")
    args= parser.parse_args()

    extractor = ExtractFromZip()
    extractor.extract_por_anos(range(args.inicio, args.fim + 1, args.intervalo))