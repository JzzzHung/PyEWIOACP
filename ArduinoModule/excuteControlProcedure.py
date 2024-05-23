from PyQt5.QtWidgets import QTableWidgetItem,QMessageBox,QFileDialog
from PyQt5.QtCore import QTimer
from core.ThreadJob import DoThreadJob, DoQThreadJob
from functools import partial
import numpy,time
from InstrumentMudule.Agilent33522B import Agilent33522B
import pyvisa

class ControlProcedure:
    def __init__(self):
        self.initActionTypes()
        self.initFG()
        self.initStatusConst()

    def initActionTypes(self):
        self.actionType = 0
        self.ACTION_NOT_FOUND = 0
        self.ARDUINO_ACTION = 1
        self.INSTR_ACTION = 2

    def initStatusConst(self):
        self.STATUS_NORMAL = 0
        self.STATUS_EMERGENCY = 1

    # Connect to Agilent 33500 series waveform generator
    def initFG(self):
        Series = "335"
        self.address = ''
        rm = pyvisa.ResourceManager()
        for addr in rm.list_resources():
            try:
                instr = rm.open_resource(addr)
                idn = instr.query('*IDN?')
                if (Series in idn):
                    self.address = addr
                instr.close()
            except:
                continue

    def AddNewRow(self):
        row = self.ControlProcedureList.rowCount()
        self.ControlProcedureList.insertRow(row)

    def RemoveSelectedRow(self):
        row = self.ControlProcedureList.currentRow()
        self.ControlProcedureList.removeRow(row)

    # Logic
    def StartProcess(self):
        if self.address != '':
            self.FG = Agilent33522B(self.address)
            self.FGConnectSucced()
        self.ProcedureReload()
        self.ControlProcedureList.selectRow(0)
        self.ControlProcedureTimer = QTimer(self)
        self.ControlProcedureTimer.timeout.connect(self.ExcuteProcess)
        self.ControlProcedureTimer.start()

    def ExcuteProcess(self):
        totalRow = self.ControlProcedureList.rowCount()
        if totalRow == 0:  return  # bug?
        currentRow = self.ControlProcedureList.currentRow()
        Action = self.ControlProcedureList.item(currentRow,0).text()
        isFinish = self.ControlProcedureList.item(currentRow,2).text()
        SpendTime = int(self.ControlProcedureList.item(currentRow,1).text())

        self.actionType = self.IsActionExists(Action)
        if isFinish == "":
            # Type
            if self.actionType == self.ARDUINO_ACTION:
                f = getattr(self,Action)
                DoThreadJob(f)   # Do something
            elif self.actionType == self.INSTR_ACTION:
                Action = Action.lower()
                DoQThreadJob(partial(self.instrAction, Action)).start()

            # Finish
            self.ControlProcedureList.setItem(currentRow,2,QTableWidgetItem("V"))
            if self.isProcessEnd(currentRow,totalRow):
                if self.actionType == self.INSTR_ACTION:
                    DoQThreadJob(self.instrClose, SpendTime).start()
                self.ControlProcedureTimer.stop()
                return

        # Exit
        elif self.actionType == self.ACTION_NOT_FOUND:
            self.instrClose()
            self.ControlProcedureTimer.stop()
            QMessageBox.information(self,"Action is NOT exists","%s action isn't exists, Please confirm."%Action,QMessageBox.Ok)
            return

        self.ControlProcedureList.selectRow(currentRow+1)
        self.ControlProcedureTimer.setInterval(SpendTime)
        return

    def instrAction(self, Action):
        v = Action.split(',')[0].split('v')[0]
        f = Action.split(',')[1].split('hz')[0]
        v = self.FG.autoranging('v', float(v))
        f = self.FG.autoranging('f', float(f))
        if (v == self.FG.P['V_MIN']) and (f == self.FG.P['F_MIN']):
            self.instrClose()
            return
        self.FG.applyBurst(v, f)

    def instrClose(self, status=0):
        if hasattr(self, 'FG'):
            self.FG.close()
            if status == self.STATUS_EMERGENCY:
                self.FG.closeSession()

    def isProcessEnd(self,currentRow,totalRow):
        if totalRow == (currentRow+1):
            return True
        else:
            return False

    def IsActionExists(self,Action):
        if hasattr(self,Action):
            return self.ARDUINO_ACTION
        elif ('v' in Action.lower()) and ('hz' in Action.lower()):
            return self.INSTR_ACTION
        else:
            return self.ACTION_NOT_FOUND

    def ProcedureReload(self):
        totalRow = self.ControlProcedureList.rowCount()
        for row in range(totalRow):
            self.ControlProcedureList.setItem(row,2,QTableWidgetItem(""))

    def StopProcess(self):
        if hasattr(self, 'ControlProcedureTimer'):
            self.ControlProcedureTimer.stop()
            self.instrClose(self.STATUS_EMERGENCY)
            self.FGDisconnect()

    def GetProcedureFileName(self):
        fileName, _ = QFileDialog.getSaveFileName(self,"Contorl Process File Choose","./ProcessFile", "Text Files(*.pcs)")
        if fileName == "":
            return
        self.ProcessSourceFilePath.setText(fileName)

    def ReadProcedureFile(self):
        FileName = self.ProcessSourceFilePath.text()
        with open(FileName,"r") as file:
            all = file.readlines()
            return [p.strip() for p in all]

    def LoadProcedure(self):
        timelist = numpy.ndarray([])
        try:
            ProcedureList = self.ReadProcedureFile()
            self.ControlProcedureList.setRowCount(0)
            for i in range(len(ProcedureList)):
                self.AddNewRow()
                rowItem = ProcedureList[i].split("\t")
                self.ControlProcedureList.setItem(i,0,QTableWidgetItem(rowItem[0]))
                self.ControlProcedureList.setItem(i,1,QTableWidgetItem(rowItem[1]))
                timelist = numpy.append(timelist,int(rowItem[1]))
            else:
                sec = sum(timelist) / 1000
                convertTime = time.strftime("%H:%M:%S",time.gmtime(sec))
                self.ProcedureEstimatedTime.setText(convertTime)

        except FileNotFoundError:
            QMessageBox.information(self,"File Not Found!!!","File Not Found! plese confirm",QMessageBox.Ok)

    def GetControlProcedureListItem(self):
        totalRow = self.ControlProcedureList.rowCount()
        l = []
        for row in range(totalRow):
            actionText = self.ControlProcedureList.item(row,0).text()
            spendTimeText = self.ControlProcedureList.item(row,1).text()
            l.append(actionText+"\t"+spendTimeText)
        else:
            return [p+"\n" for p in l]

    def SaveProcedure(self):
        ProcedureList = self.GetControlProcedureListItem()
        FileName = self.ProcessSourceFilePath.text()
        if FileName == "":
            return
        with open(FileName,'w') as file:
            file.writelines(ProcedureList)
        QMessageBox.information(self,"Save Success","Save Sucessful.",QMessageBox.Ok)
