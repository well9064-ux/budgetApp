"""Tests for budget core functions."""

import csv
from typing import Any

from budget.core import add_transaction, get_balance


def test_add_transaction_increases_length() -> None:
    transactions: list[dict[str, Any]] = []
    transaction: dict[str, Any] = {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert len(result) == 1


def test_add_transaction_stores_negative_expense_amount() -> None:
    transactions: list[dict[str, Any]] = []
    transaction: dict[str, Any] = {
        "date": "2026-01-10",
        "type": "지출",
        "category": "교통",
        "description": "지하철",
        "amount": -1500,
        "memo": "",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["amount"] == -1500


def test_add_transaction_stores_positive_income_amount() -> None:
    transactions: list[dict[str, Any]] = []
    transaction: dict[str, Any] = {
        "date": "2026-01-07",
        "type": "수입",
        "category": "급여",
        "description": "월급",
        "amount": 3500000,
        "memo": "1월급여",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["amount"] == 3500000


def test_add_transaction_accepts_empty_description() -> None:
    transactions: list[dict[str, Any]] = []
    transaction: dict[str, Any] = {
        "date": "2026-01-28",
        "type": "기타수입",
        "category": "기타수입",
        "description": "",
        "amount": 25000,
        "memo": "중고마켓",
    }

    result = add_transaction(transactions, transaction)

    assert result[0]["description"] == ""


def test_get_balance_returns_sum_of_income_and_expense() -> None:
    transactions: list[dict[str, Any]] = [
        {
            "date": "2026-01-05",
            "type": "지출",
            "category": "식비",
            "description": "점심식사",
            "amount": -12000,
            "memo": "",
        },
        {
            "date": "2026-01-07",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 3500000,
            "memo": "1월급여",
        },
    ]

    result = get_balance(transactions)

    assert result == 3488000.0


def test_get_balance_returns_zero_for_empty_transactions() -> None:
    assert get_balance([]) == 0.0


def test_get_balance_with_step2_transactions_csv() -> None:
    transactions: list[dict[str, Any]] = []

    with open("data/step2_transactions.csv", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["amount"] = int(row["amount"])
            transactions.append(row)

    assert get_balance(transactions) == 24285027.0
