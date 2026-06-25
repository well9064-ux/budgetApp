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
