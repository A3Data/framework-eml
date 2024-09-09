# src/data/download_data.py
import requests
from pathlib import Path
import typer
from config.settings import RAW_DATA_DIR  # Importa o caminho do diretório raw

app = typer.Typer()


@app.command()
def download(url: str, output_file: str = f"{RAW_DATA_DIR}/data.csv"):
    """
    Faz o download de dados a partir de uma URL e salva no diretório especificado ou no padrão.

    Args:
        url (str): URL dos dados a serem baixados.
        output_file (str): Caminho do arquivo onde os dados serão salvos. Se não fornecido, salva em artifacts/data/raw/.
    """

    response = requests.get(url, timeout=60)
    if response.status_code == 200:
        output_path = Path(output_file)
        output_path.parent.mkdir(
            parents=True, exist_ok=True
        )  # Certifica que o diretório existe
        with open(output_path, "w") as f:
            f.write(response.text)
        typer.echo(f"Dados salvos em: {output_path}")
    else:
        typer.echo(
            f"Falha ao baixar os dados. Status code: {response.status_code}", err=True
        )


if __name__ == "__main__":
    app()
