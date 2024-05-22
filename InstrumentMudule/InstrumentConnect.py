import pyvisa
from InstrumentMudule.Agilent33522B import Agilent33522B

class InstrumentConnect:
    def __init__(self):
        self.InstrumentDict = {}
        self.Series = "335"

    def detectInstruments(self):
        self.rm = pyvisa.ResourceManager()
        for addr in self.rm.list_resources():
            try:
                self.instr = self.rm.open_resource(addr)
                idn = self.instr.query('*IDN?')
                if (self.Series in idn):
                    instrName = f"{idn.split(',')[0]} {idn.split(',')[1]}"
                    self.InstrumentDict[instrName] = addr
                self.instr.close()
            except:
                pass

    # Connect to Agilent 33500 series waveform generator
    def instrumentConnectAction(self, instrName):
        if instrName != '':
            self.WaveformGenerator = Agilent33522B(self.InstrumentDict[instrName])
            return True
        else:
            return False