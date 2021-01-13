from matplotlib import style
from matplotlib import pyplot as plt
from matplotlib import use as mpl_use
import numpy as np
from kivy.uix.boxlayout import BoxLayout

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
mpl_use('module://kivy.garden.matplotlib.backend_kivy')
style.use('dark_background')

class SingleGraph(BoxLayout):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.fig, self.ax = plt.subplots()
        self.ax.plot(data)
        self.mpl_canvas = self.fig.canvas
        self.add_widget(self.mpl_canvas)
        #self.fig.canvas.draw_idle()
        
    def renderGraph(self):
        self.ax.clear()
        self.ax.plot(self.data)
        self.fig.canvas.draw_idle()
        
    def updateGraph(self, data):
        self.data = data
        self.renderGraph()
    
    def do_layout(self, *largs):
        super().do_layout(*largs)
        self.renderGraph()