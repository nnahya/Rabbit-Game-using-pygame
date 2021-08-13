import pygame
pygame.init()

win = pygame.display.set_mode((800,600)) # screen size
pygame.display.set_caption("Rabbit Game")

bcGround = pygame.image.load('assets/bg_kebun.gif').convert()
player = pygame.image.load('assets/kelinci_left.gif').convert_alpha()
player_rect = player.get_rect(center=(300, 500))
food = pygame.image.load('assets/carrot2.gif').convert_alpha()

vel = 15

run = True

while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player = pygame.image.load('assets/kelinci_left.gif').convert_alpha()
        player_rect.x -= vel

    if keys[pygame.K_RIGHT]:
        player = pygame.image.load('assets/kelinci_right.gif').convert_alpha()
        player_rect.x += vel
    
    win.blit(bcGround,(0,0))
    win.blit(player, player_rect) 
    pygame.display.update() 
    
pygame.quit()
