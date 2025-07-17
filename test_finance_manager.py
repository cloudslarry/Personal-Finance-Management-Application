import pytest
import os
from finance_manager import FinanceManager
from transactions import TransactionManager
from budget import BudgetManager
from reports import ReportGenerator
from datetime import datetime

@pytest.fixture
def test_db():
    """Create a test database and clean it up after tests"""
    db_path = 'test_finance.db'
    yield db_path
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def finance_manager(test_db):
    """Create a finance manager instance for testing"""
    return FinanceManager(test_db)

@pytest.fixture
def test_user(finance_manager):
    """Create a test user and return credentials"""
    username = 'testuser'
    password = 'testpass123'
    finance_manager.register_user(username, password)
    user_id = finance_manager.authenticate_user(username, password)
    return {'username': username, 'password': password, 'user_id': user_id}

def test_user_registration(finance_manager):
    """Test user registration functionality"""
    assert finance_manager.register_user('user1', 'pass123')
    # Test duplicate username
    assert not finance_manager.register_user('user1', 'different_pass')

def test_user_authentication(finance_manager):
    """Test user authentication functionality"""
    finance_manager.register_user('user2', 'pass123')
    # Test valid credentials
    assert finance_manager.authenticate_user('user2', 'pass123') is not None
    # Test invalid password
    assert finance_manager.authenticate_user('user2', 'wrong_pass') is None
    # Test non-existent user
    assert finance_manager.authenticate_user('nonexistent', 'pass123') is None

def test_transaction_management(finance_manager, test_user):
    """Test transaction management functionality"""
    tm = TransactionManager(finance_manager.db_path)
    user_id = test_user['user_id']

    # Test adding transactions
    assert tm.add_transaction(user_id, 'income', 'Salary', 5000, 'Monthly salary')
    assert tm.add_transaction(user_id, 'expense', 'Food', 100, 'Groceries')

    # Test getting transactions
    transactions = tm.get_transactions(user_id)
    assert transactions is not None
    assert 'Salary' in transactions
    assert 'Food' in transactions

    # Test balance calculation
    balance = tm.get_balance(user_id)
    assert balance == 4900  # 5000 - 100

def test_budget_management(finance_manager, test_user):
    """Test budget management functionality"""
    bm = BudgetManager(finance_manager.db_path)
    user_id = test_user['user_id']
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Test setting budget
    assert bm.set_budget(user_id, 'Food', 500, current_month, current_year)
    assert bm.set_budget(user_id, 'Entertainment', 200, current_month, current_year)

    # Test getting budgets
    budgets = bm.get_budgets(user_id, current_month, current_year)
    assert budgets is not None
    assert 'Food' in budgets
    assert 'Entertainment' in budgets

    # Test budget status
    status = bm.check_budget_status(user_id, current_month, current_year)
    assert status is not None
    assert 'Food' in status
    assert 'Entertainment' in status

def test_report_generation(finance_manager, test_user):
    """Test report generation functionality"""
    rg = ReportGenerator(finance_manager.db_path)
    tm = TransactionManager(finance_manager.db_path)
    user_id = test_user['user_id']
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Add some test transactions
    tm.add_transaction(user_id, 'income', 'Salary', 5000, 'Monthly salary')
    tm.add_transaction(user_id, 'expense', 'Food', 100, 'Groceries')
    tm.add_transaction(user_id, 'expense', 'Entertainment', 150, 'Movies')

    # Test monthly report
    monthly_report = rg.generate_monthly_report(user_id, current_month, current_year)
    assert monthly_report is not None
    assert 'Monthly Financial Report' in monthly_report
    assert 'Total Income: $5000.00' in monthly_report
    assert 'Total Expenses: $250.00' in monthly_report

    # Test yearly report
    yearly_report = rg.generate_yearly_report(user_id, current_year)
    assert yearly_report is not None
    assert 'Yearly Financial Report' in yearly_report
    assert 'Total Income: $5000.00' in yearly_report
    assert 'Total Expenses: $250.00' in yearly_report

    # Test category analysis
    analysis = rg.generate_category_analysis(user_id)
    assert analysis is not None
    assert 'Food' in analysis
    assert 'Entertainment' in analysis