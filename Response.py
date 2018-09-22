# -*- coding: utf-8 -*-

# things we need for NLP
import nltk
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer('spanish')
# things we need for Tensorflow
import numpy as np
import tflearn
import random
import pickle
import json
import os
#*obser = unicode(self.edit_observ.toPlainText())*
#* obser1 = obser.encode('utf-8')*

class Response:

    def __init__(self):
        self.model = None
        self.data = None
        self.words = []
        self.classes = []
        self.train_x = []
        self.train_y = []
        self.ERROR_THRESHOLD = 0.25
        self.context = {}
        self.intents = {}
        self.action = ''
        self.pathModel = ''
        self.jsonFile = ''
        self.chatbotName = ''

    #carga los atributos de arrays que necesita del modelo de entrenamiento
    def loadArrays(self,pathModel):
        self.pathModel = pathModel
        # listSplit = self.pathModel.split(os.sep)
        # pathTrainingData = self.pathModel.replace(listSplit[len(listSplit) - 1], '')

        self.data = pickle.load(open(os.path.join(os.path.sep,self.pathModel, "training_data"), "rb"))
        self.words = self.data['words']
        self.classes = self.data['classes']
        self.train_x = self.data['train_x']
        self.train_y = self.data['train_y']

    #lee el fichero json y actualiza el atributo 'intents'
    def readJSON(self,jsonFile,chatbotName):
        self.jsonFile = jsonFile
        self.chatbotName = chatbotName
        with open(self.jsonFile) as json_data:
            self.intents = json.load(json_data)

    #construye la red
    def buildNetwork(self):
        net = tflearn.input_data(shape=[None, len(self.train_x[0])])
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, 8)
        net = tflearn.fully_connected(net, len(self.train_y[0]), activation='softmax')
        net = tflearn.regression(net)
        # Define model and setup tensorboard
        self.model = tflearn.DNN(net, tensorboard_dir = self.pathModel)

    #carga el objeto 'model'
    def loadModel(self):
        # listSplit = self.pathModel.split(os.sep)
        # pathModelFiles = self.pathModel.replace(listSplit[len(listSplit) - 1], '')
        self.model.load(os.path.join(os.path.sep,self.pathModel,'model.tflearn'))

    #
    def clean_up_sentence(self,sentence):
        # tokenize the pattern
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word
        sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
    def bow(self,sentence, words, show_details=False):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words
        bag = [0] * len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)

        return (np.array(bag))

    #clasifica una frase
    def classify(self,sentence):
        # generate probabilities from the model
        results = self.model.predict([self.bow(sentence, self.words)])[0]
        # filter out predictions below a threshold
        results = [[i, r] for i, r in enumerate(results) if r > self.ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append((self.classes[r[0]], r[1]))
        # return tuple of intent and probability
        return return_list

    #da una respuesta acorde a la frase introducida
    def response(self,sentence, userID='123', show_details=False):

        results = self.classify(sentence)

        # if we have a classification then find the matching intent tag
        if results:
            # loop as long as there are matches to process
            while results:
                for i in self.intents[self.chatbotName]:
                    # find a tag matching the first result
                    if i['tag'] == results[0][0]:

                        if 'action' in i:
                            # myAction.selectOption(sentence, i['tag'])
                            self.action = i['action']


                        if self.context == {}:
                            # set context for this intent if necessary
                            if 'context_set' in i:
                                if show_details: print('context:', i['context_set'])
                                self.context[userID] = i['context_set']

                            # check if this intent is contextual and applies to this user's conversation
                            # if (not 'context_filter' in i) or (userID in self.context and 'context_filter' in i and i['context_filter'] == self.context[userID]):
                            #     if show_details: print('tag:', i['tag'])

                            # a random predict from the intent - si no hay respuestas no se imprime nada
                            if not len(i['responses']) == 0:
                                return print( (random.choice(i['responses'])) )
                            else:
                                return
                        #comprobacion de que la intención, si tiene context_filter, concuerde con el context_set
                        elif 'context_filter' in i and self.context[userID] == i['context_filter']:
                            #reinicia en contexto
                            self.context = {}

                            # a random predict from the intent - si no hay respuestas no se imprime nada
                            if not len(i['responses']) == 0:
                                return print((random.choice(i['responses'])))
                            else:
                                return

                results.pop(0)


