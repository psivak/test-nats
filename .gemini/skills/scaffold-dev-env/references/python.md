# Python Templates (UV & Ruff)

## pyproject.toml Template
```toml
[project]
name = "app"
version = "0.1.0"
description = "Dev environment app"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastapi",
    "uvicorn",
    "sqlalchemy",
    "psycopg2-binary",
    "python-dotenv",
]

[tool.uv]
dev-dependencies = [
    "pytest",
    "ruff",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
python_classes = ["Test*"]
```

## ruff.toml Template
```toml
# Displayed in VS Code via the Ruff extension
line-length = 88
target-version = "py312"

[lint]
select = ["E", "F", "I", "N", "UP", "B", "C4", "SIM", "ARG"]
ignore = []

[format]
quote-style = "double"
indent-style = "space"
```
