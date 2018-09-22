from Abstract.AActionSubclasses.ActionNotLine import ActionNotLine

class CListUnresolvedErrors(ActionNotLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self, ):
        """
        Método que muestra la lista de errores.
        :return: void
        """
        if self.chatbot.nameChatbotToSolve == '':
            self.chatbot.output.exec('No hay un chatbot seleccionado.')
        elif not (self.chatbot.nameChatbotToSolve == '') and self.chatbot.dictUnresolvedErrors == {}:
            self.chatbot.output.exec('El ChatBot "'+self.chatbot.nameChatbotToSolve+'" no tiene errores.')
        else:
            self.chatbot.printListUnresolvedErrors()