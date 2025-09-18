from budget_manager import BudgetManager
def set_budget():
    categories = CategoryManager.load_categories()
    print("Available categories:")
    for idx, cat in enumerate(categories, 1):
        print(f"{idx}. {cat}")
    cat_choice = input("Select category by number: ")
    try:
        cat_idx = int(cat_choice) - 1
        category = categories[cat_idx]
    except (ValueError, IndexError):
        print("Invalid category. Defaulting to first category.")
        category = categories[0]
    amount = input(f"Enter monthly budget for '{category}': $")
    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount. Defaulting to $0.")
        amount = 0.0
    BudgetManager.set_budget(category, amount)

def view_budgets():
    budgets = BudgetManager.get_all_budgets()
    print("\nBudgets:")
    for cat, amt in budgets.items():
        print(f"{cat}: ${amt}")

def show_budget_progress():
    budgets = BudgetManager.get_all_budgets()
    df = pd.read_csv(CSV.CSV_FILE)
    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
    this_month = datetime.today().strftime("%Y-%m")
    df["month"] = df["date"].dt.strftime("%Y-%m")
    month_df = df[df["month"] == this_month]
    print(f"\nBudget Progress for {this_month}:")
    for cat, budget in budgets.items():
        spent = month_df[month_df["category"] == cat]["amount"].sum()
        print(f"{cat}: Spent ${spent:.2f} / Budget ${budget:.2f}")
        if spent > budget:
            print(f"  Over budget by ${spent-budget:.2f}!")
from fpdf import FPDF
def export_to_excel():
    df = pd.read_csv(CSV.CSV_FILE)
    file_name = input("Enter Excel file name (e.g., export.xlsx): ")
    df.to_excel(file_name, index=False)
    print(f"Data exported to {file_name}")

def export_to_pdf():
    df = pd.read_csv(CSV.CSV_FILE)
    file_name = input("Enter PDF file name (e.g., export.pdf): ")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    col_width = pdf.w / (len(df.columns) + 1)
    row_height = pdf.font_size * 1.5
    # Header
    for col in df.columns:
        pdf.cell(col_width, row_height, col, border=1)
    pdf.ln(row_height)
    # Rows
    for _, row in df.iterrows():
        for item in row:
            pdf.cell(col_width, row_height, str(item), border=1)
        pdf.ln(row_height)
    pdf.output(file_name)
    print(f"Data exported to {file_name}")

def import_from_csv():
    file_name = input("Enter CSV file name to import: ")
    try:
        df = pd.read_csv(file_name)
        df.to_csv(CSV.CSV_FILE, mode='a', header=False, index=False)
        print(f"Data imported from {file_name}")
    except Exception as e:
        print(f"Import failed: {e}")
from recurring_manager import RecurringManager
def add_recurring():
    date = get_date("Enter the start date for recurring transaction (dd-mm-yyyy): ")
    amount = get_amount()
    categories = CategoryManager.load_categories()
    print("Available categories:")
    for idx, cat in enumerate(categories, 1):
        print(f"{idx}. {cat}")
    cat_choice = input("Select category by number: ")
    try:
        cat_idx = int(cat_choice) - 1
        category = categories[cat_idx]
    except (ValueError, IndexError):
        print("Invalid category. Defaulting to first category.")
        category = categories[0]
    description = get_descriptipn()
    print("Frequency options: daily, weekly, monthly")
    frequency = input("Enter frequency: ").lower()
    if frequency not in ["daily", "weekly", "monthly"]:
        print("Invalid frequency. Defaulting to monthly.")
        frequency = "monthly"
    RecurringManager.add_recurring(date, amount, category, description, frequency)

import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_date, get_descriptipn
from category_manager import CategoryManager
import matplotlib.pyplot as plt
from user_auth import UserAuth



class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transactions found in the given date range.")
        else:
            print(
                f"Transactions from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered_df.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )

            total_income = filtered_df[filtered_df["category"] == "Income"][
                "amount"
            ].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"][
                "amount"
            ].sum()
            print("\nSummary:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ",
        allow_default=True,
    )
    amount = get_amount()
    categories = CategoryManager.load_categories()
    print("Available categories:")
    for idx, cat in enumerate(categories, 1):
        print(f"{idx}. {cat}")
    cat_choice = input("Select category by number: ")
    try:
        cat_idx = int(cat_choice) - 1
        category = categories[cat_idx]
    except (ValueError, IndexError):
        print("Invalid category. Defaulting to first category.")
        category = categories[0]
    description = get_descriptipn()
    CSV.add_entry(date, amount, category, description)


    CSV.initialize_csv()
    date = get_date(
        "Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ",
        allow_default=True,
    )
    amount = get_amount()
    categories = CategoryManager.load_categories()
    print("Available categories:")
    for idx, cat in enumerate(categories, 1):
        print(f"{idx}. {cat}")
    cat_choice = input("Select category by number: ")
    try:
        cat_idx = int(cat_choice) - 1
        category = categories[cat_idx]
    except (ValueError, IndexError):
        print("Invalid category. Defaulting to first category.")
        category = categories[0]
    description = get_descriptipn()
    CSV.add_entry(date, amount, category, description)



