import argparse
import datetime
import math
import random
import turtle

from PIL import Image


class Spiro:
    # constructor
    def __init__(self, xc, yc, col, R, r, l):

        # create own turtle 构造一个新的turtle对象
        self.t = turtle.Turtle()
        # set cursor shape
        # 设置光标形状：“arrow”, “turtle”, “circle”, “square”, “triangle”, “classic”
        self.t.shape('arrow')
        # set step in degrees
        # 将参数绘图角度的增量设置为5度
        self.step = 5
        # set drawing complete flag
        self.drawingComplete = False

        # set parameters
        self.setparams(xc, yc, col, R, r, l)
        # initiatize drawing
        self.restart()

    # set the parameters 帮助初始化Spiro对象
    def setparams(self, xc, yc, col, R, r, l):
        # spirograph parameters

        # 曲线的中心坐标
        self.xc = xc
        self.yc = yc;

        # 将每个圆的半径(R和r)转换为整数并保存这些值
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col

        # reduce r/R to smallest from by dividing with GCD
        # 用Python模块fractions内置的gcd()方法来计算半径的GCD
        # 用来确定曲线的周期性
        gcdVal = math.gcd(self.r, self.R)
        self.nRot = self.r // gcdVal

        # get ratio of radii
        self.k = r / float(R)
        # set color
        self.t.color(*col)
        # current angle
        # 保存当前的角度，用来创建动画
        self.a = 0

    # restart()方法重置Spiro对象的绘制参数,让它准备好重画
    def restart(self):
        # set flag 用来确定绘图是否已经完成
        self.drawingComplete = False
        # show turtle 显示光标，以防它被隐藏
        self.t.showturtle()
        # go to first point 提起笔
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        # 计算角度设为0时的x和y坐标，以获得曲线的起点
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))
        #  完成
        self.t.setpos(self.xc + x, self.yc + y)
        # 落笔
        self.t.down()

    # draw the whole thing
    def draw(self):
        # draw rest of points
        R, k, l = self.R, self.k, self.l
        # 迭代遍历参数i的完整范围，它以度表示，是360乘以nRot。
        for i in range(0, 360 * self.nRot + 1, self.step):
            a = math.radians(i)
            # 计算参数i的每个值对应的X和Y坐标
            x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
            y = R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))
            self.t.setpos(self.xc + x, self.yc + y)
        # done - hide turtle
        self.t.hideturtle()

    # update() 方法展示了一段一段绘制曲线来创建动画时所使用的绘图方法
    # update by one step
    def update(self):
        # skip if done
        if self.drawingComplete:
            return
            # increment angle
        self.a += self.step
        # draw step
        R, k, l = self.R, self.k, self.l
        # set angle
        a = math.radians(self.a)
        x = self.R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = self.R * ((1 - k) * math.sin(a) - l * k * math.sin((1 - k) * a / k))
        self.t.setpos(self.xc + x, self.yc + y);
        # check if drawing is complete and set flag
        if self.a >= 360 * self.nRot:
            self.drawingComplete = True
            # done - hide turtle
            self.t.hideturtle()

    # clear everything
    def clear(self):
        self.t.clear()


