from datetime import datetime, timedelta

from sqlalchemy import extract, func

from project.api.models import Account, TransactionList


def parse_amount(amount):
    return amount if amount else 0


def get_transaction_sum_by_category(user_id, category):
    return (
        TransactionList.query.filter_by(
            transaction_owner=user_id, transaction_type=category
        )
        .with_entities(func.sum(TransactionList.transaction_amount).label("total"))
        .first()
        .total
    )


def get_today():
    return (datetime.utcnow() + timedelta(hours=6)).date()


def get_transaction_sum_by_month(user_id, category, date=get_today()):
    return (
        TransactionList.query.filter_by(transaction_owner=user_id)
        .filter_by(transaction_type=category)
        .filter(extract("year", TransactionList.transaction_date) == date.year)
        .filter(extract("month", TransactionList.transaction_date) == date.month)
        .with_entities(func.sum(TransactionList.transaction_amount).label("total"))
        .first()
        .total
    )


def get_basic_summary(user_id):
    current_balance = (
        Account.query.filter_by(account_owner=user_id)
        .with_entities(func.sum(Account.account_balance).label("total"))
        .first()
        .total
    )
    income_all = get_transaction_sum_by_category(user_id, "income")
    expense_all = get_transaction_sum_by_category(user_id, "expense")

    income_month = get_transaction_sum_by_month(user_id, "income")
    expense_month = get_transaction_sum_by_month(user_id, "expense")
    return {
        "balance": parse_amount(current_balance),
        "incomeAll": parse_amount(income_all),
        "expenseAll": parse_amount(expense_all),
        "incomeMonth": parse_amount(income_month),
        "expenseMonth": parse_amount(expense_month),
    }
