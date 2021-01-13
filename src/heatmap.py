from tdms import read_tdms_to_nparray
# Implementation of matplotlib function
import matplotlib.pyplot as plt
import numpy as np

from kivy.uix.boxlayout import BoxLayout


from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

class Heatmap(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        #self.data = read_tdms_to_nparray('test.tdms')
        self.data = np.zeros((376, 256, 128))
        self.dataIndex = 0
        self.renderHeatmap()
        #plt.colorbar(heatmap)
        
    def renderHeatmap(self):
        plt.clf()
        plt.imshow(self.data[self.dataIndex], origin='lower')
        self.clear_widgets()
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
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