# A class for animating spirographs
class SpiroAnimator:
    # constructor
    def __init__(self, N):
        # timer value in milliseconds
        self.deltaT = 10  # 将deltaT设置为10，这是以毫秒为单位的时间间隔，将用于定时器
        # get window dimensions
        self.width = turtle.window_width()
        self.height = turtle.window_width()
        # create spiro objects
        self.spiros = []
        for i in range(N):
            # generate random parameters
            rparams = self.genRandomParams()
            # set spire params
            # 创建一个新的Spiro对象，并将它添加到Spiro对象的列表中
            # 这里的rparams是一个元组，需要传入到Spiro构造函数
            # 但是，构造函数需要一个参数列表，所以用Python的*运算符将元组转换为参数列表
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
        # call timer
        # turtle.ontimer()方法每隔DeltaT毫秒调用update()。
        turtle.ontimer(self.update, self.deltaT)

    # restart sprio drawing
    def restart(self):
        for spiro in self.spiros:
            # clear
            spiro.clear()
            # generate random parameters
            rparams = self.genRandomParams()
            # set spiro params
            spiro.setparams(*rparams)
            # restart drawing
            spiro.restart()

    # generate random parameters
    def genRandomParams(self):
        width, heigh = self.width, self.height
        # 将R设置为50至窗口短边一半长度的随机整数
        R = random.randint(50, min(width, heigh) // 2)
        # 将r设置为R的10%至90%之间
        r = random.randint(10, 9 * R // 10)
        # 将l设置为0.1至0.9之间的随机小数。
        l = random.uniform(0.1, 0.9)
        # 在屏幕内随机选择x和y坐标，选择屏幕上的一个随机点作为螺线的中心
        xc = random.randint(-width // 2, width // 2)
        yc = random.randint(-heigh // 2, heigh // 2)
        # 随机设置为红、绿和蓝颜色的成分，为曲线指定随机的颜色
        col = (random.random(),
               random.random(),
               random.random())
        # 所有计算的参数作为一个元组返回
        return (xc, yc, col, R, r, l)

    # update()方法 由定时器调用，以动画的形式更新所有的Spiro对象
    def update(self):
        # update all spiros
        nComplete = 0
        for spiro in self.spiros:
            # update
            spiro.update()
            # count completed spiros
            if spiro.drawingComplete:
                nComplete += 1
        # restart if all spiros are complete
        if nComplete == len(self.spiros):
            self.restart()
        # call timer
        turtle.ontimer(self.update, self.deltaT)

    # toggle turtle cursor on and off
    # 打开或者关闭光标
    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.invisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()

    # 保存曲线,将绘制保存为PNG图像文件


def saveDrawing():
    # hide turtle
    turtle.hideturtle()
    # generate unique file name
    dateStr = (datetime.now()).strftime()
    fileName = 'spiro-' + dateStr
    print("saving drawing to %s.esp/png" % fileName)
    # get tkinter canvas
    canvas = turtle.getcanvas()
    canvas.postscript(file=fileName + '.eps')
    # use Pillow module to convert to the postsrcipt image file to PNG
    img = Image.open(fileName + ".eps")
    img.save(fileName + ".png", "png")
    # show the turtle cursor
    turtle.showturtle()


def main():
    # use sys.argv if needed
    print('generating spirograph..')
    descStr = """This program draws spirographs using the Turtle module. 
    When run with no arguments, this program draws random spirographs.
    
    Terminology:

    R: radius of outer circle.
    r: radius of inner circle.
    l: ratio of hole distance to r.
    """
    parser = argparse.ArgumentParser(description=descStr)

    # add expected arguments
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
                        help="The three arguments in sparams: R, r, l.")

    # parse args
    args = parser.parse_args()
    # set to 80% screen width
    # 用setup()将绘图窗口的宽度设置为屏幕宽度的80%
    turtle.setup(width=0.5)

    # set cursor shape 设置光标形状
    turtle.shape('turtle')

    # set title 设置程序启动窗口的标题
    turtle.title("Spirographs!")

    # add key handler for saving images
    # 利用 onKey和saveDrawing,在按下S时保存图画
    turtle.onkey(saveDrawing, 's')

    # start listening 调用listen() 让窗口监听用户事件
    turtle.listen()

    # hide main turtle cursor，隐藏光标
    turtle.hideturtle()

    # check args and draw
    # 检查是否有参数赋值给sparams，如果有，就从字符串中提取他们，
    # 用"列表解析"将他们转换成浮点数
    # 列表解析是一种python结构 如 a=[2* x for x in range(1,5)] 表示创造前四个偶数的列表
    if args.sparams:
        print("有参数")
        print(args)
        params = [float(x) for x in args.sparams]
        for p in params:
            print(p)
        # draw spirograph with given parameters
        # black by default
        col = (0.0, 0.0, 0.0)
        # 利用提取的参数来构造Spiro对象
        # 利用python的*运算符，它将列表转换为参数
        spiro = Spiro(0, 0, col, *params)
        # 调用draw() 绘制螺线
        spiro.draw()
    else:
        print("没有参数")
        # 如果命令行上没有指定参数，就进入随机模式。
        # create animator object，
        # 创建一个SpiroAnimator对象，向它传入参数4，
        # 告诉它创建4福图画
        spiroAnim = SpiroAnimator(4)
        # add key handler to toggle turtle cursor
        # 利用onkey() 来捕捉按键T，可以用来切换光标
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        # add key handler to restart animation
        # 处理空格键，用来重新启动动画
        turtle.onkey(spiroAnim.restart, "space")

    # start turtle main loop 调用mainloop()告诉tkinter窗口保持打开，监听事件
    turtle.mainloop()


# call main

if __name__ == '__main__':
    main()
