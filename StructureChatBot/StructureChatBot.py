import os,unicodedata,json
from StructureChatBot.StructureIntent import CStructureIntent

#clase para obetener el tipo de entrada/salida de datos
from Abstract.AInteractor import IInteractor


class CStructureChatBot:

    def __init__(self):
        self.name = ''
        self.nameTransformed = ''
        self.dicIntents = {}
        self.currentIntent = None
        self.ouput = IInteractor.output

    def setName(self, name):
        """
        Actualiza el nombre el chatbot
        :param name: Nombre del chatbot
        :return: void
        """
        self.name = name

    def printCurrentIntent(self):
        """
        Muestra la intención actual
        :return: void
        """
        if self.currentIntent is None:
            self.ouput.exec('No hay una Intención actual para el ChatBot "'+self.name+'".')
        else:
            self.ouput.exec('La Intención actual es "'+self.currentIntent.tag+'".')

    def printDictIntents(self):
        """
        Muestra las intenciones del chatbot
        :return: void
        """
        result = ", ".join(str(value.tag) for key, value in self.dicIntents.items())
        self.ouput.exec('Las Intenciones del ChatBot "'+self.name+'" son:'+result)

    def addIntent(self, nameIntent):
        """
        Añade una intención a la lista y actualiza la intención actual, devuelve un estado según cómo haya ido la inserción
        :param nameIntent: Nombre de la intención a insertar
        :return: boolean
        """
        if nameIntent in self.dicIntents:
            self.ouput.exec('Ya existe "'+ nameIntent+ '" en la lista de Intenciones del ChatBot "'+ self.name+ '".')
            return False
        else:
            myIntent = CStructureIntent()
            myIntent.setTag(nameIntent)
            self.dicIntents[nameIntent] = myIntent
            self.currentIntent = myIntent
            return True

    def deleteIntent(self, nameIntent):
        """
        Elimina la intención de la lista, si existe, y si es el actual reinicia el atributo 'currentIntent'
        :param nameIntent: Intención a borrar
        :return: void
        """
        if nameIntent in self.dicIntents:
            del self.dicIntents[nameIntent]
            self.ouput.exec('Se ha eliminado "'+nameIntent+'" de la lista de Intenciones del ChatBot "'+self.name+'".')

            if not(self.currentIntent is None) and nameIntent == self.currentIntent.tag:
                self.currentIntent = None                                           # reinicio del atributo
                self.ouput.exec('"'+nameIntent+'" ha dejado se ser la intención actual.')
        else:
            self.ouput.exec('No existe "'+nameIntent+'" en la lista de Intenciones del ChatBot "'+self.name+'".')

    def setCurrentIntent(self, nameIntent):
        """
        Cambia la intención actual si existe en la lista
        :param nameIntent: Intención que será la actual
        :return: void
        """
        if nameIntent in self.dicIntents:
            if not self.currentIntent is None:
                self.ouput.exec('Se ha cambiado "'+ self.currentIntent.tag+ '" por "'+nameIntent+'".')
            else:
                self.ouput.exec('Ahora "'+nameIntent+'" es la Intención actual.')
            self.currentIntent = self.dicIntents[nameIntent]
        else:
            self.ouput.exec('No existe "'+ nameIntent+ '" en la lista de intenciones del ChatBot "'+ self.name+ '".')

    def dicToJSON(self,dicIntents):
        """
        Convierte la estructura de un diccionario a json
        :param dicIntents: Diccionario a convertir
        :return: list
        """
        listIntents = []
        if len(dicIntents) > 0:
            for intent in dicIntents:
                listIntents.append(dicIntents[intent].toJSON())
        return listIntents

    def toJSON(self):
        """
        Convierte la estructura del chatbot a JSON
        :return: dict
        """
        dictJson = {}
        dictJson[self.name] = self.dicToJSON(self.dicIntents)
        return dictJson

    def toCode(self,listGeneralActions,pathAction):
        """
        Devuelve un string con la estructura adecuada para generar un fichero .py
        :param listGeneralActions: Lista de acciones que se crearán
        :param pathAction: Ruta donde se guardarán los ficheros de las acciones
        :return: string
        """
        lengDict = 1
        strImports = 'import os,inspect,json \nfrom Abstract.AChatBot import CChatBot\nfrom Abstract.AActionSubclasses.NotLineClasses.NotRecognizedSentence import CNotRecognizedSentence\n'
        strActions = 'self.actionsCB = {'

        # seleccionar acciones que no sean las acciones generales y aquellas intenciones que si tengan acción
        listActions = []
        for tag in self.dicIntents:
            if not tag in listGeneralActions:
                intent = self.dicIntents[tag]
                if not intent.action == '':
                    listActions.append(intent.action)

        # recorre la lista de acciones para crear sus ficheros
        for action in listActions:
            actionTransformed = self.removeASCII(action)
            nameActionFile = actionTransformed.title()
            nameActionClass = 'C'+actionTransformed.title()
            self.createActions(pathAction,nameActionFile,nameActionClass)        #crea los ficheros .py de cada acción

            #construye el diccionario de acciones
            if lengDict == 1:
                strActions += '\''+action+'\':'+nameActionClass+'(self)'
                lengDict = 0
            else:
                strActions += ', \''+action+'\':'+nameActionClass+'(self)'

            #construye el string de todos los import para las acciones
            strImports += 'from Chatbots.'+self.nameTransformed+'.Actions.'+nameActionFile+' import '+nameActionClass+'\n'

        strActions += ' }'
        strChatbotClass = 'C'+self.nameTransformed
        strChatbotCode = strImports+'\nclass '+strChatbotClass+'(CChatBot):\n'
        strChatbotCode += '\tdef __init__(self):\n'
        strChatbotCode += '\t\tsuper('+strChatbotClass+', self).__init__()\n'
        strChatbotCode += '\t\t'+strActions+'\n'
        strChatbotCode += '\t\tself.initializePaths()\n\n'

        #initializePaths
        strChatbotCode +='\tdef initializePaths(self):\n'
        strChatbotCode += '\t\tstrSplit = (os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))).split(os.path.sep)\n'
        strChatbotCode += '\t\tself.nameTransformed = strSplit[len(strSplit)-1]\n'
        strChatbotCode += '\t\tself.generalPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))\n'
        strChatbotCode += '\t\tself.jsonPath = os.path.join(os.path.sep,self.generalPath,self.nameTransformed+\'.json\')\n'
        strChatbotCode += '\t\twith open(self.jsonPath, \'r+\', encoding=\'utf-8\') as f:\n'
        strChatbotCode += '\t\t\tdata = json.load(f)\n'
        strChatbotCode += '\t\t\tself.name = list(data.keys())[0]\n'
        strChatbotCode += '\t\tself.errorFilePath = os.path.join(os.path.sep, self.generalPath, self.nameTransformed + \'_ErrorFile.json\')\n'
        strChatbotCode += '\t\tif not os.path.isfile(self.errorFilePath):\n'
        strChatbotCode += '\t\t\twith open(self.errorFilePath, \'w\', encoding=\'utf-8\') as f:\n'
        strChatbotCode += '\t\t\t\tjson.dump({}, f)\n\n'

        #saveUnrecognizedSentence
        strChatbotCode += '\tdef saveUnrecognizedSentence(self,key,value):\n'
        strChatbotCode += '\t\tself.errorDict[key] = value\n\n'

        return strChatbotCode

    def removeASCII(self,name):
        """
        Transforma el parámetro quitando los caracteres especiales y los espacios en blanco
        :param name:
        :return: string
        """
        actionTransformed = unicodedata.normalize('NFKD', name).encode('ASCII','ignore')  # elimiona los caracteres especiales
        actionTransformed = actionTransformed.decode("utf-8")  # transforma en string
        actionTransformed = actionTransformed.replace(' ', '_')  # elimina espacies en blanco
        return actionTransformed

    def createActions(self, pathAction, nameActionFile, nameActionClass):
        """
        Crea ficheros de las acciones
        :param pathAction: Ruta de la acción
        :param nameActionFile: Nombre del fichero de la acción
        :param nameActionClass: Nombre de la clase de la acción
        :return: void
        """
        codeFile = open(os.path.join(os.path.sep, pathAction, nameActionFile + '.py'), 'w')
        codeFile.write(self.actionToCode(nameActionClass))
        codeFile.close()

    def actionToCode(self, nameActionClass):
        """
        Devuelve la estructura de una acción para un fichero .py
        :param nameActionClass: Nombre de la clase
        :return: string
        """
        str = 'from Abstract.AActionSubclasses.ActionNotLine import ActionNotLine\n'
        str += 'class ' + nameActionClass + '(ActionNotLine):\n\n'
        str += '\tdef __init__(self,chatbot):\n'
        str += '\t\tself.chatbot = chatbot\n\n'
        str += '\tdef exec(self,):\n'
        str += '\t\tpass'
        return str

    def codeToStructureChatbot(self,chatbot,intents):
        """
        Carga la estructura del chatbot desde su json
        :param chatbot: Nombre del chatbot
        :param intents: Lista de intenciones del chatbot
        :return: void
        """
        lastIntent = 1
        for intent in intents:                                      # recorre las intenciones
            structureIntent = CStructureIntent()                    # crea inteniones por cada elemento en la lista
            structureIntent.codeToStructureIntent(intent)           # método para generar la estructura adecuada
            chatbot.dicIntents[structureIntent.tag]=structureIntent # añade la intención a la lista
            if lastIntent == len(intents):
                chatbot.setCurrentIntent(structureIntent.tag)       # establece la ultima intención como intención actual
            lastIntent += 1