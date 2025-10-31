# test_expenses.py
from budget import Budget
from expense import Expense

# create budgets
b1 = Budget(100, "19/10/2025", "Grocery", "Last coins left")
b2 = Budget(50, "2025-10-20", "Transport", "Bus fares")

# create expenses (Expense.__init__ is minimal; attach budget fields after)
e1 = Expense(b1, 25)
if e1.date is None:
    e1.date = b1.date
if e1.category is None:
    e1.category = b1.category

e2 = Expense(b1, 10, note="Snack")
if e2.date is None:
    e2.date = b1.date
if e2.category is None:
    e2.category = b1.category

e3 = Expense(b2, 5)
if e3.date is None:
    e3.date = b2.date
if e3.category is None:
    e3.category = b2.category

expenses = [e1, e2, e3]

print("Budgets:")
print(b1)
print(b2)

print("\nExpenses:")
for e in expenses:
    print(e)

grocery = Expense.filter_by_category(expenses, "Grocery")
print("\nGrocery expenses count:", len(grocery))
print("Total amount (all):", Expense.total_amount(expenses))

# Basic checks (will raise AssertionError if something's wrong)
assert Expense.total_amount(expenses) == 40.0
assert len(grocery) == 2

print("\nTests passed.")
