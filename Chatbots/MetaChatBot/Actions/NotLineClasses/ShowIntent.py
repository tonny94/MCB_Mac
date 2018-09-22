from Abstract.AActionSubclasses.ActionNotLine import ActionNotLine


class CShowIntent(ActionNotLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot= chatbot

    def exec(self,):
        """
        Muestra la intención actual del chatbot actual.
        :return: void
        """
        if self.chatbot.currentStructureChatBot is None:
            self.chatbot.output.exec('ERROR: No hay Chatbot actual para mostrar su Intención actual.')
        else:
            self.chatbot.currentStructureChatBot.printCurrentIntent()
