import os,json
import TrainerPredictor

#importaciones para clases de Acciones

from Abstract.AActionSubclasses.NotLineClasses.FinishRunningCB import CFinishRunningCB
from Abstract.AActionSubclasses.NotLineClasses.SaveSentence import CSaveSentence
from Abstract.AActionSubclasses.NotLineClasses.DontSaveSentence import CDontSaveSentence
from Abstract.AActionSubclasses.NotLineClasses.NotRecognizedSentence import CNotRecognizedSentence

#clase para obetener el tipo de entrada/salida de datos
from Abstract.AInteractor import IInteractor


class CChatBot(object):

    def __init__(self):

        # variables propias del Chatbot a crear
        self.name = ''
        self.nameTransformed = ''
        self.intents = []
        self.jsonPath = ''
        self.generalPath = ''
        self.actionsPath = ''
        self.errorFilePath = ''
        self.errorDict = {}

        # variable que cancela la ejecucion de un Chatbot
        self.runChatBot = True

        # variable para guardar la semtemcia no guardada
        self.currentSentence = None
        self.currentIntent = None
        self.unrecognizedSentence = None
        self.unrecognizeIntent = None

        # acciones por defecto a la hora de crear Chatbots
        self.listGeneralActions = ['finishRunningChatbot','saveSentence','dontSaveSentence']
        self.actions = {
            'finishRunningChatbot': CFinishRunningCB(self),
            'saveSentence': CSaveSentence(self),
            'dontSaveSentence': CDontSaveSentence(self)
            }

        # clase con metodos de entrenar y predecir
        self.TrainerAndPredictor = None

        # modos de entrada/saalida de datos
        self.input = IInteractor.input
        self.output = IInteractor.output

    def initializePaths(self):
        """
        Método de inicialización de rutas del chatbot a crear.
        :return:
        """
        pass

    def isEmpty(self,sentence):
        """
        Comprueba si la sentencia introducida es vacía o no.
        :param sentence:
        :return: boolean
        """
        return sentence in ['',None,""]

    def saveUnrecognizedSentence(self,key,value):
        """
        Guarda la sentencia no reconocida del chatbot en ejecución.
        :param key:
        :param value:
        :return: void
        """
        self.errorDict[key] = value

    def showRandomResponse(self):
        """
        Muestra la respuesta al patrón introducido.
        :return: void
        """
        self.output.exec(self.TrainerAndPredictor.randomResponse)

    def execPrediction(self,sentence):
        """
        Ejecuta la acción que se reconoce con el Predictor.
        :param sentence: Sentencia que se usa para la predicción.
        :return:
        """
        valorClasificacion = self.TrainerAndPredictor.classify(sentence)            # valores de la clasificación de la sentencia
        if (not valorClasificacion == []) and valorClasificacion[0][1] >= 0.9:
            self.TrainerAndPredictor.predict(sentence)                              # predice la acción
            self.currentAction = self.TrainerAndPredictor.action                    # se guarda la acción

            if not self.currentAction == '':
                self.setCurrentSentence(sentence)                                   # guarda la sentencia
                self.setCurrentIntent(self.TrainerAndPredictor.intent['tag'])       # guarda la intención que se predijo
                self.actions[self.currentAction].exec()                             # ejecuta la acción
                self.TrainerAndPredictor.action = ''                                # reinicia la acción

            # reinicia los atributos de sentencias no reconocidas
            self.setUnrecognizedSentence(None)
            self.setUnrecognizedIntent(None)
        else:
            self.setUnrecognizedSentence(sentence)                                  #guarda la sentencia que no se reconoció
            value = '"No se le asoció una intención"'
            if not valorClasificacion == []:
               value = valorClasificacion[0][0]                                     #guarda en la variable la intención de la clasificación
            self.setUnrecognizedIntent(value)                                       #guarda la intención asociada a la sentencia no reconocida
            CNotRecognizedSentence(self.unrecognizedSentence).exec()

    def setUnrecognizedSentence(self, sentence):
        """
        Guarda la sentencia no reconocida.
        :param sentence:
        :return: void
        """
        self.unrecognizedSentence = sentence

    def setUnrecognizedIntent(self, intent):
        """
        Guarda la intención asociada a la sentencia no reconocida.
        :param intent:
        :return: void
        """
        self.unrecognizeIntent = intent

    def setCurrentSentence(self, sentence):
        """
        Guarda la sentencia reconocida.
        :param sentence:
        :return: void
        """
        self.currentSentence = sentence

    def setCurrentIntent(self, intent):
        """
        Guarda la intención asociada a la sentencia reconocida.
        :param intent:
        :return: void
        """
        self.currentIntent = intent

    def existModel(self,path):
        """
        Comprueba si existe un modelo para el ChatBot.
        :param path: Ruta donde está el modelo.
        :return: boolean
        """
        return os.path.exists(os.path.join(os.path.sep,path,'model.h5'))

    def startModel(self):
        """
        Genera el modelo para el ChatBot.
        :return:
        """
        if not (os.path.exists(self.jsonPath)):
            self.output.exec('No existe el fichero JSON "'+self.jsonPath+'".')
        else:
            if not self.existModel(self.generalPath):
                self.output.exec('Generando modelo...')
                self.TrainerAndPredictor = TrainerPredictor.CTrainerPredictor()
                self.TrainerAndPredictor.readJSON(self.jsonPath,self.name)                  #lee el fichero json
                self.TrainerAndPredictor.createElementsToModel()                            #genera el modelo con el json
                value = self.TrainerAndPredictor.trainingModel(self.generalPath)            #entrena el modelo
                if not value:
                    self.output.exec('No se ha podido generar el Modelo porque se necesita más de 1 Intención con Patrones creados.')
                else:
                    self.TrainerAndPredictor.doPickle()                                     #guarda ficheros
                    self.output.exec('Modelo generado correctamente.')
            else:
                self.output.exec('El modelo ya existe')

    def startPredictor(self):
        """
        Inicializa los atributos necesarios del "TrainerAndPredictor"
        :return:void
        """
        if not (os.path.exists(self.jsonPath)):
            self.output.exec('No existe el fichero JSON "'+self.jsonPath+'".')
        else:
            self.output.exec('Ejecutando el Predictor...')
            if self.TrainerAndPredictor is None:
                self.TrainerAndPredictor = TrainerPredictor.CTrainerPredictor()
                self.TrainerAndPredictor.loadArrays(self.generalPath)                       #carga las listas necesarias
                self.TrainerAndPredictor.readJSON(self.jsonPath,self.name)                  #lee el json
                self.TrainerAndPredictor.loadModel()                                        #carga el modelo

            self.setIntentsList()                                                           #actualiza el atributo de intenciones
            self.setErrorDict()                                                             #actualiza el atributo de errores
            self.output.exec('Predictor ejecutado correctamente.')

    def setIntentsList(self):
        """
        Actualiza el atributo de intenciones.
        :return:
        """
        self.intents = self.TrainerAndPredictor.classes

    def setErrorDict(self):
        """
        Actualiza el atributo de errores.
        :return: 
        """
        with open(self.errorFilePath, 'r', encoding='utf-8') as json_data:
            self.errorDict = json.load(json_data)