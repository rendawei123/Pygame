#!/usr/bin/python
# -*- coding: utf-8 -*-

# 导入模块
import pygame
import sys
import my_plane
import enemy
import bullet
import supply
from random import *
from pygame.locals import *

# 初始化模块、混音器
pygame.init()
pygame.mixer.init()

# 设置背景窗口
bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption('飞机大战——RenDaWei')

# 添加背景图片
background = pygame.image.load_extended('images/background.png')

# 定义颜色
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# 载入音乐
pygame.mixer.music.load('sound/game_music.ogg')
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound('sound/bullet.wav')
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound('sound/use_bomb.wav')
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound('sound/supply.wav')
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound('sound/get_bomb.wav')
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound('sound/get_bullet.wav')
get_bullet_sound.set_volume(0.2)
up_grade_sound = pygame.mixer.Sound('sound/upgrade.wav')
up_grade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound('sound/enemy3_flying.wav')
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound('sound/enemy1_down.wav')
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound('sound/enemy2_down.wav')
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound('sound/enemy3_down.wav')
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound('sound/me_down.wav')
me_down_sound.set_volume(0.2)


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def add_mid_enemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def add_big_enemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


def increase_speed(target, inc):
    for each in target:
        each.speed += inc


def main():
    pygame.mixer.music.play(-1)

    # 生成我方飞机
    me = my_plane.MyPlane(bg_size)

    # 敌机组
    enemies = pygame.sprite.Group()

    # 生成敌方小飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    # 生成敌方中飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    # 生成敌方大飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    # 生成普通子弹
    bullet1 = []
    bullet1_index = 0
    bullet1_num = 4
    for i in range(bullet1_num):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    # 生成超级子弹
    bullet2 = []
    bullet2_index = 0
    bullet2_num = 8
    for i in range(bullet2_num // 2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))

    # 中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # 统计得分
    score = 0
    score_font = pygame.font.Font('font/font.ttf', 36)  # 设置字体

    clock = pygame.time.Clock()

    # 标志是否暂停游戏
    paused = False

    # 载入暂停按钮图片
    pause_nor_image = pygame.image.load_extended('images/pause_nor.png').convert_alpha()
    pause_pressed_image = pygame.image.load_extended('images/pause_pressed.png').convert_alpha()
    resume_nor_image = pygame.image.load_extended('images/resume_nor.png').convert_alpha()
    resume_pressed_image = pygame.image.load_extended('images/resume_pressed.png').convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image

    # 设置游戏级别
    level = 1

    # 全屏炸弹
    bomb_image = pygame.image.load_extended('images/bomb.png')
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font('font/font.ttf', 48)
    bomb_num = 3

    # 每30秒发放一个补给包
    bullet_supply = supply.BulletSupply(bg_size)
    bomb_supply = supply.BombSupply(bg_size)
    # 设置定时器
    supply_time = USEREVENT  # 自定义事件
    # 将此自定义时间设置时间为20秒
    pygame.time.set_timer(supply_time, 30 * 1000)

    # 超级子弹定时器
    double_bullet_time = USEREVENT + 1

    # 接触我方无敌状态定时器
    invincible_time = USEREVENT + 2

    # 标志是否使用超级子弹
    is_double_bullet = False

    # 生命数量
    life_image = pygame.image.load_extended('images/life.png').convert_alpha()
    life_rect = life_image.get_rect()
    life_num = 3

    # 用于阻止重复打开记录文件
    recorded = False

    # 游戏结束画面
    game_over_font = pygame.font.Font('font/font.ttf', 48)
    again_image = pygame.image.load_extended('images/again.png').convert_alpha()
    again_rect = again_image.get_rect()
    game_over_image = pygame.image.load_extended('images/gameover.png').convert_alpha()
    game_over_rect = game_over_image.get_rect()

    # 切换飞机图片
    switch_image = True

    # 用于延迟
    delay = 100

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):  # 检测鼠标是否在paused_rect区域
                    paused = not paused

                    if paused:
                        # 补给暂停
                        pygame.time.set_timer(supply_time, 0)
                        # 音乐暂停
                        pygame.mixer.music.pause()
                        # 音效暂停
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(supply_time, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()

                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False

            elif event.type == supply_time:
                supply_sound.play()
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == double_bullet_time:
                is_double_bullet = False
                # 关闭定时器
                pygame.time.set_timer(double_bullet_time, 0)

            elif event.type == invincible_time:
                me.invincible = False
                pygame.time.set_timer(invincible_time, 0)

        if level == 1 and score > 50000:
            level = 2
            up_grade_sound.play()
            # 增加3架小型敌机，2架中型敌机，1架大型敌机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            # 提升小型敌机的速度
            increase_speed(small_enemies, 1)
        elif level == 2 and score > 300000:
            level = 3
            up_grade_sound.play()
            # 增加5架小型敌机，3架中型敌机，2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升小型、中型敌机的速度
            increase_speed(small_enemies, 1)
            increase_speed(mid_enemies, 1)
        elif level == 3 and score > 600000:
            level = 4
            up_grade_sound.play()
            # 增加5架小型敌机，3架中型敌机，2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升小型、中型敌机的速度
            increase_speed(small_enemies, 1)
            increase_speed(mid_enemies, 1)
        elif level == 4 and score >1000000:
            level = 5
            up_grade_sound.play()
            # 增加5架小型敌机，3架中型敌机，2架大型敌机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            # 提升小型、中型敌机的速度
            increase_speed(small_enemies, 1)
            increase_speed(mid_enemies, 1)

        # 绘制背景图片
        screen.blit(background, (0, 0))

        if life_num and not paused:
            # 检测用户键盘操作
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_w] or key_pressed[K_UP]:
                me.move_up()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.move_down()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.move_left()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.move_right()

            # 绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            # 绘制超级子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    # 发射超级子弹
                    is_double_bullet = True
                    pygame.time.set_timer(double_bullet_time, 18 * 1000)
                    bullet_supply.active = False

            # 每10帧发射一颗子弹
            if not (delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % bullet2_num

                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % bullet1_num

            # 检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active = False

            # 绘制大型敌机
            for each in big_enemies:
                if each.active:  # 存活
                    each.move()

                    if each.hit:  # 如果被击中
                        # 绘制被打到的画面
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_image:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, black, (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5), 2)
                    # #当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = green
                    else:
                        energy_color = red
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain,
                                      each.rect.top - 5), 2)

                    # 即将出现在画面中, 播放音效
                    if each.rect.bottom == -50:
                        enemy3_fly_sound.play(-1)

                else:
                    # 毁灭
                    if not (delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 10000
                            each.reset()

            # 绘制中型敌机
            for each in mid_enemies:
                if each.active:
                    each.move()

                    if each.hit:  # 如果被打到
                        # 绘制被打到的画面
                        screen.blit(each.image_hit, each.rect)
                    else:
                        # 绘制正常画面
                        screen.blit(each.image, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, black, (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5), 2)
                    # 当生命大于20%显示绿色，否则显示红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = green
                    else:
                        energy_color = red
                    pygame.draw.line(screen, energy_color, (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain,
                                      each.rect.top - 5), 2)

                else:
                    # 毁灭
                    if not (delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 6000
                            each.reset()

            # 绘制小型敌机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 毁灭
                    if not (delay % 3):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 1000
                            each.reset()

            # 检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False

            # 绘制我放飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                # 毁灭
                if not (delay % 3):
                    if me_destroy_index == 0:
                        me_down_sound.play()
                    screen.blit(me.destroy_images[me_destroy_index], me.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(invincible_time, 3 * 1000)

            # 绘制全屏炸弹数量
            bomb_text = bomb_font.render('× %d' % bomb_num, True, white)
            bomb_text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - bomb_text_rect.height))

            # 绘制剩余生命数量
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, (width - 10 - life_rect.width * (i + 1),
                                             height - 10 - life_rect.height))
            # 绘制分数
            score_text = score_font.render('Score : %s' % str(score), True, white)
            screen.blit(score_text, (10, 5))

        # 绘制游戏结束
        elif life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()
            # 音效停止
            pygame.mixer.stop()
            # 停止发放补给
            pygame.time.set_timer(supply_time, 0)

            if not recorded:
                recorded = True
                # 读取历史最高得分
                with open('record.txt', 'r') as f:
                    record_score = int(f.read())

                # 如果玩家得分高于历史最高得分, 则存档
                if score > record_score:
                    with open('record.txt', 'w') as f:
                        f.write(str(score))

            # 绘制游戏结束画面
            # 绘制最高分数
            record_score_text = score_font.render('Best:%d' % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))

            # 绘制'Your Score'
            game_over_txt1 = game_over_font.render('Your Score', True, (255, 255, 255))
            game_over_txt1_rect = game_over_txt1.get_rect()
            game_over_txt1_rect.left, game_over_txt1_rect.top = \
                (width - game_over_txt1_rect.width) // 2, height // 3
            screen.blit(game_over_txt1, game_over_txt1_rect)

            # 绘制自己得分
            game_over_txt2 = game_over_font.render(str(score), True, (255, 255, 255))
            game_over_txt2_rect = game_over_txt2.get_rect()
            game_over_txt2_rect.left, game_over_txt2_rect.top = \
                (width - game_over_txt2_rect.width) // 2, game_over_txt1_rect.bottom + 10
            screen.blit(game_over_txt2, game_over_txt2_rect)

            # 绘制重新开始
            again_rect.left, again_rect.top = \
                (width - again_rect.width) // 2, game_over_txt2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            # 绘制结束游戏
            game_over_rect.left, game_over_rect.top = \
                (width - game_over_rect.width) // 2, again_rect.bottom + 10
            screen.blit(game_over_image, game_over_rect)

            # 检测用户鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击重新开始
                if again_rect.left < pos[0] < again_rect.right \
                        and again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，游戏重新开始
                    main()
                # 如果用户点击结束游戏
                elif game_over_rect.left < pos[0] < game_over_rect.right \
                        and game_over_rect.top < pos[1] < game_over_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()

        # 绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        # 切换飞机图片
        if not (delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()

