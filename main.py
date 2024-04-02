import asyncio
import tkinter as tk
from Application import Application


def main():
    root = tk.Tk(screenName="Tweet Scraper - Ateş Dijital")
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
