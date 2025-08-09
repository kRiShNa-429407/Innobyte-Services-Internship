# Personal Finance Management Application

A command-line application built in Python to help users manage their personal finances by tracking income, expenses, setting budgets, and generating financial reports.

---

## Features

* **User Authentication**: Secure user registration and login system with password hashing.
* **Transaction Management**: Full CRUD (Create, Read, Update, Delete) functionality for income and expense records.
* **Financial Reporting**: Generate monthly summaries of total income, expenses, and net savings, including a detailed breakdown of spending by category.
* **Budgeting**: Set monthly spending budgets for different categories and receive automatic warnings when a budget is exceeded.
* **Data Persistence**: All user data is stored securely in an SQLite database.
* **Backup & Restore**: Functionality to create timestamped backups of the database and restore from them.
* **Unit Tested**: Key application logic for authentication and reporting is verified with unit tests.

---

## Installation & Setup

Follow these steps to get the application running on your local machine.

1.  **Clone the Repository**
    ```bash
    # Replace <your-repo-url> with your actual repository URL
    git clone <your-repo-url>
    cd finance_app
    ```

2.  **Create and Activate a Virtual Environment**
    * On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Initialize the Application**
    Run the main script once to create the database and necessary tables.
    ```bash
    python main.py
    ```

---

## Usage Guide

Once set up, run `python main.py` to start the application.

### Main Menu
* **Register**: Create a new user account with a unique username and a password.
* **Login**: Sign in to your existing account.
* **Create Backup**: Saves a timestamped copy of the current database to a `backups/` folder.
* **Restore from Backup**: Overwrites the current database with a selected backup file. **Use with caution!**
* **Exit**: Closes the application.

### Logged-In Menu
After logging in, you will have access to the following options:

* **Add Income/Expense**: Record a new transaction. You will be prompted for a category, amount, and an optional description.
* **View Transactions**: Displays a list of all your past transactions, sorted by most recent.
* **Delete a Transaction**: Shows a list of your transactions and prompts you for the ID of the one you wish to delete.
* **Update a Transaction**: Allows you to select a transaction by its ID and change its details.
* **View Financial Report**: Asks for a year and month to generate a summary of your income, expenses, and a breakdown of spending by category.
* **Set Budget**: Allows you to set or update a monthly spending limit for a specific category (e.g., "Food", "Transport").
* **View Budgets**: Shows a summary of all your set budgets, how much you've spent, and how much remains for the current month.
* **Logout**: Logs you out and returns you to the main menu.

---

## Running Tests

The project includes a suite of unit tests to ensure key functionality is working correctly. To run the tests, navigate to the project's root directory in your terminal and run:

```bash
python -m unittest discover