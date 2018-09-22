import os,json
import inspect

# Clases chatbot
from Chatbots.MetaChatBot.Actions.NotLineClasses.ShowChatBot import CShowChatBot
from Chatbots.MetaChatBot.Actions.NotLineClasses.ListChatBots import CListChatBots
from Chatbots.MetaChatBot.Actions.LineClasses.ChangeChatbot import CChangeChatbot
from Chatbots.MetaChatBot.Actions.LineClasses.CreateChatbot import CCreateChatbot
from Chatbots.MetaChatBot.Actions.LineClasses.DeleteChatbot import CDeleteChatbot
from Chatbots.MetaChatBot.Actions.NotLineClasses.BuildChatbot import CBuildChatbot
from Chatbots.MetaChatBot.Actions.LineClasses.StartRunningChatbot import CStartRunningChatbot

# Clases intents
from Chatbots.MetaChatBot.Actions.NotLineClasses.ListIntents import CListIntents
from Chatbots.MetaChatBot.Actions.LineClasses.ChangeIntent import CChangeIntent
from Chatbots.MetaChatBot.Actions.LineClasses.CreateIntent import CCreateIntent
from Chatbots.MetaChatBot.Actions.LineClasses.DeleteIntent import CDeleteIntent
from Chatbots.MetaChatBot.Actions.NotLineClasses.ShowIntent import CShowIntent

# Clases patterns
from Chatbots.MetaChatBot.Actions.LineClasses.CreatePattern import CCreatePattern
from Chatbots.MetaChatBot.Actions.LineClasses.DeletePattern import CDeletePattern
from Chatbots.MetaChatBot.Actions.NotLineClasses.ListPatterns import CListPatterns

# Clases responses
from Chatbots.MetaChatBot.Actions.LineClasses.CreateResponse import CCreateResponse
from Chatbots.MetaChatBot.Actions.LineClasses.DeleteResponse import CDeleteResponse
from Chatbots.MetaChatBot.Actions.NotLineClasses.ListResponses import CListResponses

# Clases actions
from Chatbots.MetaChatBot.Actions.LineClasses.CreateAction import CCreateAction
from Chatbots.MetaChatBot.Actions.NotLineClasses.DeleteAction import CDeleteAction
from Chatbots.MetaChatBot.Actions.NotLineClasses.ShowAction import CShowAction

# Clases generales
from Abstract.AChatBot import CChatBot
from StructureChatBot.StructureChatBot import CStructureChatBot


