from Abstract.AActionSubclasses.ActionLine import ActionLine


class CCreatePattern(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self):
        """
        Crea un Patrón.
        :return: void
        """
        if self.chatbot.currentStructureChatBot is None:
            self.chatbot.output.exec('ERROR: No hay un Chatbot actual para crear un PAtrón en una Intención.')
        elif self.chatbot.currentStructureChatBot.currentIntent is None :
            self.chatbot.output.exec('ERROR: No hay Intención actual para asociarle un Patrón.')
        else:
            self.chatbot.showRandomResponse()                           # muestra la respuesta relacionada con el patrón.
            sentence = self.chatbot.input.exec()                        # se espera la entrada del usuario.
            if not(self.checkCancellation(sentence)):
                if not self.chatbot.isEmpty(sentence):
                    state = self.chatbot.currentStructureChatBot.currentIntent.addPattern(sentence) # se guarda el estado al añadir una intención
                    if state:
                        self.chatbot.output.exec('Se ha añadido el Patrón "'+sentence+'" correctamente.')
                else:
                    self.chatbot.output.exec('No se admiten valores vacíos.')

    # def checkCancellation(self,sentence):
    #     if (sentence.lower() in self.listKeysWordsCancelRunning):
    #         self.chatbot.output.exec('Se ha cancelado la operación.')
    #         self.chatbot.unrecognizedSentence = self.chatbot.currentSentence
    #         return True
    #     else:
    #         return False