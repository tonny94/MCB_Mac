from Abstract.AActionSubclasses.ActionLine import ActionLine


class CChangeIntent(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Cambia la intención actual por otro ya creado.
        :return: void
        """
        if self.chatbot.currentStructureChatBot is None:
            self.chatbot.output.exec('ERROR: No se puede cambiar de Intención porque no hay un Chatbot actual.')
        else:
            self.chatbot.showRandomResponse()
            sentence = self.chatbot.input.exec()
            if not(self.checkCancellation(sentence)):
                if not self.chatbot.isEmpty(sentence):
                    self.chatbot.currentStructureChatBot.setCurrentIntent(sentence)         # cambia la intención actual
                else:
                    self.chatbot.output.exec('No se admiten valores vacíos.')

    # def checkCancellation(self,sentence):
    #     if (sentence.lower() in self.listKeysWordsCancelRunning):
    #         self.chatbot.output.exec('Se ha cancelado la operación.')
    #         return True
    #     else:
    #         return False