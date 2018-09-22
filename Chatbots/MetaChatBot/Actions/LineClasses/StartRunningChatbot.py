from Abstract.AActionSubclasses.ActionLine import ActionLine
from ChatBotProcessor import CBProcessor


class CStartRunningChatbot(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        self.chatbot.showRandomResponse()                               # muestra la respuesta relacionada con el patrón.
        sentence = self.chatbot.input.exec()                            # se espera la entrada del usuario.
        if not (self.checkCancellation(sentence)):
            if not self.chatbot.isEmpty(sentence):
                if not sentence in self.chatbot.dictChatBots.keys():
                    self.chatbot.output.exec('No se ha encontrado el Chatbot "'+sentence+'".')
                else:
                    nameTransformed = self.chatbot.dictChatBots[sentence].nameTransformed
                    self.executeChatbot(nameTransformed)                       # ejecuta el chatbot
            else:
                self.chatbot.output.exec('No se admiten valores vacíos.')

    # def checkCancellation(self, sentence):
    #     if (sentence.lower() in self.listKeysWordsCancelRunning):
    #         self.chatbot.output.exec('Se ha cancelado la operación.')
    #         self.chatbot.unrecognizedSentence = self.chatbot.currentSentence
    #         return True
    #     else:
    #         return False

    def executeChatbot(self,nameChatbot):
        """
        Ejecuta un chatbot de la lista de chatbots.
        :param nameChatbot: Nombre del chatbot a ejecutar
        :return: void
        """
        stringToImport = 'Chatbots.'+nameChatbot+'.'+nameChatbot                    # estructura de directorios del chatbot a ejecutar.
        pathChatbot = __import__(stringToImport)
        pathDirectory = getattr(pathChatbot,nameChatbot)
        pathFile = getattr(pathDirectory,nameChatbot)
        classChatbot = getattr(pathFile,'C'+nameChatbot)                            # ruta del la clase del chatbot a ejecutar

        chatbotInstance = classChatbot()                                            # instancia la clase del chatbot a ejecutar
        self.chatbot.output.exec('Cargando modelo del Chatbot "'+nameChatbot+'"...')
        cbp = CBProcessor(chatbotInstance)                                          # objeto del Procesor para ejecutar el chatbot
        cbp.startModel()                                                            # genera el model
        cbp.startPredictor()                                                        # empieza ejecución del Predictor
        cbp.run()                                                                   # ejecuta el chatbot