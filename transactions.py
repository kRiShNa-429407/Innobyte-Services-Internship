## This file will handle all logic related to income and expenses.

import sqlite3
from datetime import date
from budget import check_spending_against_budget

def add_transaction(user_id, trans_type, category, amount, description):
    """
    Adds a new income or expense record to the transactions table.

    Args:
        user_id (int): The ID of the user adding the transaction.
        trans_type (str): The type of transaction ('income' or 'expense').
        category (str): The category of the transaction (e.g., 'Salary', 'Food').
        amount (float): The amount of the transaction.
        description (str): A brief description of the transaction.
    """
    db = sqlite3.connect('finance.db')
    cursor = db.cursor()

    # Get the current date in YYYY-MM-DD format
    current_date = date.today().isoformat()

    cursor.execute(
        """INSERT INTO transactions (user_id, type, category, amount, date, description)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, trans_type, category, amount, current_date, description)
    )

    db.commit()
    db.close()
    print(f"✅ {trans_type.capitalize()} of ${amount} added successfully.")

     # --- NEW: Check budget after adding an expense ---
    if trans_type == 'expense':
        is_over, amount_over = check_spending_against_budget(user_id, category)
        if is_over:
            print(f"⚠️  Warning: You have exceeded your budget for '{category}' by ${amount_over:,.2f} this month.")


def view_transactions(user_id):
    """
    Retrieves and returns all transactions for a specific user.

    Args:
        user_id (int): The ID of the user whose transactions to view.

    Returns:
        list: A list of tuples, where each tuple is a transaction record.
    """
    db = sqlite3.connect('finance.db')
    cursor = db.cursor()
    cursor.execute(
        """SELECT date, type, category, amount, description FROM transactions
           WHERE user_id = ? ORDER BY date DESC""",
        (user_id,)
    )
    transactions = cursor.fetchall()
    db.close()
    return transactions

def delete_transaction(transaction_id, user_id):
    """Deletes a specific transaction belonging to a user."""
    db = sqlite3.connect('finance.db')
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM transactions WHERE id = ? AND user_id = ?",
        (transaction_id, user_id)
    )
    success = cursor.rowcount > 0
    db.commit()
    db.close()
    return success


def update_transaction(transaction_id, user_id, new_amount, new_category, new_desc):
    """Updates the details of a specific transaction."""
    db = sqlite3.connect('finance.db')
    cursor = db.cursor()
    cursor.execute(
        """UPDATE transactions 
           SET amount = ?, category = ?, description = ?
           WHERE id = ? AND user_id = ?""",
        (new_amount, new_category, new_desc, transaction_id, user_id)
    )
    success = cursor.rowcount > 0
    db.commit()
    db.close()
    return success