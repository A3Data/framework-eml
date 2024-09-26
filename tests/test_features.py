import pytest
import pandas as pd
from src.pipelines.features import load_data, preprocess, preprocess_data
from config.settings import TEST_LOAD_DATA_CSV


def test_load_data_success():
    # Carrega os dados usando a função load_data
    df = load_data(TEST_LOAD_DATA_CSV)

    # DataFrame esperado
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


def test_preprocess_failure(capfd):
    # Chamar a função preprocess e garantir que uma exceção seja levantada
    with pytest.raises(SystemExit):
        preprocess(
            input_file="fake_input.csv",
            output_train_file="fake_train.csv",
            output_test_file="fake_test.csv",
        )

    # Capturar a saída de erro (stderr)
    captured = capfd.readouterr()
    print(captured)

    # Verificar se a mensagem de erro está no stderr
    assert "Falha ao carregar os dados. Arquivo não encontrado." in captured.err
