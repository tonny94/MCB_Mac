from Abstract.AInput import IInput
import threading
from xmlrpc.server import SimpleXMLRPCServer


class CKeyboard(IInput):
    
    def exec(self):
        value = input('=> ')
        return value













