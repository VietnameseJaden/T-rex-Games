import pygame
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
widthoscreen = 400
heightoscreen = 400
screen = pygame.display.set_mode((widthoscreen, heightoscreen))
rect1 = pygame.Rect(0, 170, 50, 50)
rect2 = pygame.Rect(0, 180, 400, 50)
rect3 = pygame.Rect(0,350,50,50)
rect4 = pygame.Rect(0,0,50,50)
rect1_speed = [5, 0]
rect3_speed = [20,0]
rect4_speed = [10,0]
surf = pygame.Surface((rect1.w, rect1.h))
surf2 = pygame.Surface((rect2.w, rect2.h))
surf3 = pygame.Surface((rect3.w,rect3.h))
surf4 = pygame.Surface((rect4.w,rect4.h))
surf.fill((0, 0, 255))
surf2.fill((255, 0, 0))
surf3.fill((0, 0, 255))
surf4.fill((0,0,255))
list1 = [rect1, rect2]
list2 = [rect3, rect2]
list3 = [rect4, rect2]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(color=(0, 0, 0))
    screen.blit(surf2, (rect2.x, rect2.y))
    pygame.display.flip()
    rect1 = rect1.move(rect1_speed)
    screen.blit(surf,(rect1.x,rect1.y))
    pygame.display.flip()
    clock.tick(60)
    if rect1.x > widthoscreen:
        screen.fill(color=(255,0,0))
        
        pygame.display.flip()
        clock.tick(20)
        rect1.x=0
    keys = pygame.key.get_pressed()
    if keys[K_w]:  
        if(rect1.x < 30 or rect1.x > 30) and (rect1.y < 30 or rect1.y > 30):
            rect1_speed[0] = -rect1_speed[0]
            rect1_speed[1] = -rect1_speed[1]
            rect1.y -= 1
            screen.blit(surf, (rect1.x, rect1.y))
            pygame.display.flip()
            clock.tick(60)
    if keys[K_s]: 
        if (rect1.x < 30 or rect1.x > 30) and (rect1.y < 30 or rect1.y > 0):
            rect1_speed[0] = -rect1_speed[0]
            rect1_speed[1] = -rect1_speed[1]
            rect1.y += 1
            screen.blit(surf, (rect1.x, rect1.y))
            pygame.display.flip()
            clock.tick(60)
    if keys[K_a]:  
        if(rect1.x < 0 or rect1.x > 30) and (rect1.y < 30 or rect1.y > 0):
            rect1_speed[0] = -rect1_speed[0]
            rect1_speed[1] = -rect1_speed[1]
            rect1.x -= 1
            screen.blit(surf, (rect1.x, rect1.y))
            pygame.display.flip()
            clock.tick(60)
    if keys[K_d]:  
        if(rect1.x < 0 or rect1.x > 30) and (rect1.y < 30 or rect1.y > 0):
            rect1_speed[0] = -rect1_speed[0]
            rect1_speed[1] = -rect1_speed[1]
            rect1.x += 1
            screen.blit(surf, (rect1.x, rect1.y))
            pygame.display.flip()
            clock.tick(60)
