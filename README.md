"""
# Python OOP Banking System (CLI) + Docker


Small example project demonstrating:
- Object-oriented design (Account, Bank, Transaction)
- Persistence with SQLite
- Simple CLI interface (argparse; optional rich for nicer tables)
- Dockerfile to containerize the app
- Unit tests with pytest


Files:
- app.py -> CLI entrypoint (uses argparse; works without external deps)
- bank.py -> core OOP models and DB layer (DB path can be overridden with ENV)
- requirements.txt -> python dependencies (optional for richer UI and testing)
- Dockerfile -> build runtime image
- tests/test_bank.py -> basic unit tests with pytest
- README.md -> this file


How to run locally (recommended):
1. Create a virtualenv and install requirements (optional for rich UI & tests):
python -m venv venv
source venv/bin/activate # Windows: venv\\Scripts\\activate
pip install -r requirements.txt


2. Run the CLI (no external deps required):
python app.py --help
python app.py create Alice --initial 100
python app.py list
python app.py deposit 1 50
python app.py withdraw 1 20
python app.py transfer 1 2 10
python app.py balance 1
python app.py statement 1 --limit 20


How to run tests:
pytest -q


How to run with Docker:
1. Build: docker build -t py-bank:latest .
2. Run: docker run --rm -it -v $(pwd)/data:/app/data py-bank:latest


Notes:
- The app stores a SQLite database in `data/bank.db` by default. You can override the DB path with the
environment variable `PYBANK_DB_PATH` (useful for tests and container mounts).
"""
