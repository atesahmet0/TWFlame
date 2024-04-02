import tkinter as tk
import sys
from loguru import logger
from Helper import is_valid_date


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill='both', expand=True)
        self.create_widgets()

    def create_widgets(self):
        self.page1 = tk.Frame(self)
        self.page2 = tk.Frame(self)

        self.page1_inputs_frame = tk.Frame(self.page1)
        self.page1_inputs_frame.grid(row=0, column=0, sticky='w')
        self.username_label = tk.Label(self.page1_inputs_frame, text="Username")
        self.username_label.grid(row=0, column=0, sticky='w')

        self.start_date_label = tk.Label(self.page1_inputs_frame, text="Start Date")
        self.start_date_label.grid(row=0, column=2, sticky='w')

        self.start_date_entry = tk.Entry(self.page1_inputs_frame)
        self.start_date_entry.grid(row=0, column=3, sticky='w')

        self.final_date_label = tk.Label(self.page1_inputs_frame, text="Final Date")
        self.final_date_label.grid(row=0, column=4, sticky='w')

        self.final_date_entry = tk.Entry(self.page1_inputs_frame)
        self.final_date_entry.grid(row=0, column=5, sticky='w')

        self.page1_date_info_label = tk.Label(self.page1_inputs_frame, text="Date Format: 'YYYY-MM-DD'")
        self.page1_date_info_label.grid(row=0, column=6, sticky='w')

        self.username_entry = tk.Entry(self.page1_inputs_frame)
        self.username_entry.grid(row=0, column=1, sticky='w')

        self.page1_button = tk.Button(self.page1, text="Submit", command=self.submit_button)
        self.page1_button.grid(row=2, column=0, sticky='w')

        self.console_output = tk.Text(self.page1)
        self.console_output.grid(row=3, column=0, sticky='nsew')
        # Redirect stdout to the console_output
        text_redirector = TextRedirector(self.console_output)
        sys.stdout = text_redirector
        sys.stdin = text_redirector
        sys.stderr = text_redirector
        logger.add(widget_sink(self.console_output))

        self.page1.grid_rowconfigure(3, weight=1)
        self.page1.grid_columnconfigure(0, weight=1)

        self.username_label_page2 = tk.Label(self.page2, text="Username")
        self.username_label_page2.grid(row=0, column=0, sticky='w')

        self.username_entry_page2 = tk.Entry(self.page2)
        self.username_entry_page2.grid(row=1, column=0, sticky='w')

        self.navbar = tk.Frame(self)
        self.navbar.pack(side='bottom', fill='x')

        self.page1_button = tk.Button(self.navbar, text="Page 1", command=self.show_page1)
        self.page1_button.pack(side='left')

        self.page2_button = tk.Button(self.navbar, text="Page 2", command=self.show_page2)
        self.page2_button.pack(side='left')

        self.show_page1()

    def submit_button(self):
        start_date = self.start_date_entry.get()
        final_date = self.final_date_entry.get()

        if not is_valid_date(start_date):
            logger.error(f"Start Date: {start_date} is not in the correct format 'YYYY-MM-DD'")
            return

        if not is_valid_date(final_date):
            logger.error(f"Final Date: {final_date} is not in the correct format 'YYYY-MM-DD'")
            return

        logger.info(f"Username: {self.username_entry.get()}")
        logger.info(f"Start Date: {start_date}")
        logger.info(f"Final Date: {final_date}")

    def show_page1(self):
        self.page2.pack_forget()
        self.page1.pack(fill='both', expand=True)

    def show_page2(self):
        self.page1.pack_forget()
        self.page2.pack(fill='both', expand=True)


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
