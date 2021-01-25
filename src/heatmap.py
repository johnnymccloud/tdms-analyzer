from tdms import read_tdms_to_nparray
# Implementation of matplotlib function
import matplotlib.pyplot as plt
import numpy as np

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

# from kivy.graphics import *


from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

class Heatmap(BoxLayout):
    
    def __init__(self, on_hit, **kwargs):
        super().__init__(**kwargs)
        
        
        self.hitX = 0
        self.hitY = 0
        # self.chosen = None
        self.data = np.zeros((376, 256, 128))
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
        
        
    def nextFigure(self, btn):
        if self.dataIndex < len(self.data) - 1:
            self.dataIndex += 1
            self.renderHeatmap()
        
    def prevFigure(self, btn):
        if self.dataIndex > 0:
            self.dataIndex -= 1
            self.renderHeatmap()
            
    def loadData(self, path):
        self.data = read_tdms_to_nparray(path)
        self.renderHeatmap()
        
    def getDataElement(self, frame, x, y):
        return self.data[frame][y][x]
    def getNumberOfFrames(self):
        return len(self.data)
    def getFrameNumber(self):
        return self.dataIndex
    
    def on_touch_down(self, touch):
        inX, inY = touch.pos
        X = inX / self.width - 1
        Y = inY / self.height
        heatmapX = round((X - 0.18353) / 0.005140390625)
        heatmapY = round((Y - 0.1107) / 0.00301171875)      
        if 0 <= heatmapX <= 127 and 0 <= heatmapY <= 255:
            self.hitX, self.hitY = (heatmapX, heatmapY)
            print('\n--- TOUCH ---\n')
            print((self.hitX, self.hitY))
            self.on_hit(self.hitX, self.hitY)
            # if self.chosen != None:
            #     self.canvas.remove(self.chosen)
            # self.chosen = Rectangle(pos=(inX, inY), size=(10, 10))
            # self.canvas.add(self.chosen)
        #print(touch.pos)
        