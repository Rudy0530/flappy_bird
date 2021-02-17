# -*- coding:utf-8 -*-
from random import randrange
from time import sleep
from config.config import *


def check_pip(pipes):
    if len(pipes) < 4:  # 如果屏幕中的管道总数小于4，则添加管道
        x = pipes[-1][0] + 200  # 设置x的值为最后一个管道的坐标值加上200
        open_pos = randrange(1, 9)  # 1-9中随机生成一个整数作为管道的中断起始位置
        pipes.append([x, open_pos])
    if pipes[0][0] < -80:  # 去除已经不在画面中的管道
        pipes.pop(0)


def draw_bird(bird_position, frame, bird_wing_up, bird_wing_down, velocity):
    if 0 <= frame <= 30:
        game_screen.blit(bird_wing_up, (bird_position[0], bird_position[1]))
        frame += 1
    elif 30 < frame <= 60:
        game_screen.blit(bird_wing_down, (bird_position[0], bird_position[1]))
        frame += 1
        if frame == 60:
            frame = 0
    bird_position[1] += velocity
    return frame


# 小鸟位置以及小鸟扇动翅膀特效
def draw_pipes(pipes, pipe_end, pipe_body):
    for n in range(len(pipes)):
        for m in range(pipes[n][1]):  # 从第n个管道的身体画到开口
            game_screen.blit(pipe_body, (pipes[n][0], m * 32))
        for m in range(pipes[n][1] + 6, 16):  # 从开口的末尾画到管道的末尾，这里默认了开口的大小固定为6
            game_screen.blit(pipe_body, (pipes[n][0], m * 32))
        game_screen.blit(pipe_end, (pipes[n][0], (pipes[n][1]) * 32))  # 添加管道的末端
        game_screen.blit(pipe_end, (pipes[n][0], (pipes[n][1] + 5) * 32))  # 添加管道的末端
        pipes[n][0] -= 1


def touch_pip(bird_position, pipes):
    if bird_position[1] > map_height - 35:
        return True
    if bird_position[1] < 0:
        return True
    if pipes[0][0] - 30 < bird_position[0] < pipes[0][0] + 79:
        if bird_position[1] < (pipes[0][1] + 1) * 32 or bird_position[1] > (pipes[0][1] + 4) * 32:
            return True
    return False


def reset():
    sleep(3)
    return init()


def init():
    pipes = [[180, 4]]  # 设置管道列表
    bird_position = [40, map_height // 2 - 50]  # // 取下整的除法
    velocity = 0  # 当前小鸟在垂直方向上的速度
    frame = 0
    return pipes, bird_position, velocity, frame


def update_velocity(velocity, gravity):
    velocity += gravity
    return velocity


def run():
    pipes, bird_position, velocity, frame = init()
    while True:
        check_pip(pipes)
        # # 将用户所有的操作获取到，比如鼠标移动，比如鼠标点击、鼠标抬起
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # 判断事件类型是否为按动键盘操作
                bird_position[1] -= 40  # 控制小鸟坐标向上移动40
                velocity = 0
            # 点击关闭按钮之后会触发这里进行退出游戏操作
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        # 小鸟下降时头部转动效果制作
        bird_wing_down = pygame.transform.rotate(bird_wing_down_copy, -90 * (velocity / 15))
        bird_wing_up = pygame.transform.rotate(bird_wing_up_copy, -90 * (velocity / 15))
        game_screen.blit(background, (0, 0))
        velocity = update_velocity(velocity, gravity)
        frame = draw_bird(bird_position, frame, bird_wing_up, bird_wing_down, velocity)  # // 取下整的除法
        draw_pipes(pipes, pipe_end, pipe_body)
        pygame.display.update()
        if touch_pip(bird_position, pipes):
            pipes, bird_position, velocity, frame = reset()
        clock.tick(FPS)


if __name__ == '__main__':
    run()
