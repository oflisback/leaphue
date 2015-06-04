from phue import Bridge
from threading import Thread
import time
from rgb_cie import ColorHelper
import numpy as np

class HueController:

    LEFT_LAMP_NBR = 1
    RIGHT_LAMP_NBR = 3
    BRIDGE_IP = '192.168.0.243'

    def __init__(self, frame_listener):
        def lamp_controller():
            while True:
                time.sleep(0.1)

                if self.frame_listener.get_confidence() > 0.1:
                    hand_angle = self.frame_listener.get_hand_angle()
                    prev_lamp = self.current_lamp
                    if self.current_lamp == self.LEFT_LAMP_NBR and hand_angle > np.pi/2.0 + np.pi/8.0:
                        self.current_lamp = self.RIGHT_LAMP_NBR
                    elif self.current_lamp == self.RIGHT_LAMP_NBR and hand_angle < np.pi/2.0 - np.pi/8.0:
                        self.current_lamp = self.LEFT_LAMP_NBR

                    if prev_lamp != self.current_lamp:
                        xy = b.get_light(prev_lamp, 'xy')
                        b.set_light(prev_lamp, 'on', False)
                        b.set_light(self.current_lamp, 'on', True)
                        b.set_light(self.current_lamp, 'xy', xy)

                bri = self.get_current_brightness()
                lamp_on = b.get_light(self.current_lamp, 'on')
                if bri == 0:
                    if lamp_on:
                        b.set_light(self.current_lamp, 'on', False)
                else:
                    if not lamp_on:
                        b.set_light(self.current_lamp, 'on', True)
                    b.set_light(self.current_lamp, 'bri', bri)

                new_finger_down = self.frame_listener.pop_new_finger_down_if_any()
                if not new_finger_down is None:
                    b.lights[self.current_lamp - 1].xy = ColorHelper().getXYPointFromRGB(*self.colors[new_finger_down])

        self.current_lamp = self.RIGHT_LAMP_NBR

        self.frame_listener = frame_listener
        b = Bridge(self.BRIDGE_IP)
        b.connect()
        b.set_light(self.LEFT_LAMP_NBR, 'on', False)
        b.set_light(self.RIGHT_LAMP_NBR, 'on', False)
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
        Thread(target=lamp_controller).start()

    def get_current_brightness(self):
        # roughly go between ranges [1, 0] to [0, 255]
        angle = self.frame_listener.get_average_angle()
        if self.frame_listener.get_confidence() == 0 or angle is None:
            return 0
        return int(min(255, 255.0*min(1.0, max(0.0, -angle + 0.5))))

