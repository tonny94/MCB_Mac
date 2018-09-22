from Abstract.AActionSubclasses.ActionLine import ActionLine


class CDeleteChatbot(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Borra un ChatBot.
        :return: void
        """
        self.chatbot.showRandomResponse()                       # muestra la respuesta relacionada con el patrón.
        sentence = self.chatbot.input.exec()                    # se espera la entrada del usuario.
        if not (self.checkCancellation(sentence)):
            if not self.chatbot.isEmpty(sentence):
                self.chatbot.deleteStructureChatbotDict(sentence)   # borra un chatbot de la lista de chatbots creados.
            else:
                self.chatbot.output.exec('No se admiten valores vacíos.')

    # def checkCancellation(self,sentence):
    #     if (sentence.lower() in self.listKeysWordsCancelRunning):
    #         self.chatbot.output.exec('Se ha cancelado la operación.')
    #         self.chatbot.unrecognizedSentence = self.chatbot.currentSentence
    #         return True
    #     else:
    #         return False
