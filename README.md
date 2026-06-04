# Convert Service

A small, production-shaped **FastAPI microservice** for length, mass, temperature, and
(illustrative) currency conversion — built to showcase a complete **CI/CD pipeline**:
linting, tests with coverage, and an automated Docker build on every push.

> Built as a portfolio project to demonstrate microservice structure, clean error
> handling, comprehensive testing, and GitHub Actions CI/CD.

---

## What it demonstrates

- **Microservice design** — a focused single-responsibility HTTP service with a clean
  separation between pure logic (`conversions.py`) and the web layer (`main.py`).
- **Typed, validated API** — Pydantic request/response models, correct status codes
  (200/400/404/422), and a dispatch table for conversion kinds.
- **Robust error handling** — domain errors (`ConversionError`) map cleanly to HTTP 400,
  unknown kinds to 404, malformed payloads to 422.
- **Thorough testing** — 17 tests split between pure-logic unit tests and API-level tests.
- **CI/CD** — a GitHub Actions pipeline that lints (ruff), runs tests with coverage,
  uploads the coverage report, and — only if tests pass — builds the Docker image.
- **Containerised** — minimal slim-Python Dockerfile.

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health probe |
| `POST` | `/convert/length` | Length conversion |
| `POST` | `/convert/mass` | Mass conversion |
| `POST` | `/convert/temperature` | Temperature conversion |
| `POST` | `/convert/currency` | Currency conversion (illustrative fixed rates) |

### Example

```bash
curl -X POST http://localhost:8000/convert/length \
  -H "Content-Type: application/json" \
  -d '{"value": 100, "from_unit": "km", "to_unit": "mi"}'
# → {"value":100,"from_unit":"km","to_unit":"mi","result":62.137119}
```

## Quick start

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
# open http://127.0.0.1:8000/docs
```

## Run with Docker

```bash
docker build -t convert-service .
docker run --rm -p 8000:8000 convert-service
```

## CI/CD pipeline

On every push/PR to `main`, GitHub Actions:

1. **Lints** the code with ruff.
2. **Tests** with pytest and produces a coverage report.
3. Uploads the coverage XML as a build artifact.
4. **Builds the Docker image** — but only if linting and tests pass (`needs:` gate).

See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Tests

```bash
pytest --cov=app --cov-report=term-missing
```

## Project structure

```
nsw-convert-service/
├── app/
│   ├── conversions.py   # pure conversion logic (unit-tested)
│   └── main.py          # FastAPI app + routing + error handling
├── tests/
│   ├── test_conversions.py   # 11 unit tests
│   └── test_api.py           # 6 API tests
├── Dockerfile
└── .github/workflows/ci.yml  # lint → test → docker build
```

## Note

Currency rates are **fixed illustrative values**, not live market rates — the focus of
this project is the service architecture and CI/CD, not exchange-rate accuracy.

## License

MIT
