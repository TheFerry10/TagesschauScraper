from pathlib import Path

DEFAULT_TIMEOUT = None
TEST_HTML_DIR = Path("tests/data/bluescraper/html/")
TEST_CONFIG_DIR = Path("tests/data/bluescraper/config/")
VALID_HTML_PATH = TEST_HTML_DIR.joinpath("valid.html")
INVALID_HTML_PATH = TEST_HTML_DIR.joinpath("invalid.html")
CONFIG_YAML = TEST_CONFIG_DIR.joinpath("config.yml")
CONFIG_NO_VALIDATION_YAML = TEST_CONFIG_DIR.joinpath(
    "config-no-validation.yml"
)
CONFIG_JSON = TEST_CONFIG_DIR.joinpath("config.json")
