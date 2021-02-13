from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label

class ThresholdSlider(FloatLayout):
    def __init__(self, thresholdUpdateFnc, **kwargs):
        super().__init__(**kwargs)
        self.thresholdUpdateFnc = thresholdUpdateFnc
        self.slider = Slider(min = 0, max = 375, value = 0,
                             size_hint = (0.9, 1),
                             pos_hint = {'x': 0.1, 'y' : 0})
        self.slider.bind(value = self.thresholdUpdate)
        self.lblSliderValue = Label(text = '0',
                                    size_hint = (0.1, 1),
                                    pos_hint = {'x': 0, 'y' : 0})
        self.add_widget(self.slider)
        self.add_widget(self.lblSliderValue)
        
    def thresholdUpdate(self, instance, val):
        try:
            frame_number = int(val)
            if self.slider.min <= frame_number <= self.slider.max:
                th_new = self.thresholdUpdateFnc(frame_number)
                self.lblSliderValue.text = str(th_new)
            else:
                raise Exception('negative threshold value')
        except Exception as exception:
            print(exception)
        return True
    
    def thresholdInc(self):
        if self.slider.value < self.slider.max:
            self.slider.value += 1
            
    def thresholdDec(self):
        if self.slider.value > self.slider.min:
            self.slider.value -= 1
            
    def updateThresholdList(self, thresholdList):
        self.slider.range = (int(min(thresholdList)), int(max(thresholdList)))
        self.thresholdUpdate('dummyInstance', self.slider.value)
            
        