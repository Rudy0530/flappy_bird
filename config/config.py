# -*- coding:utf-8 -*-
import pygame

pygame.init()
map_width = 284
map_height = 512
FPS = 60
gravity = 0.2  # 设置重力参数

bird_wing_up_copy = pygame.image.load("../images/bird_wing_up.png")
bird_wing_down_copy = pygame.image.load("../images/bird_wing_down.png")
background = pygame.image.load("../images/background.png")
pipe_body = pygame.image.load("../images/pipe_body.png")
pipe_end = pygame.image.load("../images/pipe_end.png")

game_screen = pygame.display.set_mode((map_width, map_height))
clock = pygame.time.Clock()
