# Models

## Code Style

```bash
sudo apt update
sudo apt install python3-venv python3-pip
cd models
python3 -m venv .venv
source .venv/bin/activate
poetry install
```

```bash
isort .
black .
pycodestyle *.py annotation
pylint *.py annotation
```

```bash
pytest tests --maxfail=1
```