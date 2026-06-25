"""Core budget functions for the CSV-based CLI app."""

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
