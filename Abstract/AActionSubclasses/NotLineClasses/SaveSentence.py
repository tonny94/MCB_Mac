from Abstract.AActionSubclasses.ActionLine import ActionLine
import json


class CSaveSentence(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Guarda la sentencia no reconocida.
        :param : void
        :return: void
        """
        if self.chatbot.unrecognizedSentence is None and self.chatbot.currentSentence is None:
            self.chatbot.output.exec('ERROR: No hay sentencia que guardar.')
        elif self.chatbot.unrecognizedSentence in self.chatbot.errorDict or self.chatbot.currentSentence in self.chatbot.errorDict:
            self.chatbot.output.exec('La sentencia no reconocida ya existe en la lista de errores del Chatbot "'+self.chatbot.name+'".')
        else:
            key = ''
            value = ''

            # se guarda la sentencia y la intención asociada si es que no se ha reconocido dicha sentencia o si la ha
            # reconocido mal.
            if self.chatbot.unrecognizedSentence is None:
                value= self.chatbot.currentIntent.tag
                key = self.chatbot.currentSentence
            else:
                value = self.chatbot.unrecognizeIntent
                key = self.chatbot.unrecognizedSentence

            # método para guardar los errores.
            self.chatbot.saveUnrecognizedSentence(key,value)

            # guarda errores en el fichero de errores del ChatBot.
            with open(self.chatbot.errorFilePath, 'r+', encoding='utf-8') as f:
                json_data = json.load(f)                                            # carga los datos del json
                json_data.update(self.chatbot.errorDict)                            # actualiza la variable con el json
                f.seek(0)
                json.dump(json_data, f, ensure_ascii=False, indent=4)               # guarda los nuevos datos en el json
                f.truncate()

            self.chatbot.output.exec('Se ha guardado la sentencia "' + key + '" que se le asoció con la intención "'+value+'".')
