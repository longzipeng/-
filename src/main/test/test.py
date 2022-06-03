"""
@Project ：pythonGame 
@File    ：test
@Describe：
@Author  ：KlNon
@Date    ：2022/6/1 16:11 
"""

import pygame

from pymouse import *
from pykeyboard import *


class Test:
    def __init__(self):
        self.m = PyMouse()  # 建立鼠标对象
        self.k = PyKeyboard()  # 建立键盘对象

    def test(self):
        self.m.click(979, 533)
        self.k.tap_key('a')


if __name__ == "__main__":
    keyboard = PyKeyboard()
    keyboard.press_key('Q')
    keyboard.release_key('Q')
