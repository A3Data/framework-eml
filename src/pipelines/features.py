import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from pathlib import Path
import typer
from config.settings import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()


def load_data(file_path: str) -> pd.DataFrame:
    """
    Carrega o dataset a partir de um arquivo CSV.

    Args:
        file_path (str): Caminho para o arquivo CSV que contém o dataset.

    Returns:
        pd.DataFrame: DataFrame contendo o dataset carregado, com as colunas nomeadas.
    """
    column_names = [
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
        "species",
    ]
    df = pd.read_csv(file_path, header=None, names=column_names)
    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza o pré-processamento do dataset, incluindo codificação das variáveis de alvo,
    escalonamento das features e divisão em conjuntos de treino e teste.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados a serem pré-processados.

    Returns:
        tuple: Dois DataFrames, um para os dados de treino e outro para os dados de teste.
    """
    # Codificar a variável alvo (species)
    label_encoder = LabelEncoder()
    df["species"] = label_encoder.fit_transform(df["species"])

    # Separar as features e a variável alvo
    X = df.drop("species", axis=1)
    y = df["species"]

    # Escalar as features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Combinar as features escaladas com a variável alvo em um DataFrame final
    df_processed = pd.DataFrame(X_scaled, columns=X.columns)
    df_processed["species"] = y.values

    return df_processed


@app.command()
def preprocess(input_file: str = None, output_file: str = None):
    """
    Função principal para o pré-processamento dos dados. Carrega os dados brutos, realiza
    o pré-processamento e salva os conjuntos de treino e teste.

    Args:
        input_file (str, optional): Caminho para o arquivo CSV de dados brutos. Usa um valor padrão se não for fornecido.
        output_train_file (str, optional): Caminho para salvar o arquivo CSV de dados de treino. Usa um valor padrão se não for fornecido.
    """
    # Definir caminhos para os dados brutos e processados
    if input_file is None:
        input_file = RAW_DATA_DIR / "data.csv"
    if output_file is None:
        output_file = PROCESSED_DATA_DIR / "data_processed.csv"

    # Garantir que os diretórios existam
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Carregar dados
    df = load_data(input_file)

    # Pré-processar dados
    df_processed = preprocess_data(df)

    # Salvar dados processados
    df_processed.to_csv(output_file, index=False)
    typer.echo(f"Dados pré-processados salvos em: {output_file}")


if __name__ == "__main__":
    app()
