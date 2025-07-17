# Personal Finance Management System

A comprehensive personal finance management application with both CLI and GUI interfaces, allowing users to track income, expenses, manage budgets, and generate financial reports.

## Features

- User authentication (registration and login)
- Income and expense tracking
- Budget management by categories
- Monthly and yearly financial reports
- Category-wise spending analysis
- Dual interface support (CLI and GUI)
- Secure password handling
- SQLite database for data persistence

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI Interface

To start the graphical interface:
```bash
python finance_gui.py
```

The GUI provides intuitive access to all features:
- Login/Register through the welcome screen
- Add transactions using the transaction form
- Set budgets using the budget management panel
- View reports through the reporting section

### CLI Interface

The command-line interface supports all core functionalities:

1. **User Management**
   ```bash
   # Register new user
   python finance_manager.py register

   # Login
   python finance_manager.py login
   ```

2. **Transaction Management**
   ```bash
   # Add transaction
   python finance_manager.py add-transaction

   # View transactions
   python finance_manager.py view-transactions
   ```

3. **Budget Management**
   ```bash
   # Set budget
   python finance_manager.py set-budget

   # Check budget status
   python finance_manager.py check-budget
   ```

4. **Financial Reports**
   ```bash
   # Monthly report
   python finance_manager.py monthly-report

   # Yearly report
   python finance_manager.py yearly-report
   ```

## Project Structure

- `finance_manager.py`: Core application and CLI interface
- `finance_gui.py`: Graphical user interface
- `transactions.py`: Transaction management logic
- `budget.py`: Budget tracking functionality
- `reports.py`: Financial report generation
- `test_finance_manager.py`: Test suite
- `requirements.txt`: Project dependencies
- `EXPLAIN.md`: Technical documentation

## Database Schema

- **Users**: Stores user credentials and information
- **Transactions**: Records all financial transactions
- **Budgets**: Stores budget settings by category

## Security Features

- Password hashing using bcrypt
- Secure session management
- Input validation and sanitization
- No plaintext password storage

## Testing

Run the test suite:
```bash
python -m pytest test_finance_manager.py
```

## Dependencies

- bcrypt: Password hashing
- click: CLI interface
- tabulate: Data presentation
- pytest: Testing framework
- python-dotenv: Environment management
- tkinter: GUI (built-in)
- sqlite3: Database (built-in)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
