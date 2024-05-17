import threading
from PyQt5.QtCore import QThread

def DoThreadJob(target_func):
    THREAD = threading.Thread(target = target_func)
    THREAD.start()



class DoQThreadJob(QThread):

    def __init__(self,func, sleepMSec=0):
        QThread.__init__(self)
        self.func = func
        self.sleepMSec = sleepMSec

    def __del__(self):
        self.wait()

    def run(self):
        if self.sleepMSec:
            self.msleep(self.sleepMSec)
        self.func()
