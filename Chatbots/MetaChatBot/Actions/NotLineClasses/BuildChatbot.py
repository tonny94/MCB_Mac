from Abstract.AActionSubclasses.ActionNotLine import ActionNotLine
import os,json
from TrainerPredictor import CTrainerPredictor


class CBuildChatbot(ActionNotLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot
        self.structureChatbot = None
        self.generalPath = os.path.join(os.path.sep,os.getcwd(),'Chatbots')
        self.structureChatbotPath = ''
        self.structureDirJsonFile = ''
        self.structureDirCodeFile = ''
        self.structureActionsPath = ''

    def exec(self,):
        """
        Construye el chatbot, genera su JSON y ficheros .py .
        :return: void
        """
        self.structureChatbot = self.chatbot.currentStructureChatBot
        if self.structureChatbot is None:
            self.chatbot.output.exec('ERROR: No hay un Chatbot actual para construir.')
        else:

            # inicializa las variables de rutas
            self.structureChatbotPath = os.path.join(os.path.sep,self.generalPath,self.structureChatbot.nameTransformed)
            self.structureDirJsonFile = os.path.join(os.path.sep,self.structureChatbotPath,self.structureChatbot.nameTransformed+'.json')
            self.structureDirCodeFile = os.path.join(os.path.sep,self.structureChatbotPath,self.structureChatbot.nameTransformed+'.py')
            self.structureActionsPath = os.path.join(os.path.sep,self.structureChatbotPath,'Actions')

            if not (os.path.isdir(self.generalPath)):
                self.chatbot.output.exec('ERROR: No existe la ruta general "',self.generalPath,'".')
            else:
                if not os.path.isdir(self.structureChatbotPath):
                    os.makedirs(self.structureChatbotPath)                  # crea el directorio del chatbot
                if not os.path.isdir(self.structureActionsPath):
                    os.makedirs(self.structureActionsPath)                  # crea el directorio para las acciones del chatbot
                self.createJSON()                                           # genera el JSON
                self.createCodeFile()                                       # crea los ficheros .py
                self.chatbot.output.exec('Se ha construido el ChatBot "'+self.structureChatbot.name+ '" correctamente.')

    def createJSON(self):
        """
        Crea el fichero JSON para un chatbot.
        :return: void
        """
        with open(self.structureDirJsonFile, 'w', encoding='utf-8') as f:
            json.dump(self.chatbotToJson(), f,ensure_ascii=False,indent=4)
        self.startTrainer()                                                 # genera el modelo

    def chatbotToJson(self):
        """
        Convierte la estructura de un chatbot en JSON
        :return: string
        """
        strJSON = self.structureChatbot.toJSON()                            # estructura de json
        return strJSON

    def createCodeFile(self):
        """
        Crea los ficheros .py para el chatbot
        :return: void
        """
        # with open(self.structureDirCodeFile, 'w', encoding='utf-8') as f:
        #     json.dump(self.chatbotToCode(), f,ensure_ascii=False,indent=4)
        codeFile = open(self.structureDirCodeFile, 'w')
        codeFile.write(self.chatbotToCode())
        codeFile.close()


    def chatbotToCode(self):
        """
        Convierte la estructura del chatbot en string
        :return: string
        """
        strCode = self.structureChatbot.toCode(self.chatbot.listGeneralActions,self.structureActionsPath)
        return strCode

    def startTrainer(self):
        """
        Inicia la creación del modelo
        :return: void
        """
        VTrainer = CTrainerPredictor()                                                      # instancia de un objeto Predictor
        VTrainer.readJSON(self.structureDirJsonFile,self.structureChatbot.name)             # lee el JSON
        VTrainer.createElementsToModel()                                                    # crea el modelo
        value = VTrainer.trainingModel(self.structureChatbotPath)                           # entrena el modelo
        if not value:
            self.chatbot.output.exec('No se ha podido generar el Modelo porque se necesita más de 1 Intención con Patrones creados.')
        else:
            VTrainer.doPickle()                                                             # guarda el modelo
            self.chatbot.output.exec('El modelo del ChatBot "'+self.structureChatbot.name+'" se ha creado.')
