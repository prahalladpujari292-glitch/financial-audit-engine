# Financial Transaction Audit Engine

A demonstration FastAPI microservice that validates transaction payloads and
flags potential anomalies using a small set of heuristic rules.

> **Important:** This is a starter/demo project, not a certified fraud-detection
> or compliance system. The thresholds are illustrative, and a flagged result
> is not proof of wrongdoing. Review the rules, security, privacy, and legal
> requirements before using real financial data.

## Requirements

- Python 3.10+
- Git (optional, for publishing to GitHub)

## Install

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
```

## Run locally

```bash
uvicorn main:app --reload
```

- Health check: http://127.0.0.1:8000/health
- Interactive API docs: http://127.0.0.1:8000/docs

## Example request

Send a `POST` request to `/audit` with JSON:

```json
{
  "account_id": "ACC-1001",
  "amount": 12500,
  "currency": "USD",
  "timestamp": "2026-10-27T03:30:00Z",
  "merchant_category": "gambling"
}
```

## Run tests

```bash
pytest -v
```

## Publish to GitHub

1. Create a new empty repository named `financial-audit-engine` on GitHub.
2. Extract this ZIP file and open a terminal in the extracted folder.
3. Run:

```bash
git init
git add .
git commit -m "Initial financial audit engine"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the repository URL shown by GitHub.
Never commit API keys, passwords, real customer records, or other secrets.

## Current limitations

- No database or durable audit history.
- No authentication or authorization.
- Heuristic rules are examples and need business/compliance review.
- No rate limiting, monitoring, or deployment configuration.
- `amount` uses floating-point for a simple demo; production money handling
  should use decimal-safe representations and explicit currency rules.
