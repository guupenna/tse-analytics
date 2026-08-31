import argparse

from downloader import DownloadTSE
from extract import ExtractFromZip


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Baixar dados do TSE")
    parser.add_argument("--inicio", "-i", type=int, help="Primeiro ano a ser baixado")
    parser.add_argument("--fim", "-f", type=int, help="Último ano a ser baixado")
    parser.add_argument("--intervalo", type=int, default=2, help="Interavalo entre os anos a serem baixados")
    args= parser.parse_args()

    downloader = DownloadTSE()
    downloader.download_por_anos(range(args.inicio, args.fim + 1, args.intervalo))

    extractor = ExtractFromZip()
    extractor.extract_por_anos(range(args.inicio, args.fim + 1, args.intervalo))