class CMetaChatBot(CChatBot):

    def __init__(self):
        super(CMetaChatBot, self).__init__()

        # variables para guardar los chatbots que se estan creando y el actual
        self.dictChatBots = {}
        self.currentStructureChatBot = None

        # lista para saber cuales no son chatbots creados por el MetaChatbot
        self.listNoChatbots = ['MetaChatBot','SolveError']

        # acciones propias del MetaChatbot
        self.actionsCB ={
            'buildChatBot': CBuildChatbot(self),

            'createChatBot': CCreateChatbot(self),
            'deleteChatBot': CDeleteChatbot(self),
            'listChatBot': CListChatBots(self),
            'changeChatBot': CChangeChatbot(self),
            'showcurrentChatBot': CShowChatBot(self),

            'createIntent': CCreateIntent(self),
            'deleteIntent':CDeleteIntent(self),
            'listIntent': CListIntents(self),
            'changeIntent': CChangeIntent(self),
            'showcurrentIntent': CShowIntent(self),

            'createPattern': CCreatePattern(self),
            'deletePattern': CDeletePattern(self),
            'listPattern': CListPatterns(self),

            'createResponse': CCreateResponse(self),
            'deleteResponse': CDeleteResponse(self),
            'listResponse': CListResponses(self),

            'createAction': CCreateAction(self),
            'deleteAction': CDeleteAction(self),
            'showAction':CShowAction(self),

            'startRunningChatbot': CStartRunningChatbot(self)
        }

        # metodos para inicializar rutas del chatbot y cargar los cahtbots creados por el MetaChatbot
        self.initializePaths()
        self.loadChatbots()

    def loadChatbots(self):
        """
        Carga los chatbots que se han creado con el MetaChatBot y los pone en la variable lista de chatbots.
        :return: void
        """
        pathChatbots = os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))   # ruta donde se guardarán los chatbots
        listAllChatbots = os.listdir(pathChatbots)                          # lista de chatbots en la ruta
        if len(listAllChatbots) == len(self.listNoChatbots):                # si son iguales es que no hay más chatbots que los que están por defecto
            self.output.exec('No hay chatbots para cargar.')
        else:
            currentChatbotLoaded = False                                    # variable para establecer que ya hay un chatbot actual
            for nameChatbot in listAllChatbots:
                if not nameChatbot in self.listNoChatbots:
                    pathJson = os.path.join(os.path.sep, pathChatbots, nameChatbot,nameChatbot+'.json') # path del json del chatbot
                    if os.path.isfile(pathJson):
                        chatbot = CStructureChatBot()                       # objeto chatbot

                        with open(pathJson, 'r', encoding='utf-8') as json_data:
                            dictChatBot = json.load(json_data)                  # carga el json
                            nameWithoutTranform = list(dictChatBot.keys())[0]   # se obtiene el nombre del chatbot
                            chatbot.setName(nameWithoutTranform)
                            intents = dictChatBot[nameWithoutTranform]          # guarda las intenciones del chatbot
                            chatbot.codeToStructureChatbot(chatbot, intents)    # convierte el json en un chatbot
                            chatbot.nameTransformed = nameChatbot               # guarda el nombre del chatbot sin caracteres especiales
                            self.dictChatBots[nameWithoutTranform] = chatbot    # se añade el chatbot a la lista


                        if not currentChatbotLoaded :
                            self.currentStructureChatBot =chatbot           # se establece el primer chatbot como chatbot actual
                            currentChatbotLoaded = True                     # se cambia el boleano
            self.output.exec('Ahora el chatbot actual es "'+self.currentStructureChatBot.name+'".')

    def initializePaths(self):
        """
        Inicializa las rutas del MetaChatbot para saber dónde está el fichero de errores, la ruta donde guardar el modelo, etc...
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
                json.dump({}, f)        # si no existe el fichero de errores crea uno vacío

    def addStructureChatbotDict(self,sentence):
        """
        Genera una estructura de Chatbot con sus intenciones por defecto.
        :param sentence: Nombre del chatbot
        :return: void
        """
        if not sentence in self.dictChatBots:
            myChatBot = CStructureChatBot()             # objeto Chatbot
            nameTransformed = myChatBot.removeASCII(sentence)
            myChatBot.setName(sentence)
            myChatBot.nameTransformed = nameTransformed

            # crea las intenciones por defecto para cada chatbot que se cree
            CCreateIntent(myChatBot).createExitIntent(myChatBot)
            CCreateIntent(myChatBot).createSaveSentenceIntent(myChatBot)
            CCreateIntent(myChatBot).createDontSaveSentenceIntent(myChatBot)

            self.dictChatBots[sentence] = myChatBot         # añade el chatbot a la lista
            self.currentStructureChatBot = myChatBot        # se cambia el chatbot actual
            self.output.exec('El ChatBot "' + sentence + '" se ha añadido correctamente.')
        else:
            self.output.exec('El ChatBot "' + sentence + '" ya existe.')

    def deleteStructureChatbotDict(self,sentence):
        """
        Elimina un chatbot de la lista
        :param sentence: Nombre del chatbot
        :return: void
        """
        if sentence in self.dictChatBots:
            del self.dictChatBots[sentence]
            if not(self.currentStructureChatBot is None) and sentence == self.currentStructureChatBot.name:
                self.currentStructureChatBot = None             # se reestablece el chatbot actual
                self.output.exec('El ChatBot "'+sentence+'" ha dejado de ser el ChatBot actual.')
            self.output.exec('El ChatBot "' + sentence + '" se ha eliminado correctamente .')
        else:
            self.output.exec('El ChatBot "' + sentence + '" no existe .')

    def changeStrunctureCurrentChatbot(self,sentence):
        """
        Cambia el chatbot actual
        :param sentence: Nombre del chatbot
        :return: void
        """
        if not sentence in self.dictChatBots:
            self.output.exec('No existe ese Chatbot.')
        else:
            if not self.currentStructureChatBot is None:
                self.output.exec('Se ha cambiado "'+ self.currentStructureChatBot.name+ '" por "'+ sentence+ '".')
            else:
                self.output.exec('Ahora "'+ sentence+ '" es el actual Chatbot.')
            self.currentStructureChatBot = self.dictChatBots[sentence]  # establece el nuevo chatbot

    def printCurrentStructureChatbot(self):
        """
        Muestra el chatbot actual
        :return: void
        """
        if self.currentStructureChatBot is None:
            self.output.exec('No hay un ChatBot actual.')
        else:
            self.output.exec('El ChatBot actual es "'+ self.currentStructureChatBot.name+ '"')

    def printStructureChatbotDict(self):
        """
        Muestra la lista de Chatbots
        :return:
        """
        if self.dictChatBots == {}:
            self.output.exec('No hay chatbots creados.')
        else:
            result = ", ".join(str(value.name) for key, value in self.dictChatBots.items()) # une los nombres de los chatbots
            self.output.exec('Los chatbot creados son: [ '+ result+' ]')

    # def printIntents(self):
    #     """
    #     Muestra la lista de intenciones del chatbot actual
    #     :return:
    #     """
    #     if self.currentStructureChatBot.currentIntent is None:
    #         self.output.exec('No hay intenciones creadas para el ChatBot "'+self.currentStructureChatBot.name+'".')
    #     else:
    #         self.output.exec(self.intents)

    # def setListIntents(self,list):
    #     """
    #     Actualiza la lista de intenciones del chatbot
    #     :param list: Lista de intenciones
    #     :return: void
    #     """
    #     self.intents = list

    # def setNameChabot(self,name):
    #     """
    #     Actualiza el nombre del chatbot
    #     :param name: Nuevo nombre chatbot
    #     :return: void
    #     """
    #     self.name = name

    # def getErrorList(self):
    #     """
    #     Devuelve el diccionario de errores
    #     :return: dict
    #     """
    #     return self.errorDict