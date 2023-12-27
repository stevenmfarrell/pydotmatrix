import os

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


class Screen:
    def __init__(self):
        # create a 16x16 matrix of black pixels
        self.pixels = [[Color(0,0,0) for i in range(16)] for j in range(16)]

    def set_pixel(self, x, y, color):
        self.pixels[x][y] = color

    def simulate_render(self):
        # clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')

        # print the matrix with boxes of the correct color
        for row in self.pixels:
            for pixel in row:
                print(f"\033[48;2;{pixel.r};{pixel.g};{pixel.b}m  \033[0m", end="")
            print()


if __name__ == "__main__":
    screen = Screen()

    # set the top left pixel to red
    screen.set_pixel(0, 0, Color(255, 0, 0))

    # set the bottom right pixel to green
    screen.set_pixel(15, 15, Color(0, 255, 0))

    # set the bottom left pixel to blue
    screen.set_pixel(0, 15, Color(0, 0, 255))

    # set the top right pixel to yellow
    screen.set_pixel(15, 0, Color(255, 255, 0))

    # render the screen
    screen.simulate_render()





