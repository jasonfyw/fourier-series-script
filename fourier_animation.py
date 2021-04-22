import pygame
import sys
import numpy as np

from fourier_computation import *


class Canvas():
    def __init__(self):
        self.width, self.height = 800, 800

        pygame.init()

        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Fourier series animation')

        self.running = False
        self.dragging = False

        self.start()

    def centre_coords(self, x, y):
        return x + self.width / 2, -y + self.height / 2


    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.inputting_function:
                self.dragging = True
                self.prev_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.inputting_function:
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

        if event.type == pygame.MOUSEMOTION:
            if self.dragging and self.inputting_function:
                x, y = pygame.mouse.get_pos()
                a = x - self.width / 2
                b = -y + self.height / 2

                self.function_points.append(a + b * 1j)

                pygame.draw.line(self.window, (255, 255, 255), self.prev_pos, (x, y), 2)

                self.prev_pos = (x, y)


    def draw_fourier_series(self, n):
        f = compute_fourier_series(n, generate_function(self.function_points))


        step = 0.001

        z0 = f(0)
        x1, y1 = z0.real, z0.imag

        for t in np.arange(step, 1 + step, step):
            z = f(t)
            x2, y2 = z.real, z.imag

            pygame.draw.line(self.window, (255, 0, 0), self.centre_coords(x1, y1), self.centre_coords(x2, y2), 1)

            x1, y1 = x2, y2

    
    def start(self):
        self.running = True
        self.inputting_function = True

        self.function_points = []

        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            
            if not self.inputting_function:
                self.draw_fourier_series(20)


            pygame.display.flip()





if __name__ == "__main__":
    canvas = Canvas()
