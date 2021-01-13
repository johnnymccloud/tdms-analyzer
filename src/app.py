import pkg_resources
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import kivy

import sys
if sys.version_info.major != 3 or sys.version_info.minor != 8:
    print(sys.version_info)
    sys.exit('Python 3.8.X or is required.')
pkg_resources.require("matplotlib==3.1.3")
import matplotlib.pyplot as plt

from heatmap import Heatmap
from fileChooser import FileChooser
from graph import SingleGraph

kivy.require('1.11.1')

class tdmsAnalyzer(App):

    # Function that returns
    # the root widget
    def build(self):
        box = BoxLayout()
        leftpanel = BoxLayout(orientation='vertical')
        buttons = BoxLayout()
        # plt.plot([1, 23, 2, 4])
        # plt.ylabel('some numbers')
        heatmap = Heatmap()
        filechooser = FileChooser(loadingFunction = heatmap.loadData)
        btnNext = Button(text = 'NEXT FIGURE',
                    size = (100,100),
                    on_press = heatmap.nextFigure)
        btnPrev = Button(text = 'PREVIOUS FIGURE',
                    size = (100,100),
                    on_press = heatmap.prevFigure)
        btnExit = Button(text = 'EXIT',
                    size = (100,100),
                    on_press = self.stop)
        
        singlegraph = SingleGraph(range(376))
        multigraph = SingleGraph(range(375, -1, -1))
        
        
        buttons.add_widget(btnPrev)
        buttons.add_widget(btnNext)
        buttons.add_widget(btnExit)
        
        leftpanel.add_widget(singlegraph)
        leftpanel.add_widget(multigraph)
        leftpanel.add_widget(buttons)
        
        box.add_widget(leftpanel)
        box.add_widget(heatmap)
        
        box.add_widget(filechooser)
        
        return box

    def on_stop(self):
        pass #TBD: add saving last path in file
    def on_start(self):
        pass #TBD: add loading last path from file

tdmsAnalyzer().run()
