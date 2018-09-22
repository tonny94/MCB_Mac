from Abstract.AActionSubclasses.ActionLine import ActionLine
import os,json
from TrainerPredictor import CTrainerPredictor

class CProcessSolutions(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Método que procesa los errores a resolver.
        :return: void
        """
        if self.chatbot.nameChatbotToSolve == '':
            self.chatbot.output.exec('No hay un chatbot seleccionado.')
        elif not (self.chatbot.nameChatbotToSolve == '') and self.chatbot.dictResolvedErrors == {}:
            self.chatbot.output.exec('El ChatBot "'+self.chatbot.nameChatbotToSolve+'" no tiene soluciones que aplicar.')
        else:
            with open(self.chatbot.pathJSONChatbotToSolve, 'r+',encoding='utf-8') as f:
                data = json.load(f)                                     # carga los datos del json
                intents = data[self.chatbot.nameChatbotToSolve]         # selecciona las intenciones del chatbot
                for sentence,intent in self.chatbot.dictResolvedErrors.items():
                    for i in intents:
                        if i['tag'] == intent:                          # encuentra la intención donde añadirá la sentencia a resolver
                            i['patterns'].append(sentence)
                            break                                       # para no seguir buscando

                f.seek(0)
                json.dump(data, f, ensure_ascii=False,indent=4)         # se vuelve a cargar el json editado
                f.truncate()

            listSolvedErros = []
            with open(self.chatbot.pathErrorFileChatbotToSolve, 'r+', encoding='utf-8') as f:
                json_data = json.load(f)                                    # se carga los errores del fichero de errores
                copyResolvedErrores = self.chatbot.dictResolvedErrors.copy()# copia para el recorrido de errores resueltos
                for k, v in copyResolvedErrores.items():
                    listSolvedErros.append(k)                               # se guarda en una lista solo las sentencias resueltas
                    del (json_data[k])                                      # se elimina del json las sentencias resueltas
                    del (self.chatbot.dictResolvedErrors[k])                # se elimina las sentencias del diccionario de errores
                result = ", ".join(str(value) for value in listSolvedErros) # se genera un string para el aviso

                f.seek(0)
                json.dump(json_data, f, ensure_ascii=False, indent=4)       # se guarda los cambios en el json
                f.truncate()

            self.rebuildModel()                                             # reconstruye el modelo
            self.chatbot.output.exec('Se han resuelto los errores: '+result)# muestra el mensaje


    def rebuildModel(self):
        """
        Reconstruye el modelo
        :return: void
        """
        if not (os.path.exists(self.chatbot.pathJSONChatbotToSolve)):
            self.chatbot.output.exec('No existe el fichero JSON "'+self.chatbot.pathJSONChatbotToSolve+'".')
        else:
            self.chatbot.output.exec('Generando el modelo para el ChatBot "'+self.chatbot.name+'"...')
            TrainerAndPredictor = CTrainerPredictor()
            TrainerAndPredictor.readJSON(self.chatbot.pathJSONChatbotToSolve,self.chatbot.nameChatbotToSolve)   # lee el json
            TrainerAndPredictor.createElementsToModel()                                 # crea elementos para el modelo
            pathModelChatbotToSolve = os.path.join(os.path.sep,self.chatbot.generalPathChatbotToSolve,self.chatbot.nameTransformedChatbotToSolve)  # ruta donde se guardará el modelo
            value = TrainerAndPredictor.trainingModel(pathModelChatbotToSolve)  # valor si el modelo se ha generado correctamente
            if not value:
                self.chatbot.output.exec('No se ha podido generar el Modelo porque se necesita más de 1 Intención con Patrones creados.')
            else:
                TrainerAndPredictor.doPickle()             # guarda el modelo
                self.chatbot.output.exec('El modelo se ha generado correctamente')
