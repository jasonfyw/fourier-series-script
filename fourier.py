import numpy as np
import turtle






def integrate(a, b, f, dx):
    # return np.sum(f(np.arange(a, b, dx)) * dx)

    total = 0
    for x in np.arange(a, b, dx):
        total += f(x) * dx

    return total





def compute_constant(n, f_vals):
    # n_t = f(t) e^(n2πit) 
    n_t = lambda t: f_vals[int(t * (len(f_vals) - 1))] * np.exp(n * 2j * np.pi * t)

    return integrate(0, 1, n_t, 0.0001)



class Canvas():
    def __init__(self):
        self.t = turtle.Turtle(visible = False)
        self.canvas = turtle.getcanvas()
        self.screen = turtle.Screen()
        turtle.hideturtle()

        
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen.setup(self.WIDTH, self.HEIGHT) 
        self.screen.setworldcoordinates(-self.WIDTH / 2, -self.HEIGHT / 2, self.WIDTH / 2, self.HEIGHT / 2)


        turtle.colormode(255)
        turtle.pencolor('black')
        turtle.tracer(0)
        self.t.speed(0)

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

        self.function = [a + b * 1j for a, b in self.function]

        self.draw_fourier_series()


    """
    Computing the Fourier series
    """

    def compute_fourier_series(self, n_min, n_max):
        self.constants = {}

        for n in range(n_min, n_max + 1):
            self.constants[n] = compute_constant(n, self.function)

            
        self.f = lambda t: sum([c * np.exp(n * 2j * np.pi * t) for n, c in self.constants.items()])

    def draw_fourier_series(self):
        n = 5
        self.compute_fourier_series(-n, n)

        self.t.up()
        turtle.tracer(10)
        self.t.pencolor('red')

        # repeat animation three times
        for i in range(3):
            for t in np.arange(0, 1 + self.step, self.step):
                val = self.f(t)
                x, y = val.real, val.imag

                self.t.goto(x, y)
                self.t.down()






if __name__ == "__main__":
    c = Canvas()