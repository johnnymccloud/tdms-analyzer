from nptdms import TdmsFile, TdmsWriter, ChannelObject, RootObject
import numpy as np
import pandas as pd
import re

import json

class TdmsReader():
    def __init__(self):
       
        self.dataset = None
        self.thresholds = None
        self.values = None
        self.thresholdsConfig = None
        self.valuesConfig = None
        self.thresholdNames = None
        self.settings = None
        self.comment = None
        
        self.readConfigFromJson()

    def readTdms(self, name):
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
            thresholdSet = np.array(data[thresholdConfig], dtype='int32').reshape(-1) #flatten to 1-D
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
        
        # for i in len(thresholds):
        #     if len(thresholds[i]) < len(thresholds[0]):
        #         thresholds[i].append(thresholds[len(thresholds[i]):len(thresholds[0])])
        self.thresholds[1] = self.thresholds[0]
        #self.properties = file.properties['PXDDACsSettings']     
        self.comment = file.properties['Comment']
        self.digestSettings(file.properties['PXDDACsSettings'])
        
    def digestSettings(self, settings_from_properties):
        self.settings = []
        pattern = '<(.*)>\s*<Name>(.*)<\/Name>\s*<Val>(.*)<\/Val>\s*<\/(.*)>'
        matches = re.findall(pattern, settings_from_properties)
        for match in matches:
            datatype = 'DT: ' + match[0]
            name = 'Name: ' + match[1]
            value = 'Value: ' + match[2]
            setting = name + '\n' + value #datatype + '\n' + 
            self.settings.append(setting)

    def getCurrentData(self):
        return self.values[self.dataset]
    def getCurrentThreshold(self):
        return self.thresholds[self.dataset]
    def getSettings(self):
        return self.settings
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
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.thresholdsConfig = config['thresholdsConfig']
                self.valuesConfig = config['valuesConfig']
        except:
            print('CONFIG CORRUPTED\ngenerating example config file: --example_config.json--')
            with open("example_config.json", "w") as config_file:
                data_set = {'thresholdsConfig': [0, 2],
                            'valuesConfig' : [1, 3]
                            }
                config_file.write(json.dumps(data_set, indent=4))
                print('application will exit now...')
                exit()
