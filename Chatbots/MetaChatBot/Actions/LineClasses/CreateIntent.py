from Abstract.AActionSubclasses.ActionLine import ActionLine

from StructureChatBot.StructureIntent import CStructureIntent


class CCreateIntent(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self):
        """
        Crea una Intención.
        :return: void
        """
        if self.chatbot.currentStructureChatBot is None:
            self.chatbot.output.exec('ERROR: No hay un Chatbot actual para asociarle una Intención.')
        else:
            self.chatbot.showRandomResponse()                                           # muestra la respuesta relacionada con el patrón.
            sentence = self.chatbot.input.exec()                                        # se espera la entrada del usuario.
            if not(self.checkCancellation(sentence)):
                if not self.chatbot.isEmpty(sentence):
                    state = self.chatbot.currentStructureChatBot.addIntent(sentence)    # se guarda el estado al añadir una intención
                    if state:
                        self.chatbot.output.exec('La Intención "' + sentence + '" se ha añadido correctamente.')
                else:
                    self.chatbot.output.exec('No se admiten valores vacíos.')

    def createExitIntent(self,chatbot):
        """
        Crea la intención por defecto de FinishRunningChatbot
        :param chatbot: El Chatbot que se está  creando.
        :return: void
        """
        intent = CStructureIntent()
        intent.setTag('finishRunningChatbot')
        intent.setAction('finishRunningChatbot')
        intent.addPattern('salir')
        intent.addPattern('salir del chatbot')
        intent.addPattern('parar chatbot')
        intent.addPattern('terminar de ejecutar chatbot')
        intent.addPattern('parar')
        intent.responses = []
        chatbot.dicIntents['finishRunningChatbot'] = intent

    def createSaveSentenceIntent(self,chatbot):
        """
        Crea la intención por defecto de SaveSentence
        :param chatbot: El Chatbot que se está  creando.
        :return: void
        """
        intent = CStructureIntent()
        intent.setTag('saveSentence')
        intent.setAction('saveSentence')
        intent.addListPatterns(["@Guardar","@Salvar"])
        intent.responses = []
        chatbot.dicIntents['saveSentence'] = intent

    def createDontSaveSentenceIntent(self,chatbot):
        """
        Crea la intención por defecto de DontSaveSentence
        :param chatbot: El Chatbot que se está  creando.
        :return: void
        """
        intent = CStructureIntent()
        intent.setTag('dontSaveSentence')
        intent.setAction('dontSaveSentence')
        intent.addListPatterns(["@No guardar","@No salvar"])
        intent.responses = []
        chatbot.dicIntents['dontSaveSentence'] = intent

    # def checkCancellation(self,sentence):
    #     if (sentence.lower() in self.listKeysWordsCancelRunning):
    #         self.chatbot.output.exec('Se ha cancelado la operación.')
    #         return True
    #     else:
    #         return False