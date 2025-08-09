# main.py - Updated version

from database import initialize_database
from reports import get_monthly_summary # <-- Add this new import
from auth import register_user, login_user
from transactions import add_transaction # <-- Import this
from transactions import add_transaction, view_transactions # <-- Add view_transactions
from budget import set_budget
from budget import set_budget, get_budgets_with_spending
from backup import create_backup
from backup import create_backup, restore_from_backup


def handle_add_transaction(user_id, trans_type):
    """
    Handles the user input for adding a new transaction.
    """
    category = input(f"Enter {trans_type} category (e.g., Salary, Food, Rent): ")
    try:
        amount = float(input(f"Enter amount: $"))
    except ValueError:
        print("❌ Invalid amount. Please enter a number.")
        return
    description = input(f"Enter a brief description (optional): ")
    add_transaction(user_id, trans_type, category, amount, description)

def handle_delete_transaction(user_id):
    """Handles the user input for deleting a transaction."""
    transactions = view_transactions(user_id)
    if not transactions:
        print("\nNo transactions to delete.")
        return
    
    print("\n--- Select a Transaction to Delete ---")
    print(f"{'ID':<5}{'Date':<12}{'Type':<10}{'Category':<15}{'Amount':>10}")
    print("-" * 65)
    for t in transactions:
        trans_id, date, trans_type, category, amount, desc = t
        print(f"{trans_id:<5}{date:<12}{trans_type:<10}{category:<15}${amount:>9.2f}")

    try:
        choice = int(input("\nEnter the ID of the transaction to delete (or 0 to cancel): "))
        if choice == 0:
            return
        
        if delete_transaction(choice, user_id):
            print("✅ Transaction deleted successfully.")
        else:
            print("❌ Error: Transaction ID not found or does not belong to you.")
    except ValueError:
        print("❌ Invalid ID. Please enter a number.")


def handle_update_transaction(user_id):
    """Handles the user input for updating a transaction."""
    transactions = view_transactions(user_id)
    if not transactions:
        print("\nNo transactions to update.")
        return

    print("\n--- Select a Transaction to Update ---")
    print(f"{'ID':<5}{'Date':<12}{'Type':<10}{'Category':<15}{'Amount':>10}")
    print("-" * 65)
    for t in transactions:
        trans_id, date, trans_type, category, amount, desc = t
        print(f"{trans_id:<5}{date:<12}{trans_type:<10}{category:<15}${amount:>9.2f}")

    try:
        trans_id_to_update = int(input("\nEnter the ID of the transaction to update (or 0 to cancel): "))
        if trans_id_to_update == 0:
            return

        print("\nEnter the new details:")
        new_category = input("Enter new category: ")
        new_amount = float(input("Enter new amount: $"))
        new_desc = input("Enter new description: ")
        
        if update_transaction(trans_id_to_update, user_id, new_amount, new_category, new_desc):
            print("✅ Transaction updated successfully.")
        else:
            print("❌ Error: Transaction ID not found or does not belong to you.")
    except ValueError:
        print("❌ Invalid input. Please enter numbers for ID and amount.")

def handle_view_reports(user_id):
    """Handles user input for viewing monthly financial reports."""
    try:
        year = int(input("Enter the year (e.g., 2025): "))
        month = int(input("Enter the month (1-12): "))
        if not 1 <= month <= 12:
            print("❌ Invalid month. Please enter a number between 1 and 12.")
            return
    except ValueError:
        print("❌ Invalid input. Please enter numbers for year and month.")
        return

    summary = get_monthly_summary(user_id, year, month)

    # --- Print Main Summary ---
    print(f"\n--- Monthly Summary for {year}-{month:02d} ---")
    print(f"Total Income:   ${summary['income']:>10,.2f}")
    print(f"Total Expenses: ${summary['expenses']:>10,.2f}")
    print("-" * 30)
    print(f"Net Savings:    ${summary['savings']:>10,.2f}")

    # --- Print Expense Breakdown ---
    if summary['expense_breakdown']:
        print("\n--- Expense Breakdown by Category ---")
        for category, amount in summary['expense_breakdown']:
            print(f"{category:<20} ${amount:>10,.2f}")
    else:
        print("\nNo expenses to break down for this month.")

