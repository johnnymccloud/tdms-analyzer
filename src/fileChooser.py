import os
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

from tdms import TdmsReader


class ThresholdList(GridLayout):
    def __init__(self, chooseThFnc, **kwargs):
        super().__init__(cols = 2, **kwargs)
        
        self.btnList = None
        self.chooseThFnc = chooseThFnc
        
    def updateThresholds(self, thresholds):
        self.clear_widgets()
        for th in thresholds:
            btn = Button(text = th,
                         on_press = self.chooseThFnc)
            self.add_widget(btn)
            

            
        
        
class FileList(FileChooserListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = os.getcwd()
        #self.filters = ['\*.tdms']
        self.filter_dirs = False
        
class FileChooser(FloatLayout):
    def __init__(self, loadingFunction, **kwargs):
        super().__init__(**kwargs)
        self.loadingfunction = loadingFunction
        self.tdmsReader = TdmsReader()
        
        
        self.filelist = FileList(size_hint = (1, 0.7),
                                 pos_hint = {'x': 0, 'y' : 0.3})
        self.thresholdlist = ThresholdList(size_hint = (1, 0.2),
                                           pos_hint = {'x': 0, 'y' : 0.1},
                                           chooseThFnc = self.changeTh)
        self.loadbutton = Button(size_hint = (0.5, 0.1),
                                 pos_hint = {'x': 0.5, 'y' : 0},
                                 text = 'LOAD FILE',
                                 on_press = self.loadFileFromPath)
        self.coordinates = Label(size_hint = (0.5, 0.1),
                                 pos_hint = {'x': 0, 'y' : 0},
                                 text = '0, 0')
        
        self.add_widget(self.filelist)
        self.add_widget(self.thresholdlist)
        self.add_widget(self.loadbutton)
        self.add_widget(self.coordinates)
        
    def loadFileFromPath(self, btn):
        try:
            tdmsPath = self.filelist.selection[0]
            print(tdmsPath + ' check if TDMS file')
            if '.tdms' in tdmsPath:
                print(tdmsPath + ' loading...')
                self.tdmsReader.readTdmsToNpArray(tdmsPath)
                data = self.tdmsReader.getCurrentData()
                self.loadingfunction(data)
                self.thresholdlist.updateThresholds(self.tdmsReader.getThresholdNames())
                print('SUCCESSFULLY LOADED')
            else:
                print('Incorrect File')
        except:
            print('Select File')
            
    def changeTh(self, btn):
        updateRequired = self.tdmsReader.setThreshold(btn.text)
        if updateRequired:
            data = self.tdmsReader.getCurrentData()
            self.loadingfunction(data)
    
    def updateCoordinates(self, x, y):
        tempText = str(x) + ', ' + str(y)
        self.coordinates.text = tempText
            