from Abstract.AActionSubclasses.ActionNotLine import ActionNotLine


class CListChatBots(ActionNotLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Mustra la lista de chatbots.
        :return: void
        """
        self.chatbot.printStructureChatbotDict()

