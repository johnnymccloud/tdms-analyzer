from nptdms import TdmsFile, TdmsWriter, ChannelObject, RootObject
import numpy as np
import pandas as pd

class TdmsReader():
    def __init__(self):
        self.dict = None #TBD: add reading single properties from tdms file
        
        self.dataset = None
        self.thresholds = None
        self.values = None
        self.thresholdsConfig = None
        self.valuesConfig = None
        self.thresholdNames = None
        
        
        self.readConfigFromJson()

    def readTdmsToNpArray(self, name):
        file = TdmsFile.read(name)
        data = []
        names = []
        for group in file.groups():
            df_group = group.as_dataframe()
            data.append(df_group)
            names.append(group.name)
        thresholds = []
        thresholdNames = []
        for thresholdConfig in self.thresholdsConfig:
            thresholdSet = np.array(data[thresholdConfig], dtype='int32')
            thresholds.append(thresholdSet)
            thresholdNames.append(names[thresholdConfig])
        self.thresholds = thresholds
        self.thresholdNames = thresholdNames
        values = []
        for valueConfig in self.valuesConfig:
            df = pd.DataFrame(data[valueConfig])
            frames = [np.array(df.iloc[i], dtype='int32').reshape((256, 128)) for i in range(len(df))]
            values.append(frames)
        self.values = values
        self.dataset = 0
        
        #self.thresholds[1] = self.thresholds[0]
        
    def getCurrentData(self):
        return self.values[self.dataset]
    def getThresholdNames(self):
        return self.thresholdNames
    def setThreshold(self, th_name):
        try:
            dataset = self.thresholdNames.index(th_name)
            if dataset != self.dataset:
                self.dataset = dataset
                return True
            return False
        except:
            print('threshold name not found')
            return False
    
    def readConfigFromJson(self):
        self.thresholdsConfig = [0, 2]
        self.valuesConfig = [1, 3]
        
