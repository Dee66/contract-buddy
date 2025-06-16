# Contract Buddy

A modular, production-ready AI pipeline for code and document analysis.

---

## 🚀 Quickstart

```sh
pip install -r requirements.txt
set PYTHONPATH=%CD%\src
python src/pipeline_runner.py config.yaml
python -m unittest discover -s src/tests
```

---

## 📚 Documentation Overview

- **[Solution Foundation](docs/foundation/README.md)**  
  Business value, architecture, risk, and strategy.
- **[AI Core & Optimization](docs/core/README.md)**  
  Data pipeline, model implementation, benchmarking, and evaluation.
- **[System Build & Readiness](docs/build/README.md)**  
  API, UI, deployment, CI/CD, and operational playbooks.
- **[Portfolio & Narrative](docs/portfolio/README.md)**  
  Portfolio, narrative, and future roadmap.
- **[Project Checklist](docs/checklist.md)**  
  Implementation and delivery checklist.

---

## 🗂️ Project Structure

```
contract-buddy/
│   README.md
│   requirements.txt
│   config.yaml
│   run_tests.py
│   organize_project.py
│
├── src/             # All source code (modular, OOP, SOLID)
│   ├── ingestion/
│   ├── cleaning/
│   ├── chunking/
│   ├── embedding/
│   ├── storage/
│   ├── utils/
│   └── tests/
│
├── data/            # Data (excluded from git)
├── logs/            # Logs (excluded from git)
├── docs/            # Full documentation (see above)
```

---

## 📝 About This README

This is the main entry point for the project and documentation.  
For in-depth technical and business documentation, start with [docs/foundation/README.md](docs/foundation/README.md).

---

## 🏷️ License

MIT

---
