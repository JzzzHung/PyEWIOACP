import re
import queue
import pandas as pd

class ProcedureGenerator:
    def __init__(self):
        self.ThreadJobComplete = queue.Queue(1)
        self.ArrayComplete = queue.Queue(1)
        self.setPadToSeriesDict()

    def setPadToSeriesDict(self):
        rawDict = pd.read_csv('./padRules/48pad.csv', index_col=0, dtype=str).T.to_dict(orient='list')
        self.padToSeries = {str(k) : ','.join(v)+',' for (k,v) in rawDict.items()}
        # self.padToSeries  = {
        #     '5': '0,0,0,0,1,-1,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,0,0,0,0,0,0,0,'
        #     ...
        # }

    def compare(self, *args):
        if 1 in args:         # 只要有1就回傳1
            return '1'
        elif -1 in args:      # 以下只會出現-1或0的組合，只要有-1就回傳-1
            return '-1'
        else:                 # 全都是0才回傳0
            return '0'

    def checkExist(self, inputText):
        ary = list(filter(None, re.split(',|\n', inputText))) # split by ',' or '\n'
        for i in ary:
            if i not in self.padToSeries:
                self.bug = i
                return False
        return True

    def createProcedure(self, electrode_num):
        inputText = self.ControlArrayProcedure.toPlainText().replace(' ', '')
        inputTextAry = inputText.split('\n')
        inputTextAry = list(filter(None, inputTextAry))  # remove empty
        allProcedure = []

        # check input text exist in padToSeries or not
        if not self.checkExist(inputText):
            self.ArrayComplete.put(f'pad {self.bug} not exists')
            self.ThreadJobComplete.put(True)
            return

        # input text -> procedure
        for line in inputTextAry:
            if len(line.split(',')) > 1:
                ary = []
                combinedSeries = []
                for text in line.split(','):
                    tmp = self.padToSeries[text].split(',')
                    tmp = list(filter(None, tmp))  # remove empty
                    tmp = [eval(t) for t in tmp]
                    ary.append(tmp)
                for i in range(electrode_num):
                    cols = []
                    for j in range(len(ary)):
                        cols.append(ary[j][i])
                    combinedSeries.append(self.compare(*cols))
                allProcedure.append(','.join(combinedSeries) + ',')
            else:
                allProcedure.append(self.padToSeries[line])

        # finish
        self.ArrayComplete.put('\n'.join(allProcedure))
        self.ThreadJobComplete.put(True)