def plot_transactions(df):
    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
    df.set_index("date", inplace=True)

    print("\nChoose plot type:")
    print("1. Line chart: Income and Expenses Over Time")
    print("2. Pie chart: Category Breakdown")
    print("3. Bar chart: Monthly Trends")
    plot_choice = input("Enter your choice (1-3): ")

    if plot_choice == "1":
        income_df = (
            df[df["category"] == "Income"]
            .resample("D")
            .sum()
            .reindex(df.index, fill_value=0)
        )
        expense_df = (
            df[df["category"] == "Expense"]
            .resample("D")
            .sum()
            .reindex(df.index, fill_value=0)
        )
        plt.figure(figsize=(10, 5))
        plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
        plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Income and Expenses Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()
    elif plot_choice == "2":
        cat_sum = df.groupby("category")["amount"].sum()
        plt.figure(figsize=(7, 7))
        plt.pie(cat_sum, labels=cat_sum.index, autopct="%1.1f%%", startangle=140)
        plt.title("Category Breakdown")
        plt.show()
    elif plot_choice == "3":
        df["month"] = df.index.to_period("M")
        monthly = df.groupby(["month", "category"])["amount"].sum().unstack(fill_value=0)
        monthly.plot(kind="bar", stacked=True, figsize=(10, 6))
        plt.xlabel("Month")
        plt.ylabel("Amount")
        plt.title("Monthly Trends by Category")
        plt.legend()
        plt.tight_layout()
        plt.show()
    else:
        print("Invalid choice.")



def main():
    print("Welcome to Finance Tracker!")
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        auth_choice = input("Enter your choice (1-3): ")
        if auth_choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            if UserAuth.login(username, password):
                break
        elif auth_choice == "2":
            username = input("Choose a username: ")
            password = input("Choose a password: ")
            UserAuth.register(username, password)
        elif auth_choice == "3":
            print("Exiting...")
            return
        else:
            print("Invalid choice. Enter 1, 2 or 3.")

    # Authenticated user menu
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and summary within a date range")
        print("3. Manage categories")
        print("4. Manage recurring transactions")
        print("5. Export to Excel")
        print("6. Export to PDF")
        print("7. Import from CSV")
        print("8. Set monthly budget")
        print("9. View budgets")
        print("10. Show budget progress")
        print("11. Logout")
        choice = input("Enter your choice (1-11): ")

        # Automatically add due recurring transactions for today
        due = RecurringManager.get_due_transactions()
        for entry in due:
            CSV.add_entry(entry["date"], entry["amount"], entry["category"], entry["description"])

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = CSV.get_transactions(start_date, end_date)
            if input("Do you want to see a plot? (y/n) ").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            while True:
                print("\nCategory Management:")
                print("1. Add category")
                print("2. Edit category")
                print("3. Delete category")
                print("4. Back")
                cat_mgmt = input("Choose an option (1-4): ")
                if cat_mgmt == "1":
                    new_cat = input("Enter new category name: ")
                    CategoryManager.add_category(new_cat)
                elif cat_mgmt == "2":
                    old_cat = input("Enter category to edit: ")
                    new_cat = input("Enter new name: ")
                    CategoryManager.edit_category(old_cat, new_cat)
                elif cat_mgmt == "3":
                    del_cat = input("Enter category to delete: ")
                    CategoryManager.delete_category(del_cat)
                elif cat_mgmt == "4":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "4":
            while True:
                print("\nRecurring Transactions Management:")
                print("1. Add recurring transaction")
                print("2. Back")
                rec_mgmt = input("Choose an option (1-2): ")
                if rec_mgmt == "1":
                    add_recurring()
                elif rec_mgmt == "2":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "5":
            export_to_excel()
        elif choice == "6":
            export_to_pdf()
        elif choice == "7":
            import_from_csv()
        elif choice == "8":
            set_budget()
        elif choice == "9":
            view_budgets()
        elif choice == "10":
            show_budget_progress()
        elif choice == "11":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Enter a number between 1 and 11.")


if __name__ == "__main__":
    main()