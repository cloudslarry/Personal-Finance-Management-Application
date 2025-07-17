import tkinter as tk
from tkinter import ttk, messagebox
from finance_manager import FinanceManager
from datetime import datetime
import sqlite3

class FinanceManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Personal Finance Manager')
        self.root.geometry('800x600')
        self.finance_manager = FinanceManager()
        self.current_user_id = None
        
        self.setup_styles()
        self.create_login_frame()

    def setup_styles(self):
        style = ttk.Style()
        style.configure('TLabel', padding=5, font=('Helvetica', 10))
        style.configure('TButton', padding=5, font=('Helvetica', 10))
        style.configure('TEntry', padding=5)
        style.configure('Heading.TLabel', font=('Helvetica', 12, 'bold'))

    def create_login_frame(self):
        self.login_frame = ttk.Frame(self.root, padding="20")
        self.login_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(self.login_frame, text="Personal Finance Manager", style='Heading.TLabel').grid(column=0, row=0, columnspan=2, pady=20)

        ttk.Label(self.login_frame, text="Username:").grid(column=0, row=1, sticky=tk.W)
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(column=1, row=1, padx=5, pady=5)

        ttk.Label(self.login_frame, text="Password:").grid(column=0, row=2, sticky=tk.W)
        self.password_entry = ttk.Entry(self.login_frame, show='*')
        self.password_entry.grid(column=1, row=2, padx=5, pady=5)

        ttk.Button(self.login_frame, text="Login", command=self.login).grid(column=0, row=3, pady=20)
        ttk.Button(self.login_frame, text="Register", command=self.register).grid(column=1, row=3, pady=20)

    def create_main_frame(self):
        self.login_frame.grid_remove()
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Transaction Frame
        transaction_frame = ttk.LabelFrame(self.main_frame, text="Add Transaction", padding="10")
        transaction_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))

        ttk.Label(transaction_frame, text="Type:").grid(column=0, row=0, sticky=tk.W)
        self.transaction_type = ttk.Combobox(transaction_frame, values=['income', 'expense'])
        self.transaction_type.grid(column=1, row=0, padx=5, pady=5)

        ttk.Label(transaction_frame, text="Category:").grid(column=0, row=1, sticky=tk.W)
        self.category_entry = ttk.Entry(transaction_frame)
        self.category_entry.grid(column=1, row=1, padx=5, pady=5)

        ttk.Label(transaction_frame, text="Amount:").grid(column=0, row=2, sticky=tk.W)
        self.amount_entry = ttk.Entry(transaction_frame)
        self.amount_entry.grid(column=1, row=2, padx=5, pady=5)

        ttk.Label(transaction_frame, text="Description:").grid(column=0, row=3, sticky=tk.W)
        self.description_entry = ttk.Entry(transaction_frame)
        self.description_entry.grid(column=1, row=3, padx=5, pady=5)

        ttk.Button(transaction_frame, text="Add Transaction", 
                   command=self.add_transaction).grid(column=0, row=4, columnspan=2, pady=10)

        # Budget Frame
        budget_frame = ttk.LabelFrame(self.main_frame, text="Set Budget", padding="10")
        budget_frame.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))

        ttk.Label(budget_frame, text="Category:").grid(column=0, row=0, sticky=tk.W)
        self.budget_category_entry = ttk.Entry(budget_frame)
        self.budget_category_entry.grid(column=1, row=0, padx=5, pady=5)

        ttk.Label(budget_frame, text="Amount:").grid(column=0, row=1, sticky=tk.W)
        self.budget_amount_entry = ttk.Entry(budget_frame)
        self.budget_amount_entry.grid(column=1, row=1, padx=5, pady=5)

        ttk.Button(budget_frame, text="Set Budget", 
                   command=self.set_budget).grid(column=0, row=2, columnspan=2, pady=10)

        # Reports Frame
        reports_frame = ttk.LabelFrame(self.main_frame, text="Reports", padding="10")
        reports_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=(tk.W, tk.E))

        ttk.Button(reports_frame, text="Monthly Report", 
                   command=self.show_monthly_report).grid(column=0, row=0, padx=5)
        ttk.Button(reports_frame, text="Yearly Report", 
                   command=self.show_yearly_report).grid(column=1, row=0, padx=5)
        ttk.Button(reports_frame, text="Budget Status", 
                   command=self.show_budget_status).grid(column=2, row=0, padx=5)

        # Logout Button
        ttk.Button(self.main_frame, text="Logout", 
                   command=self.logout).grid(row=2, column=0, columnspan=2, pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id = self.finance_manager.authenticate_user(username, password)
        if user_id:
            self.current_user_id = user_id
            messagebox.showinfo("Success", "Login successful!")
            self.create_main_frame()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.finance_manager.register_user(username, password):
            messagebox.showinfo("Success", "Registration successful!")
        else:
            messagebox.showerror("Error", "Username already exists!")

    def add_transaction(self):
        try:
            type = self.transaction_type.get()
            category = self.category_entry.get()
            amount = float(self.amount_entry.get())
            description = self.description_entry.get()

            if self.finance_manager.transaction_manager.add_transaction(
                self.current_user_id, type, category, amount, description):
                messagebox.showinfo("Success", "Transaction added successfully!")
                self.clear_transaction_entries()
            else:
                messagebox.showerror("Error", "Failed to add transaction!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")

    def set_budget(self):
        try:
            category = self.budget_category_entry.get()
            amount = float(self.budget_amount_entry.get())
            current_date = datetime.now()

            if self.finance_manager.budget_manager.set_budget(
                self.current_user_id, category, amount, current_date.month, current_date.year):
                messagebox.showinfo("Success", "Budget set successfully!")
                self.clear_budget_entries()
            else:
                messagebox.showerror("Error", "Failed to set budget!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount!")

    def show_monthly_report(self):
        report = self.finance_manager.report_generator.generate_monthly_report(
            self.current_user_id)
        self.show_report("Monthly Report", report)

    def show_yearly_report(self):
        report = self.finance_manager.report_generator.generate_yearly_report(
            self.current_user_id)
        self.show_report("Yearly Report", report)

    def show_budget_status(self):
        status = self.finance_manager.budget_manager.check_budget_status(
            self.current_user_id)
        self.show_report("Budget Status", status)

    def show_report(self, title, content):
        report_window = tk.Toplevel(self.root)
        report_window.title(title)
        report_window.geometry('600x400')

        text_widget = tk.Text(report_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.insert(tk.END, content)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(expand=True, fill=tk.BOTH)

        scrollbar = ttk.Scrollbar(report_window, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget['yscrollcommand'] = scrollbar.set

    def clear_transaction_entries(self):
        self.transaction_type.set('')
        self.category_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def clear_budget_entries(self):
        self.budget_category_entry.delete(0, tk.END)
        self.budget_amount_entry.delete(0, tk.END)

    def logout(self):
        self.current_user_id = None
        self.main_frame.grid_remove()
        self.create_login_frame()
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = FinanceManagerGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()