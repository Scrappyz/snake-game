import pygame
import random

def move(player, key):
    move_dir = ()
    if key[pygame.K_a]:
        move_dir = (-20, 0)
    elif key[pygame.K_d]:
        move_dir = (20, 0)
    elif key[pygame.K_w]:
        move_dir = (0, -20)
    elif key[pygame.K_s]:
        move_dir = (0, 20)
        
    for i in range(len(player)-1, -1, -1):
        player[i]

def main():
    pygame.init()
    screen_width = 960
    screen_height = 540
    speed = 20
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    player = [pygame.Rect((screen_width / 2, screen_height / 2, 20, 20))]
    food = pygame.Rect(random.randint(0, 960), random.randint(0, 540), 15, 15)
    food_exist = False
    
    run = True
    while run:
        screen.fill((0, 0, 0))
        for i in player:
            pygame.draw.rect(screen, (0, 255, 0), i)
    
        if not food_exist:
            pygame.draw.rect(screen, (255, 0, 0), food)
            food_exist = False
        
        key = pygame.key.get_pressed()
        move(player, key)
            
        if player[0].collidepoint(food.x, food.y):
            last_segment = player[len(player)-2]
            player.append(pygame.Rect(last_segment.x-20, last_segment.y-20, 20, 20))
            screen.fill((0, 0, 0))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        pygame.display.update()
        pygame.time.wait(speed)
                
    pygame.quit()

if __name__ == "__main__":
    main()