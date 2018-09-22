#clase para obetener el tipo de entrada/salida de datos
from Abstract.AInteractor import IInteractor


class CStructureIntent:

    def __init__(self):
        self.tag = ''
        self.patterns = []
        self.responses = []
        self.action = ''
        self.ouput = IInteractor.output

    def setTag(self, tag):
        """
        Actualiza el nombre de la Intención
        :param tag: Nombre de la Intención
        :return: void
        """
        self.tag = tag

    def addResponse(self, response):
        """
        Añade una Respuesta a la lista, devuelve un estado según cómo haya ido la inserción
        :param response: Respuesta para añadir
        :return: boolean
        """
        if response in self.responses:
            self.ouput.exec('Ya existe "'+ response+ '" en la lista de Respuestas de la intención "'+self.tag+ '".')
            return False
        else:
            self.responses.append (response)
            return True

    def addListResponse(self,listResponse):
        """
        Sustituye la lista de Respuesta por otra lista.
        :param listResponse:
        :return:
        """
        self.responses = listResponse

    def deleteResponse(self, response):
        """
        Si exite la Respuesta en la lista la borra, se encarga de moestrar el estado
        :param response: Respuesta a borrar.
        :return: vid
        """
        if response in self.responses:
            self.responses.remove(response)
            self.ouput.exec('Se ha eliminado "'+response+ '" de la lista de Respuestas de la intención "'+self.tag+ '".')
        else:
            self.ouput.exec('No existe  "'+response+ '" en la lista de Respuestas de la intención"'+self.tag+ '".')

    def printResponses(self):
        """
        Muestra las Respuestas creadas.
        :return:
        """
        result = ", ".join(pattern for pattern in self.responses)
        self.ouput.exec('Las Respuestas para la Intención "'+self.tag+'" son:'+result)

    def addPattern(self, pattern):
        """
        Añade un Patrón a la lista, devuelve un estado según cómo haya ido la inserción
        :param pattern:
        :return: boolean
        """
        if pattern in self.patterns:
            self.ouput.exec('Ya existe "'+pattern+'" en la lista de Patrones de la Intención "'+self.tag+'".')
            return False
        else:
            self.patterns.append(pattern)
            return True

    def addListPatterns(self,listPatterns):
        """
        Sustituye la lista de Patrones por otra lista
        :param listPatterns: Nueva lista de Patrones
        :return: void
        """
        self.patterns = listPatterns

    def deletePattern(self, pattern):
        """
        Si exite el Patrón en la lista lo borra, se encarga de mostrar el estado
        :param pattern: Patrón a borrar
        :return: void
        """
        if pattern in self.patterns:
            self.patterns.remove(pattern)
            self.ouput.exec('Se ha eliminado "'+pattern+'" de la lista de Patrones de la intención "'+self.tag+'".')
        else:
            self.ouput.exec('No existe  "'+pattern+'" en la lista de Patrones de la intención"'+self.tag+'".')

    def printPatterns(self):
        """
        Muestra los Patrones creados.
        :return: void
        """
        result = ", ".join(pattern for pattern in self.patterns)
        self.ouput.exec('Los patrones para la Intención "'+self.tag+'" son:'+result)

    def setAction(self, action):
        """
        Actualiza la Acción de la Intención actual.
        :param action: Nombre de la acción
        :return:void
        """
        if action == '':
            self.ouput.exec('Se ha borrado la Acción para la Intención "'+self.tag+'". ')
        self.action = action

    def printAction(self):
        """
        Muestra la acción de la Intención actual.
        :return:
        """
        if self.action == '':
            self.ouput.exec('La Intención "'+self.tag+'" no tiene acción.')
        else:
            self.ouput.exec('La Acción de la Intención "'+self.tag+'" es:'+self.action)

    def tagToJSON(self):
        """
        Devuelve el nombre de la Intención
        :return: string
        """
        return self.tag

    def actionToJSON(self):
        """
        Devuelve el nombre de la Acción
        :return: string
        """
        return self.action

    def toJSON(self):
        """
        Conierte la estructura de una Intención a formato json
        :return: dict
        """
        dictIntetn ={}
        dictIntetn['tag'] = self.tagToJSON()
        dictIntetn['patterns'] = self.patterns
        dictIntetn['responses'] = self.responses
        dictIntetn['action'] = self.actionToJSON()
        return dictIntetn

    def codeToStructureIntent(self,structure):
        """
        Convierte el formato json a la estrucctura de Intención
        :param structure:
        :return: void
        """
        self.setTag(structure['tag'])
        self.addListPatterns(structure['patterns'])
        self.addListResponse(structure['responses'])
        self.setAction(structure['action'])








    # #pasa a JSON una lista
    # def listToJSON(self, lista):
    #     """
    #     Convierte una lista a un string con la estructura json
    #     :param lista: Lista de Intenciones
    #     :return: string
    #     """
    #     if len(lista)>0:
    #         length = 0
    #         strJSON = '['
    #         for elem in lista:
    #             if length == len(lista)-1:
    #                 strJSON += '"' + elem + '"]'
    #             else:
    #                 strJSON += '"'+elem+'",'
    #             length +=1
    #
    #         return strJSON
    #     else:
    #         return '[]'

