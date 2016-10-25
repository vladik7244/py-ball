#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from threading import Timer

WIN_WIDTH = 1000
WIN_HEIGHT = 500
RADIUS = 10

# def mouse_handler(point, is_right):
#     if not is_right:
#         bubble = Bubble(point, False)
#         circle_list.append(bubble)
#         bubble.add_force(Point(0, 0.1))
#         bubble.add_impulse(Point(1, 1))
#     else:
#         bubble = Bubble(point, True)
#         circle_list.append(bubble)


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = float(x)
        self.y = float(y)


def cos_vec(a, b):
    return (a.x * b.x + a.y * b.y) / (np.sqrt(a.x ** 2 + a.y ** 2) * np.sqrt(b.x ** 2 + b.y ** 2) + 0.00001)

colors = ['#ff0000', '#ffff00', '#ff00ff', '#00ffff', '#0000ff', '#00ff00']


class Bubble:
    def __init__(self, point, color = 0):
        self.X = point.x
        self.Y = point.y
        self.color = colors[color]
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
        self.speed.x = min(max(self.speed.x, -15), 15)
        self.speed.y = min(max(self.speed.y, -15), 15)
        self.X += self.speed.x
        self.Y += self.speed.y

    def add_force(self, force):
        self.forces.append(force)

    def remove_force(self, force):
        self.forces.remove(force)

    def add_impulse(self, impulse):
        self.impulses.append(impulse)

    def is_collide(self, other):
        if other == self:
            return False
        my_radius = RADIUS  # TODO
        other_radius = RADIUS  # TODO
        distance = np.sqrt((self.X - other.X) ** 2 + (self.Y - other.Y) ** 2)
        if distance < other_radius + my_radius and (other not in self.collisions):
            self.collisions.append(other)
            return True
        else:
            if other in self.collisions:
                self.collisions.remove(other)
                return False

    def is_outside(self, width, height):
        if self.X > width or self.X < 0 or self.Y < 0 or self.Y > height:
            return True
        return False

    def get_normal_vector(self, other):
        p2x = other.X - self.X
        p2y = other.Y - self.Y
        d = np.sqrt(p2x ** 2 + p2y ** 2)
        x = - p2x / d
        y = - p2y / d
        return Point(x, y)

    def draw(self, qp):
        c = QPoint(int(self.X), int(self.Y))
        qp.setBrush(QColor(self.color))
        qp.drawEllipse(c, RADIUS, RADIUS)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.circle_list = []
        self.setUpdatesEnabled(True)
        # for i in range(5):
        #     x = np.random.randint(0, WIN_WIDTH)
        #     y = np.random.randint(0, WIN_HEIGHT)
        #     dx = np.random.randint(-5, 5)
        #     dy = np.random.randint(-5, 5)
        #     bubble = Bubble(Point(x, y), True)
        #     bubble.add_force(Point(0, 0.4))
        #     bubble.add_impulse(Point(dx, dy))
        #     self.circle_list.append(bubble)
        bubble1 = Bubble(Point(100, 100), 0)
        bubble2 = Bubble(Point(100, 400), 1)
        bubble2.add_impulse(Point(0, -5))
        self.circle_list.append(bubble1)
        self.circle_list.append(bubble2)
        #     self.circle_list.append(bubble)
        bubble3 = Bubble(Point(100, 50), 2)
        bubble4 = Bubble(Point(400, 50), 3)
        bubble3.add_impulse(Point(5, 0))
        self.circle_list.append(bubble3)
        self.circle_list.append(bubble4)

        bubble5 = Bubble(Point(150, 150), 4)
        bubble6 = Bubble(Point(350, 350), 5)
        bubble5.add_impulse(Point(5, 5))
        self.circle_list.append(bubble5)
        self.circle_list.append(bubble6)

        bubble7 = Bubble(Point(200, 200), 4)
        bubble8 = Bubble(Point(400, 219), 5)
        bubble7.add_impulse(Point(5, 0))
        self.circle_list.append(bubble7)
        self.circle_list.append(bubble8)
        self.init_ui()

    def timeout(self):
        self.update()
        t = Timer(0.04, self.timeout)
        t.start()

    def init_ui(self):
        self.setGeometry(300, 300, WIN_WIDTH, WIN_HEIGHT)
        self.setWindowTitle('Points')
        self.show()
        self.timeout()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_points(qp)
        qp.end()

    def draw_points(self, qp):
        qp.setPen(Qt.black)
        n = len(self.circle_list)
        for i in range(n):
            circle = self.circle_list[i]
            # circle.add_impulse(Point(-circle.speed.x / 20, -circle.speed.y / 20))  # friction
            if circle.X > WIN_WIDTH:
                s = abs(circle.speed.x)
                circle.speed.x *= -1
                circle.add_impulse(Point(0 * -s / 2, 0))
            if circle.X < 0:
                s = abs(circle.speed.x)
                circle.speed.x *= -1
                circle.add_impulse(Point(0 * s / 2, 0))
            if circle.Y > WIN_HEIGHT - RADIUS:
                s = abs(circle.speed.y)
                circle.speed.y *= -1
                circle.add_impulse(Point(0, 0 * -s / 2))
            if circle.Y < 0:
                s = abs(circle.speed.y)
                circle.speed.y *= -1
                circle.add_impulse(Point(0, 0 * s / 2))
            circle.update()
            for j in range(i, n):
                other = self.circle_list[j]
                if circle.is_collide(other):
                    m_speed = np.sqrt(circle.speed.x ** 2 + circle.speed.y ** 2)
                    o_speed = np.sqrt(other.speed.x ** 2 + other.speed.y ** 2)
                    vec = circle.get_normal_vector(other)
                    s = (m_speed + o_speed) / 2
                    v1 = s # * cos_vec(other.speed, vec)
                    v2 = s # * cos_vec(circle.speed, vec)
                    # circle.X -= vec.x
                    # circle.Y -= vec.y
                    other.add_impulse(Point(-vec.x * v1, -vec.y * v1))
                    circle.add_impulse(Point(vec.x * v2, vec.y * v2))
        for circle in self.circle_list:
            circle.move()
            circle.draw(qp)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

