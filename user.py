import json, os
import uuid
import argparse
from datetime import date
class User:
    def __init__(self, names, username, age, bio):
        self._id = None
        self.date = date.today()
        self.id = self.user_id_generator()
        self.names = names
        self.username = username
        self.age = age
        self.bio = bio
        
    def __str__(self):
        user_details = {
            "id":self.id,
            "names":self.names,
            "username":self.username,
            "age":self.age,
            "bio":self.bio, 
            "Date": str(self.date),

        }
        return json.dumps(user_details,indent=4)
    
    @staticmethod
    def user_id_generator():
        """Generate a unique user ID using UUID4."""
        id = str(uuid.uuid4())
        return(id)
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        self._date = value
    
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        if self._id is not None:
            raise AttributeError("Id has been set already cannot be changed")
        if not value:
            raise ValueError("Id cannot be empty: ")
        self._id = value
    
    @property
    def names(self):
        return self._names
    
    @names.setter
    def names(self, value):
        if not value:
            raise ValueError("Names, cannot be empty")
        self._names = value
        
    @property
    def age(self):
        return self._age
    
    def age(self, value):
        if value < 0:
            raise ValueError("Age cannot be negative.")
        self._age = value
        
    @property
    def bio(self):
        return self._bio

    @bio.setter
    def bio(self, value):
        self._bio = value
    
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value
        
    def delete_user(self, username):
        
        try:
            users=json.load(open("user.json"))
        except FileNotFoundError:
            print("User file does not exist")
            return False
        users = [user for user in users if user["username"].lower() != self.username.lower()]
        json.dump(users, open("user.json", "w"), indent=4)
        
        for path in [
            f"data/budgets/{username.lower()}_budgets.json",
            f"data/expenses/{username.lower()}_expenses.json"
        ]:
            if os.path.exists(path):
                os.remove(path)
        print(f"User '{self.username}' deleted successfully.")
        
        return True
    
    def update_user(self, username):
        
        try:
            users=json.load(open("user.json"))
        except FileNotFoundError:
            print("User file does not exist")
            return False
        updated = False
        for user in users:
            if user["username"].lower() == username.lower():
                user["names"] = self.new_names
                user["age"] = self.new_age
                user["bio"] = self.new_bio
                

                
                updated = True
                
        if not updated:
            print(f"user {username} not found")
            return False
        
        json.dump(users, open("user.json", "w"), indent=4)
        print(f"User '{username}' updated successfully.")

        return True
        
    def cli_arg_processor():
        parser = argparse.ArgumentParser(
            description="Command-line interface to manage users, budgets, and expenses."
        )

        # User creation arguments
        parser.add_argument("-n", "--name", nargs="+", help="User's first and last name")
        parser.add_argument("-un", "--username", help="Unique username (used for file naming)")
        parser.add_argument("-a", "--age", type=int, help="User's age")
        parser.add_argument("-b", "--bio", nargs="+", help="Short biography or job description")

        #budget args
        parser.add_argument("--budget", action="store_true", help="Add or update a user's budget")

        # expense args
        parser.add_argument("--expense", action="store_true", help="Add an expense for a user")

        # shared args budget and expenses
        parser.add_argument("--amount", type=float, help="Amount for budget or expense")
        parser.add_argument("--category", type=str, help="Category name (e.g. Food, Bills, Rent)")
        parser.add_argument("--note", type=str, help="Optional note or description")

        # general args 
        parser.add_argument("file_name", nargs="?", default="user.json", help="JSON file to store users")

        parser.add_argument("--delete_user", action="store_true",help="Pass user name after argumment" )
        
        """The update user args """
        parser.add_argument("--update_user", action="store_true", help="Update an existing user")
        parser.add_argument("--new_name", type=str, help="New full name for the user")
        parser.add_argument("--new_age", type=int, help="New age for the user")
        parser.add_argument("--new_bio", type=str, help="New bio for the user")

        args = parser.parse_args()
        return args


