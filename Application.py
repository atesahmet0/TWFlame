import asyncio
import threading
import tkinter as tk
from twscrape import API
from AccountsPage import AccountsPage
from PDFPage import PDFPage
from TweetPage import TweetPage
from Config import get_current_database

class Application(tk.Frame):
    def __init__(self, master=None):
        # Create a new event loop
        self.new_loop = asyncio.new_event_loop()

        # Run the event loop in a new thread
        t = threading.Thread(target=start_loop, args=(self.new_loop,))
        t.start()

        self.api = API(get_current_database())
        super().__init__(master)
        self.master = master
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        # Page 1
        self.page1 = TweetPage(self.new_loop, self)
        self.page2 = PDFPage(self)
        self.page3 = AccountsPage(self.api, self.new_loop, self)

        # Navbar
        self.navbar = tk.Frame(self)
        self.navbar.pack(side='bottom', fill='x')

        self.page1_button = tk.Button(self.navbar, text="Tweet", command=self.show_page1)
        self.page1_button.pack(side='left')

        self.page2_button = tk.Button(self.navbar, text="PDF", command=self.show_page2)
        self.page2_button.pack(side='left')

        self.page3_button = tk.Button(self.navbar, text="Accounts", command=self.show_page3)
        self.page3_button.pack(side='left')

        self.show_page1()

    def show_page1(self):
        self.page2.pack_forget()
        self.page3.pack_forget()
        self.page1.pack(fill='both', expand=True)

    def show_page2(self):
        self.page1.pack_forget()
        self.page3.pack_forget()
        self.page2.pack(fill='both', expand=True)

    def show_page3(self):
        self.page1.pack_forget()
        self.page2.pack_forget()
        self.page3.pack(fill='both', expand=True)

    def destroy(self):
        # Stop the event loop
        self.new_loop.call_soon_threadsafe(self.new_loop.stop)

        # Call the original destroy method
        super().destroy()


def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

