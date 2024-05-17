from InstrumentMudule.InstrumentBase import Base
import time

class Agilent33522B(Base):
    def __init__(self, visaAddress) -> None:
        super().__init__(visaAddress)
        self.initUnit()

    def initUnit(self):
        # Unit
        self.instrument.write(f"SOURCE1:VOLT:UNIT {self.P['V_UNIT']}")
        self.instrument.write(f"SOURCE2:VOLT:UNIT {self.P['V_UNIT']}")
        # P
        self.P['V_MAX'] = 3.5356  # set 3.536 will cause error
        self.P['V_MIN'] = 0.000354
        self.P['F_MAX'] = 4000000
        self.P['F_MIN'] = 0.000001

    def _apply(self, src, v, f, p=0):
        self.instrument.write(f"SOURCE{src}:APPLY:{self.P['V_TYPE']} {f}{self.P['F_UNIT']}, {v}{self.P['V_UNIT']}")
        self.setBurst(src, p)

    def applyBurst(self, v, f, p=180):
        self._applyBurst(v, f, v, f, 0, p)

    def _applyBurst(self, v1, f1, v2, f2, p1=0, p2=180):
        self._apply(1, v1, f1, p1)
        self._apply(2, v2, f2, p2)
        self.instrument.write('*TRG') # Send trigger signal from remote, that is the same as press trigger button on front panel.

    # Manual p.177
    def setBurst(self, src, phase):
        self.instrument.write(f'TRIG{src}:SOURCE BUS') # Trigger by remote. Manual p.324
        self.instrument.write(f'SOURCE{src}:BURST:MODE TRIG')
        self.instrument.write(f'SOURCE{src}:BURST:NCYCles INFinity')
        self.instrument.write(f'SOURCE{src}:BURST:INTernal:PERiod MIN')
        self.instrument.write(f'SOURCE{src}:BURST:PHASE {phase}')
        self.instrument.write(f'SOURCE{src}:BURST:STATE ON')
        self.instrument.write(f'OUTPUT{src}:STAT ON')

    def outputOFF(self):
        self.instrument.write("OUTPUT1:STAT OFF")
        self.instrument.write("OUTPUT2:STAT OFF")

    def burstOFF(self):
        self.instrument.write('SOURCE1:BURST:STATE OFF')
        self.instrument.write('SOURCE2:BURST:STATE OFF')

    def close(self):
        self.outputOFF()
        self.burstOFF()
        # self.closeSession()