def handle_set_budget(user_id):
    """Handles user input for setting a budget."""
    category = input("Enter the category to set a budget for (e.g., Food): ")
    try:
        limit = float(input("Enter the budget limit amount: $"))
        set_budget(user_id, category, limit)
    except ValueError:
        print("❌ Invalid amount. Please enter a number.")

def handle_view_budgets(user_id):
    """Handles the logic for viewing budget status."""
    budgets = get_budgets_with_spending(user_id)

    if not budgets:
        print("\nYou have not set any budgets yet.")
        return

    print("\n--- Your Budget Status for this Month ---")
    print(f"{'Category':<20} {'Spent':>12} / {'Budget':<12} {'Remaining':>12}")
    print("-" * 62)

    for budget in budgets:
        spent_str = f"${budget['spent']:,.2f}"
        limit_str = f"${budget['limit']:,.2f}"
        remaining_str = f"${budget['remaining']:,.2f}"

        # Simple progress bar
        progress = budget['spent'] / budget['limit']
        bar_length = 10
        filled_length = int(bar_length * progress)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)

        print(f"{budget['category']:<20} {spent_str:>12} / {limit_str:<12} {remaining_str:>12}  [{bar}]")

# Replace the existing logged_in_menu in main.py

# Replace the existing logged_in_menu in main.py
def logged_in_menu(user_id):
    """Displays the menu for a logged-in user."""
    while True:
        print(f"\n--- Main Menu (Logged in as User ID: {user_id}) ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Delete a Transaction")
        print("5. Update a Transaction")
        print("6. View Financial Report") # <-- New option
        print("7. Set Budget")
        print("8. View Budget")
        print("9. Logged Out")

        choice = input("Please choose an option: ")

        if choice == '1':
            handle_add_transaction(user_id, 'income')
        elif choice == '2':
            handle_add_transaction(user_id, 'expense')
        elif choice == '3':
            # (This is your existing view logic)
            transactions = view_transactions(user_id)
            if not transactions:
                print("\nNo transactions found.")
            else:
                print("\n--- Your Recent Transactions ---")
                print(f"{'ID':<5}{'Date':<12}{'Type':<10}{'Category':<15}{'Amount':>10}  {'Description'}")
                print("-" * 65)
                for t in transactions:
                    trans_id, date, trans_type, category, amount, desc = t
                    print(f"{trans_id:<5}{date:<12}{trans_type:<10}{category:<15}${amount:>9.2f}  {desc}")
        elif choice == '4':
            handle_delete_transaction(user_id)
        elif choice == '5':
            handle_update_transaction(user_id)
        elif choice == '6':
            handle_view_reports(user_id) 
        elif choice == '7':
            handle_set_budget(user_id)
        elif choice == '8':
            handle_view_budgets(user_id)
        elif choice == '9':
            print("You have been logged out.")
            break
        else:
            print("Invalid option.")

# Add this new function to main.py
# main.py



# Replace the existing main_menu in main.py
def main_menu():
    """Displays the main menu for login or registration."""
    initialize_database()
    while True:
        print("\nWelcome to your Personal Finance Manager!")
        print("1. Register")
        print("2. Login")
        print("3. Create Backup")
        print("4. Restore from Backup") # <-- New option
        print("5. Exit")

        choice = input("Please choose an option: ")

        if choice == '1':
            register_user(input("Enter a new username: "), input("Enter a password: "))
        elif choice == '2':
            user_id = login_user(input("Enter your username: "), input("Enter your password: "))
            if user_id:
                logged_in_menu(user_id)
        elif choice == '3':
            create_backup()
        elif choice == '4':
            restore_from_backup() # <-- Call the new handler
        elif choice == '5':
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice, please try again.")