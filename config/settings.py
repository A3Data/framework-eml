from pathlib import Path

# Caminho absoluto para o diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminhos absolutos para as pastas principais do projeto
DATA_DIR = BASE_DIR / "artifacts" / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
INTERIM_DATA_DIR = DATA_DIR / "interim"

MODELS_DIR = BASE_DIR / "artifacts" / "models"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

SRC_DIR = BASE_DIR / "src"
PIPELINES_DIR = SRC_DIR / "pipelines"
UTILS_DIR = SRC_DIR / "utils"
API_DIR = BASE_DIR / "api"
DEPLOYMENT_DIR = BASE_DIR / "deployment"
DOCS_DIR = BASE_DIR / "docs"
TESTS_DIR = BASE_DIR / "tests"
UI_DIR = BASE_DIR / "ui"
TEST_LOAD_DATA_CSV = TESTS_DIR / "test_load_data.csv"
