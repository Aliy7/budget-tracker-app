from user import User
from usermanager import UserManager
from expense import Expense
from budget import Budget
import os, json


def add_user(args):
    #Create new user and save
    name_str = " ".join(args.name)
    bio_str = " ".join(args.bio)
    username_str = args.username
    cli_user = User(name_str, username=username_str, age=args.age, bio=bio_str)
    manager = UserManager(args.file_name)
    manager.save_user(cli_user)
    print(f"\nNew user '{args.username}' added successfully.")

def add_budget(args):
    """Add a budget for an existing user."""
    if not args.username:
        raise SystemExit("Error: --username is required when adding a budget.")
    if args.amount is None or not args.category or not args.note:
        raise SystemExit("Error: --amount, --category, and --note are required when adding a budget.")

    budget_storage = os.path.join("data", "budgets", f"{args.username}_budgets.json")
    manager = UserManager(args.file_name)
    new_budget = Budget(float(args.amount), args.category, args.note)
    manager.save_budgets(budget_storage, new_budget)
    print(f"Budget added successfully for '{args.username}'.")


def add_expense(args):
    if not args.username:
        raise SystemExit("Error: username is required when adding an expense.")
    if args.amount is None or not args.category or not args.note:
        raise SystemExit("Error: amount, --category, and --note are required when adding an expense.")

    username = args.username.lower()
    budget_storage = os.path.join("data", "budgets", f"{username}_budgets.json")
    expense_storage = os.path.join("data", "expenses", f"{username}_expenses.json")

    # Load existing budget for that user
    with open(budget_storage, "r") as f:
        budgets = json.load(f)
        if not budgets:
            raise SystemExit(f"No budgets found for {username}. Add a budget first.")
        current_budget = sum(b["amount"] for b in budgets)
    try: 
        new_expense = Expense(float(current_budget), float(args.amount), args.category, args.note)
    except ValueError:
        print(f"Your balance is £{current_budget:.2f} please write smaller amount" ) 
        return
    manager = UserManager(args.file_name)
    manager.save_expenses(expense_storage, new_expense)

    # Calculate remaining balance
    with open(expense_storage, "r") as f:
        expenses = json.load(f)
        total_expense = sum(e["amount"] for e in expenses)
        balance = current_budget - total_expense

    print(f"\nExpense recorded for '{username}'. Remaining balance: £{balance:.2f}")


def main():
    """Main entry point for project CLI."""
    args = User.cli_arg_processor()
    manager = UserManager(args.file_name)

    if args.name and args.age is not None and args.bio:
        add_user(args)

    if args.budget:
        add_budget(args)

    if args.expense:
        add_expense(args)

    if args.username and args.delete_user:
        user_to_remove = User("temp", args.username, 0, "")
        if user_to_remove.delete_user(args.username):
            print(f"User '{args.username}' deleted successfully.")

    if args.update_user and args.username:
        user = User("temp", args.username, 0, "")
        user.new_names = args.new_name
        user.new_age = args.new_age
        user.new_bio = args.new_bio
        user.update_user(args.username)

if __name__ == "__main__":
    main()
