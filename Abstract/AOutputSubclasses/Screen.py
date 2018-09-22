from Abstract.AOutput import IOutput
import os


class CScreen(IOutput):

    def exec(self,sentence):
        # sentence=sentence.replace('"','')
        # command='~/di.sh  "%s."'%sentence.replace('"','')
        # os.system(command)
        print(sentence)

        












