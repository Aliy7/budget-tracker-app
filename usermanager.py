from user import User
from budget import Budget
from expense import Expense
import json
import os
from json import JSONDecodeError

class UserManager:
    def __init__(self, file_name):
        self._file_name = file_name
    @property
    def file_name(self):
        return self._file_name
    
    @file_name.setter
    def file_name(self, value):
        if not value:
            ValueError("file not provided")
        self._file_name = value
    def save_user(self, new_user):
        users = {}
        try:
            if not os.path.exists(self._file_name) or os.path.getsize(self._file_name) == 0:
                raise FileNotFoundError
            with open(self._file_name, "r") as json_file:
                user_data = json.load(json_file)
                for row in user_data:
                    users[row['id']] = User(row['names'], row['username'], row['age'], row['bio'])


        except FileNotFoundError:
            pass
        dup_found = False
        for user in users.values():
            if (user.names == new_user.names and 
                user.username == new_user.username and 
                user.age == new_user.age and user.bio == new_user.bio):
                dup_found = True
              
        if not dup_found:
            users[new_user.id] = new_user
        if dup_found:
            print(f"User '{new_user.username}' already exists. No new files created.")
            raise SystemExit(1)
        
        user_list = []
        for user in sorted(users.values(), key=lambda userme: userme.id):
        
            user_list.append({
                    'id': user.id,
                    'names':user.names,
                    'username':user.username,
                    'age':user.age,
                    'bio': user.bio, 
                    "date": str(user.date),
                })
        with open(self._file_name, "w") as jsonfile:
            json.dump(user_list, jsonfile, indent=4)
        budgets_folder = "data/budgets"
        expenses_folder = "data/expenses"
        os.makedirs(budgets_folder, exist_ok=True)
        os.makedirs(expenses_folder, exist_ok=True)
        
        budget_path = os.path.join(budgets_folder, f"{new_user.username}_budgets.json")
        expense_path = os.path.join(expenses_folder, f"{new_user.username}_expenses.json")
        if not (os.path.exists(budget_path) and os.path.exists(expense_path)):

            if not os.path.exists(budget_path):
                with open(budget_path, "w") as f:
                    json.dump([], f, indent=4)

            if not os.path.exists(expense_path):
                with open(expense_path, "w") as f:
                    json.dump([], f, indent=4)
            
    
    def get_users(self):
        users = {}
        try:
            if not os.path.exists(self._file_name) or os.path.getsize(self._file_name) == 0:
                raise FileNotFoundError 
            with open(self._file_name, "r") as json_file:
                stored_user = json.load(json_file)
                for row in stored_user:
                    users[row['id']] = User(row['names'], row['username'], row['age'], row['bio'])
        except FileNotFoundError:
            pass
        return users
    
    def get_user_files(self, id):
        budget_storage = os.path.join("data", "budgets", f"{self._id}_budgets.json")
        expense_storage = os.path.join("expenses", f"{self._id}_expenses.json")
        return budget_storage, expense_storage

    def save_budgets(self, file_name, budget):
        try:
            if os.path.getsize(file_name) == 0:
                raise FileNotFoundError
            with open(file_name, "r") as jsonfile:
                budgets = json.load(jsonfile)
        except (FileNotFoundError, JSONDecodeError):  
            budgets = []
    
    
        budgets.append({
            "amount": budget.amount,
            "date": str(budget.date),
            "category": budget.category,
            "note": budget.note
        })

        with open(file_name, "w") as jsonfile:
            json.dump(budgets, jsonfile, indent=4)  
            
    def save_expenses(self, file_name, expense):
        
        try:
            with open(file_name, "r") as jsonfile:
                expenses = json.load(jsonfile)
                if not isinstance(expenses, list):
                    expenses = []
        except (FileNotFoundError, JSONDecodeError):
            expenses = []
        
        expenses.append(expense.to_json())
        
        with open(file_name, "w") as jsonfile:
            json.dump(expenses, jsonfile, indent=4)
        
        
       
   


                    
                        
            

                
