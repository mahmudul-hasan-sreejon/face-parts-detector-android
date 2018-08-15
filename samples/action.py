import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class Controller(BoxLayout):
    def __init__(self):
        super(Controller, self).__init__()

    def btn_clk(self):
        self.lbl.text = "You have been pressed"


class ActionApp(App):

    def build(self):
        return Controller()


myApp = ActionApp()

myApp.run()