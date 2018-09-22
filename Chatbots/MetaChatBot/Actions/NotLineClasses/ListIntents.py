from Abstract.AActionSubclasses.ActionNotLine import ActionNotLine


class CListIntents(ActionNotLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Muestra la lista de intenciones de un chatbot.
        :return: void
        """
        if self.chatbot.currentStructureChatBot is None:
            self.chatbot.output.exec('ERROR: No hay un ChatBot actual para listar sus Intenciones.')
        else:
            self.chatbot.currentStructureChatBot.printDictIntents()
