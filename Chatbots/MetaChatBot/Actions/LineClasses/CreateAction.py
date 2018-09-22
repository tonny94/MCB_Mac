from Abstract.AActionSubclasses.ActionLine import ActionLine


class CCreateAction(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self):
        """
        Crea una acción para la intención actual.
        :return: void
        """
        if self.chatbot.currentStructureChatBot is None:
            self.chatbot.output.exec('ERROR: No hay ningún Chatbot actual para crear una Acción en una Intención.')
        elif self.chatbot.currentStructureChatBot.currentIntent is None :
            self.chatbot.output.exec('ERROR: No hay Intención actual para asociarle una Acción.')
        else:
            self.chatbot.showRandomResponse()                                           # muestra la respuesta relacionada con el patrón.
            sentence = self.chatbot.input.exec()                                        # se espera la entrada del usuario.
            if not(self.checkCancellation(sentence)):
                if not self.chatbot.isEmpty(sentence):
                    self.chatbot.currentStructureChatBot.currentIntent.setAction(sentence)  # guarda la acción
                    self.chatbot.output.exec('Se ha guardado la acción "'+sentence+'".')
                else:
                    self.chatbot.output.exec('No se admiten valores vacíos.')

    # def checkCancellation(self,sentence):
    #     if (sentence.lower() in self.listKeysWordsCancelRunning):
    #         self.chatbot.output.exec('Se ha cancelado la operación.')
    #         return True
    #     else:
    #         return False