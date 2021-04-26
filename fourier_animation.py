import pygame
import sys
import numpy as np

from fourier_computation import *


class Canvas():
    def __init__(self):
        self.width, self.height = 800, 800

        pygame.init()

        # initiate pygame screen 
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Fourier series animation')

        self.running = False
        self.dragging = False

        self.draw_circles = True

        # determines number of terms in the Fourier series
        self.n = 20

        self.start()

    # Adjusts origin to the centre of the window
    def centre_coords(self, x, y):
        return x + self.width / 2, -y + self.height / 2

    """
    Event handlers
    """
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            pygame.quit()
            sys.exit()
        # Start dragging
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.inputting_function:
                self.dragging = True
                self.prev_pos = pygame.mouse.get_pos()
        # Finish dragging
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.inputting_function:
                # draw a line connecting the start and end of the user drawing
                start_point = self.function_points[0]
                end_point = self.function_points[-1]
                pygame.draw.line(
                    self.window, 
                    (255, 255, 255), 
                    self.centre_coords(start_point.real, start_point.imag), 
                    self.centre_coords(end_point.real, end_point.imag), 
                    2
                )

                self.dragging = False
                self.inputting_function = False

                # calculate Fourier series based on user-input points
                self.f = compute_fourier_series(self.n, generate_function(self.function_points))
                # initialises list of points plotted out by the Fourier series
                self.fourier_points = []
        # While mouse dragging
        if event.type == pygame.MOUSEMOTION:
            if self.dragging and self.inputting_function:
                # get coordinates of cursor
                x, y = pygame.mouse.get_pos()
                a = x - self.width / 2
                b = -y + self.height / 2

                # convert and stores x, y coords into real/imag components of complex number
                self.function_points.append(a + b * 1j)
                # render line from previous cursor position to current position
                pygame.draw.line(self.window, (255, 255, 255), self.prev_pos, (x, y), 2)

                # update previous line position
                self.prev_pos = (x, y)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_c:
                self.draw_circles = not self.draw_circles


    """
    Animation rendering
    """
    # Plots complex numbers sequentially in a given list
    def plot_points(self, points, colour, width, connect_ends = False):
        # convert complex number to x, y coords of the first point
        x1, y1 = points[0].real, points[0].imag
        # include the starting point at the end if connect_ends is true
        points = points[1:] if not connect_ends else points[1:] + [points[0]]
        for z in points:
            x2, y2 = z.real, z.imag
            pygame.draw.line(
                self.window, 
                colour, 
                self.centre_coords(x1, y1), 
                self.centre_coords(x2, y2), 
                width
            )
            x1, y1 = x2, y2

    # Render each frame 
    def draw_frame(self, t, step):
        """
        Rendering Fourier series points and user-drawn points
        """
        # Plot the original user-drawn function
        self.plot_points(self.function_points, (255, 255, 255), 2, True)

        # calculates the next value of t to be used; overflow to 0 if t ≥ 1
        next_t = t + step if t != 1 else 0

        # get the unsummed Fourier series at t and t+step
        f1 = self.f(t)
        z1 = sum(f1)
        z2 = sum(self.f(next_t))

        # add the new point to the collection of points
        self.fourier_points += [z1, z2]
        # plot all the points generated in the Fourier series
        self.plot_points(self.fourier_points, (255, 0, 0), 1)

        
        """
        Renders lines for each complex number in the Fourier series
        """
        # set starting point to the origin
        lx1, ly1 = 0, 0
        # iterate such that i descends while oscillating between positive and negative
        # e.g.: [-3, 3, -2, 2, -1, 1, 0]
        for i in [((-1) ** (n + 1)) * n // 2 for n in range(self.n, 0, -1)]:
            vector = f1[i]
            # get coords of the next vector in relation to the starting point 
            # this gives the effect of putting every vector end-to-end
            lx2, ly2 = vector.real + lx1, vector.imag + ly1

            # draw the individual vector
            pygame.draw.line(
                self.window, 
                (150, 150, 150), 
                self.centre_coords(lx1, ly1), 
                self.centre_coords(lx2, ly2), 
                1
            )

            if self.draw_circles:
                r = int(np.hypot(lx2-lx1, ly2-ly1))
                pygame.draw.circle(
                    self.window, 
                    (80, 80, 80), 
                    (int(lx1 + self.width / 2), int(-ly1 + self.height / 2)),
                    r,
                    0 if 1 >= r else 1
                )

            lx1, ly1 = lx2, ly2

        return next_t

    """
    Main simulation loop
    """
    def start(self): 
        self.running = True
        # start by inputting function from user
        self.inputting_function = True

        # initialise list of user-input points
        self.function_points = []
        
        t = 0
        step = 0.001

        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            
            # start rendering animation 
            if not self.inputting_function:
                self.window.fill((0, 0, 0))
                t = self.draw_frame(t, step)

            pygame.display.flip()





if __name__ == "__main__":
    canvas = Canvas()
