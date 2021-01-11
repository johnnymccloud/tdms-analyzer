from kivy.uix.filechooser import FileChooserListView
import os
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button



class FileList(FileChooserListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.path = os.getcwd()
        #self.filters = ['\*.tdms']
        self.filter_dirs = False
        
class FileChooser(FloatLayout):
    def __init__(self, loadingFunction, **kwargs):
        super().__init__(**kwargs),
        self.loadingfunction = loadingFunction
        self.filelist = FileList(size_hint = (1, 0.9),
                                 pos_hint = {'x': 0, 'y' : 0.1})
        self.loadbutton = Button(size_hint = (0.5, 0.1),
                                 pos_hint = {'x': 0, 'y' : 0},
                                 text = 'LOAD FILE',
                                 on_press = self.loadFileFromPath)
        
        self.add_widget(self.filelist)
        self.add_widget(self.loadbutton)
        
    def loadFileFromPath(self, btn):
        tdmsPath = self.filelist.selection[0] 
        print(tdmsPath + ' check if TDMS file')
        if '.tdms' in tdmsPath:
            print(tdmsPath + ' loading...')
            self.loadingfunction(tdmsPath)
        else:
            print('Incorrect File')
            