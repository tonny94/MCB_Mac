from Abstract.AActionSubclasses.ActionLine import ActionLine


class CDeleteIntent(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Borra una Intención.
        :return: void
        """
        if self.chatbot.currentStructureChatBot is None:
            self.chatbot.output.exec('ERROR: No hay un Chatbot actual para eliminar una Intención de su lista.')
        else:
            self.chatbot.showRandomResponse()                       # muestra la respuesta relacionada con el patrón.
            sentence = self.chatbot.input.exec()                    # se espera la entrada del usuario.
            if not(self.checkCancellation(sentence)):
                if not self.chatbot.isEmpty(sentence):
                    self.chatbot.currentStructureChatBot.deleteIntent(sentence) #borra una intención de la lista de intenciones creados.
                else:
                    self.chatbot.output.exec('No se admiten valores vacíos.')


    # def checkCancellation(self,sentence):
    #     if (sentence.lower()  in self.listKeysWordsCancelRunning):
    #         self.chatbot.output.exec('Se ha cancelado la operación.')
    #         self.chatbot.unrecognizedSentence = self.chatbot.currentSentence
    #         return True
    #     else:
    #         return False