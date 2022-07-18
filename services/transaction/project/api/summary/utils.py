from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from sqlalchemy import extract, func

from project.api.models import Account, ChoiceType, TransactionList


def parse_amount(amount):
    return amount if amount else 0


def parse_month(months):
    return [
        datetime(year=month[0], month=month[1], day=1).strftime("%b")
        for month in months
    ]


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


def get_current_balance(user_id):
    return (
        Account.query.filter_by(account_owner=user_id)
        .with_entities(func.sum(Account.account_balance).label("total"))
        .first()
        .total
    )


def get_basic_summary(user_id):
    current_balance = get_current_balance(user_id)
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


def get_last_months(start_date, months):
    tmp = []
    for _ in range(months):
        tmp.append((start_date.year, start_date.month))
        start_date = start_date + relativedelta(months=-1)
    return tmp


def get_summary(user_id):
    transactions = TransactionList.query.filter_by(transaction_owner=user_id).all()
    today = get_today()
    current_balance = get_current_balance(user_id)
    income_all, expense_all, = (
        0,
        0,
    )
    income, expense = {}, {}
    last_12_months = get_last_months(today, 12)
    for transaction in transactions:
        if transaction.transaction_type == ChoiceType.income:
            income_all += transaction.transaction_amount
            income_key = (
                transaction.transaction_date.year,
                transaction.transaction_date.month,
            )
            if income_key in income:
                income[income_key] += transaction.transaction_amount
            else:
                income[income_key] = transaction.transaction_amount
        else:
            expense_all += transaction.transaction_amount
            expense_key = (
                transaction.transaction_date.year,
                transaction.transaction_date.month,
            )
            if expense_key in expense:
                expense[expense_key] += transaction.transaction_amount
            else:
                expense[expense_key] = transaction.transaction_amount
    income_group, expense_group = [], []
    for months in last_12_months:
        income_group.append(income.get(months, 0))
        expense_group.append(expense.get(months, 0))

    return {
        "balance": parse_amount(current_balance),
        "incomeAll": parse_amount(income_all),
        "expenseAll": parse_amount(expense_all),
        "incomeMonth": parse_amount(income[(today.year, today.month)]),
        "expenseMonth": parse_amount(expense[(today.year, today.month)]),
        "previousMonths": parse_month(last_12_months),
        "incomeLastYear": income_group,
        "expenseLastYear": expense_group,
    }
