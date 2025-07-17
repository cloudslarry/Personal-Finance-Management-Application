import sqlite3
from datetime import datetime
from tabulate import tabulate

class ReportGenerator:
    def __init__(self, db_path='finance.db'):
        self.db_path = db_path

    def generate_monthly_report(self, user_id, month=None, year=None):
        """Generate a monthly financial report"""
        if not month or not year:
            current_date = datetime.now()
            month = month or current_date.month
            year = year or current_date.year

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Get total income
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) 
                FROM transactions 
                WHERE user_id = ? 
                AND type = 'income' 
                AND strftime('%m', date) = ? 
                AND strftime('%Y', date) = ?
            """, (user_id, str(month).zfill(2), str(year)))
            total_income = cursor.fetchone()[0]

            # Get total expenses
            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0) 
                FROM transactions 
                WHERE user_id = ? 
                AND type = 'expense' 
                AND strftime('%m', date) = ? 
                AND strftime('%Y', date) = ?
            """, (user_id, str(month).zfill(2), str(year)))
            total_expenses = cursor.fetchone()[0]

            # Get expenses by category
            cursor.execute("""
                SELECT category, SUM(amount) 
                FROM transactions 
                WHERE user_id = ? 
                AND type = 'expense' 
                AND strftime('%m', date) = ? 
                AND strftime('%Y', date) = ? 
                GROUP BY category
            """, (user_id, str(month).zfill(2), str(year)))
            expenses_by_category = cursor.fetchall()

            # Format the report
            report = f"\nMonthly Financial Report - {month}/{year}\n"
            report += "=" * 40 + "\n\n"
            report += f"Total Income: ${total_income:.2f}\n"
            report += f"Total Expenses: ${total_expenses:.2f}\n"
            report += f"Net Savings: ${(total_income - total_expenses):.2f}\n\n"

            # Add expenses breakdown
            if expenses_by_category:
                expense_data = [
                    [category, f"${amount:.2f}", 
                     f"{(amount/total_expenses*100):.1f}%" if total_expenses > 0 else "0%"]
                    for category, amount in expenses_by_category
                ]
                report += "Expenses Breakdown:\n"
                report += tabulate(expense_data, 
                                 headers=['Category', 'Amount', 'Percentage'], 
                                 tablefmt='grid')

            return report

        except sqlite3.Error as e:
            print(f"Error generating monthly report: {e}")
            return None
        finally:
            conn.close()

    def generate_yearly_report(self, user_id, year=None):
        """Generate a yearly financial report"""
        if not year:
            year = datetime.now().year

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Get monthly totals
            cursor.execute("""
                SELECT 
                    strftime('%m', date) as month,
                    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
                    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expenses
                FROM transactions 
                WHERE user_id = ? AND strftime('%Y', date) = ? 
                GROUP BY month 
                ORDER BY month
            """, (user_id, str(year)))
            monthly_data = cursor.fetchall()

            # Get yearly totals
            cursor.execute("""
                SELECT 
                    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
                    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expenses
                FROM transactions 
                WHERE user_id = ? AND strftime('%Y', date) = ?
            """, (user_id, str(year)))
            yearly_totals = cursor.fetchone()
            total_income, total_expenses = yearly_totals

            # Format the report
            report = f"\nYearly Financial Report - {year}\n"
            report += "=" * 40 + "\n\n"
            report += f"Total Income: ${total_income:.2f}\n"
            report += f"Total Expenses: ${total_expenses:.2f}\n"
            report += f"Net Savings: ${(total_income - total_expenses):.2f}\n\n"

            # Add monthly breakdown
            if monthly_data:
                month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                             'July', 'August', 'September', 'October', 'November', 
                             'December']
                monthly_breakdown = [
                    [month_names[int(month)-1], 
                     f"${income:.2f}", 
                     f"${expenses:.2f}", 
                     f"${income - expenses:.2f}"]
                    for month, income, expenses in monthly_data
                ]
                report += "Monthly Breakdown:\n"
                report += tabulate(monthly_breakdown, 
                                 headers=['Month', 'Income', 'Expenses', 'Savings'], 
                                 tablefmt='grid')

            return report

        except sqlite3.Error as e:
            print(f"Error generating yearly report: {e}")
            return None
        finally:
            conn.close()

    def generate_category_analysis(self, user_id, start_date=None, end_date=None):
        """Generate a detailed analysis of spending by category"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = """
            SELECT 
                category,
                COUNT(*) as transaction_count,
                SUM(amount) as total_amount,
                AVG(amount) as avg_amount,
                MIN(amount) as min_amount,
                MAX(amount) as max_amount
            FROM transactions 
            WHERE user_id = ? AND type = 'expense'
        """
        params = [user_id]

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

        query += " GROUP BY category ORDER BY total_amount DESC"

        try:
            cursor.execute(query, params)
            categories = cursor.fetchall()

            if categories:
                analysis_data = [
                    [category, count, f"${total:.2f}", 
                     f"${avg:.2f}", f"${min:.2f}", f"${max:.2f}"]
                    for category, count, total, avg, min, max in categories
                ]
                return tabulate(analysis_data, 
                               headers=['Category', 'Count', 'Total', 'Average', 
                                       'Minimum', 'Maximum'], 
                               tablefmt='grid')
            return "No transaction data available for analysis."

        except sqlite3.Error as e:
            print(f"Error generating category analysis: {e}")
            return None
        finally:
            conn.close()