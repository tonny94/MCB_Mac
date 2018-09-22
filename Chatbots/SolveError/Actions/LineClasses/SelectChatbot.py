from Abstract.AActionSubclasses.ActionLine import ActionLine
import os,json


class CSelectChatbot(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Carga los datos del chatbot tras seleccionarlo
        :return: void
        """
        self.chatbot.showRandomResponse()                           # muestra la respuesta relacionada con el patrón.
        sentence = self.chatbot.input.exec()                        # se espera la entrada del usuario.
        if not (self.checkCancellation(sentence)):
            if not self.chatbot.isEmpty(sentence):
                if not(sentence in self.chatbot.dictChatbots):
                    self.chatbot.output.exec('El ChatBot "'+sentence+'" no existe.')

                else:
                    nameChatbotTransformed = self.chatbot.dictChatbots[sentence]
                    if not os.path.exists(os.path.join(os.path.sep,self.chatbot.generalPathChatbotToSolve,nameChatbotTransformed,nameChatbotTransformed+'_ErrorFile.json')):  # comprueba si exite fichero de errores
                        self.chatbot.output.exec('El ChatBot "' + sentence + '" no tiene un fichero de errores.')
                    else:
                        self.chatbot.pathErrorFileChatbotToSolve = os.path.join(os.path.sep,self.chatbot.generalPathChatbotToSolve,nameChatbotTransformed,nameChatbotTransformed+'_ErrorFile.json')     # fichero de errores
                        self.chatbot.pathJSONChatbotToSolve = os.path.join(os.path.sep,self.chatbot.generalPathChatbotToSolve,nameChatbotTransformed, nameChatbotTransformed + '.json')                 # fichero json

                        with open(self.chatbot.pathErrorFileChatbotToSolve, 'r', encoding='utf-8') as json_data:
                            self.chatbot.dictUnresolvedErrors = json.load(json_data)    # carga la lista de errores

                        if self.chatbot.dictUnresolvedErrors == {}:
                            self.chatbot.output.exec('El ChatBot "'+sentence+'" no tiene sentencias que resolver.')
                        else:
                            self.chatbot.nameChatbotToSolve = sentence
                            self.nameTransformedChatbotToSolve = nameChatbotTransformed
                            listIntents = []
                            with open(self.chatbot.pathJSONChatbotToSolve, 'r', encoding='utf-8') as json_data:
                                jsonChatbot = json.load(json_data)
                                for i in jsonChatbot[sentence]:
                                    listIntents.append(i['tag'])            # se carga las intenciones del chatbot seleccionado
                            self.chatbot.listIntens = listIntents
                            self.chatbot.output.exec('Se ha seleccionado el ChatBot "'+ sentence+ '".')
            else:
                self.chatbot.output.exec('No se admiten valores vacíos.')

    # def checkCancellation(self, sentence):
    #     if (sentence.lower()  in self.listKeysWordsCancelRunning):
    #         self.chatbot.output.exec('Se ha cancelado la operacion')
    #         self.chatbot.unrecognizedSentence = self.chatbot.currentSentence
    #         return True
    #     else:
    #         return False
