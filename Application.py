import tkinter as tk
import sys
from loguru import logger
from Helper import is_valid_date
import tkinter.ttk as ttk
from BackendEngine import BackendEngine
from TweetPage import TweetPage


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Page 1
        self.page1 = TweetPage(self)




        # Page 2
        self.page2 = tk.Frame(self)

        self.tree = ttk.Treeview(self.page2, show='headings')
        self.tree.grid(row=2, column=0, sticky='nsew')

        self.username_label_page2 = tk.Label(self.page2, text="Username")
        self.username_label_page2.grid(row=0, column=0, sticky='w')

        self.username_entry_page2 = tk.Entry(self.page2)
        self.username_entry_page2.grid(row=1, column=0, sticky='w')

        self.page2.grid_rowconfigure(2, weight=1)
        self.page2.grid_columnconfigure(0, weight=1)

        self.navbar = tk.Frame(self)
        self.navbar.pack(side='bottom', fill='x')

        # Navbar
        self.page1_button = tk.Button(self.navbar, text="Tweet", command=self.show_page1)
        self.page1_button.pack(side='left')

        self.page2_button = tk.Button(self.navbar, text="PDF", command=self.show_page2)
        self.page2_button.pack(side='left')

        self.show_page1()

    def show_page1(self):
        self.page2.pack_forget()
        self.page1.pack(fill='both', expand=True)

    def show_page2(self):
        self.page1.pack_forget()
        self.update_tree()
        self.page2.pack(fill='both', expand=True)

    def update_tree(self):
        # Clear the existing tree
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Fetch data from the database
        data = self.fetch_data_from_database()

        # Create the treeview columns
        self.tree['columns'] = list(data[0].keys())
        for column in self.tree['columns']:
            self.tree.heading(column, text=column)

        # Insert the data into the treeview
        for row in data:
            self.tree.insert('', 'end', values=list(row.values()))

    def fetch_data_from_database(self):
        # This is a placeholder function. Replace this with your actual database fetching code.
        return [
            {'column1': 'data1', 'column2': 'data2'},
            {'column1': 'data3', 'column2': 'data4'},
            # Add more rows as needed...
        ]


