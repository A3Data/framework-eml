from src.pipelines.train import save_model
from unittest.mock import MagicMock


def test_save_model(mocker):
    # Mock para joblib.dump
    mock_dump = mocker.patch("joblib.dump")

    # Mock para typer.echo
    mock_echo = mocker.patch("typer.echo")

    # Modelo fictício
    mock_model = MagicMock()

    # Caminho fictício para o arquivo
    output_file = "fake_model.joblib"

    # Chamar a função save_model
    save_model(mock_model, output_file)

    # Verificar se joblib.dump foi chamado corretamente
    mock_dump.assert_called_once_with(mock_model, output_file)
    mock_echo.assert_called_once_with(f"Modelo salvo em: {output_file}")
