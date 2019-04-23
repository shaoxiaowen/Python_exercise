import math
import turtle


def drawCircleTurtle(x, y, r):
    # move to the start of circle
    turtle.up()
    turtle.setpos(x + r, y)
    turtle.down()

    # draw the circle
    for i in range(0, 365, 5):
        a = math.radians(i)
        turtle.setpos(x + r * math.cos(a), y + r * math.sin(a))
    # drawCircleTurtle(100, 100, 50)
    # turtle.mainloop()


def drawSpiralTurtle(x, y, r):
    # move to the start of circle
    turtle.up()
    turtle.setpos(x + r, y)
    turtle.down()

    # draw spiral
    for i in range(0, 360 * 10, 5):
        a = math.radians(i)
        x = r * math.cos(a) * math.exp(0.05 * a)
        y = r * math.sin(a) * math.exp(0.05 * a)
        turtle.setpos(x, y)


if __name__ == '__main__':
    # drawCircleTurtle(100, 100, 10)
    drawSpiralTurtle(0,0,5)
