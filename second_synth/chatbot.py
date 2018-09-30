import nltk.sentiment
import csv
import datetime
from chatterbot import ChatBot
from pythonosc import osc_message_builder, udp_client


def run_Bot(text):
    """This is the main function to run the chatbot, analyse
    the responses with nltk and send OSC messages to Pure Data.
    """

    # Get chatbot response from the user input.
    bot_response = chatbot.get_response(text).text
    print(bot_response)

    # Get polarity score from chatbot response.
    analysis = vader_analyzer.polarity_scores(text)

    # Change polarity score relatively to a audible frequency.
    freq = (analysis['compound'])

    # Send OSC message, to be listened to by pd.
    client.send_message("/filter", freq)

    print (freq)

    # Log conversation.
    convo_log.update({text:bot_response})


# Set up chatbot.
chatbot = ChatBot(
    'Sentiment Music Bot',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Train based on the english corpus.
chatbot.train("chatterbot.corpus.english")

# Download lexicon for nltk.
nltk.download('vader_lexicon')

# Set up sentiment analyzer.
vader_analyzer = nltk.sentiment.vader.SentimentIntensityAnalyzer()

# Set up dict to log conversation.
convo_log = {}

# Set up OSC client.
ip = 'localhost'
port = 9000
client = udp_client.SimpleUDPClient(ip, port)

# Run the chatbot.
while True:
    user_response = input("Talk ('exit' to exit): ")
    if user_response == 'exit':   # Exit on 'exit' string.

        # Save conversation log.
        with open('conversation_log.csv','a') as f:
            w = csv.writer(f)
            w.writerow(['NEW SESSION AT: '+ str(datetime.datetime.now())])
            w.writerows(convo_log.items())

        break

    else:
        run_Bot(user_response)
        
