# Implementation of matplotlib function
import matplotlib.pyplot as plt
import numpy as np

from kivy.uix.boxlayout import BoxLayout

# from kivy.graphics import *


from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

class Heatmap(BoxLayout):
    
    def __init__(self, initial_frames_number, on_hit, **kwargs):
        super().__init__(**kwargs)
        self.hitX = 0
        self.hitY = 0
        self.data = np.zeros((initial_frames_number, 256, 128))
        self.thresholds = range(initial_frames_number)
        self.dataIndex = 0
        self.fig, self.ax = plt.subplots()
        self.renderHeatmap()
        self.on_hit = on_hit        
        
    def renderHeatmap(self):
        self.ax.clear()
        self.ax.imshow(self.data[self.dataIndex], origin='lower')
        self.ax.axis('off')
        self.clear_widgets()
        self.add_widget(FigureCanvasKivyAgg(self.fig))
        
        
    def nextFigure(self):
        if self.dataIndex < len(self.data) - 1:
            self.dataIndex += 1
            self.renderHeatmap()
        
    def prevFigure(self):
        if self.dataIndex > 0:
            self.dataIndex -= 1
            self.renderHeatmap()
            
    def setDataIndex(self, dataIndex_new):
        if 0 <= dataIndex_new < len(self.data):
            self.dataIndex = dataIndex_new
            self.renderHeatmap()
            return True
        else:
            return False
            
    def loadData(self, data, thresholds):
        self.data = data
        self.thresholds = thresholds
        self.renderHeatmap()
        
    def getDataElement(self, frame, x, y):
        return self.data[frame][y][x]
    def getNumberOfFrames(self):
        return len(self.data)
    def getFrameNumber(self):
        return self.dataIndex
    def getThresholdValue(self):
        return self.thresholds[self.dataIndex]
    def getThresholdList(self):
        return self.thresholds
    
    def on_touch_down(self, touch):
        inX, inY = touch.pos
        X = inX / self.width - 1
        Y = inY / self.height
        heatmapX = round((X - 0.18353) / 0.005140390625)
        heatmapY = round((Y - 0.1107) / 0.00301171875)      
        if 0 <= heatmapX <= 127 and 0 <= heatmapY <= 255:
            self.hitX, self.hitY = (heatmapX, heatmapY)
            self.on_hit(self.hitX, self.hitY)
        