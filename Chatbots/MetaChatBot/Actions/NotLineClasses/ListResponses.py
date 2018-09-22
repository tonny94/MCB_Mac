from Abstract.AActionSubclasses.ActionNotLine import ActionNotLine


class CListResponses(ActionNotLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Muestra la lista de respuestas de un chatbot.
        :return: void
        """
        if self.chatbot.currentStructureChatBot is None:
            self.chatbot.output.exec('ERROR: No hay un ChatBot actual para listar las Respuestas de su Intención actual.')
        elif self.chatbot.currentStructureChatBot.currentIntent is None:
            self.chatbot.output.exec('ERROR: No hay una Intención actual para listar sus Respuestas')
        else:
            self.chatbot.currentStructureChatBot.currentIntent.printResponses()
