import pytest
import pandas as pd
from unittest.mock import patch, mock_open
from src.pipelines.features import load_data, preprocess, preprocess_data


def test_load_data_success():
    # Dados CSV fictícios para simular a leitura do arquivo
    csv_data = "5.1,3.5,1.4,0.2,setosa\n4.9,3.0,1.4,0.2,setosa"

    # Usar mock_open para simular a leitura do arquivo CSV
    with patch("builtins.open", mock_open(read_data=csv_data)):
        df = load_data("fake_path.csv")

    # Verificar se o DataFrame foi carregado corretamente
    expected_df = pd.DataFrame(
        {
            "sepal_length": [5.1, 4.9],
            "sepal_width": [3.5, 3.0],
            "petal_length": [1.4, 1.4],
            "petal_width": [0.2, 0.2],
            "species": ["setosa", "setosa"],
        }
    )
    # Verifica se o DataFrame carregado corresponde ao esperado
    pd.testing.assert_frame_equal(df, expected_df)


def test_preprocess_data_no_species_column():
    # Dados fictícios sem a coluna 'species' para verificar o comportamento
    df = pd.DataFrame(
        {
            "sepal_length": [5.1, 4.9, 4.7, 4.6],
            "sepal_width": [3.5, 3.0, 3.2, 3.1],
            "petal_length": [1.4, 1.4, 1.3, 1.5],
            "petal_width": [0.2, 0.2, 0.2, 0.2],
        }
    )

    with pytest.raises(KeyError):
        preprocess_data(df)


def test_preprocess_failure(mocker):
    mock_echo = mocker.patch("typer.echo")

    # Chamar a função preprocess e garantir que uma exceção seja levantada
    with pytest.raises(SystemExit):
        preprocess(
            input_file="fake_input.csv",
            output_train_file="fake_train.csv",
            output_test_file="fake_test.csv",
        )
    # Verificar se a mensagem de erro foi exibida
    mock_echo.assert_called_once_with(
        "Falha ao carregar os dados. Arquivo não encontrado.", err=True
    )
