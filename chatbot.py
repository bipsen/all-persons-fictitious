from chatterbot import ChatBot
from pythonosc import osc_message_builder
from pythonosc import udp_client
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import operator


def run_Bot(text):
    """This is the main function to run the chatbot, analyse
    the responses with nltk and send OSC messages to pure data.
    """

    # Get chatbot response from the user input.
    bot_response = chatbot.get_response(text).text

    # Print response in bold.
    print('\033[1m' + bot_response + '\033[0m')

    # Get polarity score from chatbot response.
    analysis = vader_analyzer.polarity_scores(text)

    # Change polarity score relatively to a audible frequency.
    freq = (analysis['compound'] - -1) / (1 - -1) * (800 - 200) + 200

    # Send OSC message, to be listened to by pd.
    client.send_message("/filter", freq)


# Set up chatbot.
chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Train based on the english corpus.
chatbot.train("chatterbot.corpus.english")

# Download lexicon for nltk.
nltk.download('vader_lexicon')

# Set up sentiment analyzer.
vader_analyzer = SentimentIntensityAnalyzer()

# Set up OSC client.
ip = 'localhost'
port = 9000
client = udp_client.SimpleUDPClient(ip, port)


# Run the chatbot.
while True:
    user_response = input('Talk (empty to exit): ')
    if not user_response:   # Exit on empty string.
        break
    else:
        run_Bot(user_response)
