import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.animation as animation

# Animation used in A2 Physics, Simple Harmonic Motion lesson.  Goal was to show
# how a simple harmonic oscillator (mass-spring system) is similar to a bead on 
# a hoop and the connections between the two.  Also, shows the PE and KE of the 
# system.  

# Modified from the Matplotlib Animation Examples
# http://matplotlib.org/examples/animation/subplots.html

# Clinton H. Durney
# September 15, 2014

# This example uses subclassing, but there is no reason that the proper function
# couldn't be set up and then use FuncAnimation. The code is long, but not
# really complex. The length is due solely to the fact that there are a total
# of 9 lines that need to be changed for the animation as well as 3 subplots
# that need initial set up.


n = 4           
m = 1.0             # mass of spring in kg 
k = 1.0             # spring constant in Nm
w = np.sqrt(k/m)    # angular velocity 

class SubplotAnimation(animation.TimedAnimation):
    def __init__(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(2, 2, 2)
        ax3 = fig.add_subplot(2, 2, 4)

        self.t = np.linspace(0, n*np.pi, 201)
        self.x = np.cos(w*self.t)
        self.y = np.sin(w*self.t)

        ax1.set_xlabel('x')
        ax1.set_ylabel('y')
        ax1.grid()
        self.line1 = Line2D([], [], color='black')
        self.line1e = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        self.mass = Line2D([],[], color='blue', marker = 'o', markeredgecolor='b')
        self.spring = Line2D([],[], color='black')

        ax1.add_line(self.line1)
        ax1.add_line(self.line1e)
        ax1.add_line(self.mass)
        ax1.add_line(self.spring)

        ax1.set_xlim(-2, 2)
        ax1.set_ylim(-2, 2)
        ax1.set_aspect('equal', 'datalim')

        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Potential Energy (J)')
        self.line2 = Line2D([], [], color='black')
        self.line2a = Line2D([], [], color='red', linewidth=2)
        self.line2e = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        ax2.add_line(self.line2)
        ax2.add_line(self.line2a)
        ax2.add_line(self.line2e)
        ax2.set_xlim(0, n*np.pi)
        ax2.set_ylim(0, np.amax(0.5 * k * np.power(self.x,2)))

        ax3.set_xlabel('Time (s)')
        ax3.set_ylabel('Kinetic Energy (J)')
        self.line3 = Line2D([], [], color='black')
        self.line3a = Line2D([], [], color='red', linewidth=2)
        self.line3e = Line2D([], [], color='red', marker='o', markeredgecolor='r')
        ax3.add_line(self.line3)
        ax3.add_line(self.line3a)
        ax3.add_line(self.line3e)
        ax3.set_xlim(0, n*np.pi)
        ax3.set_ylim(0, np.amax(0.5 * m * w * w * np.power(self.y,2)))

        animation.TimedAnimation.__init__(self, fig, interval=50, blit=True)

    def _draw_frame(self, framedata):
        i = framedata
        head = i - 1
        head_len = 10
        head_slice = (self.t > self.t[i] - 1.0) & (self.t < self.t[i])

        self.line1.set_data(self.x[:i], self.y[:i])
        self.line1e.set_data(self.x[head], self.y[head])
        self.mass.set_data(self.x[head],0)
        self.spring.set_data([-2,self.x[head]],[0,0])

        self.line2.set_data(self.t[:i], 0.5 * k * np.power(self.x[:i],2))
        self.line2a.set_data(self.t[head_slice], 0.5 * k * np.power(self.x[head_slice],2))
        self.line2e.set_data(self.t[head], 0.5 * k * np.power(self.x[head],2))

        self.line3.set_data(self.t[:i], 0.5 * m * w*w * np.power(self.y[:i],2))
        self.line3a.set_data(self.t[head_slice], 0.5 * m * w*w * np.power(self.y[head_slice],2))
        self.line3e.set_data(self.t[head], 0.5 * m  * w*w * np.power(self.y[head],2))

        self._drawn_artists = [self.line1, self.line1e, self.mass, self.spring,
            self.line2, self.line2a, self.line2e,
            self.line3, self.line3a, self.line3e]

    def new_frame_seq(self):
        return iter(range(self.t.size))

    def _init_draw(self):
        lines =  [self.line1, self.line1e, self.mass, self.spring,
            self.line2, self.line2a, self.line2e,
            self.line3, self.line3a, self.line3e]
        for l in lines:
            l.set_data([], [])

ani = SubplotAnimation()
#ani.save('test_sub.mp4')
plt.show()
