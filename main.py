import pygame
import random
from pygame import mixer
pygame.init()

#setting layar
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode(((WIDTH, HEIGHT)))
pygame.display.set_caption("Rabbit Game")

#load Backgroud
BG = pygame.image.load('assets/bg_kebun.gif')

#load sound
eatSound = pygame.mixer.Sound("rabbit_eat2.mp3")

class Player:
    def __init__(self, x, y, kode='left'):
        self.x = x
        self.y = y
        self.player_img = None
        self.kode = kode

        if self.kode == 'left':
            self.player_img = pygame.image.load('assets/kelinci_left.gif')
        if self.kode == 'right':
            self.player_img = pygame.image.load('assets/kelinci_right.gif')
        
        self.mask = pygame.mask.from_surface(self.player_img)


    def draw(self, window):
        window.blit(self.player_img, (self.x, self.y))
    
    def get_width(self):
        return self.player_img.get_width()

    def get_height(self):
        return self.player_img.get_height()
        
class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.food_img = pygame.image.load('assets/carrot2.gif')
        self.foods=[]
        self.mask = pygame.mask.from_surface(self.food_img)

    def draw(self, window):
        window.blit(self.food_img, (self.x, self.y))

    def move_food(self, vel, obj):
        self.y += vel
        for food in self.foods:
            food.move(vel)
            if food.off_screen(HEIGHT):
                self.foods.remove(food)
            elif food.collision(obj):
                self.foods.remove(food)
        

    def get_width(self):
        return self.food_img.get_width()

    def get_height(self):
        return self.food_img.get_height()

    def off_screen(self, height):
        return self.y <= height and self.y >= 0
    

def collide (obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main () :
    run = True
    FPS = 60
    level = 0
    lives = 4
    score = 0

    main_font = pygame.font.Font('04B_19__.ttf',20)
    lost_font = pygame.font.Font('04B_19__.ttf',30)
    again_font = pygame.font.SysFont('Courier',30, True)

    player_vel = 5
    player = Player(300, 500, 'left')

    foods = []
    foods_vel = 2
    lost = False
    lost_count = 0
    jml_wortel = 0

    
    clock = pygame.time.Clock()

    def redraw_window() :
        WIN.blit(BG, (0,0))
        #draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        score_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))
        

        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10,40))
        WIN.blit(score_label, (WIDTH - score_label.get_width() - 10,10))
        

        for food in foods :
            food.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render('GAME OVER...', 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2,200))
            again_label = again_font.render('Enter to Play again', 1, (0,0,0))
            WIN.blit(again_label, (WIDTH/2 -  again_label.get_width()/2,250))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN] :
                main_menu()

        pygame.display.update()


    while run :
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 :
            lost = True
            lost_count += 1

        if len(foods) == 0:
            level += 1
            lives += 1
            jml_wortel += 5
            #foods_vel += 1
            player_vel +=1
            for i in range (jml_wortel):
                food = Food(random.randrange(10, WIDTH-50), random.randrange(-1500, -100))
                foods.append(food)     

            if lost == True:
                level -= 1
                
        for food in foods:
            food.move_food(foods_vel, player)

            if collide(player,food):
                eatSound.play()
                score +=10
                foods.remove(food)
            if food.y > HEIGHT:
                lives -= 1
                foods.remove(food)
            if lost == True:
                lives = 0
                foods.remove(food)

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                run = False
                exit()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player= Player(player.x, player.y, 'left')
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + 70 < WIDTH:
            player = Player(player.x, player.y, 'right')
            player.x += player_vel

def main_menu():
    title_font = pygame.font.SysFont('Courier',30, True)
    run = True
    while run:
        WIN.blit(BG, (0,0))  
        title_label = title_font.render("PRESS SPACE TO BEGIN...", 1, (0,0,0))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()
        keys = pygame.key.get_pressed()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                exit()
        if keys[pygame.K_SPACE]:
            main()
        

    pygame.quit()
        
main_menu()

