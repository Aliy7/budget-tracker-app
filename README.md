# Budget Tracker App

A simple command-line budgeting and expense tracker built with Python.

This tool lets users create accounts, set budgets, record expenses, and calculate remaining balances — all stored locally in JSON files.  
It’s designed for easy personal finance tracking without needing a database or internet connection.

---

## Features
- Add, update, or delete users  
- Add budgets and record expenses  
- Prevent duplicate user creation  
- Automatic balance calculation  
- Separate data files for each user  

---

## Quick Start

```bash
# Clone repository
git clone https://github.com/Aliy7/budget-tracker-app.git
cd budget-tracker-app

# Install dependencies
pip install -r requirements.txt


# Create a new user
python project.py -n "Sarah Khan" --username "sarahk" -a 29 -b "Graphic Designer"

# Add a budget
python project.py --username sarahk --budget --amount 2600 --category "Car bills" --note "General spending"

# Record an expense
python project.py --username sarahk --expense --amount 250 --category "Bills" --note "Electricity and internet"

# Update user info
python project.py --update_user --username sarahk --new_name "Sarah Hussein" --new_age 30 --new_bio "Lead Designer"

# Delete a user
python project.py --delete_user --username sarahk
