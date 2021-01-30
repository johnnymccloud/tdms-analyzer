from matplotlib import style
from matplotlib import pyplot as plt
#from matplotlib import use as mpl_use
from kivy.uix.boxlayout import BoxLayout

#mpl_use('module://kivy.garden.matplotlib.backend_kivy')
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
style.use('dark_background')

class SingleGraph(BoxLayout):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.frameNumber = 0
        self.scale = 0
        self.fig, self.ax = plt.subplots()
        self.ax.plot(data, lw=0.5)
        self.ax.set_ylim(0, self.scale)
        self.add_widget(FigureCanvasKivyAgg(self.fig))
        self.fig.canvas.draw_idle()
        
    def renderGraph(self):
        self.ax.clear()
        self.ax.plot([self.frameNumber, self.frameNumber], [0, max(self.data)], 'k-', lw=1, color='red')
        self.ax.plot(self.data, lw=0.5)
        if self.scale != 0:
            self.ax.set_ylim(bottom = 0, top = self.scale)
        else:
            self.ax.set_ylim(bottom = 0, top = None)
        self.fig.canvas.draw_idle()
       
    def updateGraph(self, data, frameNumber):
        self.data = data
        self.frameNumber = frameNumber
        self.renderGraph()
    
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
        self.frameNumber = 0
        self.fig, self.ax = plt.subplots()
        self.ax.plot(data, lw=0.5)
        self.add_widget(FigureCanvasKivyAgg(self.fig))
        self.fig.canvas.draw_idle()
        
    def renderGraph(self):
        #self.ax.plot([self.frameNumber, self.frameNumber], [0, max(self.data)], 'k-', lw=2, color='red')
        self.ax.plot(self.data, lw=0.5)
        self.ax.set_ylim(bottom = 0, top = None)
        self.fig.canvas.draw_idle()
       
    def updateGraph(self, data, frameNumber):
        self.data = data
        self.frameNumber = frameNumber
        self.renderGraph()
        
    def clearGraph(self):
        self.ax.clear()
        self.renderGraph()