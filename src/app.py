from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from kivy.uix.button import Button

import kivy

from heatmap import Heatmap
from fileChooser import FileChooser

kivy.require('1.11.1')

class tdmsAnalyzer(App):

    # Function that returns
    # the root widget
    def build(self):
        box = BoxLayout()
        buttons = BoxLayout(orientation='vertical')
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
        
        buttons.add_widget(btnPrev)
        buttons.add_widget(btnNext)
        buttons.add_widget(btnExit)
        
        box.add_widget(buttons)
        box.add_widget(heatmap)
        
        box.add_widget(filechooser)
        
        return box

    def on_stop(self):
        pass #TBD: add saving last path in file
    def on_start(self):
        pass #TBD: add loading last path from file

tdmsAnalyzer().run()
