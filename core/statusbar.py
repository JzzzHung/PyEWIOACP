class StatusBarDisplay:
    def __init__(self):
        self.statusArduino = 'Disconnected'
        self.statusFG = 'Disconnected'

    def updateStatusBar(self):
        self.StatusBar.showMessage(f"Arduino {self.statusArduino} | Waveform Generator {self.statusFG}")

    def StatusBarDisplayInitialize(self):
        self.updateStatusBar()

    def ArduinoConnectSucced(self):
        self.statusArduino = 'Connect'
        self.updateStatusBar()

    def FGConnectSucced(self):
        self.statusFG = 'Connect'
        self.updateStatusBar()

    def FGDisconnect(self):
        self.statusFG = 'Disconnected'
        self.updateStatusBar()
