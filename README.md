# Personal Finance Management System

A command-line application for managing personal finances, tracking income and expenses, setting budgets, and generating financial reports.

## Features

- User Registration and Authentication
- Income and Expense Tracking
- Budget Management
- Monthly and Yearly Financial Reports
- Category-wise Expense Analysis
- Budget Status Monitoring

## Installation

1. Clone the repository or download the source code
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### User Management

1. Register a new user:
   ```bash
   python finance_manager.py register
   ```

2. Login:
   ```bash
   python finance_manager.py login
   ```

### Transaction Management

1. Add a new transaction:
   ```bash
   python finance_manager.py add-transaction
   ```
   You'll be prompted to enter:
   - Transaction type (income/expense)
   - Category
   - Amount
   - Description
   - Login credentials

### Budget Management

1. Set a budget for a category:
   ```bash
   python finance_manager.py set-budget
   ```

2. Check budget status:
   ```bash
   python finance_manager.py check-budget
   ```

### Reports

1. Generate monthly report:
   ```bash
   python finance_manager.py monthly-report
   ```

2. Generate yearly report:
   ```bash
   python finance_manager.py yearly-report
   ```

## Project Structure

- `finance_manager.py`: Main application file with CLI interface
- `transactions.py`: Transaction management functionality
- `budget.py`: Budget management functionality
- `reports.py`: Financial reporting functionality
- `requirements.txt`: Required Python packages

## Database Schema

### Users Table
- id (PRIMARY KEY)
- username (UNIQUE)
- password (hashed)
- created_at

### Transactions Table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- type (income/expense)
- category
- amount
- description
- date

### Budgets Table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- category
- amount
- month
- year

## Security Features

- Passwords are hashed using bcrypt
- SQLite database for data persistence
- Input validation and error handling

## Dependencies

- click: Command-line interface creation
- bcrypt: Password hashing
- sqlite3: Database management
- tabulate: Formatted table output
- pytest: Unit testing

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.