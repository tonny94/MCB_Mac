import unicodedata
from Abstract.AAction import IAction

# clase para obetener el tipo de entrada/salida de datos
from Abstract.AInteractor import IInteractor


class ActionLine(IAction):

    # lista de palabras clave para la cancelación de una acción.
    listKeysWordsCancelRunning = ['cancelar','abortar','parar','no seguir','cancelar ejecución','parar ejecución','dejar de ejecutar','abortar ejecución','error']
    output = IInteractor.output
    def exec(self):
        """
        Método para la ejecución de una acción.
        :return: void.
        """
        pass

    def checkCancellation(self,sentence):
        """
        Método que compara si el parámetro está en la lista de cancelación de acción.
        :param sentence: Senencia a comprobar si existe en la lista de cancelación de acción.
        :return: boolean.
        """
        wordTransformed = unicodedata.normalize('NFKD', sentence).encode('ASCII','ignore').lower()  # elimiona los caracteres especiales
        listTransformed = [unicodedata.normalize('NFKD', w).encode('ASCII', 'ignore').lower() for w in self.listKeysWordsCancelRunning]  # transforma los elementos de la lista
        if (wordTransformed in listTransformed):
            self.output.exec('Se ha cancelado la operación.')
            return True
        else:
            return False
