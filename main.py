from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
# from kivy.base import EventLoop
# import kivy.core.text

# ///////////////////////////////

import cv2
from imutils import face_utils
import numpy as np
import imutils
import dlib


Builder.load_file('camera.kv')

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

class KivyCamera(Image):
    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = None

    def start(self, capture, fps = 30):
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule_interval(self.update)
        self.capture = None

    def update(self, dt):
        return_value, frame = self.capture.read()
        if return_value:
            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]

            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()

            global detector
            global predictor

            frame = imutils.resize(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            rects = detector(gray, 1)
            for (i, rect) in enumerate(rects):
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                output = face_utils.visualize_facial_landmarks(frame, shape)
                texture.blit_buffer(output.tobytes(), colorfmt='bgr')

            # texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()

capture = None

class AppHome(BoxLayout):
    def init_home(self):
        pass

    def dostart(self, *largs):
        if(self.ids.button_start.text == "Start"):
            self.ids.button_start.text = "Stop"
            global capture
            capture = cv2.VideoCapture(0)
            self.ids.app_cam.start(capture)
        else:
            self.ids.button_start.text = "Start"
            global capture
            if capture != None:
                capture.release()
                capture = None

    def doexit(self):
        global capture
        if capture != None:
            capture.release()
            capture = None
            
        # EventLoop.close()

        App.get_running_app().stop()
        Window.close()


class CamApp(App):
    def build(self):
        Window.clearcolor = (.4,.4,.4,1)
        Window.size = (400, 300)
        homeWin = AppHome()
        homeWin.init_home()
        return homeWin

    def on_stop(self):
        global capture
        if capture != None:
            capture.release()
            capture = None

if __name__ == '__main__':
    CamApp().run()
