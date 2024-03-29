import pkg_resources
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
import kivy

import sys
if sys.version_info.major != 3 or sys.version_info.minor != 8:
    print(sys.version_info)
    sys.exit('Python 3.8.X is required.')
pkg_resources.require("matplotlib==3.1.3")
from heatmap import Heatmap
from fileChooser import FileChooser
from graph import GraphPanel
from thresholdSlider import ThresholdSlider

kivy.require('1.11.1')

WINDOW_RATIO = 1.7578051087984862819299905392621
INITIAL_FRAMES_NUMBER = 376

class tdmsAnalyzer(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = BoxLayout()
        self.leftpanel = BoxLayout(orientation='vertical')
        self.sliderandbuttons = BoxLayout(orientation='vertical')
        self.thresholdslider = ThresholdSlider(thresholdUpdateFnc = self.thresholdUpdate)
        self.buttons = BoxLayout()
        self.heatmap = Heatmap(initial_frames_number = INITIAL_FRAMES_NUMBER, on_hit = self.updateGraphs)
        self.filechooser = FileChooser(loadingFunction = self.loadData)
        self.singlegraphpanel = GraphPanel(data = [0] * INITIAL_FRAMES_NUMBER, single = True)
        self.multigraphpanel = GraphPanel(data = [0] * INITIAL_FRAMES_NUMBER, multi = True)  
        
        self.btnNext = Button(text = 'NEXT\nFIGURE',
                    on_press = self.nextFigure)
        self.btnPrev = Button(text = 'PREVIOUS\nFIGURE',
                    on_press = self.prevFigure)
        self.btnAddGraph = Button(text = 'COPY\nGRAPH',
                    on_press = self.addCurrentToMultiGraph)
        self.btnClearHistory = Button(text = 'CLEAR\nGRAPH',
                    on_press = self.clearHistory)
        self.btnExit = Button(text = 'EXIT',
                    on_press = self.stop)

    def build(self):
        Window.size = (int(600 * WINDOW_RATIO), 600)
        Window.bind(on_resize=self.checkResize)
        self.buttons.add_widget(self.btnPrev)
        self.buttons.add_widget(self.btnNext)
        self.buttons.add_widget(self.btnAddGraph)
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
        updateData = [self.heatmap.getDataElement(frame, x, y) for frame in range(self.heatmap.getNumberOfFrames())]
        threshold_new = self.heatmap.getThresholdValue()
        self.singlegraphpanel.updateGraph(frameNumber = threshold_new, data = updateData)
        self.filechooser.updateCoordinates(x, y)
    
    def thresholdUpdate(self, val):
        try:
            data_index = int(val)
            if self.heatmap.setDataIndex(data_index):
                threshold_new = self.heatmap.getThresholdValue()
                self.singlegraphpanel.updateGraph(frameNumber = threshold_new)
                self.multigraphpanel.updateGraph(frameNumber = threshold_new)
                return threshold_new
            else:
                raise Exception
        except:
            return 0
    def loadData(self, data, thresholds):
        self.heatmap.loadData(data, thresholds)
        self.singlegraphpanel.updateThresholdList(thresholds)
        self.multigraphpanel.updateThresholdList(thresholds)
        
    def addCurrentToMultiGraph(self,btn):
        currentData = self.singlegraphpanel.graph.getData()
        self.multigraphpanel.updateGraph(data = currentData)
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

tdmsAnalyzer().run()
