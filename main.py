from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from kivy.clock import Clock
from kivy.graphics.texture import Texture


from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2


# detector = dlib.get_frontal_face_detector()
# predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


Builder.load_file('camera.kv')

class OpencvCamera(BoxLayout):
    def __init__(self, capture, fps, **kwargs):
        super(OpencvCamera, self).__init__(**kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, fps)

    def btn_clk(self):
        if self.ids['camera'].play == True:
            self.ids['button'].text = "Play"
            self.ids['camera'].play = False
        else:
            self.ids['button'].text = "Pause"
            self.ids['camera'].play = True

    def update(self):
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

        ret, image = self.capture.read()
        if ret is True:
            image = imutils.resize(image, width = 500)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            rects = detector(gray, 1)
            for (i, rect) in enumerate(rects):
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

            output = face_utils.visualize_facial_landmarks(image, shape)

            # convert it to texture
            buf1 = cv2.flip(output, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size = (output.shape[1], output.shape[0]), colorfmt = 'bgr')
            image_texture.blit_buffer(buf, colorfmt = 'bgr', bufferfmt = 'ubyte')
            # display image from the texture
            self.texture = image_texture


            # cv2.imshow("Image", output)


class RunCamera(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = OpencvCamera(capture=self.capture, fps=30)
        return self.my_camera

    def on_stop(self):
        self.capture.release()


if __name__ == '__main__':
    RunCamera().run()
