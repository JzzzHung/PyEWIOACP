from time import sleep

class SendCommand:
    def __init__(self):
        pass

    def SerialWrite(self,command):
        self.Serial.write(command.encode("utf-8"))
        rv = self.Serial.readline()
        self.Serial.flushInput()

    def ACET(self):
        command = "ACET"
        self.SerialWrite(command)

    def SeriesLight(self):
        command = "b"
        self.SerialWrite(command)

    def DFPMix(self):
        command = "DFPMix"
        self.SerialWrite(command)

    def QFPMix(self):
        command = "QFPMix"
        self.SerialWrite(command)

    def QFPXMix(self):
        command = "QFPXMix"
        self.SerialWrite(command)

    # Magnetic bead with NAEB Experiment

    def LeftIN(self):
        command = "LeftIN"
        self.SerialWrite(command)

    def RightIN(self):
        command = "RightIN"
        self.SerialWrite(command)

    def ToLeftOut(self):
        command = "ToLeftOut"
        self.SerialWrite(command)

    def ToRightOut(self):
        command = "ToRightOut"
        self.SerialWrite(command)

    def LeftRightIN(self):
        command = "LeftRightIN"
        self.SerialWrite(command)

    def Mix(self):
        command = "Mix"
        self.SerialWrite(command)

    def ToTopOut(self):
        command = "ToTopOut"
        self.SerialWrite(command)

    def ToBottomOut(self):
        command = "ToBottomOut"
        self.SerialWrite(command)

    def TopIN(self):
        command = "TopIN"
        self.SerialWrite(command)

    def BottomIN(self):
        command = "BottomIN"
        self.SerialWrite(command)

    def LRinAndMix(self):
        command = "LRinAndMix"
        self.SerialWrite(command)

    def ServoMag(self):
        command = "="
        self.SerialWrite(command)

    def LeftToRight(self):
        command = "LeftToRight"
        self.SerialWrite(command)

    def RightToLeft(self):
        command = "RightToLeft"
        self.SerialWrite(command)

    def Merge(self):
        command = "Merge"
        self.SerialWrite(command)

    def Straight(self):
        command = "Straight"
        self.SerialWrite(command)

    def CycleMove(self):
        command = "CycleMove"
        self.SerialWrite(command)

    def HybridMix(self):
        command = "HybridMix"
        self.SerialWrite(command)

    def Null(self):
        command = "Hello"
        print(command)