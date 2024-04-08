**This is an application made for scraping tweets from Twitter.**


This application made possible thanks to the vladkens's twscrape.
Please also checkout it: https://github.com/vladkens/twscrape


# Setup
Python3.11 has to be installed.
Python dependencies are
- twscrape
- loguru
- reportlab
- asyncio

To install dependencies use: `python3 -m pip install -r requirements.txt`

or install them one by one manually
- `python3 -m pip install twscrape`
- `python3 -m pip install loguru`
- `python3 -m pip install reportlab`

**Then you can run the applicatin with `python3 main.py`**

# Usage
Application acts as a normal user on twitter. So we have to provide accounts to for application to use.

### Accounts Page 
<img width="876" alt="atesdijital.com Accounts page" src="https://github.com/atesahmet0/TWFlame/assets/85938355/6f0ef485-d03e-4c1a-9f4f-e03975bf9cc8"/>


- username: username of the twitter account
- password: password of the twitter account
- email: email of the twitter account
- email_password: email password of the email

> [!WARNING]
> Not all email providers are supported Eg. @yandex.com.
> Only: yahoo, icloud, hotmail and outlook are supported for now.
> For more information: https://github.com/vladkens/twscrape/issues/67

After adding accounts use "login all accounts" button to login. If accounts are not active head to the Tweet page 
and checkout application output to see what is wrong.

### Tweet Page
<img width="1068" alt="atesdijital.com Tweet Scraper's Tweet Page" src="https://github.com/atesahmet0/TWFlame/assets/85938355/7b2f719f-848b-46fb-9132-48205f0ae0d8">

_Tweet Page has the output field of the program. Any errors or infos may be read here._


Input username then provide dates to scrape Tweets. Note that dates must be "Year-month-day" format like "2024-04-03". 

> [!NOTE]
> Scraped tweets will be stored in a database with the specified username.
> Eg. if you scraped tweets of "elonmusk" then tweets will be stored in a SQLite3 database called "elonmusk.db"

### PDF Page
<img width="876" alt="atesdijtial.com Tweet Scraper's PDF Page" src="https://github.com/atesahmet0/TWFlame/assets/85938355/5c021827-8416-4a49-b9b0-d0a8a9350bd4">

There is an example database that has ~500 tweets. Use "TansuYegen" as username to test PDF Page.
Input username then click import to fetch all the tweets of the user that is stored in the database. Select tweets that you want then click
turn to pdf button. PDF will be stored in the same directory as "main.py" file.

> [!NOTE]
> Note that you don't need an active account
> nor internet connection in order to do this. PDF Page only works with the tweets that are stored in the database.

















