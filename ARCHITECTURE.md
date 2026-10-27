# Architecture

```text
Client
  |
  | POST /audit (JSON)
  v
FastAPI + Pydantic validation
  |
  v
AuditEngine heuristic rules
  |-- Amount threshold
  |-- Merchant-category list
  |-- Configured off-hours window
  v
JSON response: status, reasons, risk_score
```

## Components

- **API layer:** FastAPI exposes `/health` and `/audit`.
- **Validation:** Pydantic checks required fields and basic constraints.
- **Audit engine:** Stateless rules add points to a risk score.
- **Tests:** Pytest and FastAPI TestClient exercise the health and audit routes.

## Production considerations

Before real-world use, add authentication/authorization, a database with
appropriate retention controls, structured logging, monitoring, rate limiting,
idempotency, privacy controls, and documented rule governance. Use decimal-safe
money representations and validate currency-specific limits. Risk rules should
be reviewed for false positives, fairness, and applicable legal obligations.
