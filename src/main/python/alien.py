"""
@Project ：pythonGame 
@File    ：alien
@Describe：
@Author  ：KlNon
@Date    ：2022/5/30 12:09 
"""

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类."""

    def __init__(self, ai_game):
        """初始化外星人并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #          加载外星人图像并设置其rect属性.
        self.image = pygame.image.load('images/alienLeft.bmp')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 储存外星人的精确竖直位置
        self.y = float(self.rect.y)

    def check_edges(self):
        """如果外星人位于屏幕边缘,就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.top <= 0 or self.rect.bottom >= screen_rect.bottom:
            return True

    def update(self):
        """向下或向上移动外星人"""
        self.y += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.y = self.y
