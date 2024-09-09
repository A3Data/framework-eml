import pandas as pd
from sklearn.model_selection import train_test_split
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


def preprocess_data(df: pd.DataFrame):
    """
    Realiza o pré-processamento do dataset, incluindo codificação das variáveis de alvo,
    escalonamento das features e divisão em conjuntos de treino e teste.

    Args:
        df (pd.DataFrame): DataFrame contendo os dados a serem pré-processados.

    Returns:
        tuple: Dois DataFrames, um para os dados de treino e outro para os dados de teste.
    """
    # Codificar a variável alvo (species) para valores numéricos
    label_encoder = LabelEncoder()
    df["species"] = label_encoder.fit_transform(df["species"])

    # Separar as features (X) e a variável alvo (y)
    X = df.drop("species", axis=1)
    y = df["species"]

    # Dividir os dados em conjuntos de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Escalar as features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Combinar as features escaladas com a variável alvo em DataFrames separados
    train_data = pd.DataFrame(X_train_scaled, columns=X.columns)
    train_data["species"] = y_train.values

    test_data = pd.DataFrame(X_test_scaled, columns=X.columns)
    test_data["species"] = y_test.values

    return train_data, test_data


@app.command()
def preprocess(
    input_file: str = None, output_train_file: str = None, output_test_file: str = None
):
    """
    Função principal para o pré-processamento dos dados. Carrega os dados brutos, realiza
    o pré-processamento e salva os conjuntos de treino e teste.

    Args:
        input_file (str, optional): Caminho para o arquivo CSV de dados brutos. Usa um valor padrão se não for fornecido.
        output_train_file (str, optional): Caminho para salvar o arquivo CSV de dados de treino. Usa um valor padrão se não for fornecido.
        output_test_file (str, optional): Caminho para salvar o arquivo CSV de dados de teste. Usa um valor padrão se não for fornecido.
    """
    # Definir caminhos padrão para os dados brutos e processados
    if input_file is None:
        input_file = RAW_DATA_DIR / "data.csv"
    if output_train_file is None:
        output_train_file = PROCESSED_DATA_DIR / "train_data.csv"
    if output_test_file is None:
        output_test_file = PROCESSED_DATA_DIR / "test_data.csv"

    # Garantir que os diretórios existam
    output_train_file = Path(output_train_file)
    output_test_file = Path(output_test_file)
    output_train_file.parent.mkdir(parents=True, exist_ok=True)

    # Carregar dados
    df = load_data(input_file)

    # Pré-processar dados (dividir em treino/teste e escalonar)
    train_data, test_data = preprocess_data(df)

    # Salvar os conjuntos de dados pré-processados
    train_data.to_csv(output_train_file, index=False)
    test_data.to_csv(output_test_file, index=False)

    # Mensagens de confirmação
    typer.echo(f"Dados de treino salvos em: {output_train_file}")
    typer.echo(f"Dados de teste salvos em: {output_test_file}")


if __name__ == "__main__":
    app()
