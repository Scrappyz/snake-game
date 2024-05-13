import pygame, sys, time, random

# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
frame_size_x = 720
frame_size_y = 480

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game Over
def game_over(score):
    my_font = pygame.font.SysFont('times new roman', 90) # set font
    game_over_surface = my_font.render('YOU DIED', True, red) # renders text on screen
    game_over_rect = game_over_surface.get_rect() # use to position text
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4) # set text location
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect) # draws it all on the window
    show_score(score, 0, red, 'times', 20)

# Score
def show_score(score, choice, color, font, size):
    score_font = pygame.font.SysFont(font, size) # set font
    score_surface = score_font.render('Score : ' + str(score), True, color) # renders text on screen
    score_rect = score_surface.get_rect() # use to position the text
    if choice == 1: # 1 for in-game
        score_rect.midtop = (frame_size_x/10, 15) # set text location top left
    else: # 0 for game over
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25) # set text location to bottom middle
    game_window.blit(score_surface, score_rect) # draws it all on the window
    
def main():
    snake_pos = [frame_size_x / 2, frame_size_y / 2] # snake head position
    snake_body = [[100, 50], [100-10, 50], [100-(10*2), 50]] # snake segment positions

    food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10] # The position of food on the screen
    food_spawn = True # Keeps track if there is food on screen

    direction = 'RIGHT'
    change_to = direction

    score = 0
    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # To prevent the snake from colliding on itself when moving the opposite direction
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Moving the snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        
        # Checks if snake head collides with food
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Generate food
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
        food_spawn = True

        # GFX
        game_window.fill(black)
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

        # Spawn food
        pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
            game_over(score)
            playing = False
        if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
            game_over(score)
            playing = False
            
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over(score)
                playing = False

        # Refresh game screen
        pygame.display.update()
        
        # Refresh rate (controls speed of snake)
        fps_controller.tick(difficulty)
    
    # show score at end of game
    show_score(score, 1, red, 'consolas', 20)
    time.sleep(3)
    pygame.quit()
    
if __name__ == "__main__":
    main()