import os
from ChatBotProcessor import CBProcessor
from Chatbots.MetaChatBot.MetaChatBot import CMetaChatBot
from Chatbots.SolveError.SolveError import CSolveError

#META CHATBOT
mcb = CMetaChatBot()
cbp = CBProcessor(mcb)
cbp.startModel()
cbp.startPredictor()
cbp.run()



#SOLVE ERROR
# se = CSolveError()
# cbp = CBProcessor(se)
# cbp.startModel()
# cbp.startPredictor()
# cbp.run()


# import nltk
# nltk.download('punkt')