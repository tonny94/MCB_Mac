from Abstract.AActionSubclasses.ActionNotLine import ActionNotLine


class CListPatterns(ActionNotLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Muestra los patrones de una intención.
        :return: void
        """
        if self.chatbot.currentStructureChatBot is None:
            self.chatbot.output.exec('ERROR: No hay un ChatBot actual para listar los Patrones de su Intención actual.')
        elif self.chatbot.currentStructureChatBot.currentIntent is None:
            self.chatbot.output.exec('ERROR: No hay una Intención actual para listar sus Patrones')
        else:
            self.chatbot.currentStructureChatBot.currentIntent.printPatterns()
