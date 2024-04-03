import asyncio
import tkinter as tk
from tkinter import ttk
from loguru import logger
from twscrape import API
from Config import get_current_database, get_accounts_database_default_table_name
from Database import Database


class AccountsPage(tk.Frame):
    def __init__(self, api: API, loop, master=None):
        super().__init__(master)
        self.loop = loop
        self.api = api
        self.accounts_logger = logger.bind(name="AccountsPage")
        self.master = master
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Inputs Begin
        self.input_field = tk.Frame(self)
        self.input_field.grid(row=0, column=0, sticky='w')

        self.username_label = tk.Label(self.input_field, text="Username")
        self.username_label.grid(row=0, column=0, sticky='w')
        self.username_entry = tk.Entry(self.input_field)
        self.username_entry.grid(row=0, column=1, sticky='w')

        self.username_password_label = tk.Label(self.input_field, text="Username Password")
        self.username_password_label.grid(row=1, column=0, sticky='w')
        self.username_password_entry = tk.Entry(self.input_field, show="*")
        self.username_password_entry.grid(row=1, column=1, sticky='w')

        self.email_label = tk.Label(self.input_field, text="Email")
        self.email_label.grid(row=2, column=0, sticky='w')
        self.email_entry = tk.Entry(self.input_field)
        self.email_entry.grid(row=2, column=1, sticky='w')

        self.email_password_label = tk.Label(self.input_field, text="Email Password")
        self.email_password_label.grid(row=3, column=0, sticky='w')
        self.email_password_entry = tk.Entry(self.input_field, show="*")
        self.email_password_entry.grid(row=3, column=1, sticky='w')

        # Buttons Begin
        self.button_field = tk.Frame(self)
        self.button_field.grid(row=1, column=0, sticky='w')

        self.add_account_button = tk.Button(self.button_field, text="Add Account", command=self.add_account_button)
        self.add_account_button.grid(row=0, column=0, sticky='w')

        self.remove_account_button = tk.Button(self.button_field, text="Remove Account",
                                               command=self.remove_account_button)
        self.remove_account_button.grid(row=0, column=1, sticky='w')

        self.list_accounts_button = tk.Button(self.button_field, text="List Accounts",
                                              command=self.list_accounts_button)
        self.list_accounts_button.grid(row=0, column=2, sticky='w')

        self.login_all_accounts_button = tk.Button(self.button_field, text="Login All Accounts",
                                                   command=self.login_all_accounts_button)
        self.login_all_accounts_button.grid(row=0, column=3, sticky='w')

        # Output fields begin

        self.output_field = tk.Frame(self)
        self.output_field.grid(row=2, column=0, sticky='nsew')

        self.tree_table = ttk.Treeview(self.output_field, show='headings')
        self.tree_table.grid(row=0, column=0, sticky='nsew')

        # Log display
        self.log_text = tk.Text(self.output_field)
        self.log_text.grid(row=1, column=0, sticky='nsew')
        self.accounts_logger.add(self.log_sink, filter=lambda record: record["extra"].get("name") == "AccountsPage")

        self.output_field.grid_rowconfigure(0, weight=1)
        self.output_field.grid_rowconfigure(1, weight=1)
        self.output_field.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def add_account_button(self):
        # Create a task for the add_account coroutine
        task = asyncio.run_coroutine_threadsafe(self.add_account(), self.loop)

        # Add a callback to the task to update the GUI when the coroutine has finished running
        task.add_done_callback(lambda t: self.log_text.insert(tk.END, "Account added successfully\n"))

    def login_all_accounts_button(self):
        # Create a task for the login_all_accounts coroutine
        task = asyncio.run_coroutine_threadsafe(self.api.pool.login_all(), self.loop)

        task.add_done_callback(lambda t: self.log_text.insert(tk.END, "Accounts logging in finished\n"))

    def remove_account_button(self):
        task = asyncio.run_coroutine_threadsafe(self.remove_account(), self.loop)
        task.add_done_callback(lambda t: self.log_text.insert(tk.END, "Account removed successfully\n"))

    def list_accounts_button(self):
        # Create a task for the fetch_accounts coroutine
        task = asyncio.run_coroutine_threadsafe(self.fetch_accounts(), self.loop)

        # Add a callback to the task to update the GUI when the coroutine has finished running
        task.add_done_callback(lambda t: self.fill_tree(task.result()))

    async def add_account(self):
        # Get username and other details from entry boxs
        await self.api.pool.add_account(self.username_entry.get(),
                                        self.username_password_entry.get(),
                                        self.email_entry.get(),
                                        self.email_password_entry.get())

    async def remove_account(self):
        await self.api.pool.delete_accounts(self.username_entry.get())

    async def fetch_accounts(self):
        database = Database(get_current_database())
        data = database.fetch_data(get_accounts_database_default_table_name())
        logger.info(f"Data: {data}")

        accounts = []
        for account in data:
            accounts.append({
                "username": account[0],
                "username_password": account[1],
                "email": account[2],
                "email_password": account[3],
                "active": account[5]
            })
        return accounts

    def fill_tree(self, data):
        # Clear the existing tree
        for i in self.tree_table.get_children():
            self.tree_table.delete(i)

        # Create the treeview columns
        self.tree_table['columns'] = list(data[0].keys())
        for column in self.tree_table['columns']:
            self.tree_table.heading(column, text=column)

        # Insert the data into the treeview
        for row in data:
            self.tree_table.insert('', 'end', values=list(row.values()))

    def log_sink(self, message):
        if message.record["extra"].get("name") == "AccountsPage":
            self.log_text.insert(tk.END, message + '\n')
