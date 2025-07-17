import sqlite3
from datetime import datetime
from tabulate import tabulate

class BudgetManager:
    def __init__(self, db_path='finance.db'):
        self.db_path = db_path

    def set_budget(self, user_id, category, amount, month, year):
        """Set or update a budget for a specific category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Check if budget already exists
            cursor.execute("""
                SELECT id FROM budgets 
                WHERE user_id = ? AND category = ? AND month = ? AND year = ?
            """, (user_id, category, month, year))
            existing = cursor.fetchone()

            if existing:
                # Update existing budget
                cursor.execute("""
                    UPDATE budgets 
                    SET amount = ? 
                    WHERE user_id = ? AND category = ? AND month = ? AND year = ?
                """, (amount, user_id, category, month, year))
            else:
                # Create new budget
                cursor.execute("""
                    INSERT INTO budgets (user_id, category, amount, month, year)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, category, amount, month, year))

            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error setting budget: {e}")
            return False
        finally:
            conn.close()

    def get_budgets(self, user_id, month=None, year=None):
        """Get all budgets for a user with optional month/year filter"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = "SELECT category, amount, month, year FROM budgets WHERE user_id = ?"
        params = [user_id]

        if month:
            query += " AND month = ?"
            params.append(month)
        if year:
            query += " AND year = ?"
            params.append(year)

        try:
            cursor.execute(query, params)
            budgets = cursor.fetchall()
            headers = ['Category', 'Budget Amount', 'Month', 'Year']
            return tabulate(budgets, headers=headers, tablefmt='grid')
        except sqlite3.Error as e:
            print(f"Error retrieving budgets: {e}")
            return None
        finally:
            conn.close()

    def check_budget_status(self, user_id, month=None, year=None):
        """Check budget status and return warnings for categories exceeding budget"""
        if not month or not year:
            current_date = datetime.now()
            month = month or current_date.month
            year = year or current_date.year

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Get all budgets for the specified month/year
            cursor.execute("""
                SELECT category, amount 
                FROM budgets 
                WHERE user_id = ? AND month = ? AND year = ?
            """, (user_id, month, year))
            budgets = cursor.fetchall()

            status = []
            for category, budget_amount in budgets:
                # Get total expenses for this category
                cursor.execute("""
                    SELECT COALESCE(SUM(amount), 0) 
                    FROM transactions 
                    WHERE user_id = ? 
                    AND category = ? 
                    AND type = 'expense' 
                    AND strftime('%m', date) = ? 
                    AND strftime('%Y', date) = ?
                """, (user_id, category, str(month).zfill(2), str(year)))
                spent = cursor.fetchone()[0]

                percentage = (spent / budget_amount) * 100 if budget_amount > 0 else 0
                status.append({
                    'category': category,
                    'budget': budget_amount,
                    'spent': spent,
                    'percentage': percentage,
                    'exceeded': spent > budget_amount
                })

            # Format status report
            report_data = [
                [s['category'], s['budget'], s['spent'], 
                 f"{s['percentage']:.1f}%", 
                 'EXCEEDED!' if s['exceeded'] else 'Within budget']
                for s in status
            ]
            headers = ['Category', 'Budget', 'Spent', 'Used %', 'Status']
            return tabulate(report_data, headers=headers, tablefmt='grid')

        except sqlite3.Error as e:
            print(f"Error checking budget status: {e}")
            return None
        finally:
            conn.close()