import click
import sqlite3
import bcrypt
from datetime import datetime
from pathlib import Path
from transactions import TransactionManager
from budget import BudgetManager
from reports import ReportGenerator

class FinanceManager:
    def __init__(self, db_path='finance.db'):
        self.db_path = db_path
        self.setup_database()
        self.transaction_manager = TransactionManager(db_path)
        self.budget_manager = BudgetManager(db_path)
        self.report_generator = ReportGenerator(db_path)

    def setup_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # Create transactions table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)

        # Create budgets table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)

        conn.commit()
        conn.close()

    def register_user(self, username, password):
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Hash the password
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

            cursor.execute(
                'INSERT INTO users (username, password) VALUES (?, ?)',
                (username, hashed)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def authenticate_user(self, username, password):
        """Authenticate a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        conn.close()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[1]):
            return result[0]  # Return user_id
        return None

@click.group()
def cli():
    """Personal Finance Management System"""
    pass

@cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def register(username, password):
    """Register a new user"""
    manager = FinanceManager()
    if manager.register_user(username, password):
        click.echo('Registration successful!')
    else:
        click.echo('Username already exists!')

@cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def login(username, password):
    """Login to the system"""
    manager = FinanceManager()
    user_id = manager.authenticate_user(username, password)
    if user_id:
        click.echo('Login successful!')
        return user_id
    else:
        click.echo('Invalid credentials!')
        return None

@cli.command()
@click.option('--type', type=click.Choice(['income', 'expense']), prompt=True)
@click.option('--category', prompt=True)
@click.option('--amount', type=float, prompt=True)
@click.option('--description', prompt=True)
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def add_transaction(type, category, amount, description, username, password):
    """Add a new transaction"""
    manager = FinanceManager()
    user_id = manager.authenticate_user(username, password)
    if user_id:
        if manager.transaction_manager.add_transaction(user_id, type, category, amount, description):
            click.echo('Transaction added successfully!')
        else:
            click.echo('Failed to add transaction!')
    else:
        click.echo('Authentication failed!')

@cli.command()
@click.option('--category', prompt=True)
@click.option('--amount', type=float, prompt=True)
@click.option('--month', type=int, prompt=True)
@click.option('--year', type=int, prompt=True)
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def set_budget(category, amount, month, year, username, password):
    """Set a budget for a category"""
    manager = FinanceManager()
    user_id = manager.authenticate_user(username, password)
    if user_id:
        if manager.budget_manager.set_budget(user_id, category, amount, month, year):
            click.echo('Budget set successfully!')
        else:
            click.echo('Failed to set budget!')
    else:
        click.echo('Authentication failed!')

@cli.command()
@click.option('--month', type=int, default=None)
@click.option('--year', type=int, default=None)
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def monthly_report(month, year, username, password):
    """Generate monthly financial report"""
    manager = FinanceManager()
    user_id = manager.authenticate_user(username, password)
    if user_id:
        report = manager.report_generator.generate_monthly_report(user_id, month, year)
        if report:
            click.echo(report)
        else:
            click.echo('Failed to generate report!')
    else:
        click.echo('Authentication failed!')

@cli.command()
@click.option('--year', type=int, default=None)
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def yearly_report(year, username, password):
    """Generate yearly financial report"""
    manager = FinanceManager()
    user_id = manager.authenticate_user(username, password)
    if user_id:
        report = manager.report_generator.generate_yearly_report(user_id, year)
        if report:
            click.echo(report)
        else:
            click.echo('Failed to generate report!')
    else:
        click.echo('Authentication failed!')

@cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def check_budget(username, password):
    """Check current budget status"""
    manager = FinanceManager()
    user_id = manager.authenticate_user(username, password)
    if user_id:
        status = manager.budget_manager.check_budget_status(user_id)
        if status:
            click.echo(status)
        else:
            click.echo('Failed to check budget status!')
    else:
        click.echo('Authentication failed!')

if __name__ == '__main__':
    cli()