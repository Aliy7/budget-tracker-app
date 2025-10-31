import json
from datetime import date
class Expense:
    def __init__(self, budget, amount, category=None, note=""):
        self.budget = budget
        self.amount = float(amount)
        self.date = date.today()
        self.category = category
        self.note = note
        
        if hasattr(budget, "amount"):  
            if self.amount > budget.amount:
                raise ValueError("Expense exceeds available budget!")
        elif isinstance(budget, (int, float)):
            if self.amount > budget:
                raise ValueError("Expense exceeds available budget amount!")

    def to_json(self):
        return {
            "amount": self.amount,
            "date": str(self.date),
            "category": self.category,
            "note": self.note
        }

    def __str__(self):
        return json.dumps(self.to_json(), indent=4)

    @staticmethod
    def filter_by_category(expenses, category):
        result = []
        for expense in expenses:
            if expense.category == category:
                result.append(expense)
        return result

    @staticmethod
    def total_amount(expenses):
        total = 0.0
        for expense in expenses:
            total += expense.amount
        return total
