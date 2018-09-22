from Abstract.AActionSubclasses.ActionNotLine import ActionNotLine


class CShowChatBot(ActionNotLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot= chatbot

    def exec(self,):
        """
        Muestra el chatbot actual.
        :return: void
        """
        self.chatbot.printCurrentStructureChatbot()

