from Abstract.AActionSubclasses.ActionLine import ActionLine


class CDontSaveSentence(ActionLine):

    def __init__(self,chatbot):
        """
        Constructor de la Clase.
        :param chatbot: Es el ChatBot que tiene como acción la instancia de esta clase.
        """
        self.chatbot = chatbot

    def exec(self,):
        """
        Muestra una aviso al ausuario.
        :param : void
        :return: void
        """
        if self.chatbot.unrecognizedSentence is None:
            self.chatbot.output.exec('No hay una sentencia que guardar.')
        else:
            self.chatbot.output.exec('No se ha guardado la sentencia "'+self.chatbot.unrecognizedSentence+'".')
