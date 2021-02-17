# -*- coding:utf-8 -*-
import pygame
from random import randrange
from time import sleep

pygame.init()

frame = 0
map_width = 284
map_height = 512
FPS = 60
pipes = [[180, 4]]  # 设置管道列表
bird = [40, map_height // 2 - 50]  # // 取下整的除法
gravity = 0.2  # 设置重力参数
velocity = 0  # 当前小鸟在垂直方向上的速度

gameScreen = pygame.display.set_mode((map_width, map_height))
clock = pygame.time.Clock()

bird_wing_up = bird_wing_up_copy = pygame.image.load("images/bird_wing_up.png")
bird_wing_down = bird_wing_down_copy = pygame.image.load("images/bird_wing_down.png")
background = pygame.image.load("images/background.png")
pipe_body = pygame.image.load("images/pipe_body.png")
pipe_end = pygame.image.load("images/pipe_end.png")


# 小鸟位置以及小鸟扇动翅膀特效
def draw_pipes():
    global pipes  # 引用全局变量 pipes
    for n in range(len(pipes)):
        for m in range(pipes[n][1]):  # 从第n个管道的身体画到开口
            gameScreen.blit(pipe_body, (pipes[n][0], m * 32))
        for m in range(pipes[n][1] + 6, 16):  # 从开口的末尾画到管道的末尾，这里默认了开口的大小固定为6
            gameScreen.blit(pipe_body, (pipes[n][0], m * 32))
        gameScreen.blit(pipe_end, (pipes[n][0], (pipes[n][1]) * 32))  # 添加管道的末端
        gameScreen.blit(pipe_end, (pipes[n][0], (pipes[n][1] + 5) * 32))  # 添加管道的末端
        pipes[n][0] -= 1


def draw_bird(x, y):
    global frame
    if 0 <= frame <= 30:
        gameScreen.blit(bird_wing_up, (x, y))
        frame += 1
    elif 30 < frame <= 60:
        gameScreen.blit(bird_wing_down, (x, y))
        frame += 1
        if frame == 60: frame = 0


def touch_pip():
    if bird[1] > map_height - 35:
        return True
    if bird[1] < 0:
        return True
    if pipes[0][0] - 30 < bird[0] < pipes[0][0] + 79:
        if bird[1] < (pipes[0][1] + 1) * 32 or bird[1] > (pipes[0][1] + 4) * 32:
            return True
    return False


def reset():
    global frame, map_width, map_height, FPS, pipes, bird, gravity, velocity
    frame = 0
    map_width = 284
    map_height = 512
    FPS = 60
    pipes.clear()
    bird.clear()
    pipes = [[180, 4]]
    bird = [40, map_height // 2 - 50]
    gravity = 0.2
    velocity = 0


def run():
    global velocity, bird_wing_down, bird_wing_up
    while True:
        if len(pipes) < 4:  # 如果屏幕中的管道总数小于4，则添加管道
            x = pipes[-1][0] + 200  # 设置x的值为最后一个管道的坐标值加上200
            open_pos = randrange(1, 9)  # 1-9中随机生成一个整数作为管道的中断起始位置
            pipes.append([x, open_pos])
        if pipes[0][0] < -80:  # 去除已经不在画面中的管道
            pipes.pop(0)
        # 将用户所有的操作获取到，比如鼠标移动，比如鼠标点击、鼠标抬起
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # 判断事件类型是否为按动键盘操作
                bird[1] -= 40  # 控制小鸟坐标向上移动40
                velocity = 0
                print(event)
            # 点击关闭按钮之后会触发这里进行退出游戏操作
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        gameScreen.blit(background, (0, 0))
        draw_bird(bird[0], bird[1])  # // 取下整的除法
        velocity += gravity
        bird[1] += velocity
        # 小鸟下降时头部转动效果制作
        bird_wing_down = pygame.transform.rotate(bird_wing_down_copy, -90 * (velocity / 15))
        bird_wing_up = pygame.transform.rotate(bird_wing_up_copy, -90 * (velocity / 15))
        draw_pipes()
        pygame.display.update()
        if touch_pip():
            sleep(3)
            reset()
        clock.tick(FPS)


if __name__ == '__main__':
    run()
