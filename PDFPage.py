import tkinter as tk
from datetime import datetime

from loguru import logger
from tkinter import ttk
import asyncio

from twscrape import API

from BackendEngine import BackendEngine
from DatabaseManager import DatabaseManager
from SimpleTweet import SimpleTweet
from TweetToPDFConverter import TweetToPDFConverter


class PDFPage(tk.Frame):
    def __init__(self, api: API, master=None):
        super().__init__(master)
        self.api = api
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

        self.button_field = tk.Frame(self)
        self.button_field.grid(row=1, column=0, sticky='nsew')

        self.import_button = tk.Button(self.button_field, text="Import", command=self.import_button)
        self.import_button.grid(row=1, column=0, sticky='w')

        self.turn_to_pdf_button = tk.Button(self.button_field, text="Turn to PDF", command=self.turn_to_pdf_button)
        self.turn_to_pdf_button.grid(row=1, column=1, sticky='w')

        self.tree_table = ttk.Treeview(self, show='headings')
        self.tree_table.grid(row=2, column=0, sticky='nsew')

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self.on_load()

    def on_load(self):
        # Code to execute when the frame is packed
        pass

    def import_button(self):
        """Import all the data from the database and display it in the treeview."""
        try:
            asyncio.run(self._fetch_and_display_tweets())
        except Exception as e:
            logger.error(e)

    def turn_to_pdf_button(self):
        selected_rows = self.get_selected_rows()

        # Convert selected rows to SimpleTweet
        tweets = []
        for row in selected_rows:
            tweet_id, username, content, date = row
            tweet = SimpleTweet(tweet_id, username, content, date)
            tweets.append(tweet)

        # Convert SimpleTweet to PDF
        converter = TweetToPDFConverter(tweets)
        start_date_str = tweets[0].date
        final_date_str = tweets[len(tweets) - 1].date
        converter.convert_to_pdf(f"{username}_{datetime.now().timestamp()}.pdf")

    def get_selected_rows(self):
        selected_items = self.tree_table.selection()  # This returns a list of item IDs for the currently selected items.
        logger.info(f"Selected items: {selected_items}")
        selected_rows = []
        for item_id in selected_items:
            item = self.tree_table.item(item_id)  # Get the item's data.
            selected_rows.append(item['values'])  # Add the item's values to the list.
        logger.info(f"Selected rows: {selected_rows}")
        return selected_rows

    async def _fetch_tweets(self, username):
        """Fetch tweets from database for a given username."""
        logger.info(f"Fetching tweets for {username}")
        database_manager = DatabaseManager(username)
        tweets = database_manager.fetch_all_tweets()
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

    async def _fetch_and_display_tweets(self):
        """Use this to update treeview"""
        username = self.username_entry.get()
        logger.info(f"Fetching tweets for {username}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tweets = await self._fetch_tweets(username)
        logger.info(f"Fetched {len(tweets)} tweets for {username}")
        self._update_tree(tweets)
        loop.close()

    def _on_fetch_complete(self, future):
        tweets = future.result()
        logger.info(f"Fetched {len(tweets)} tweets for {tweets[0]['username']}")
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
