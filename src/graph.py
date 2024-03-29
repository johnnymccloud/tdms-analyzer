import numpy as np
from matplotlib import style
from matplotlib import pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
style.use('dark_background')

class GraphPanel(FloatLayout):
    def __init__(self, data, multi = False, single = False, **kwargs):
        super().__init__(**kwargs)
        if single:
            self.graph = SingleGraph(data,
                                     size_hint = (0.9, 1),
                                     pos_hint = {'x': 0.1, 'y' : 0})
        elif multi:
            self.graph = MultiGraph(data,
                                    size_hint = (0.9, 1),
                                    pos_hint = {'x': 0.1, 'y' : 0})
        else:
            raise Exception('Graph has to be either Multi or Single')
        self.slider = Slider(min = 0, max = 1, value = 0,
                             orientation = 'vertical',
                             size_hint = (0.1, 0.9),
                             pos_hint = {'x': 0, 'y' : 0.1})
        self.slider.bind(value = self.graphScaleUpdate)
        self.lblSliderValue = Label(text = '0',
                             size_hint = (0.1, 0.1),
                             pos_hint = {'x': 0, 'y' : 0})
        
        self.add_widget(self.graph)
        self.add_widget(self.slider)
        self.add_widget(self.lblSliderValue)
        
    def graphScaleUpdate(self, instance, val):
        try:
            scale_new = int(val)
            if val >= 0:
                self.graph.setScale(scale_new)
                self.lblSliderValue.text = str(scale_new)
            else:
                raise Exception('negative scale value')
        except Exception as exception:
            print(exception)
        return True
            
    def sliderRangeUpdate(self, val):
        if val > 0:
            self.slider.max = int(val)
            
    def updateGraph(self, frameNumber = None, data = None):
        self.graph.updateGraph(data, frameNumber)
        if data != None:
            if type(self.graph) is SingleGraph:
                self.sliderRangeUpdate(max(data))
            else:
                self.sliderRangeUpdate(max(max(data), self.graph.indicatorLength))
                
    def updateThresholdList(self, thresholdList):
        self.graph.updateThresholdList(thresholdList)

class SingleGraph(BoxLayout):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.thresholds = range(len(self.data))
        self.frameNumber = 0
        self.scale = 0
        self.fig, self.ax = plt.subplots()
        self.ax.plot(self.thresholds, data, lw=0.5)
        self.indicatorLength = 1
        self.ax.set_ylim(bottom = 0, top = self.indicatorLength)
        self.add_widget(FigureCanvasKivyAgg(self.fig))
        self.fig.canvas.draw_idle()
        
    def renderGraph(self):
        self.ax.clear()
        self.ax.set_ylim(auto = True)
        self.indicatorLength = max(max(self.data), self.scale, 1)
        self.ax.plot([self.frameNumber, self.frameNumber], [0, self.indicatorLength], 'k-', lw=0.5, color='red')
        self.ax.plot(self.thresholds, self.data, lw=0.5)
        if self.scale != 0:
            self.ax.set_ylim(bottom = 0, top = self.scale)
        else:
            self.ax.set_ylim(bottom = 0, top = self.indicatorLength)
        self.fig.canvas.draw_idle()
       
    def updateGraph(self, data = None, frameNumber = None):
        if data != None:
            self.data = data
        self.frameNumber = frameNumber
        self.renderGraph()
        
    def updateThresholdList(self, thresholdList):
        self.thresholds = thresholdList
    
    def getData(self):
        return self.data
    
    def setScale(self, scale_new):
        if 0 <= scale_new:
            self.scale = scale_new
            self.renderGraph()
            return True
        else:
            return False
            
    def getScale(self):
        return self.scale
        
        
class MultiGraph(BoxLayout):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.thresholds = range(len(self.data))
        self.frameNumber = 0
        self.scale = 0
        self.fig, self.ax = plt.subplots()
        #self.ax.plot(self.thresholds, self.data, lw=0.5)
        self.indicatorLength = 1
        self.ax.set_ylim(bottom = 0, top = self.indicatorLength)
        self.add_widget(FigureCanvasKivyAgg(self.fig))
        self.fig.canvas.draw_idle()
        self.frameIndicator = None
        

    def renderGraph(self, drawData = True):
        if drawData:
            self.ax.plot(self.thresholds, self.data, lw=0.5)
        self.updateScale()
        self.fig.canvas.draw_idle()
    
    def renderFrameIndicator(self):
        if self.frameIndicator != None:
            vertical_line = self.frameIndicator.pop(0)
            vertical_line.remove()
        self.indicatorLength = max(max(self.data), self.scale, self.indicatorLength)
        self.frameIndicator = self.ax.plot([self.frameNumber, self.frameNumber], [0, self.indicatorLength], 'k-', lw=0.5, color='red')
        self.fig.canvas.draw_idle()
       
    def updateGraph(self, data = None, frameNumber = None):
        if frameNumber != None:
            self.frameNumber = frameNumber
            self.renderFrameIndicator()
        if data != None:
            self.data = data
            self.renderFrameIndicator()
            self.renderGraph()
            
    def updateThresholdList(self, thresholdList):
        self.thresholds = thresholdList
    
    def updateScale(self):
        self.ax.set_ylim(auto = True)
        if self.scale != 0:
            self.ax.set_ylim(bottom = 0, top = self.scale)
        else:
            self.ax.set_ylim(bottom = 0, top = self.indicatorLength)
        self.fig.canvas.draw_idle()
    
    def clearGraph(self):
        self.ax.clear()
        self.data = np.zeros(len(self.data))
        self.indicatorLength = 1
        self.renderGraph()
        self.renderFrameIndicator()
    
    def setScale(self, scale_new):
        if 0 <= scale_new:
            self.scale = scale_new
            self.updateScale()
            return True
        else:
            return False
            
    def getScale(self):
        return self.scale