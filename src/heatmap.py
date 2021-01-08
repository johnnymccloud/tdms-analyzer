from tdms import read_tdms_to_nparray
# Implementation of matplotlib function
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

from kivy.uix.boxlayout import BoxLayout


from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

class Heatmap(BoxLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.data = read_tdms_to_nparray('test.tdms')
        self.dataIndex = 0
        self.renderGraph()
        #plt.colorbar(heatmap)
        
    def renderGraph(self):
        plt.imshow(self.data[self.dataIndex])
        self.clear_widgets()
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        
    def nextFigure(self, btn):
        if self.dataIndex < len(self.data) - 1:
            self.dataIndex += 1
            self.renderGraph()
        
    def prevFigure(self, btn):
        if self.dataIndex > 0:
            self.dataIndex -= 1
            self.renderGraph()
        
    