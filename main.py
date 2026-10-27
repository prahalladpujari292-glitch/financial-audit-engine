import uuid
from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, status
from pydantic import BaseModel, Field, field_validator

app = FastAPI(
    title="Financial Transaction Audit Engine",
    description=(
        "A demonstration microservice that validates transactions and flags "
        "potential anomalies using simple, configurable heuristic rules."
    ),
    version="1.0.0",
)


class Transaction(BaseModel):
    transaction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    account_id: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0, allow_inf_nan=False)
    currency: str = Field(..., min_length=3, max_length=3)
    timestamp: datetime
    merchant_category: str = Field(..., min_length=1, max_length=100)

    @field_validator("currency")
    @classmethod
    def currency_must_be_letters(cls, value: str) -> str:
        value = value.upper()
        if not value.isalpha():
            raise ValueError("currency must contain three letters")
        return value


class AuditResult(BaseModel):
    transaction_id: str
    status: str
    reasons: List[str]
    risk_score: int
    audited_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class AuditEngine:
    @staticmethod
    def evaluate(transaction: Transaction) -> AuditResult:
        reasons: List[str] = []
        risk_score = 0

        if transaction.amount > 10000:
            reasons.append("High value transaction alert (> 10,000 currency units)")
            risk_score += 40

        high_risk_categories = {"gambling", "crypto_exchange", "offshore_trust"}
        if transaction.merchant_category.strip().lower() in high_risk_categories:
            reasons.append(
                f"High risk merchant category: {transaction.merchant_category}"
            )
            risk_score += 35

        tx_hour = transaction.timestamp.hour
        if 1 <= tx_hour <= 4:
            reasons.append("Transaction occurred during the configured off-hours window")
            risk_score += 25

        return AuditResult(
            transaction_id=transaction.transaction_id,
            status="FLAGGED" if risk_score >= 50 else "APPROVED",
            reasons=reasons,
            risk_score=min(risk_score, 100),
        )


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}


@app.post("/audit", response_model=AuditResult, status_code=status.HTTP_201_CREATED)
def audit_transaction(transaction: Transaction):
    return AuditEngine.evaluate(transaction)
