import asyncio
import tkinter as tk

from BackendEngine import BackendEngine
from Helper import is_valid_date
from loguru import logger
import sys


class TweetPage(tk.Frame):
    def __init__(self, loop, master=None):
        super().__init__(master)
        self.loop = loop
        self.master = master
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.input_frame = tk.Frame(self)
        self.input_frame.grid(row=0, column=0, sticky='nsew')

        self.username_label = tk.Label(self.input_frame, text="Username")
        self.username_label.grid(row=0, column=0, sticky='w')

        self.username_entry = tk.Entry(self.input_frame)
        self.username_entry.grid(row=0, column=1, sticky='w')

        self.start_date_label = tk.Label(self.input_frame, text="Start Date")
        self.start_date_label.grid(row=0, column=2, sticky='w')

        self.start_date_entry = tk.Entry(self.input_frame)
        self.start_date_entry.grid(row=0, column=3, sticky='w')

        self.final_date_label = tk.Label(self.input_frame, text="Final Date")
        self.final_date_label.grid(row=0, column=4, sticky='w')

        self.final_date_entry = tk.Entry(self.input_frame)
        self.final_date_entry.grid(row=0, column=5, sticky='w')

        self.date_info_label = tk.Label(self.input_frame, text="Date Format: 'YYYY-MM-DD'")
        self.date_info_label.grid(row=0, column=6, sticky='w')

        self.button_field = tk.Frame(self)
        self.button_field.grid(row=1, column=0, sticky='nsew')

        self.submit_button = tk.Button(self.button_field, text="Fetch Tweets", command=self.submit_button)
        self.submit_button.grid(row=0, column=0, sticky='w')

        self.terminate_button = tk.Button(self.button_field, text="Terminate", command=self.terminate_button)
        self.terminate_button.grid(row=0, column=1, sticky='w')

        self.console_output = tk.Text(self)
        self.console_output.grid(row=3, column=0, sticky='nsew')

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.redirect_stdout(self.console_output)

    def terminate_button(self):
        for task in asyncio.all_tasks(self.loop):
            task.cancel()

    def submit_button(self):
        start_date = self.start_date_entry.get()
        final_date = self.final_date_entry.get()

        if not is_valid_date(start_date):
            logger.error(f"Start Date: {start_date} is not in the correct format 'YYYY-MM-DD'")
            return

        if not is_valid_date(final_date):
            logger.error(f"Final Date: {final_date} is not in the correct format 'YYYY-MM-DD'")
            return

        logger.info(f"Start Date: {start_date}")
        logger.info(f"Final Date: {final_date}")

        # Create a task for the fetch_accounts coroutine
        task = asyncio.run_coroutine_threadsafe(self.fetch_tweets(), self.loop)

        # Add a callback to the task to update the GUI when the coroutine has finished running
        task.add_done_callback(lambda t: logger.info(f"Task finished: {t.result()}"))

    async def fetch_tweets(self):
        # Fetch the tweets
        backend = BackendEngine(self.username_entry.get())
        await backend.setup()
        logger.info(f"Backend Engine: {backend.get_current_state()}")
        return await backend.fetch_all_tweets(self.final_date_entry.get())

    def redirect_stdout(self, widget):
        # Redirect stdout to the console_output
        text_redirector = TextRedirector(widget)
        sys.stdout = text_redirector
        sys.stdin = text_redirector
        sys.stderr = text_redirector
        logger.add(widget_sink(widget))


class TextRedirector(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, message, tag=None):
        self.widget.insert(tk.END, message, tag)
        self.widget.see(tk.END)

    def flush(self):
        pass


def widget_sink(widget):
    def sink(message):
        widget.insert(tk.END, message)
        widget.see(tk.END)

    return sink
