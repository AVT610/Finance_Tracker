import json
import os

CATEGORIES_FILE = "categories.json"
DEFAULT_CATEGORIES = ["Income", "Expense"]

class CategoryManager:
    @staticmethod
    def load_categories():
        if not os.path.exists(CATEGORIES_FILE):
            CategoryManager.save_categories(DEFAULT_CATEGORIES)
            return DEFAULT_CATEGORIES.copy()
        with open(CATEGORIES_FILE, "r") as f:
            return json.load(f)

    @staticmethod
    def save_categories(categories):
        with open(CATEGORIES_FILE, "w") as f:
            json.dump(categories, f)

    @staticmethod
    def add_category(category):
        categories = CategoryManager.load_categories()
        if category in categories:
            print("Category already exists.")
            return False
        categories.append(category)
        CategoryManager.save_categories(categories)
        print(f"Category '{category}' added.")
        return True

    @staticmethod
    def edit_category(old, new):
        categories = CategoryManager.load_categories()
        if old not in categories:
            print("Category not found.")
            return False
        if new in categories:
            print("New category name already exists.")
            return False
        idx = categories.index(old)
        categories[idx] = new
        CategoryManager.save_categories(categories)
        print(f"Category '{old}' renamed to '{new}'.")
        return True

    @staticmethod
    def delete_category(category):
        categories = CategoryManager.load_categories()
        if category not in categories:
            print("Category not found.")
            return False
        categories.remove(category)
        CategoryManager.save_categories(categories)
        print(f"Category '{category}' deleted.")
        return True
