from Abstract.AActionSubclasses.ActionLine import ActionLine

class CSaveSolution(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Método que guarda la sentencia e intención no reconocida.
        :return: void
        """
        if self.chatbot.nameChatbotToSolve == '':
            self.chatbot.output.exec('No hay un ChatBot seleccionado.')
        elif not (self.chatbot.nameChatbotToSolve == '') and self.chatbot.dictUnresolvedErrors == {}:
            self.chatbot.output.exec('El ChatBot "'+self.chatbot.nameChatbotToSolve+'" no tiene errores.')
        elif self.chatbot.senteceToSolve is None and self.chatbot.intentToSolve is None:
            self.chatbot.output.exec('No hay una sentencia ni una intención seleccionados.')
        elif self.chatbot.senteceToSolve is None:
            self.chatbot.output.exec('No hay una sentencia de error seleccionada.')
        elif self.chatbot.intentToSolve is None:
            self.chatbot.output.exec('No hay una intención a la que vincular la sentencia.')
        else:
            self.chatbot.saveSolution()
