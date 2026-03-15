from datetime import date
import pytest
from pytest_bdd import scenarios, given, when, then, parsers

from core.expense_service import ExpenseService
from core.in_memory_expense_repository import InMemoryExpenseRepository

scenarios("./expense_management.feature")


@pytest.fixture
def context():
    repo = InMemoryExpenseRepository()
    service = ExpenseService(repo)
    return {"service": service, "db": repo}


@given(parsers.parse("un gestor de gastos vacío"))
def empty_manager(context):
    pass


@given(parsers.parse("un gestor con un gasto de {amount:d} euros"))
def manager_with_one_expense(context, amount):
    context["service"].create_expense(
        title="Gasto inicial", amount=amount, description="", expense_date=date.today()
    )


@when(parsers.parse("añado un gasto de {amount:d} euros llamado {title}"))
def add_expense(context, amount, title):
    context["service"].create_expense(
        title=title, amount=amount, description="", expense_date=date.today()
    )


@when(parsers.parse("elimino el gasto con id {expense_id:d}"))
def remove_expense(context, expense_id):
    context["service"].remove_expense(expense_id)


@then(parsers.parse("el total de dinero gastado debe ser {total:d} euros"))
def check_total(context, total):
    assert context["service"].total_amount() == total


@then(parsers.parse("{month_name} debe sumar {expected_total:d} euros"))
def check_month_total(context, month_name, expected_total):
    total_actual = context["totals"].get(month_name, 0)
    assert total_actual == expected_total


@then(parsers.parse("debe haber {expenses:d} gastos registrados"))
def check_expenses_length(context, expenses):
    total = len(context["db"]._expenses)
    assert expenses == total


@given("un gestor con gastos repartidos entre enero y febrero")
def manager_with_expenses_in_two_months(context):
    context["service"].create_expense(
        title="Libros",
        amount=15,
        description="Material de clase",
        expense_date=date(2025, 1, 10),
    )
    context["service"].create_expense(
        title="Fotocopias",
        amount=10,
        description="Apuntes",
        expense_date=date(2025, 1, 20),
    )
    context["service"].create_expense(
        title="Autobús",
        amount=7,
        description="Transporte",
        expense_date=date(2025, 2, 3),
    )


@when("calculo el total por mes")
def calculate_total_by_month(context):
    context["totals"] = context["service"].total_by_month()
