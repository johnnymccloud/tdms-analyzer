from matplotlib import style
from matplotlib import pyplot as plt
#from matplotlib import use as mpl_use
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label

#mpl_use('module://kivy.garden.matplotlib.backend_kivy')
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
        except:
            print('invalid scale value')
        return True
            
    def sliderRangeUpdate(self, val):
        if val > 0:
            self.slider.max = int(val)
        else:
            print('invalid slider max value')
            
    def updateGraph(self, frameNumber = None, data = None):
        self.graph.updateGraph(data, frameNumber)
        if data != None:
            self.sliderRangeUpdate(max(data))
    
    # def autoScale(self, *args):
    #     self.slider.value = 0
    #     return False

class SingleGraph(BoxLayout):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.frameNumber = 0
        self.scale = 0
        self.fig, self.ax = plt.subplots()
        self.ax.plot(data, lw=0.5)
        self.ax.set_ylim(bottom = 0, top = None)
        self.add_widget(FigureCanvasKivyAgg(self.fig))
        self.fig.canvas.draw_idle()
        
    def renderGraph(self):
        self.ax.clear()
        self.ax.plot([self.frameNumber, self.frameNumber], [0, max(max(self.data), self.scale)], 'k-', lw=1, color='red')
        self.ax.plot(self.data, lw=0.5)
        if self.scale != 0:
            self.ax.set_ylim(bottom = 0, top = self.scale)
        else:
            self.ax.set_ylim(bottom = 0, top = None)
        self.fig.canvas.draw_idle()
       
    def updateGraph(self, data = None, frameNumber = None):
        if data != None:
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
        self.scale = 0
        self.fig, self.ax = plt.subplots()
        self.ax.plot(data, lw=0.5)
        self.ax.set_ylim(bottom = 0, top = None)
        self.add_widget(FigureCanvasKivyAgg(self.fig))
        self.fig.canvas.draw_idle()
        
    def renderGraph(self):
        self.ax.set_ylim(auto = True)
        self.ax.plot(self.data, lw=0.5)
        if self.scale != 0:
            self.ax.set_ylim(bottom = 0, top = self.scale)
        else:
            self.ax.set_ylim(bottom = 0, top = None)
        self.fig.canvas.draw_idle()
       
    def updateGraph(self, data = None, frameNumber = None):
        if data != None:
            self.data = data
            self.renderGraph()
        
    def clearGraph(self):
        self.ax.clear()
        self.renderGraph()
    
    def setScale(self, scale_new):
        if 0 <= scale_new:
            self.scale = scale_new
            self.renderGraph()
            return True
        else:
            return False
            
    def getScale(self):
        return self.scale