from Abstract.AActionSubclasses.ActionNotLine import ActionNotLine


class CShowAction(ActionNotLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot= chatbot

    def exec(self,):
        """
        Muestra la acción de la intención actual.
        :return: void
        """
        if self.chatbot.currentStructureChatBot is None:
            self.chatbot.output.exec('ERROR: No hay un Chatbot actual para mostrar un Action en una Intención.')
        elif self.chatbot.currentStructureChatBot.currentIntent is None :
            self.chatbot.output.exec('ERROR: No hay una Intención actual para asociarle una Acción.')
        else:
            self.chatbot.currentStructureChatBot.currentIntent.printAction()

