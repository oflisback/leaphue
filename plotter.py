from matplotlib import pyplot as plt
from matplotlib import animation
import numpy as np


class Plotter:
    def __init__(self, frame_listener):
        def plot_init():
            for line in self.lines:
                line.set_data([], [])
            return self.lines

        def animate(i):
            x = np.linspace(0, 2, 1000)
            for i, y_values in enumerate(frame_listener.get_angle_data()):
                self.lines[i].set_data(x, list(y_values))
            return self.lines

        self.frame_listener = frame_listener
        fig = plt.figure()
        ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
        self.lines = [ax.plot([], [], lw=2)[0] for j in range(4)]

        # For some reason we must store the return value somewhere, otherwise it doesn't work!
        _ = animation.FuncAnimation(fig, animate, init_func=plot_init, frames=200, interval=20, blit=True)

        plt.show()
