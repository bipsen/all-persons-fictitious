
# coding: utf-8

# In[ ]:


from chatterbot import ChatBot
import nltk
import time
from pythonosc import osc_message_builder
from pythonosc import udp_client
import operator

chatbot = ChatBot(
    'Ron Obvious',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# Train based on the english corpus
chatbot.train("chatterbot.corpus.english")

#download lexicon for nltk
nltk.download('vader_lexicon')

#set up a OSC client
ip = 'localhost'
port = 9000
client = udp_client.SimpleUDPClient(ip, port)


def ana(text):
    response = chatbot.get_response(text).text
    print('\033[1m' + response + '\033[0m')
    demo_vader_instance(response)


def demo_vader_instance(text):
    global analysis
    from nltk.sentiment import SentimentIntensityAnalyzer
    vader_analyzer = SentimentIntensityAnalyzer()
    analysis = vader_analyzer.polarity_scores(text)
    amp = (analysis['compound'] - -1) / (1 - -1) * (800 - 200) + 200

    client.send_message("/filter", amp)


while True:
    a_str = input('Talk (empty to exit): ')
    if not a_str:   # Exit on empty string.
        break
    else:
        ana(a_str)

