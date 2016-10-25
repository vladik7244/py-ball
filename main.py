from graphics import *
import random
import time
import numpy as np

WIN_WIDTH = 860
WIN_HEIGHT = 480
win = GraphWin("My Circle", WIN_WIDTH, WIN_HEIGHT)


"""
def nonlin(x, deriv = False):
    if deriv == True: return x*(1-x)
    return 1/(1+np.exp(-x))

x = np.array([[0, 0, 1],
              [0, 1, 1],
              [1, 0, 1],
              [1, 1, 1]])

y = np.array([[0],
              [1],
              [1],
              [0]])

np.random.seed(1)
synapse0 = np.random.random((3, 4)) - 1
synapse1 = np.random.random((4, 1)) - 1

for j in xrange(60000):
    layer0 = x
    layer1 = nonlin(np.dot(layer0, synapse0))
    layer2 = nonlin(np.dot(layer1, synapse1))
    layer2_error = y - layer2
    if j % 10000:
        print("Error: " + str(np.mean(np.abs(layer2_error))))
    layer2_delta = layer2_error * nonlin(layer2, deriv=True)
    layer1_error = layer2_delta.dot(synapse1.T)
    layer1_delta = layer1_error * nonlin(layer1, deriv=True)
    synapse1 += layer1.T.dot(layer2_delta)
    synapse0 += layer0.T.dot(layer1_delta)
print("Outputs: ")
print(layer2)


"""


def main():
    global win

    circle_list = []

    def mouse_handler(point, is_right):
        if not is_right:
            bubble = Bubble(point, False)
            circle_list.append(bubble)
            bubble.add_force(Point(0, 0.1))
            bubble.add_impulse(Point(1, 1))
        else:
            bubble = Bubble(point, True)
            circle_list.append(bubble)

    win.setMouseHandler(mouse_handler)
    while True:
        win.checkMouse()
        for circle in circle_list:
            circle.add_impulse(Point(-circle.speed.x / 100, -circle.speed.y / 100))  # friction
            circle.update()
            for other in circle_list:
                if circle.is_collide(other):
                    m_speed = np.sqrt(circle.speed.x ** 2 + circle.speed.y ** 2)
                    o_speed = np.sqrt(other.speed.x ** 2 + other.speed.y ** 2)
                    v = (m_speed+o_speed/2)/2
                    vec = circle.get_normal_vector(other)
                    circle.add_impulse(Point(vec.x * v, vec.y * v))
        for circle in circle_list:
            circle.move()
            if circle.is_outside(WIN_WIDTH, WIN_HEIGHT):
                circle.destroy()
                circle_list.remove(circle)
        time.sleep(0.02)


class Bubble:
    def __init__(self, point, is_red):
        self.circle = Circle(point, 15)
        if is_red:
            self.circle.setFill('#ff0000')
        else:
            self.circle.setFill('#007722')

        self.circle.draw(win)
        self.forces = []
        self.impulses = []
        self.speed = Point(0, 0)
        self.result_force = Point(0, 0)
        self.collisions = []

    def update(self):
        result_force = Point(0, 0)
        for force in self.forces:
            result_force.x += force.x
            result_force.y += force.y
        for impulse in self.impulses:
            result_force.x += impulse.x
            result_force.y += impulse.y
            self.impulses.remove(impulse)
        self.result_force = result_force

    def move(self):
        self.speed.x += self.result_force.x
        self.speed.y += self.result_force.y
        self.circle.move(self.speed.x, self.speed.y)

    def add_force(self, force):
        self.forces.append(force)

    def remove_force(self, force):
        self.forces.remove(force)

    def add_impulse(self, impulse):
        self.impulses.append(impulse)

    def is_collide(self, other):
        if (other == self):
            return False
        my_radius = self.circle.getRadius()
        other_radius = other.circle.getRadius()
        my_pos = self.circle.getCenter()
        other_pos = other.circle.getCenter()
        distance = np.sqrt((my_pos.x - other_pos.x) ** 2 + (my_pos.y - other_pos.y) ** 2)
        if (distance < other_radius + my_radius) and (other not in self.collisions):
            self.collisions.append(other)
            return True
        else:
            if (other in self.collisions): self.collisions.remove(other)
            return False

    def is_outside(self, width, height):
        my_pos = self.circle.getCenter()
        if my_pos.x > width or my_pos.x < 0 or my_pos.y < 0 or my_pos.y > height:
            return True
        return False

    def destroy(self):
        self.circle.undraw()

    def get_normal_vector(self, other):
        p1 = self.circle.getCenter()
        p2 = other.circle.getCenter()
        p2x = p2.x - p1.x
        p2y = p2.y - p1.y
        d = np.sqrt(p2x ** 2 + p2y ** 2)
        x = - p2x / d
        y = - p2y / d
        return Point(x, y)

main()
