from functools import partial
from core.ThreadJob import DoThreadJob
from PyQt5.QtCore import QTimer
import time
from InstrumentMudule.InstrumentConnect import InstrumentConnect

class InstrumentUiOperation(InstrumentConnect):
    def __init__(self) -> None:
        super().__init__()
        self.isOutput = False
        self.btnStyle = {
            'ON': 'background:#FFF574;',
            'OFF': 'background:#E1E1E1;'
        }

    def InstrumentUiActionInitialize(self):
        self.btnOutput.setEnabled(False)
        self.btnTrig.setEnabled(False)
        self.btnOutput.clicked.connect(self.clickOutputBtn)
        self.btnTrig.clicked.connect(self.singleBurst)
        self.RefreshInstrumentsBtn.clicked.connect(partial(DoThreadJob,self.refreshInstruments))
        self.InstrumentConnectBtn.clicked.connect(partial(DoThreadJob,self.connectInstruments))

    def connectInstruments(self):
        self.InstrumentConnectBtn.setEnabled(False)
        self.RefreshInstrumentsBtn.setEnabled(False)
        self.InstrumentComboBox.setEnabled(False)
        self.instrumentConnectAction(self.InstrumentComboBox.currentText())
        self.btnOutput.setEnabled(True)

    def refreshInstruments(self):
        self.InstrumentDict.clear()
        self.detectInstruments()
        self.InstrumentComboBox.clear()
        self.InstrumentComboBox.addItems(self.InstrumentDict.keys())

    def clickOutputBtn(self):
        self.isOutput =  not self.isOutput
        if self.isOutput:
            self.startCountUp()
            self.btnTrig.setEnabled(True)
            DoThreadJob(self.btnOutput.setStyleSheet(self.btnStyle['ON']))
            DoThreadJob(self.singleBurst)
        else:
            self.stopCountUp()
            self.btnTrig.setEnabled(False)
            DoThreadJob(self.btnOutput.setStyleSheet(self.btnStyle['OFF']))
            DoThreadJob(self.WaveformGenerator.close)

    def singleBurst(self):
        DoThreadJob(self.flash)
        v, f, p = self.getVFP()
        self.WaveformGenerator.applyBurst(v, f, p)
        self.EditV.setText(str(v))
        self.EditF.setText(str(f))
        self.EditP.setText(str(p))

    def flash(self):
        self.btnTrig.setStyleSheet(self.btnStyle['ON'])
        time.sleep(0.2)
        self.btnTrig.setStyleSheet(self.btnStyle['OFF'])

    def getVFP(self):
        v, f, p, dv, df, dp = self.getLineEditText()
        v = self.updateParameter('v', v, dv)
        f = self.updateParameter('f', f, df)
        p = self.updateParameter('p', p, dp)
        return v, f, p

    def updateParameter(self, xType, x, dx):
        x += dx
        return self.WaveformGenerator.autoranging(xType, x)

    def getLineEditText(self):
        pAry = [self.EditV, self.EditF, self.EditP, self.DeltaV, self.DeltaF, self.DeltaP]
        return [float(p.text()) for p in pAry]

    ########## Count-up timer ##########
    def startCountUp(self):
        self.t = 0
        self.countUpTimer = QTimer(self)
        self.countUpTimer.timeout.connect(self.updateCountUpTimer)
        self.countUpTimer.start(1000)
        self.isRunning = False

    def updateCountUpTimer(self):
        self.t += 1
        convertTime = time.strftime("%Hh%Mm%Ss",time.gmtime(self.t))
        self.labelTimer.setText(convertTime)

    def stopCountUp(self):
        self.countUpTimer.stop()
    ########## Count-up timer ##########