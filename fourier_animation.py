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

        self.n = 20

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

                self.f = compute_fourier_series(self.n, generate_function(self.function_points))

        if event.type == pygame.MOUSEMOTION:
            if self.dragging and self.inputting_function:
                x, y = pygame.mouse.get_pos()
                a = x - self.width / 2
                b = -y + self.height / 2

                self.function_points.append(a + b * 1j)

                pygame.draw.line(self.window, (255, 255, 255), self.prev_pos, (x, y), 2)

                self.prev_pos = (x, y)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.running = False
                pygame.quit()
                sys.exit()


    def draw_raw_function(self):
        x1, y1 = self.function_points[0].real, self.function_points[0].imag
        points = self.function_points[1:] + [self.function_points[0]]
        for z in points:
            x2, y2 = z.real, z.imag
            pygame.draw.line(
                self.window, 
                (255, 255, 255), 
                self.centre_coords(x1, y1), 
                self.centre_coords(x2, y2), 
                2
            )
            x1, y1 = x2, y2


    def draw_frame(self, t, step):
        self.draw_raw_function()

        next_t = t + step if t != 1 else 0

        f1 = self.f(t)
        z1 = sum(f1)
        x1, y1 = z1.real, z1.imag

        z2 = sum(self.f(next_t))
        x2, y2 = z2.real, z2.imag

        pygame.draw.line(
            self.window,
            (255, 0, 0),
            self.centre_coords(x1, y1),
            self.centre_coords(x2, y2),
            1
        )

        lx1, ly1 = 0, 0
        for i in [((-1) ** (n + 1)) * n // 2 for n in range(self.n, 0, -1)]:
            vector = f1[i]
            lx2, ly2 = vector.real + lx1, vector.imag + ly1

            pygame.draw.line(
                self.window, 
                (150, 150, 150), 
                self.centre_coords(lx1, ly1), 
                self.centre_coords(lx2, ly2), 
                1
            )

            lx1, ly1 = lx2, ly2

        return next_t

    
    def start(self):
        self.running = True
        self.inputting_function = True

        self.function_points = []
        
        t = 0
        step = 0.001

        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            
            if not self.inputting_function:
                self.window.fill((0, 0, 0))
                t = self.draw_frame(t, step)

            pygame.display.flip()





if __name__ == "__main__":
    canvas = Canvas()
