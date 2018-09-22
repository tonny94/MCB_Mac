from Abstract.AActionSubclasses.ActionNotLine import ActionNotLine

class CListChatbots(ActionNotLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self, ):
        """
        Ejecuta el método de mostrar la lista de chatbots
        :return: void
        """
        self.chatbot.printChatbots()
