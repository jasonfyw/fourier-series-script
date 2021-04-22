import numpy as np
import turtle





# definite integration
def integrate(a, b, f, dx):
    # return np.sum(f(np.arange(a, b, dx)) * dx)

    total = 0
    for x in np.arange(a, b, dx):
        total += f(x) * dx

    return total



# calculates complex coefficients for each term
def compute_constant(n, f_vals):
    # n_t = f(t) e^(n2πit) 
    n_t = lambda t: f_vals[int(t * (len(f_vals) - 1))] * np.exp(n * 2j * np.pi * t)

    return integrate(0, 1, n_t, 0.0001)



class Canvas():
    def __init__(self):
        self.t = turtle.Turtle(visible = False)
        self.canvas = turtle.getcanvas()
        self.screen = turtle.Screen()

        
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen.setup(self.WIDTH, self.HEIGHT) 
        self.screen.setworldcoordinates(-self.WIDTH / 2, -self.HEIGHT / 2, self.WIDTH / 2, self.HEIGHT / 2)


        turtle.colormode(255)
        turtle.pencolor('black')
        turtle.tracer(0)
        self.t.speed(0)

        turtle.hideturtle()
        self.t.hideturtle()

        self.step = 0.001

        self.input_function()

        turtle.mainloop()


    """
    Function created by user drawing on canvas
    """

    def input_function(self):
        self.function = []

        self.t.up()
        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<ButtonRelease-1>', self.release)
    
    def drag(self, event):
        x, y = event.x - (self.WIDTH / 2), -event.y + (self.HEIGHT / 2)
        self.function.append((x, y))
        self.t.goto(x, y)
        self.t.down()

    def release(self, event):
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')

        self.t.goto(self.function[0])

        # convert coordinate points to complex numbers
        self.function = [a + b * 1j for a, b in self.function]

        # compute and draw the fourier series
        self.draw_fourier_series()


    """
    Computing the Fourier series
    """

    def compute_fourier_series(self, n_min, n_max):
        self.constants = {}

        for n in range(n_min, n_max + 1):
            self.constants[n] = compute_constant(n, self.function)

            
        # self.f = lambda t: sum([c * np.exp(n * 2j * np.pi * t) for n, c in self.constants.items()])
        self.f = lambda t: [c * np.exp(n * 2j * np.pi * t) for n, c in self.constants.items()]

    def draw_fourier_series(self):
        n = 5
        self.compute_fourier_series(-n, n)

        self.t.up()
        turtle.tracer(50)
        self.t.pencolor('red')

        # trace the computed fourier series 10 times while rendering the circles
        for i in range(10):
            for t in np.arange(0, 1 + self.step, self.step):

                values = self.f(t)
                self.t.up()
                self.t.goto(0, 0)

                # for vector in values:
                for i in [0, 1, -1, 2, -2, 3, -3, 4, -4, 5, -5][::-1]: # very janky, hardcoded fix
                    curr_x, curr_y = self.t.pos()
                    vector = values[i]

                    x, y = vector.real, vector.imag
                    self.t.down()
                    self.t.goto(curr_x + x, curr_y + y)

                self.t.clear()





if __name__ == "__main__":
    c = Canvas()