import os
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

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
            
class SettingsList(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(cols = 4, **kwargs)
        
        self.lblList = None
        
    def updateSettings(self, settings):
        self.clear_widgets()
        for setting in settings:
            lbl = Label(text = setting)
            self.add_widget(lbl)
               
        
class FileList(FileChooserListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = os.getcwd()
        self.filters = ['*.tdms']
        self.filter_dirs = False
        
class FileChooser(FloatLayout):
    def __init__(self, loadingFunction, **kwargs):
        super().__init__(**kwargs)
        self.loadingfunction = loadingFunction
        self.tdmsReader = TdmsReader()
        
        self.filelist = FileList(size_hint = (1, 0.4),
                                 pos_hint = {'x': 0, 'y' : 0.6})
        self.comment = TextInput(text = '',
                                 readonly = True,
                                 size_hint = (1, 0.1),
                                 pos_hint = {'x': 0, 'y' : 0.5})
        self.settingslist = SettingsList(size_hint = (1, 0.35),
                                           pos_hint = {'x': 0, 'y' : 0.15})
        self.thresholdlist = ThresholdList(size_hint = (1, 0.1),
                                           pos_hint = {'x': 0, 'y' : 0.05},
                                           chooseThFnc = self.changeTh)
        self.loadbutton = Button(size_hint = (0.5, 0.05),
                                 pos_hint = {'x': 0.5, 'y' : 0},
                                 text = 'LOAD FILE',
                                 on_press = self.loadFileFromPath)
        self.coordinates = Label(size_hint = (0.5, 0.05),
                                 pos_hint = {'x': 0, 'y' : 0},
                                 text = '0, 0')
        
        self.add_widget(self.filelist)
        self.add_widget(self.comment)
        self.add_widget(self.settingslist)
        self.add_widget(self.thresholdlist)
        self.add_widget(self.loadbutton)
        self.add_widget(self.coordinates)
        
    def loadFileFromPath(self, btn):
        try:
            tdmsPath = self.filelist.selection[0]
            print(tdmsPath + ' check if TDMS file')
            if '.tdms' in tdmsPath:
                print(tdmsPath + ' loading...')
                self.tdmsReader.readTdms(tdmsPath)
                self.updateDataAndThresholds()
                self.settingslist.updateSettings(self.tdmsReader.getSettings())
                self.thresholdlist.updateThresholds(self.tdmsReader.getThresholdNames())
                self.comment.text = self.tdmsReader.getComment()
                print('SUCCESSFULLY LOADED')
            else:
                print('Incorrect File')
        except Exception as exception:
            print(exception)
            print('Select File')
            
    def changeTh(self, btn):
        updateRequired = self.tdmsReader.setThreshold(btn.text)
        if updateRequired:
            self.updateDataAndThresholds()
            
    def updateDataAndThresholds(self):
        data = self.tdmsReader.getCurrentData()
        thresholds = self.tdmsReader.getCurrentThreshold()
        self.loadingfunction(data, thresholds)
    
    def updateCoordinates(self, x, y):
        tempText = str(x) + ', ' + str(y)
        self.coordinates.text = tempText
            