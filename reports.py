# reports.py

import sqlite3

def get_monthly_summary(user_id, year, month):
    """
    Calculates total income, expenses, savings, and a breakdown
    of expenses by category for a specific month.

    Returns:
        dict: A dictionary containing all report data.
    """
    db = sqlite3.connect('finance.db')
    cursor = db.cursor()
    month_str = f"{year}-{month:02d}"

    # --- Totals (same as before) ---
    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'income' AND strftime('%Y-%m', date) = ?",
        (user_id, month_str)
    )
    total_income = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE user_id = ? AND type = 'expense' AND strftime('%Y-%m', date) = ?",
        (user_id, month_str)
    )
    total_expenses = cursor.fetchone()[0] or 0

    # --- New: Expense Breakdown by Category ---
    # The GROUP BY clause groups rows with the same category together,
    # and SUM(amount) calculates the total for each group.
    cursor.execute(
        """SELECT category, SUM(amount) FROM transactions
           WHERE user_id = ? AND type = 'expense' AND strftime('%Y-%m', date) = ?
           GROUP BY category
           ORDER BY SUM(amount) DESC""",
        (user_id, month_str)
    )
    expense_breakdown = cursor.fetchall()

    db.close()

    savings = total_income - total_expenses

    # Return all data in one dictionary
    return {
        'income': total_income,
        'expenses': total_expenses,
        'savings': savings,
        'expense_breakdown': expense_breakdown
    }