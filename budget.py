# budget.py

import sqlite3

def set_budget(user_id, category, limit):
    """
    Sets or updates the budget for a specific category for a user.

    Args:
        user_id (int): The ID of the user.
        category (str): The category to set the budget for (e.g., 'Food').
        limit (float): The budget limit amount.
    """
    db = sqlite3.connect('finance.db')
    cursor = db.cursor()

    # 'INSERT OR REPLACE' is a handy SQLite command.
    # If a budget for this user/category exists, it updates it.
    # If not, it inserts a new one.
    cursor.execute(
        "INSERT OR REPLACE INTO budgets (user_id, category, limit_amount) VALUES (?, ?, ?)",
        (user_id, category, limit)
    )

    db.commit()
    db.close()
    print(f"✅ Budget for '{category}' set to ${limit:,.2f}.")

    # budget.py

from datetime import date # Make sure this import is at the top

# ... (set_budget function is here) ...

def check_spending_against_budget(user_id, category):
    """
    Checks current monthly spending against the budget for a category.

    Args:
        user_id (int): The ID of the user.
        category (str): The category to check.

    Returns:
        tuple: A tuple containing (is_over_budget, amount_over) or (False, 0)
               if no budget is set or not over budget.
    """
    db = sqlite3.connect('finance.db')
    cursor = db.cursor()

    # 1. Get the budget limit for the category
    cursor.execute(
        "SELECT limit_amount FROM budgets WHERE user_id = ? AND category = ?",
        (user_id, category)
    )
    result = cursor.fetchone()

    # If no budget is set for this category, we can't check it.
    if result is None:
        db.close()
        return (False, 0)

    limit_amount = result[0]

    # 2. Calculate total spending for the current month in that category
    current_month_str = date.today().strftime('%Y-%m')
    cursor.execute(
        """SELECT SUM(amount) FROM transactions
           WHERE user_id = ? AND category = ? AND type = 'expense' AND strftime('%Y-%m', date) = ?""",
        (user_id, category, current_month_str)
    )
    total_spent = cursor.fetchone()[0] or 0
    db.close()

    # 3. Compare and return the result
    if total_spent > limit_amount:
        amount_over = total_spent - limit_amount
        return (True, amount_over)
    else:
        return (False, 0)
    
# budget.py

def get_budgets_with_spending(user_id):
    """
    Retrieves all budgets for a user and calculates current spending for each.

    Returns:
        list: A list of dictionaries, each containing budget details and spending.
    """
    db = sqlite3.connect('finance.db')
    cursor = db.cursor()
    current_month_str = date.today().strftime('%Y-%m')

    # This SQL query joins the budgets table with the transactions table.
    # A LEFT JOIN ensures that all budgets are shown, even if there's no spending yet.
    # COALESCE(SUM(t.amount), 0) turns NULL (no spending) into 0.
    cursor.execute("""
        SELECT 
            b.category, 
            b.limit_amount,
            COALESCE(SUM(t.amount), 0) AS total_spent
        FROM 
            budgets b
        LEFT JOIN 
            transactions t ON b.category = t.category 
            AND t.user_id = b.user_id 
            AND t.type = 'expense' 
            AND strftime('%Y-%m', t.date) = ?
        WHERE 
            b.user_id = ?
        GROUP BY 
            b.category
    """, (current_month_str, user_id))

    results = cursor.fetchall()
    db.close()

    # Process the results into a more usable list of dictionaries
    budgets_overview = []
    for row in results:
        category, limit, spent = row
        remaining = limit - spent
        budgets_overview.append({
            'category': category,
            'limit': limit,
            'spent': spent,
            'remaining': remaining
        })

    return budgets_overview

