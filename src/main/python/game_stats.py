"""
@Project ：pythonGame 
@File    ：game_stats
@Describe：
@Author  ：KlNon
@Date    ：2022/5/30 14:32 
"""


class GameStats:
    """跟踪游戏的统计信息."""

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.ships_left = 3
        self.settings = ai_game.settings
        self.reset_stats()

        self.game_active = False

        #     任何情况下都不应重置最高分
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.kill_count = 0
        self.super_mode = False
