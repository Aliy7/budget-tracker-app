import datetime
import json
from datetime import date
class Budget:
    def __init__(self, amount, category, note):
        self._amount = 0
        self.date = date.today()
        self.amount = amount
        self.category = category
        self.note = note
    
    def __str__(self):
        budget = {
            "Amount":self.amount,
            "Date": str(self.date),
            "category":self.category,
            "note to self":self.note
        }
        return json.dumps(budget,indent=4)

    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, value):
        self._date = value
    
    @property
    def amount(self):
        return self._amount 
    
    @amount.setter
    def amount(self, value):
        self._amount = value
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        self._category = value
    
    @property
    def note(self):
        return self._note
    
    @note.setter
    def note(self, value):
        self._note = value
        
    def deposit(self, amount_to_deposit):
        
        if amount_to_deposit < 0:
            raise ValueError("Amount cannot be negative number")
        self._amount += amount_to_deposit
    
    def withdraw(self, amount_to_withdraw):
        if amount_to_withdraw < 0:
            raise ValueError("You cannot withdraw negative amount")
        elif amount_to_withdraw <= self._amount:
            self._amount -= amount_to_withdraw
        else:
            raise ValueError("Insufficient funds")
        return self._amount
        
    
    def get_balance(self):
        return str(self._amount)
    
    def transfer(self, amount, target_budget):
        if self._amount <= 0:
            raise ValueError("No sufficient fund")
        elif self._amount > 0:
            self._amount -= amount
            target_budget._amount += amount
        return target_budget
    
    
