from Abstract.AInput import IInput
import threading
from xmlrpc.server import SimpleXMLRPCServer


class CVoice(IInput):
    def __init__(self):
        """
        Constructor de la clase.
        """
        self.iString=""
        thread = threading.Thread(target=self.xmlsvr, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def xmlsvr(self):
        """
        Método que ejecuta el thread.
        :return: void
        """
        server = SimpleXMLRPCServer(("", 8000))
        print("Listening on port 8000...")
        server.register_instance(self)
        server.serve_forever()

    def asr(self,s):
        """
        Método adicional de comprobación.
        :param s: sentencia recibida en el puerto
        :return: string: una confirmación
        """
        print("Recibido ",s)
        self.iString=s
        return "ok-from MetaChatBot"
    
    def exec(self):
        while self.iString=="":
            pass
        value=self.iString
        self.iString=""
        return value













