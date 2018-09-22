import os,inspect,json
from Abstract.AChatBot import CChatBot

from Chatbots.SolveError.Actions.LineClasses.SelectIntent import CSelectIntent
from Chatbots.SolveError.Actions.LineClasses.SelectError import CSelectError
from Chatbots.SolveError.Actions.NotLineClasses.SaveSolution import CSaveSolution
from Chatbots.SolveError.Actions.NotLineClasses.ListResolvedErrors import CListResolvedErrors
from Chatbots.SolveError.Actions.NotLineClasses.ListUnresolvedErrors import CListUnresolvedErrors
from Chatbots.SolveError.Actions.NotLineClasses.ListIntents import CListIntents
from Chatbots.SolveError.Actions.NotLineClasses.ProcessSolutions import CProcessSolutions
from Chatbots.SolveError.Actions.NotLineClasses.ShowCurrentSolution import CShowCurrentSolution
from Chatbots.SolveError.Actions.LineClasses.SelectChatbot import CSelectChatbot
from Chatbots.SolveError.Actions.NotLineClasses.ListChatbots import CListChatbots


class CSolveError(CChatBot):
    """Father class"""

    def __init__(self):
        super(CSolveError, self).__init__()

        #variables para cargar las soluciones resueltas o por resolver
        self.dictUnresolvedErrors = {}
        self.dictResolvedErrors = {}
        self.listIntens = []
        self.currentSolution = {}

        #variables para las rutas del chatbot a resolver
        self.generalPathChatbotToSolve = ''
        self.nameChatbotToSolve=''
        self.nameTransformedChatbotToSolve = ''
        self.pathErrorFileChatbotToSolve = ''
        self.pathJSONChatbotToSolve = ''

        #variables de la solucion dada por el usuario
        self.senteceToSolve = None
        self.intentToSolve = None

        #acciones propias del SolveError
        self.actionsCB = {
                            'selectChatbot': CSelectChatbot(self),
                            'listChatbot': CListChatbots(self),
                            'selectError': CSelectError(self),
                            'selectIntent': CSelectIntent(self),
                            'saveSolution': CSaveSolution(self),
                            'listResolvedErros': CListResolvedErrors(self),
                            'listUnresolvedErros': CListUnresolvedErrors(self),
                            'listIntents': CListIntents(self),
                            'showCurrentSolution':CShowCurrentSolution(self),
                            'processSolutions': CProcessSolutions(self)
                        }

        #Metodos para inicializar variables de ruta y lista de chatbots
        self.initializePaths()
        self.dictChatbots = self.getChatbots()

    def initializePaths(self):
        """
        Inicializa las rutas del SolveError para saver dónde está el fichero de errores, la ruta donde guardar el modelo, etc...
        :return: void
        """
        strSplit = (os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))).split(os.path.sep)   # nombre de los directorios que contiene este fichero
        self.nameTransformed = strSplit[len(strSplit)-1]                                                                       # se selecciona el último directorio
        self.generalPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))                # ruta donde está el chatbot
        self.jsonPath = os.path.join(os.path.sep,self.generalPath,self.nameTransformed+'.json')                                # ruta del json del chatbot
        with open(self.jsonPath, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            self.name = list(data.keys())[0]
        self.errorFilePath = os.path.join(os.path.sep, self.generalPath, self.nameTransformed + '_ErrorFile.json')             # ruta del fichero de errores del chatbot

        if not os.path.isfile(self.errorFilePath):
            with open(self.errorFilePath, 'w', encoding='utf-8') as f:
                json.dump({}, f)                    # si no existe el fichero de errores crea uno vacío

    def getChatbots(self):
        """
        Método que obtiene lista de todos los chatbots
        :return: dict
        """
        dictChatbotToSolve = {}
        self.generalPathChatbotToSolve = os.path.dirname(self.generalPath)
        listAllChatbots = os.listdir(self.generalPathChatbotToSolve)

        for nameChatbot in listAllChatbots:
            pathJson = os.path.join(os.path.sep, self.generalPathChatbotToSolve , nameChatbot,nameChatbot + '.json')  # path del json del chatbot
            with open(pathJson, 'r', encoding='utf-8') as json_data:
                dictChatBot = json.load(json_data)                          # carga el json
                nameWithoutTranform = list(dictChatBot.keys())[0]           # se obtiene el nombre del chatbot
                dictChatbotToSolve[nameWithoutTranform] = nameChatbot
        return dictChatbotToSolve

    def printListResolvedErrors(self):
        """
        Muestra los errores resueltos
        :return: void
        """
        result = ", ".join('"'+str(key)+'" resuelto con el intent "'+str(value)+'"' for key, value in self.dictResolvedErrors.items())
        self.output.exec(result)

    def printListUnresolvedErrors(self):
        """
        Muestra los errores
        :return: void
        """
        result = ", ".join('"'+str(key)+'" que se asoció con el intent "'+str(value)+'"' for key, value in self.dictUnresolvedErrors.items())
        self.output.exec(result)

    def printCurrentSolution(self):
        """
        Muestra la solución actual.
        :return: void
        """
        result = "".join('"' + str(key) + '" asociado a la intención "' + str(value) + '"' for key, value in self.currentSolution.items())
        self.output.exec(result)

    def saveSolution(self):
        """
        Guarda la colución dada por el usuario
        :return: void
        """
        self.dictResolvedErrors[self.senteceToSolve] = self.intentToSolve
        self.currentSolution[self.senteceToSolve] = self.intentToSolve
        del(self.dictUnresolvedErrors[self.senteceToSolve])         # elimina la sentencia del diccionario de errores
        self.output.exec('La sentencia "'+ self.senteceToSolve+ '" se ha asociado a la Intención "'+self.intentToSolve+'".')
        self.senteceToSolve = None      # reinicia el valor de la sentencia
        self.intentToSolve = None       # reinicia el valor de la intención

    # def setNameChabot(self,name):
    #     """
    #     Actualiza el nombre del ChatBot "SolveError"
    #     :param name: Nuevo nombre
    #     :return: void
    #     """
    #     self.name = name

    def printChatbots(self):
        """
        Muestra los chatbots a resolver
        :return: void
        """
        self.output.exec(list(self.dictChatbots.keys()))

    def printIntents(self):
        """
        Muestra las intenciones del chatbot a resolver
        :return: void
        """
        self.output.exec(self.listIntens)

    # def getErrorList(self):
    #     """
    #     Devuelve los errores del chatbot a resolver
    #     :return: dict
    #     """
    #     return self.errorDict



















    # def setCurrentSentence(self, sentence):
    #     """
    #     Guarda la sentencia que se quiere resolver
    #     :param sentence: Sentencia errónea
    #     :return: void
    #     """
    #     self.currentSentence = sentence
    #
    # def setCurrentIntent(self, intent):
    #     """
    #     Guarda la intención con la que se le quiere asociar a la sentencia errónea
    #     :param intent: Intención para asociarlo con la sentencia errónea
    #     :return: void
    #     """
    #     self.currentIntent = intent

    # def setUnrecognizedSentence(self, sentence):
    #     """
    #
    #     :param sentence:
    #     :return: void
    #     """
    #     self.unrecognizedSentence = sentence
    #
    # def setUnrecognizedIntent(self, intent):
    #     self.unrecognizeIntent = intent
