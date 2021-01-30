import pkg_resources
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.config import Config
import kivy

import sys
if sys.version_info.major != 3 or sys.version_info.minor != 8:
    print(sys.version_info)
    sys.exit('Python 3.8.X or is required.')
pkg_resources.require("matplotlib==3.1.3")
from heatmap import Heatmap
from fileChooser import FileChooser
from graph import SingleGraph, MultiGraph

kivy.require('1.11.1')

WINDOW_RATIO = 1.7578051087984862819299905392621

class tdmsAnalyzer(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = BoxLayout()
        self.leftpanel = BoxLayout(orientation='vertical')
        self.txtandbuttons = BoxLayout(orientation='vertical')
        self.textfields = GridLayout(rows=2)
        self.buttons = BoxLayout()
        self.heatmap = Heatmap(on_hit = self.updateGraphs)
        self.filechooser = FileChooser(loadingFunction = self.heatmap.loadData)
        self.singlegraph = SingleGraph([0] * 376)
        self.multigraph = MultiGraph([0] * 376)
        
        self.lblScaleVal = Label(text = 'Y MAX')
        self.lblThVal = Label(text = 'THRESHOLD')
        self.txtScaleVal = TextInput(text = '1',
                                  multiline = False,
                                  on_text_validate = self.scaleUpdate)
        self.txtThVal = TextInput(text = '0',
                                  multiline = False,
                                  on_text_validate = self.thresholdUpdate)
        
        
        self.btnNext = Button(text = 'NEXT\nFIGURE',
                    on_press = self.heatmap.nextFigure)
        self.btnPrev = Button(text = 'PREVIOUS\nFIGURE',
                    on_press = self.heatmap.prevFigure)
        self.btnClearHistory = Button(text = 'CLEAR\nHISTORY',
                    on_press = self.clearHistory)
        self.btnExit = Button(text = 'EXIT',
                    on_press = self.stop)
    

    # Function that returns
    # the root widget
    def build(self):
        Window.size = (int(600 * WINDOW_RATIO), 600)
        Window.bind(on_resize=self.checkResize)
        self.buttons.add_widget(self.btnPrev)
        self.buttons.add_widget(self.btnNext)
        self.buttons.add_widget(self.btnClearHistory)
        self.buttons.add_widget(self.btnExit)
        
        self.textfields.add_widget(self.lblScaleVal)
        self.textfields.add_widget(self.lblThVal)
        self.textfields.add_widget(self.txtScaleVal)
        self.textfields.add_widget(self.txtThVal)
        
        self.txtandbuttons.add_widget(self.textfields)
        self.txtandbuttons.add_widget(self.buttons)
        
        self.leftpanel.add_widget(self.singlegraph)
        self.leftpanel.add_widget(self.multigraph)
        self.leftpanel.add_widget(self.txtandbuttons)
        
        self.box.add_widget(self.leftpanel)
        self.box.add_widget(self.heatmap)
        
        self.box.add_widget(self.filechooser)
        
        return self.box

    def updateGraphs(self, x, y):
        currentData = self.singlegraph.getData()
        updateData = [self.heatmap.getDataElement(frame, x, y) for frame in range(self.heatmap.getNumberOfFrames())]
        frameNumber = self.heatmap.getFrameNumber()
        self.singlegraph.updateGraph(updateData, frameNumber)
        self.multigraph.updateGraph(currentData, frameNumber)
        self.filechooser.updateCoordinates(x, y)
        
    def thresholdUpdate(self, instance):
        try:
            if self.heatmap.setDataIndex(int(instance.text)):
                print('frame: ' + instance.text)
            else:
                raise Exception
        except:
            instance.text = str(self.heatmap.getFrameNumber())
            print('invalid frame index')
            
    def scaleUpdate(self, instance):
        try:
            if self.singlegraph.setScale(int(instance.text)):
                print('scale: ' + instance.text)
            else:
                raise Exception
        except:
            instance.text = str(self.singlegraph.getScale())
            print('invalid scale value')
        
        
    def clearHistory(self, instance):
        self.multigraph.clearGraph()
    def checkResize(self, instance, x, y):
        if x >  y * WINDOW_RATIO:
            x = y * WINDOW_RATIO
        elif y > (x / WINDOW_RATIO) + 5:
            y = x / WINDOW_RATIO
        Window.size = (int(x), int(y))
        
    
    def on_stop(self):
        pass #TBD: add saving last path in file
    def on_start(self):
        pass #TBD: add loading last path from file

tdmsAnalyzer().run()
