"""
@Project ：pythonGame 
@File    ：ship
@Describe：
@Author  ：KlNon
@Date    ：2022/5/27 21:34 
"""

import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """管理飞船的类"""

    def __init__(self, ai_game) -> None:
        super().__init__()
        """初始化飞船并设置其初始位置"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #         加载飞船图像并获取起外接矩形.
        self.image = pygame.image.load('images/shipLeft.png')
        self.rect = self.image.get_rect()

        #         对于每艘新飞船,都将其放在屏幕左中位置.
        self.rect.midleft = self.screen_rect.midleft

        # 在飞船的属性x中储存小数值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

        #     子弹设置
        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

    def update(self):
        """根据移动标志调整飞船的位置."""
        # 更新飞船而不是rect对象的值
        if self.moving_right and self.rect.right < 200:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def center_ship(self):
        """让飞船居中"""
        self.rect.midleft = self.screen_rect.midleft
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def blitme(self):
        """在指定位置绘制飞船."""
        self.screen.blit(self.image, self.rect)
