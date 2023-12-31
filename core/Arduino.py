from functools import partial
from PyQt5.QtCore import QTimer

from core.ThreadJob import DoThreadJob,DoQThreadJob
from ArduinoModule.connect import ArduinoConnect
from ArduinoModule.control import SendCommand
from ArduinoModule.arrayMeasure import ControlArrayMeasure
from ArduinoModule.excuteControlProcedure import ControlProcedure

class ArduinoUiOperation(ArduinoConnect,SendCommand,ControlArrayMeasure,ControlProcedure):
    def __init__(self):
        super(ArduinoUiOperation,self).__init__()
        ControlArrayMeasure.__init__(self)
        self.ThreadTimer = QTimer(self)

    def ArduinoUiActionInitialize(self):
        self.RefreshPortsButton.clicked.connect(self.GetPort)
        self.ArduinoConnectButton.clicked.connect(partial(DoThreadJob,self.DoConnect))
        self.CreateArduinoControlArrayBtn.clicked.connect(self.CreateControlArray)

        # Path Control
        self.btnSeriesLight.clicked.connect(partial(DoThreadJob,self.SeriesLight))
        self.btnDFPMix.clicked.connect(partial(DoThreadJob,self.DFPMix))
        self.btnQFPMix.clicked.connect(partial(DoThreadJob,self.QFPMix))
        self.btnQFPXMix.clicked.connect(partial(DoThreadJob,self.QFPXMix))

        # Magnetic beads with NAEB Experiment Path Control
        self.btnLeftIN.clicked.connect(partial(DoThreadJob,self.LeftIN))
        self.btnRightIN.clicked.connect(partial(DoThreadJob,self.RightIN))
        self.btnToLeftOut.clicked.connect(partial(DoThreadJob,self.ToLeftOut))
        self.btnToRightOut.clicked.connect(partial(DoThreadJob,self.ToRightOut))
        self.btnLeftRightIN.clicked.connect(partial(DoThreadJob,self.LeftRightIN))
        self.btnMix.clicked.connect(partial(DoThreadJob,self.Mix))
        self.btnTopIN.clicked.connect(partial(DoThreadJob,self.TopIN))
        self.btnBottomIN.clicked.connect(partial(DoThreadJob,self.BottomIN))
        self.btnToTopOut.clicked.connect(partial(DoThreadJob,self.ToTopOut))
        self.btnToBottomOut.clicked.connect(partial(DoThreadJob,self.ToBottomOut))

        # Chemical Mix
        self.btnLRinAndMix.clicked.connect(partial(DoThreadJob,self.LRinAndMix))

        # Servo Magnet
        self.btnServoMag.clicked.connect(partial(DoThreadJob,self.ServoMag))

        # Control Procedurce UI Block
        self.AddRowBtn.clicked.connect(partial(DoThreadJob,self.AddNewRow))
        self.RemoveRowBtn.clicked.connect(partial(DoThreadJob,self.RemoveSelectedRow))
        self.ProcessSourceFileDialog.clicked.connect(self.GetProcedureFileName)
        self.StartProcessBtn.clicked.connect(self.StartProcess)
        self.STOPALLBtn.clicked.connect(self.StopProcess)
        self.LoadProcedureBtn.clicked.connect(self.LoadProcedure)
        self.SaveProcedureBtn.clicked.connect(self.SaveProcedure)


    def GetPort(self):
        ArduinoConnect.GetPort(self)
        self.PortComboBox.clear()
        self.PortComboBox.addItems(self.Portlist)

    def DoConnect(self):
        self.ArduinoConnectButton.setEnabled(False)
        self.RefreshPortsButton.setEnabled(False)
        self.PortComboBox.setEnabled(False)
        try:
            succ = self.ConnectAction(self.PortComboBox.currentText())

            if not succ:
                raise TimeoutError("Arduino Connect Timeout")

            self.ArduinoConnectSucced() #show in status bar


        except Exception:
            self.ArduinoConnectButton.setEnabled(True)
            self.RefreshPortsButton.setEnabled(True)
            self.PortComboBox.setEnabled(True)

    def CreateControlArray(self):
        
        electrode_num = self.ArduinoElectrodeNumber.value()

        DoQThreadJob(self.ProcedureTextToArray).start()
        # procedure = self.ProcedureTextToArray()

        DoThreadJob(partial(ControlArrayMeasure.CreateControlArray,self,self.procedureMeasureComplete.get(),electrode_num))

        if self.ThreadJobComplete.get():
            self.ArrayPannelUpdate(self.ArrayComplete.get())
            self.ThreadTimer.singleShot(5,self.PopupArduinoControlArrayWindowUI.show)
        
    
    def ArrayPannelUpdate(self,string):
        self.PopupArduinoControlArrayWindowUI.ShoWArduinoControlArray.setText(string)
        self.PopupArduinoControlArrayWindowUI.ShoWArduinoControlArray.update()