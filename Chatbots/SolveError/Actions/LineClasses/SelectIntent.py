from Abstract.AActionSubclasses.ActionLine import ActionLine


class CSelectIntent(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Selecciona una intención.
        :return: void
        """
        if self.chatbot.nameChatbotToSolve == '':
            self.chatbot.output.exec('No hay un chatbot seleccionado.')
        elif not (self.chatbot.nameChatbotToSolve == '') and self.chatbot.dictUnresolvedErrors == {}:
            self.chatbot.output.exec('El ChatBot "' + self.chatbot.nameChatbotToSolve + '" no tiene errores.')
        else:
            self.chatbot.showRandomResponse()                       # muestra la respuesta relacionada con el patrón.
            sentence = self.chatbot.input.exec()                    # se espera la entrada del usuario.
            if not (self.checkCancellation(sentence)):
                if not self.chatbot.isEmpty(sentence):
                    if not(sentence in self.chatbot.listIntens):
                        self.chatbot.output.exec('La Intención no existe en la lista.')
                    else:
                        self.chatbot.intentToSolve = sentence       # guarda la intención seleccionada.
                        self.chatbot.output.exec('Se ha seleccionado la Intención "'+sentence+'".')
                else:
                    self.chatbot.output.exec('No se admiten valores vacíos.')

    # def checkCancellation(self, sentence):
    #     if (sentence.lower() in self.listKeysWordsCancelRunning):
    #         self.chatbot.output.exec('Se ha cancelado la operacion')
    #         self.chatbot.unrecognizedSentence = self.chatbot.currentSentence
    #         return True
    #     else:
    #         return False
