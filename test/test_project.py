from usermanager import UserManager
from budget import Budget
from expense import Expense
from project import add_user, add_budget, add_expense
from user import User
import pytest, json

"""Testing usermanager class Creating and adding new user"""
def test_save_and_read_user(tmp_path):
    file = tmp_path / "users.json"
    manager = UserManager(str(file))
    user = User("Jason Miles", "JMiles", 20, "QA Intern")
    manager.save_user(user)
    users = manager.get_users()
    assert any(u.username == "JMiles" for u in users.values())
def test_duplicate_user_blocked(tmp_path):
    file = tmp_path / "users.json"
    manager = UserManager(str(file))
    u = User("Same", "dupuser", 22, "Intern")
    manager.save_user(u)
    try:
        manager.save_user(u)
    except SystemExit:
        assert True
    else:
        raise AssertionError("Duplicate not blocked")
    
"""User Class"""
def test_user_creation():
    user = User("Hussein Hassan", "hussi", 25, "Software Developer")
    assert user.names=="Hussein Hassan"
    assert user.username == "hussi"
    assert user.age == 25
    assert user.bio == "Software Developer"
    assert isinstance(user.id, str) and len(user.id) > 5
    
def test_to_string_json():
    u = User("Aisha", "aishan", 27, "Marketing")
    parsed = json.loads(str(u))
    assert parsed["username"] == "aishan"
    assert parsed["names"] == "Aisha"
    assert "bio" in parsed
    

def test_user_id_permanency():
    user = User("James", "flandders", 23, "Data analytic")
    with pytest.raises(AttributeError):
        user.id = "assignedid"
        
        
        
def test_delete_user():
    user = User("Jane Miller", "janem", 0, "Temporary QA account")
    result = user.delete_user("janem")
    assert result in [True, False]


def test_update_user():
    user = User("David Brown", "davidb", 28, "Junior Developer")
    user.new_names = "David Brown Jr."
    user.new_age = 30
    user.new_bio = "Lead Software Developer"
    result = user.update_user("davidb")
    assert result in [True, False]
    

def test_uniqueness_of_user_id():
    dave_joe = User("Dave Joe", "Djoe", "53", "Senior cyber security engineer")
    john_doe = User("John Doe", "Jdoe45", 34, "Data scientist")#
    assert dave_joe.id != john_doe.id
    

def test_user_creating_with_emptyName():
    try:
        User("", "Draco", 20, "Gryffindor")
    except ValueError as error:
        assert "" in str(error)
    else:
        raise AssertionError("User naames cannot be empty")
    


"""Testiing budget class"""

def test_budget_new_one():
    budget = Budget(120, "Food budget", "Weekly grocery")
    assert budget.amount == 120
    assert budget.category == "Food budget"
    assert budget.note == "Weekly grocery"


def test_budget_deposit():
    budget = Budget(100, "Bills", "Monthly bill")
    budget.deposit(200)
    assert budget.amount == 300


def test_budget_withdraw():
    budget = Budget(400, "Eat out to help out", "Night out burn bridges")
    remaining = budget.withdraw(150)
    assert remaining == 250


def test_budget_overSpending():
    budget = Budget(1200, "Complete bills and transport", "Food, fuel, transport and all")
    try:
        budget.withdraw(2000)
    except ValueError:
        pass
    else:
        raise AssertionError
def test_budget_zero_amount():
    budget = Budget(0, "Empty", "No funds yet")
    assert budget.amount == 0


def test_budget_negative_deposit():
    budget = Budget(100, "Bills", "Monthly bill")
    try:
        budget.deposit(-50)
    except ValueError:
        pass
    else:
        raise AssertionError


def test_budget_negative_withdraw():
    budget = Budget(300, "Leisure", "Fun stuff")
    try:
        budget.withdraw(-20)
    except ValueError:
        pass
    else:
        raise AssertionError


def test_budget_transfer_no_funds():
    a = Budget(0, "Zero", "Nothing")
    b = Budget(50, "Target", "Test")
    try:
        a.transfer(10, b)
    except ValueError:
        pass
    else:
        raise AssertionError


def test_budget_transfer_success():
    a = Budget(200, "Source", "Main")
    b = Budget(100, "Target", "Sub")
    a.transfer(50, b)
    assert a.amount == 150
    assert b.amount == 150
    
"""Testing expenses class"""

def test_expense_creation():
    budget = Budget(2000, "Food budget", "Weekly grocery")
    assert budget.amount == 2000
    assert budget.category == "Food budget"
    assert budget.note == "Weekly grocery"

    expense = Expense(budget, 200, "Travel", "Monthly travel london to brums")
    assert expense.budget == budget
    assert expense.category == "Travel"
    assert expense.note == "Monthly travel london to brums"
    
def test_expense_overspending():
    budget = Budget(2000, "Food budget", "Weekly grocery")
    try:
        Expense(budget, 800, "Food", "Over limits")
    except ValueError as e:
        assert str(e)
    else:
        AssertionError
    
def test_expense_numeric_budget():
    expense = Expense(1000.0, 250, "Winter klamotten", 
                      "Geh nach Muenchen zum einkaufen")
    assert expense.amount == 250
    assert expense.category == "Winter klamotten"
    assert expense.note == "Geh nach Muenchen zum einkaufen"
    
def test_expense_numeric_overspending():
    try:
        Expense(1000.0, 2500, "Winter klamotten", 
                "Geh nach Muenchen zum einkaufen")
    except ValueError as e:
        assert str(e)
    else:
        raise AssertionError

def test_multiple_expense():
    budget = Budget(1000, "Bills", "Monthly")
    ex1 = Expense(budget, 150, "Food", "Weekly Groceries")
    ex2 = Expense(budget, 350, "Taxi", "Travel to my next chick")
    total = Expense.total_amount([ex1, ex2])
    assert total == 500.00
    
    
def test_expense_filter_cat():
    budget = Budget(1000, "General", "Test filter")
    e1 = Expense(budget, 50, "Food", "Lunch")
    e2 = Expense(budget, 60, "Transport", "Bus")
    e3 = Expense(budget, 100, "Food", "Dinner")
    food_expenses = Expense.filter_by_category([e1, e2, e3], "Food")
    assert len(food_expenses) == 2 
    assert all(e.category == "Food" for e in food_expenses)
    

"""Testing project class it self """
def test_add_user_creates_file(tmp_path):
    file = tmp_path / "users.json"
    class Args: 
        name = ["Hussein", "Alisha"]
        username = "Alishax"
        age = 25
        bio = ["Site manager"]
        file_name = str(file)
    add_user(Args)
    assert file.exists()