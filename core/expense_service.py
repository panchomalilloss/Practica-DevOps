from datetime import date
from collections import defaultdict
from typing import Optional, Dict, List

from core.expense import Expense
from core.in_memory_expense_repository import InMemoryExpenseRepository


class ExpenseService:
    def __init__(self, repository: InMemoryExpenseRepository):
        self._repository = repository

    def create_expense(
        self,
        title: str,
        amount: float,
        description: str = "",
        expense_date: Optional[date] = None,
    ) -> Expense:
        if expense_date is None:
            expense_date = date.today()

        expense = Expense(
            title=title,
            amount=amount,
            description=description,
            expense_date=expense_date,
        )

        self._repository.save(expense)
        return expense

    def list_expenses(self) -> List[Expense]:
        return self._repository.list_all()

    def delete_expense(self, expense_id: str) -> None:
        self._repository.delete(expense_id)

    def total_expenses(self) -> float:
        expenses = self._repository.list_all()
        return sum(expense.amount for expense in expenses)

    def total_by_month(self) -> Dict[str, float]:
        totals: Dict[str, float] = defaultdict(float)

        for expense in self._repository.list_all():
            key = expense.expense_date.strftime("%Y-%m")
            totals[key] += expense.amount

        return dict(totals)
