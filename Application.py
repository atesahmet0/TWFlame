import tkinter as tk
from PDFPage import PDFPage
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
        self.page2 = PDFPage(self)

        # Navbar
        self.navbar = tk.Frame(self)
        self.navbar.pack(side='bottom', fill='x')

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
        self.page2.pack(fill='both', expand=True)
