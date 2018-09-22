import os,inspect,json 
from Abstract.AChatBot import CChatBot
from Abstract.AActionSubclasses.NotLineClasses.NotRecognizedSentence import CNotRecognizedSentence
from Chatbots.compra_online.Actions.Newproduct import CNewproduct
from Chatbots.compra_online.Actions.Pay import CPay
from Chatbots.compra_online.Actions.Creditcard import CCreditcard

class Ccompra_online(CChatBot):
	def __init__(self):
		super(Ccompra_online, self).__init__()
		self.actionsCB = {'newProduct':CNewproduct(self), 'pay':CPay(self), 'creditCard':CCreditcard(self) }
		self.initializePaths()

	def initializePaths(self):
		strSplit = (os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))).split(os.path.sep)
		self.nameTransformed = strSplit[len(strSplit)-1]
		self.generalPath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		self.jsonPath = os.path.join(os.path.sep,self.generalPath,self.nameTransformed+'.json')
		with open(self.jsonPath, 'r+', encoding='utf-8') as f:
			data = json.load(f)
			self.name = list(data.keys())[0]
		self.errorFilePath = os.path.join(os.path.sep, self.generalPath, self.nameTransformed + '_ErrorFile.json')
		if not os.path.isfile(self.errorFilePath):
			with open(self.errorFilePath, 'w', encoding='utf-8') as f:
				json.dump({}, f)

	def saveUnrecognizedSentence(self,key,value):
		self.errorDict[key] = value

