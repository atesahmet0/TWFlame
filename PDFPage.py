import tkinter as tk
from loguru import logger
from tkinter import ttk

class PDFPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.input_field = tk.Frame(self)
        self.input_field.grid(row=0, column=0, sticky='nsew')

        self.username_label = tk.Label(self.input_field, text="Username")
        self.username_label.grid(row=0, column=0, sticky='w')

        self.username_entry = tk.Entry(self.input_field)
        self.username_entry.grid(row=0, column=1, sticky='w')

        self.tree_table = ttk.Treeview(self, show='headings')
        self.tree_table.grid(row=2, column=0, sticky='nsew')

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.on_load()

    def on_load(self):
        # Code to execute when the frame is packed
        print("Frame is packed")

    def submit_button(self):
        pass


    def update_tree(self):
        # Clear the existing tree
        for i in self.tree_table.get_children():
            self.tree_table.delete(i)

        # Fetch data from the database
        data = self.fetch_data_from_database()

        # Create the treeview columns
        self.tree_table['columns'] = list(data[0].keys())
        for column in self.tree_table['columns']:
            self.tree_table.heading(column, text=column)

        # Insert the data into the treeview
        for row in data:
            self.tree_table.insert('', 'end', values=list(row.values()))

    def fetch_data_from_database(self):
        # This is a placeholder function. Replace this with your actual database fetching code.
        return [
            {'column1': 'data1', 'column2': 'data2'},
            {'column1': 'data3', 'column2': 'data4'},
            # Add more rows as needed...
        ]
