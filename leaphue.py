# use lillfingret instead of longfingret :)
# keep color when moving to other light

from huecontroller import HueController
from framelistener import FrameListener
from plotter import Plotter
import Leap

frame_listener = FrameListener()
leap_controller = Leap.Controller()
leap_controller.add_listener(frame_listener)

hue_controller = HueController(frame_listener)

plotter = Plotter(frame_listener)

while True:
    pass
