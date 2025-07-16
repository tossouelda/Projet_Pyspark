import os
import requests

def download_taxi(year: int, month: int, output_dir: str = None):
    if output_dir is None:
        output_dir = os.path.join("/opt/airflow/data", "yellow_taxi")

    os.makedirs(output_dir, exist_ok=True)

    file_name = f"yellow_tripdata_{year}-{month:02d}.parquet"
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{file_name}"
    output_path = os.path.join(output_dir, file_name)

    print(f"\nTéléchargement : {url}")
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"Fichier sauvegardé : {output_path}\n")
    else:
        print(f"Erreur téléchargement ({response.status_code}) : {url}\n")

if __name__ == "__main__":
    # Ex : Télécharger janvier 2023
    download_taxi(2023, 1)

