from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from SimpleTweet import SimpleTweet
from loguru import logger
import re


pdfmetrics.registerFont(TTFont('Verdana', 'Verdana.ttf'))


def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


class TweetToPDFConverter:
    def __init__(self, tweets: list[SimpleTweet]):
        self.tweets = sorted(tweets, key=lambda tweet: tweet.date)

    def convert_to_pdf(self, filename):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        styles["BodyText"].fontName = "Verdana"

        for tweet in self.tweets:
            # Adding a paragraph
            text = remove_emojis(tweet.rawContent)
            story.append(Paragraph(text, styles["BodyText"]))
            story.append(Paragraph(str(tweet.date), styles["BodyText"]))
            story.append(Spacer(1, 24))  # Add some space after each paragraph

        # save the pdf with name .pdf
        doc.build(story)
        logger.info(f"PDF file {filename} created.")
