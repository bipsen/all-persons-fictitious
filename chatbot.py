"""
This is the main script
"""

import datetime
import sqlite3
from sqlite3 import Error
import nltk.sentiment
from chatterbot import ChatBot
from pythonosc import udp_client


def _create_connection(db_file):
    """ Create a database connection to the SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()

        # Create a new SQLite table
        cur.execute("CREATE TABLE {tn} ({r1}, {r2}, {time} {ft})"
                    .format(tn=TABLE_NAME, r1=INPUT_COLUMN, r2=OUTPUT_COLUMN,
                            time='time', ft='TEXT'))

    except Error as err:
        print(err)

    finally:
        conn.commit()
        conn.close()


def _log_conversation(db_file, line):
    """ Log conversation in SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute("""INSERT INTO {tn} ({c1}, {c2}, {time}) VALUES ("{v1}", "{v2}", "{now}")""".
                    format(tn=TABLE_NAME, c1=INPUT_COLUMN, c2=OUTPUT_COLUMN, time='time',
                           v1=' '.join(line.keys()), v2=' '.join(line.values()),
                           now=str(datetime.datetime.now())))
        conn.commit()

    except Error as err:
        print(err)

    finally:
        conn.close()


def main(text):
    """This is the main function to run the CHATBOT, analyse
    the responses with nltk and send OSC messages to Pure Data.
    """

    # Get CHATBOT response from the user input.
    bot_response = CHATBOT.get_response(text).text
    print(bot_response)

    # Get polarity score from CHATBOT response.
    analysis = VADER_ANALYZER.polarity_scores(text)

    # Change polarity score relatively to a audible frequency.
    freq = (analysis['compound'] - -1) / (1 - -1) * (800 - 200) + 200

    # Send OSC message, to be listened to by pd.
    CLIENT.send_message("/filter", freq)

    # Log conversation.
    exchange = {text: bot_response}
    _log_conversation("conversation.db", exchange)


if __name__ == '__main__':

    # Set up database
    TABLE_NAME = 'conversation_log'
    INPUT_COLUMN = 'input_column'
    OUTPUT_COLUMN = 'output_column'
    CONVERSATION_DB = "conversation.db"
    _create_connection(CONVERSATION_DB)

    # Set up chatbot.
    CHATBOT = ChatBot(
        'Sentiment Music Bot',
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer')

    # Train based on the english corpus.
    CHATBOT.train("chatterbot.corpus.english")

    # Download lexicon for nltk.
    nltk.download('vader_lexicon')

    # Set up sentiment analyzer.
    VADER_ANALYZER = nltk.sentiment.vader.SentimentIntensityAnalyzer()

    # Set up OSC client.
    IP = 'localhost'
    PORT = 9000
    CLIENT = udp_client.SimpleUDPClient(IP, PORT)

    # Run chatbot.
    while True:
        USER_RESPONSE = input("Talk ('exit' to exit): ")
        if USER_RESPONSE == 'exit':   # Exit on 'exit' string.
            break
        else:
            main(USER_RESPONSE)
