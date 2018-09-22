#Clases de acciones
from Abstract.AActionSubclasses.ActionLine import ActionLine



class CCreateChatbot(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Crea un ChatBot.
        :return: void
        """
        self.chatbot.showRandomResponse()                           # muestra la respuesta relacionada con el patrón.
        sentence = self.chatbot.input.exec()                        # se espera la entrada del usuario.
        if not (self.checkCancellation(sentence)):
            if not self.chatbot.isEmpty(sentence):
                self.chatbot.addStructureChatbotDict(sentence)      # se añade un nuevo chatbot a la lista.
            else:
                self.chatbot.output.exec('No se admiten valores vacíos.')


    # def checkCancellation(self,sentence):
    #     if (sentence.lower() in self.listKeysWordsCancelRunning):
    #         self.chatbot.output.exec('Se ha cancelado la operación.')
    #         return True
    #     else:
    #         return False