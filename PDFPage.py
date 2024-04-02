import tkinter as tk
from loguru import logger
from tkinter import ttk
import asyncio

from BackendEngine import BackendEngine


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

        self.import_button = tk.Button(self, text="Import", command=self.import_button)
        self.import_button.grid(row=1, column=0, sticky='w')

        self.tree_table = ttk.Treeview(self, show='headings')
        self.tree_table.grid(row=2, column=0, sticky='nsew')

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.on_load()

    def on_load(self):
        # Code to execute when the frame is packed
        try:
            self._fetch_and_display_tweets()
        except Exception as e:
            logger.error(e)

    def import_button(self):
        """Import all the data from the database and display it in the treeview."""
        try:
            self._fetch_and_display_tweets()
        except Exception as e:
            logger.error(e)

    @staticmethod
    async def _fetch_tweets(username):
        """Fetch tweets from database for a given username."""
        backend = BackendEngine(username)
        await backend.setup()

        tweets = await backend.get_tweets_from_database()
        logger.info(f"Fetched {len(tweets)} tweets for {username}")

        # Convert the SimpleTweet objects into dictionaries
        data = []
        for tweet in tweets:
            data.append({
                'id': tweet.id,
                'username': tweet.username,
                'content': tweet.rawContent,
                'date': tweet.date,
                # Add more fields as needed...
            })

        return data

    def _fetch_and_display_tweets(self):
        """Use this to update treeview"""
        username = self.username_entry.get()
        logger.info(f"Fetching tweets for {username}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tweets = loop.run_until_complete(self._fetch_tweets(username))
        logger.info(f"Fetched {len(tweets)} tweets for {username}")
        loop.close()
        self._update_tree(tweets)

    def _update_tree(self, data):
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

        # Insert the data into the treeview
        for row in data:
            self.tree_table.insert('', 'end', values=list(row.values()))
