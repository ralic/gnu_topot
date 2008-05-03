from PyQt4.QtCore import *
from swig import readjoy
from PyQt4.QtGui import *
import sys

class Bridge(QObject):
    def __init__(self, parent = None):
        super(Bridge, self).__init__(parent)
    def emitMessage(self, message):
        self.emit(SIGNAL("gamepad"), message)
        

class Gamepad(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.bridge = Bridge()
        self.gamepad = readjoy.Joystick('/dev/input/js0')
        
    def run(self):
        self.readGamepad()
        self.exec_()
     
    def readGamepad(self):
        while True:
            a = self.gamepad.getEvent()
            self.bridge.emitMessage('%s%s : %s' % (str(a[0]), str(a[1]), str(a[2])))
            

gamepad = Gamepad()
def pisi(message):
    print message
    

QObject.connect(gamepad.bridge, SIGNAL('gamepad'), pisi)
gamepad.start()

