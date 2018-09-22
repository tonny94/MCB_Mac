from Abstract.AActionSubclasses.ActionLine import ActionLine


class CFinishRunningCB(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Termina la ejecución del ChatBot.
        :param : void
        :return: void
        """
        self.chatbot.runChatBot = False
        self.chatbot.output.exec('Se ha parado de ejecutar el Chatbot "'+self.chatbot.name+'".')
