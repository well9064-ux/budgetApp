"""Tests for budget core functions."""

from typing import Any

from budget.core import (
    add_transaction,
    filter_by_category,
    get_balance,
    load_transactions_from_csv,
)


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
    transactions = load_transactions_from_csv("data/step2_transactions.csv")

    assert get_balance(transactions) == 24285027.0


def test_filter_by_category_uses_step2_category() -> None:
    transactions = load_transactions_from_csv("data/step2_transactions.csv")

    result = filter_by_category(transactions, "급여")

    assert len(result) == 9
    assert all(transaction["category"] == "급여" for transaction in result)


def test_filter_by_category_matches_case_insensitively() -> None:
    transactions: list[dict[str, Any]] = [
        {
            "date": "2026-04-01",
            "type": "expense",
            "category": "Food",
            "description": "lunch",
            "amount": -12000,
            "memo": "",
        },
        {
            "date": "2026-04-02",
            "type": "expense",
            "category": "Transport",
            "description": "subway",
            "amount": -1500,
            "memo": "",
        },
    ]

    result = filter_by_category(transactions, "food")

    assert result == [transactions[0]]


def test_filter_by_category_returns_empty_list_for_missing_category() -> None:
    transactions: list[dict[str, Any]] = [
        {
            "date": "2026-01-10",
            "type": "지출",
            "category": "교통",
            "description": "지하철",
            "amount": -1500,
            "memo": "",
        },
    ]

    assert filter_by_category(transactions, "의료") == []


def test_filter_by_category_returns_independent_results() -> None:
    transactions: list[dict[str, Any]] = [
        {
            "date": "2026-01-07",
            "type": "수입",
            "category": "급여",
            "description": "월급",
            "amount": 3500000,
            "memo": "1월급여",
        },
    ]

    result = filter_by_category(transactions, "급여")
    result[0]["amount"] = 0

    assert transactions[0]["amount"] == 3500000


def test_load_transactions_from_csv_reads_step1_transactions() -> None:
    transactions = load_transactions_from_csv("data/step1_transactions.csv")

    assert len(transactions) == 10
    assert transactions[0] == {
        "date": "2026-01-05",
        "type": "지출",
        "category": "식비",
        "description": "점심식사",
        "amount": -12000,
        "memo": "",
    }


def test_load_transactions_from_csv_converts_amount_to_int() -> None:
    transactions = load_transactions_from_csv("data/step1_transactions.csv")

    assert transactions[1]["amount"] == 3500000
    assert isinstance(transactions[1]["amount"], int)
