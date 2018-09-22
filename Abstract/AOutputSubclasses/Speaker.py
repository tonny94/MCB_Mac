from Abstract.AOutput import IOutput
import os


class CSpeaker(IOutput):

    def exec(self,sentence):
        if type(sentence) is str:
            # sentence=sentence.replace('"','')
            command='~/di.sh  "%s."'%sentence.replace('"','')
            os.system(command)

        












