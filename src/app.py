import pkg_resources
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
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
from graph import SingleGraph

kivy.require('1.11.1')

WINDOW_RATIO = 1.7578051087984862819299905392621

class tdmsAnalyzer(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = BoxLayout()
        self.leftpanel = BoxLayout(orientation='vertical')
        self.buttons = BoxLayout()
        self.heatmap = Heatmap(on_hit = self.updateSinglegraphData)
        self.filechooser = FileChooser(loadingFunction = self.heatmap.loadData)
        self.btnNext = Button(text = 'NEXT\nFIGURE',
                    #size = (100,100),
                    on_press = self.heatmap.nextFigure)
        self.btnPrev = Button(text = 'PREVIOUS\nFIGURE',
                    #size = (100,100),
                    on_press = self.heatmap.prevFigure)
        self.btnExit = Button(text = 'EXIT',
                    #size = (100,100),
                    on_press = self.stop)

        self.singlegraph = SingleGraph(range(376))
        self.multigraph = SingleGraph(range(375, -1, -1))
    # Function that returns
    # the root widget
    def build(self):
        Window.size = (int(600 * WINDOW_RATIO), 600)
        Window.bind(on_resize=self.checkResize)
        self.buttons.add_widget(self.btnPrev)
        self.buttons.add_widget(self.btnNext)
        self.buttons.add_widget(self.btnExit)
        
        self.leftpanel.add_widget(self.singlegraph)
        self.leftpanel.add_widget(self.multigraph)
        self.leftpanel.add_widget(self.buttons)
        
        self.box.add_widget(self.leftpanel)
        self.box.add_widget(self.heatmap)
        
        self.box.add_widget(self.filechooser)
        
        return self.box

    def updateSinglegraphData(self, x, y):
        updateData = [self.heatmap.getDataElement(frame, x, y) for frame in range(self.heatmap.getNumberOfFrames())]
        frameNumber = self.heatmap.getFrameNumber()
        self.singlegraph.updateGraph(updateData, frameNumber)  
    
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
