import json
import os

BUDGET_FILE = "budgets.json"

class BudgetManager:
    @staticmethod
    def load_budgets():
        if not os.path.exists(BUDGET_FILE):
            BudgetManager.save_budgets({})
            return {}
        with open(BUDGET_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_budgets(budgets):
        with open(BUDGET_FILE, "w") as f:
            json.dump(budgets, f)

    @staticmethod
    def set_budget(category, amount):
        budgets = BudgetManager.load_budgets()
        budgets[category] = amount
        BudgetManager.save_budgets(budgets)
        print(f"Budget for '{category}' set to ${amount}")

    @staticmethod
    def get_budget(category):
        budgets = BudgetManager.load_budgets()
        return budgets.get(category, None)

    @staticmethod
    def get_all_budgets():
        return BudgetManager.load_budgets()
