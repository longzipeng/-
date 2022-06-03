"""
@Project ：pythonGame 
@File    ：alien_invasion.py
@Describe：
@Author  ：KlNon
@Date    ：2022/4/28 15:15 
"""
import sys
import time
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard
from stars import Stars
from random import randint
from pymouse import *


class AlienInvasion:
    """
    * @Class     : AlienInvasion 
    * @Describe  : 管理游戏资源和行为的类
    * @Date      : 2022/4/28 15:27 
    """

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # 创建一个用于储存游戏统计信息的实例
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_fleet()

        # 用于单元测试退出游戏
        self.quit_game_flag = False

        # 创建Play按钮
        self.play_button = Button(self, "Play")

        #     设置背景色为浅灰色
        # self.bg_color = (230, 230, 230)

    def run_game(self):
        """开始游戏的主循环"""
        # 读取最高分文件,并渲染其图像
        with open('score/high_score.txt') as f:  # 默认模式为‘r’，只读模式
            contents = f.read()  # 读取文件全部内容
            contents.rstrip()  # rstrip()函数用于删除字符串末的空白
            self.stats.high_score = int(contents)
            self.sb.prep_high_score()

        while not self.quit_game_flag:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._update_stars(False)
            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件"""
        # 监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """响应按键."""
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船
            # self.ship.rect.x += 1
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        #     按Q退出
        elif event.key == pygame.K_q:
            # 存储最高分到文件
            filename = 'score/high_score.txt'
            with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
                f.write(str(self.stats.high_score))
            self.quit_game_flag = True
            time.sleep(1)
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """创建一颗子弹,并将其加入编组bullets中.限制子弹数量"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹."""
        #     更新子弹的位置.
        self.bullets.update()
        #       删除消失的子弹.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.right >= self.settings.screen_width:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""
        #     检查是否有子弹击中了外星人.
        # 如果是,就删除相应的子弹和外星人,第一个True是删除子弹,第二个True是删除外星人
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, not self.settings.star_throw_enemy, True)
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    if self.stats.super_mode:
                        self.stats.kill_count += 1
                        self.sb.prep_kill()
                    if randint(0, self.settings.star_chanceA) < self.settings.star_chanceB:
                        self._create_star(alien.rect.x, alien.rect.y)

                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.sb.check_kill()
        if not self.aliens:
            # 删除现有的子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """创建外星人群"""
        #     创建一个外星人
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # # 计算一行容纳
        # available_space_x = self.settings.screen_width - (2 * alien_width)
        # number_aliens_x = available_space_x // (2 * alien_width)
        #
        # # 计算屏幕可容纳多少行外星人.
        # ship_height = self.ship.rect.height
        # available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        # number_rows = available_space_y // (2 * alien_height)

        # # 创建外星人群
        # for row_number in range(number_rows):
        #     # 创建第一行外星人.
        #     for alien_number in range(number_aliens_x):
        #         self._create_alien(alien_number, row_number)

        # 计算一列容纳
        available_space_y = self.settings.screen_height - (2 * alien_height)
        number_aliens_y = available_space_y // (2 * alien_height)
        # 计算屏幕可容纳多少列外星人
        ship_width = self.ship.rect.width
        available_space_x = (self.settings.screen_width - (3 * alien_width) - ship_width)
        number_lines = available_space_x // (2 * alien_width)

        # 创建外星人群
        for row_number in range(number_lines):
            # 创建第一列外星人.
            for alien_number in range(number_aliens_y):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并将其放在当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.y = alien_height + (2 * alien_height * alien_number)
        alien.rect.y = alien.y
        alien.rect.x = self.settings.screen_width - alien.rect.height - 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """更新外星人群中所有外星人的位置,检查是否有外星人位于屏幕边缘"""
        self._check_fleet_edges()
        self.aliens.update()

        #     检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #     检查是否有外星人到达屏幕底端
        self._check_aliens_left()

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取响应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人左移,并改变它们的方向"""
        for alien in self.aliens.sprites():
            alien.rect.x -= self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """响应飞船被外星人撞到."""
        if self.stats.ships_left > 0:
            #         将ships_left减1
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #         清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            self.stars.empty()

            #         创建一群新的外星人,并将飞船放到屏幕底端的中央
            self._create_fleet()
            self.ship.center_ship()

            #         暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_left(self):
        """检查是否有外星人到达了屏幕左端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.left <= screen_rect.left:
                # 像飞船被撞到一样进行处理
                self._ship_hit()
                break

    def _create_star(self, star_x, star_y):
        """创建一个星星"""
        star = Stars(self)
        star.rect.x = star_x
        star.rect.y = star_y
        star.change_rect(star_x, star_y)
        self.stars.add(star)

    def _update_stars(self, test_super_mode=False):
        """更新单个星星的位置,并检查是否有星星到达屏幕边缘,test_super_mode是测试超级模式"""
        self._check_stars_edges()
        self.stars.update()

        #     检测星星和飞船之间的碰撞
        if pygame.sprite.spritecollide(self.ship, self.stars, True) or test_super_mode:
            self.settings.bullet_height = self.settings.star_change_width
            self.stats.kill_count = 0
            self.stats.super_mode = True
            # 子弹穿过敌人
            self.settings.star_throw_enemy = True
            # 生命小于5的时候奖励命
            if self.stats.ships_left < 5:
                self.stats.ships_left += 1
            self.sb.prep_ships()
            self.sb.prep_kill()

        #     检查是否有星星到达屏幕底端
        self._check_stars_left()

    def _check_stars_left(self):
        """检查是否有星星到达了屏幕左端,是就删除"""
        screen_rect = self.screen.get_rect()
        for star in self.stars.copy():
            if star.rect.left <= screen_rect.left:
                self.stars.remove(star)

    def _check_stars_edges(self):
        """检查星星是否到达屏幕上下,并反弹"""
        for star in self.stars.sprites():
            if star.check_edges():
                # star.rect.x -= self.settings.star_drop_speed
                star.star_direction *= -1

    def _check_play_button(self, mouse_pos, button_clicked=False):
        """在玩家单击Play按钮时开始新游戏"""
        if not button_clicked:
            button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked or not self.stats.game_active:
            # 重置游戏设置
            self.settings.initialize_dynamic_settings()
            # 重置游戏统计信息
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            # 超级模式重置
            self.sb.prep_kill()

            #             清空外星人列表和子弹列表
            self.aliens.empty()
            self.bullets.empty()
            self.stars.empty()

            #             创建一群新的外星人,并让飞船居中
            self._create_fleet()
            self.ship.center_ship()

            #             隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _update_screen(self):
        """更新屏幕上的图像,并切换到新屏幕"""
        # 每次循环的时候都重新绘制屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        self.stars.draw(self.screen)
        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态,就绘制Play按钮
        if not self.stats.game_active:
            self.play_button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
