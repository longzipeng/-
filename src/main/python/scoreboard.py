"""
@Project ：pythonGame 
@File    ：scoreboard
@Describe：
@Author  ：KlNon
@Date    ：2022/5/31 13:11 
"""
import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """显示得分信息的类"""

    def __init__(self, ai_game):
        """初始化显示得分涉及的属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 显示得分信息时使用的字体设置
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont(None, 48)
        # 准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()
        self.prep_kill()

    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """在屏幕上显示得分,等级和剩下飞船数"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.super_image, self.super_rect)
        # 绘制飞船
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        """检查是否诞生了新的最高得分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """将等级转换为渲染的图像"""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.settings.bg_color)

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还余下多少艘飞船"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_kill(self):
        """重置超级模式击杀数,并且将超级模式转换为渲染的图像"""
        if self.stats.super_mode:
            super_str = 'ON'
        else:
            super_str = 'OFF'
        self.super_image = self.font.render(
            super_str + " : " + str(self.settings.star_kill_number - self.stats.kill_count), True, self.text_color,
            self.settings.bg_color)
        self.super_rect = self.super_image.get_rect()
        self.super_rect.right = self.level_rect.right
        self.super_rect.top = self.level_rect.bottom + 10

    def check_kill(self):
        """检查是否达到相应击杀数,取消超级状态"""
        if self.stats.super_mode and self.stats.kill_count >= self.settings.star_kill_number:
            self.settings.bullet_height = 3
            self.stats.kill_count = 0
            self.stats.super_mode = False
            self.settings.star_throw_enemy = False
            self.prep_kill()
