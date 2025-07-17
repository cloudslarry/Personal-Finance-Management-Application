from datetime import datetime
import sqlite3
from tabulate import tabulate

class TransactionManager:
    def __init__(self, db_path='finance.db'):
        self.db_path = db_path

    def add_transaction(self, user_id, type, category, amount, description=None):
        """Add a new transaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO transactions (user_id, type, category, amount, description)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, type, category, amount, description))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding transaction: {e}")
            return False
        finally:
            conn.close()

    def update_transaction(self, transaction_id, user_id, type=None, category=None, 
                          amount=None, description=None):
        """Update an existing transaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Get current transaction data
            cursor.execute("""
                SELECT type, category, amount, description 
                FROM transactions 
                WHERE id = ? AND user_id = ?
            """, (transaction_id, user_id))
            current = cursor.fetchone()

            if not current:
                return False

            # Update with new values or keep current ones
            new_type = type if type else current[0]
            new_category = category if category else current[1]
            new_amount = amount if amount else current[2]
            new_description = description if description else current[3]

            cursor.execute("""
                UPDATE transactions 
                SET type = ?, category = ?, amount = ?, description = ? 
                WHERE id = ? AND user_id = ?
            """, (new_type, new_category, new_amount, new_description, 
                  transaction_id, user_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating transaction: {e}")
            return False
        finally:
            conn.close()

    def delete_transaction(self, transaction_id, user_id):
        """Delete a transaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute("""
                DELETE FROM transactions 
                WHERE id = ? AND user_id = ?
            """, (transaction_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting transaction: {e}")
            return False
        finally:
            conn.close()

    def get_transactions(self, user_id, start_date=None, end_date=None, 
                        transaction_type=None, category=None):
        """Get transactions with optional filters"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = "SELECT * FROM transactions WHERE user_id = ?"
        params = [user_id]

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)
        if transaction_type:
            query += " AND type = ?"
            params.append(transaction_type)
        if category:
            query += " AND category = ?"
            params.append(category)

        query += " ORDER BY date DESC"

        try:
            cursor.execute(query, params)
            transactions = cursor.fetchall()
            headers = ['ID', 'User ID', 'Type', 'Category', 'Amount', 
                      'Description', 'Date']
            return tabulate(transactions, headers=headers, tablefmt='grid')
        except sqlite3.Error as e:
            print(f"Error retrieving transactions: {e}")
            return None
        finally:
            conn.close()

    def get_balance(self, user_id):
        """Calculate current balance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Calculate total income
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) 
                FROM transactions 
                WHERE user_id = ? AND type = 'income'
            """, (user_id,))
            total_income = cursor.fetchone()[0]

            # Calculate total expenses
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) 
                FROM transactions 
                WHERE user_id = ? AND type = 'expense'
            """, (user_id,))
            total_expenses = cursor.fetchone()[0]

            return total_income - total_expenses
        except sqlite3.Error as e:
            print(f"Error calculating balance: {e}")
            return None
        finally:
            conn.close()