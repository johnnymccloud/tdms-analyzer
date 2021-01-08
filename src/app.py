from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from kivy.uix.button import Button
import kivy

from heatmap import Heatmap

kivy.require('1.11.1')

class tdmsAnalyzer(App):

    # Function that returns
    # the root widget
    def build(self):
        box = BoxLayout()
        # plt.plot([1, 23, 2, 4])
        # plt.ylabel('some numbers')
        heatmap = Heatmap()
        btnNext = Button(text = 'next',
                    size = (100,100),
                    on_press = heatmap.nextFigure)
        btnPrev = Button(text = 'prev',
                    size = (100,100),
                    on_press = heatmap.prevFigure)
        
        box.add_widget(btnPrev)
        box.add_widget(btnNext)
        box.add_widget(heatmap)
        
        return box

    # Here our class is initialized

tdmsAnalyzer().run()
