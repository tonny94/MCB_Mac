
import numpy as np
import random
import json
import os
import pickle
import h5py

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD
from keras.models import load_model

import nltk
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer('spanish')


class CTrainerPredictor:

    def __init__(self):
        self.jsonFile = ''
        self.chatbotName = ''
        self.intents = []
        self.model = None
        self.pathModel = ''

        self.words = []
        self.classes = []
        self.documents = []

        self.ignore_words = ['?']
        self.training = []
        self.output = []

        self.train_x = []
        self.train_y = []

        self.action = ''
        self.intent = ''
        self.ERROR_THRESHOLD = 0.25

        self.randomResponse = ''

    def readJSON(self,jsonFile,chatbotName):
        """
        Carga carga la estructura completa del ChatBot
        :param jsonFile: Ruta del json del ChatBot
        :param chatbotName: Nombre del ChatBot
        :return: void
        """
        self.jsonFile = jsonFile
        self.chatbotName = chatbotName
        with open(self.jsonFile, 'r+', encoding='utf-8') as json_data:
            self.intents = json.load(json_data)

    def createElementsToModel(self):
        """
        Inicializa las listas que se necesita para el modelo: words,clasees,documents
        :return: void
        """
        for intent in self.intents[self.chatbotName]:
            for pattern in intent['patterns']:
                w = nltk.word_tokenize(pattern)                 # tokeniza cada palabra en la sentencia
                self.words.extend(w)                            # añade la palabra a la lista
                self.documents.append((w, intent['tag']))       # asocia cada palabra a su respectiva intención añadiendolos al documento
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])          # añade la intención a la lista de clases

        self.words = [stemmer.stem(w.lower()) for w in self.words if w not in self.ignore_words]    # elimina mayúsculas y duplicados
        self.words = sorted(list(set(self.words)))              # ordena la lista
        self.classes = sorted(list(set(self.classes)))          # ordena la lista

        print(str(len(self.documents))+ ' documents')
        print(str(len(self.classes))+ "classes ["+', '.join(self.classes)+']')
        print(str(len(self.words)) + "unique stemmed words ["+', '.join(self.words) + ']')

    def trainingModel(self,pathModel):
        """
        Entrema el modelo
        :param pathModel: Ruta donde se guardará el modelo
        :return: boolean
        """
        self.pathModel = pathModel
        if not os.path.isdir(pathModel):
            os.makedirs(pathModel)                          # crea la carpeta

        self.train_x = []
        self.train_y = []
        output_empty = [0] * len(self.classes)

        # entrenamiento de la bolsa de palabras por cada sentencia
        for doc in self.documents:
            bag = []                                                                # inicializa la bolsa de palabras
            pattern_words = doc[0]                                                  # lista de palabras para el patrón
            pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]  # stem cada palabra
            for w in self.words:
                bag.append(1) if w in pattern_words else bag.append(0)              # crea la bolsa de palabras

            # output es '0' por cada tag y '1' por el tag actual
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1

            self.train_x.append(np.array(bag))
            self.train_y.append(np.array(output_row))

        # crea las listas de entrenamiendo y test
        self.train_x = np.array(self.train_x)
        self.train_y = np.array(self.train_y)
        print(self.train_y)

        #comprueba de que hayan datos de salida > 1 para generar un modelo con más de una intención
        if self.train_y.shape[1] == 1:
            return False
        else:
            self.model = Sequential()
            self.model.add(Dense(25, input_dim=self.train_x.shape[1]))          # densidad de la primera capa de neurona y tipo de entrada
            self.model.add(Dropout(0.5))                                        # convierte a 0 la mitad de 1 en el entrenamiento
            self.model.add(Dense(25))                                           # densidad de la primera capa de neurona
            self.model.add(Dropout(0.5))                                        # convierte a 0 la mitad de 1 en el entrenamiento
            self.model.add(Dense(self.train_y.shape[1], activation='softmax'))  # densidad de la salida
            # sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
            self.model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['accuracy'])

            self.model.fit(self.train_x, self.train_y, epochs=1000, batch_size=8)   # entrena el modelo
            self.model.save(os.path.join(os.path.sep,self.pathModel,'model.h5'))    # guarda el modelo
            return True

    def doPickle(self):
        """
        Guarda los datos de entrenamiento
        :return: void
        """
        import pickle
        pickle.dump({'words': self.words, 'classes': self.classes},
                    open(os.path.join(os.path.sep,self.pathModel,"training_data"), "wb"))

    def clean_up_sentence(self,sentence):
        """
        Tokeniza y realiza el steam por cada palabra
        :param sentence:
        :return: list
        """
        sentence_words = nltk.word_tokenize(sentence)   # tokeniza los patrones
        sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]    # steam cada palabra
        return sentence_words

    def bow(self,sentence, words, show_details=False):
        """
        Devuelve una bolsa de lista: 0 ó 1 por cada palabra en la bolsa que exista en la sentencia
        :param sentence: Sentencia
        :param words: lista de palabras
        :param show_details: boolean
        :return: numpy array
        """
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(words)      # bolsa de palabras
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)

        return (np.array(bag))

    def loadArrays(self,pathModel):
        """
        Carga los arrays necesarios para realizar el Predictor
        :param pathModel: Ruta del modelo
        :return:
        """
        self.pathModel = pathModel
        self.data = pickle.load(open(os.path.join(os.path.sep,self.pathModel, "training_data"), "rb"))  # carga los datos del entrenamiento
        self.words = self.data['words']
        self.classes = self.data['classes']

    def loadModel(self):
        """
        Carga el modelo
        :return:
        """
        self.model = load_model(os.path.join(os.path.sep,self.pathModel,'model.h5'))

    def classify(self,sentence):
        """
        Clasifica la sentencia
        :param sentence: Entrada por parte del usuario
        :return: list
        """
        results = self.model.predict(np.array([self.bow(sentence, self.words)]))[0]     # genera las posibles respuestas
        results = [[i, r] for i, r in enumerate(results) if r > self.ERROR_THRESHOLD]   # filtra las predicciones por debajo de un umbral
        results.sort(key=lambda x: x[1], reverse=True)                                  # ordena por probabilidad
        return_list = []
        for r in results:
            return_list.append((self.classes[r[0]], r[1]))
        return return_list                                      # retorna una lista de tuplas (intención,probabilidad)

    def predict(self, sentence):
        """
        Da una respuesta acorde a la frase introducida
        :param sentence: Frase a predecir.
        :return:
        """
        results = self.classify(sentence)           # se oltiene la lista de la clasificación
        if results:                                 # si hay clasificación entonces se puede encontrar una coincidencia con un tag
            while results:                          # bucle hasta que se encuentre una coincidencia
                for i in self.intents[self.chatbotName]:
                    if i['tag'] == results[0][0]:   # para encontrar la coincidencia con el primer resultado de la clasificación
                        if 'action' in i:
                            self.action = i['action']           # guarda la acción
                        self.intent = i                         # se guarda la intención
                        if not len(i['responses']) == 0:        # si no hay respuestas no se imprime nada
                            self.randomResponse = random.choice(i['responses']) # una respuesta aleatoria de la predicción para la sentencia
                            return
                        else:
                            return
                results.pop(0)


