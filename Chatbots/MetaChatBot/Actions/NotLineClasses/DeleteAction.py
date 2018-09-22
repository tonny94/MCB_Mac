from Abstract.AActionSubclasses.ActionLine import ActionLine


class CDeleteAction(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self):
        """
        Reinicia la acción de la intención.
        :return: void
        """
        if self.chatbot.currentStructureChatBot is None:
            self.chatbot.output.exec('ERROR: No hay un Chatbot actual para borrar una Acción en una Intención.')
        elif self.chatbot.currentStructureChatBot.currentIntent is None :
            self.chatbot.output.exec('ERROR: No hay una Intención actual para asociarle una Acción.')
        else:
            self.chatbot.currentStructureChatBot.currentIntent.setAction('')
