import pkg_resources
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
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
from graph import GraphPanel
from thresholdSlider import ThresholdSlider

kivy.require('1.11.1')

WINDOW_RATIO = 1.7578051087984862819299905392621

class tdmsAnalyzer(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = BoxLayout()
        self.leftpanel = BoxLayout(orientation='vertical')
        self.sliderandbuttons = BoxLayout(orientation='vertical')
        self.thresholdslider = ThresholdSlider(thresholdUpdateFnc = self.thresholdUpdate)
        self.buttons = BoxLayout()
        self.heatmap = Heatmap(on_hit = self.updateGraphs)
        self.filechooser = FileChooser(loadingFunction = self.heatmap.loadData)
        self.singlegraphpanel = GraphPanel(data = [0] * 376, single = True)
        self.multigraphpanel = GraphPanel(data = [0] * 376, multi = True)  
        
        self.btnNext = Button(text = 'NEXT\nFIGURE',
                    on_press = self.nextFigure)
        self.btnPrev = Button(text = 'PREVIOUS\nFIGURE',
                    on_press = self.prevFigure)
        self.btnClearHistory = Button(text = 'CLEAR\nHISTORY',
                    on_press = self.clearHistory)
        self.btnExit = Button(text = 'EXIT',
                    on_press = self.stop)

    def build(self):
        Window.size = (int(600 * WINDOW_RATIO), 600)
        Window.bind(on_resize=self.checkResize)
        self.buttons.add_widget(self.btnPrev)
        self.buttons.add_widget(self.btnNext)
        self.buttons.add_widget(self.btnClearHistory)
        self.buttons.add_widget(self.btnExit)
        
        self.sliderandbuttons.add_widget(self.thresholdslider)
        self.sliderandbuttons.add_widget(self.buttons)
        
        self.leftpanel.add_widget(self.singlegraphpanel)
        self.leftpanel.add_widget(self.multigraphpanel)
        self.leftpanel.add_widget(self.sliderandbuttons)
        
        self.box.add_widget(self.leftpanel)
        self.box.add_widget(self.heatmap)
        
        self.box.add_widget(self.filechooser)
        
        return self.box

    def updateGraphs(self, x, y):
        currentData = self.singlegraphpanel.graph.getData()
        updateData = [self.heatmap.getDataElement(frame, x, y) for frame in range(self.heatmap.getNumberOfFrames())]
        frameNumber = self.heatmap.getFrameNumber()
        self.singlegraphpanel.updateGraph(frameNumber, updateData)
        self.multigraphpanel.updateGraph(data = currentData)
        self.filechooser.updateCoordinates(x, y)
        
    def maxThUpdate(self, val):
        print(val)
    def thresholdUpdate(self, instance, val):
        try:
            threshold_new = int(val)
            if self.heatmap.setDataIndex(threshold_new):
                self.singlegraphpanel.updateGraph(frameNumber = threshold_new)
                print('frame: ' + str(threshold_new))
            else:
                raise Exception
        except:
            print('invalid frame index')        
        
    def clearHistory(self, instance):
        self.multigraphpanel.graph.clearGraph()
    def prevFigure(self, btn):
        self.heatmap.prevFigure()
        self.thresholdslider.thresholdDec()
    def nextFigure(self, btn):
        self.heatmap.nextFigure()
        self.thresholdslider.thresholdInc()
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
