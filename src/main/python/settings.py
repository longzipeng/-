"""
@Project ：pythonGame 
@File    ：settings
@Describe：
@Author  ：KlNon
@Date    ：2022/5/27 21:09 
"""


class Settings:
    """储存游戏<外星人入侵>中所以设置的类"""

    def __init__(self):
        """初始化游戏的静态设置"""
        #         屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        #         飞船设置
        self.ship_speed = 1.05
        self.ship_limit = 3
        #         子弹设置
        self.bullet_speed = 1.5
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (30, 30, 30)
        self.bullets_allowed = 3
        #         外星人设置
        self.alien_speed = 0.15
        self.fleet_drop_speed = 8
        #         fleet_direction 为1表示向右移,为-1表示向左移
        self.fleet_direction = 1

        #     星星设置
        self.star_kill_number = 10
        self.star_speed = 0.3
        self.star_drop_speed = 0.3
        self.star_change_width = 125
        self.star_throw_enemy = False
        # A为100表示分母,B为1表示分子
        self.star_chanceA = 100
        self.star_chanceB = 10

        #         star_fleet_direction 为1表示向右移,为-1表示向左移
        self.star_direction = 1

        #         加快游戏节奏的速度
        self.speedup_scale = 1.1

        #        外星人分数提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

        #     记分
        self.alien_points = 50

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        # self.ship_speed = 1.5
        # self.bullet_speed = 3.0
        # self.alien_speed = 0.15
        # fleet_direction 为1表示向右移,为-1表示向左移
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置和外星人点数"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)
