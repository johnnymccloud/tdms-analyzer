from matplotlib import style
from matplotlib import pyplot as plt
from matplotlib import use as mpl_use
from kivy.uix.boxlayout import BoxLayout

mpl_use('module://kivy.garden.matplotlib.backend_kivy')
style.use('dark_background')

class SingleGraph(BoxLayout):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.frameNumber = 0
        self.fig, self.ax = plt.subplots()
        self.ax.plot(data)
        self.mpl_canvas = self.fig.canvas
        self.add_widget(self.mpl_canvas)
        #self.fig.canvas.draw_idle()
        
    def renderGraph(self):
        self.ax.clear()
        self.ax.plot(self.data)
        self.ax.plot([self.frameNumber, self.frameNumber], [0, max(self.data)], 'k-', lw=2, color='red')
        self.fig.canvas.draw_idle()
       
    def updateGraph(self, data, frameNumber):
        self.data = data
        self.frameNumber = frameNumber
        self.renderGraph()
    
    def do_layout(self, *largs):
        super().do_layout(*largs)
        self.renderGraph()