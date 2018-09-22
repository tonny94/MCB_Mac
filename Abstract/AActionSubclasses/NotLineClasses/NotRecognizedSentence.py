from Abstract.AActionSubclasses.ActionLine import ActionLine

#clase para obetener el tipo de entrada/salida de datos
from Abstract.AInteractor import IInteractor


class CNotRecognizedSentence(ActionLine):

    def __init__(self,sentence):
        """
        Constructor de la Clase.
        :param sentence: Es la sentencia que no se ha reconocido.
        """
        self.sentence = sentence
        self.output = IInteractor.output

    def exec(self,):
        """
        Muestra una aviso al ausuario.
        :param : void
        :return: void
        """
        self.output.exec('No se ha reconocido la sentencia "'+self.sentence+'".')
