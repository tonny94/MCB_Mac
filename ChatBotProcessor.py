from Abstract.AInteractor import IInteractor


class CBProcessor(object):

    def __init__(self,chatbot):
        self.currentRunningChatbot = chatbot
        self.currentAction = ''
        self.updateActionsCBProcessor()
        self.ouput = IInteractor.output
        self.input = IInteractor.input

    def startModel(self):
        """
        Inicia el método StartModel del ChatBot.
        :return: void
        """
        self.currentRunningChatbot.startModel()

    def startPredictor(self):
        """
        Inicia el método StartPredictor del ChatBot.
        :return: void
        """
        self.currentRunningChatbot.startPredictor()

    def doClassification(self, sentence):
        """
        Encuentra las posibles Respuestas para el Patrón dado.
        :param sentence: Patrón a clasificar
        :return: list
        """
        return self.currentRunningChatbot.TrainerAndPredictor.classify(sentence)

    def run(self):
        """
        Ejecuta el Chatbot
        :return:
        """
        self.ouput.exec('Se está ejecutando el ChatBot "'+self.currentRunningChatbot.name+'".')
        while self.currentRunningChatbot.runChatBot:
            sentence = self.input.exec()                            # espera la entrada por parte del usuario
            # print(self.doClassification(sentence))
            self.currentRunningChatbot.execPrediction(sentence)     # ejecuta la predicción del Chatbot

    def updateActionsCBProcessor(self):
        """
        Actualiza el diccionario de acciones del Processor con las acciones del ChatBot
        :return: void
        """
        self.currentRunningChatbot.actions.update(self.currentRunningChatbot.actionsCB)





















    # def doPrediction(self, sentence):
    #     """
    #
    #     :param sentence:
    #     :return:
    #     """
    #     self.currentRunningChatbot.TrainerAndPredictor.predict(sentence)


    """
        Metodos para terminar/empezar la ejecucion de un chatbot
    """
    # def finishRunningChatbot(self):
    #     CFinishRunningCB(self.runChatBot,self.currentChatbotChild)
    #
    # def startRunningChatbot(self):
    #     CStartRunningCB(self.currentChatbotChild,self.pathChildrenChatbots)


