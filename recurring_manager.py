import json
import os
from datetime import datetime, timedelta

RECURRING_FILE = "recurring.json"

class RecurringManager:
    @staticmethod
    def load_recurring():
        if not os.path.exists(RECURRING_FILE):
            RecurringManager.save_recurring([])
            return []
        with open(RECURRING_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_recurring(recurring):
        with open(RECURRING_FILE, "w") as f:
            json.dump(recurring, f)

    @staticmethod
    def add_recurring(date, amount, category, description, frequency):
        recurring = RecurringManager.load_recurring()
        entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
            "frequency": frequency  # 'daily', 'weekly', 'monthly'
        }
        recurring.append(entry)
        RecurringManager.save_recurring(recurring)
        print("Recurring transaction added.")

    @staticmethod
    def get_due_transactions():
        recurring = RecurringManager.load_recurring()
        today = datetime.today().date()
        due = []
        for entry in recurring:
            last_date = datetime.strptime(entry["date"], "%d-%m-%Y").date()
            freq = entry["frequency"]
            next_date = last_date
            while next_date <= today:
                if next_date == today:
                    due.append(entry)
                if freq == "daily":
                    next_date += timedelta(days=1)
                elif freq == "weekly":
                    next_date += timedelta(weeks=1)
                elif freq == "monthly":
                    # Add one month (approximate)
                    month = next_date.month + 1 if next_date.month < 12 else 1
                    year = next_date.year + 1 if month == 1 else next_date.year
                    day = min(next_date.day, 28)  # avoid invalid dates
                    next_date = datetime(year, month, day).date()
                else:
                    break
        return due
