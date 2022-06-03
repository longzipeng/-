"""
@Project ：pythonGame 
@File    ：stars
@Describe：
@Author  ：KlNon
@Date    ：2022/5/31 16:29 
"""
import pygame
from pygame.sprite import Sprite


class Stars(Sprite):
    """表示星星,预计为给飞船加BUFF的"""

    def __init__(self, ai_game):
        """初始化星星并设置其起始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.star_direction = self.settings.star_direction

        # 加载星星图像并设置其rect属性
        self.image = pygame.image.load('images/star.png')
        self.rect = self.image.get_rect()

        # 每个星星最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 储存星星的精确位置
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def check_edges(self):
        """如果星星位于屏幕边缘,就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.top <= 0 or self.rect.bottom >= screen_rect.bottom:
            return True

    def change_rect(self, star_x, star_y):
        """改变星星的位置"""
        self.x = star_x
        self.y = star_y

    def update(self):
        """向下或向上移动星星"""
        self.y += (self.settings.star_speed * self.star_direction)
        self.x -= self.settings.star_drop_speed
        self.rect.x = self.x
        self.rect.y = self.y
