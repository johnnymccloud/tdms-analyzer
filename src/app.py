from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import matplotlib.pyplot as plt
from kivy.uix.label import Label
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import kivy

from heatmap import heatmap_from_tdms

kivy.require('1.11.1')

class tdmsAnalyzer(App):

    # Function that returns
    # the root widget
    def build(self):
        box = BoxLayout()
        # plt.plot([1, 23, 2, 4])
        # plt.ylabel('some numbers')
        plot = heatmap_from_tdms('test.tdms')
        box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        return box

    # Here our class is initialized

tdmsAnalyzer().run()
