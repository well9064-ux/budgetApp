"""Core budget functions for the CSV-based CLI app."""

import csv
from typing import Any


def add_transaction(
    transactions: list[dict[str, Any]],
    transaction: dict[str, Any],
) -> list[dict[str, Any]]:
    """Return a transaction list with the given transaction added."""
    new_transaction = {
        "date": transaction["date"],
        "type": transaction["type"],
        "category": transaction["category"],
        "description": transaction["description"],
        "amount": transaction["amount"],
        "memo": transaction["memo"],
    }
    return [*transactions, new_transaction]


def get_balance(transactions: list[dict[str, Any]]) -> float:
    """Return the sum of all transaction amounts."""
    return float(sum(transaction["amount"] for transaction in transactions))


def filter_by_category(
    transactions: list[dict[str, Any]],
    category: str,
) -> list[dict[str, Any]]:
    """Return transactions matching the category case-insensitively."""
    normalized_category = category.casefold()
    return [
        transaction.copy()
        for transaction in transactions
        if str(transaction["category"]).casefold() == normalized_category
    ]


def load_transactions_from_csv(file_path: str) -> list[dict[str, Any]]:
    """Load transactions from a UTF-8 BOM compatible CSV file."""
    transactions: list[dict[str, Any]] = []

    with open(file_path, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["amount"] = int(row["amount"])
            transactions.append(row)

    return transactions


def monthly_summary(
    transactions: list[dict[str, Any]],
) -> dict[str, dict[str, int]]:
    """Return monthly income, expense, and net totals."""
    summary: dict[str, dict[str, int]] = {}

    for transaction in transactions:
        month = str(transaction["date"])[:7]
        amount = int(transaction["amount"])

        if month not in summary:
            summary[month] = {"income": 0, "expense": 0, "net": 0}

        if amount > 0:
            summary[month]["income"] += amount
        else:
            summary[month]["expense"] += amount

        summary[month]["net"] += amount

    return summary
