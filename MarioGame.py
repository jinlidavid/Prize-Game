import pygame
pygame.init()

screen_height = 700
screen_length = 1000

window = pygame.display.set_mode((screen_length,screen_height))
pygame.display.set_caption("Game")

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.left = False
        self.right = False
        self.jump = False
        self.jump_constant = 7
        self.step_sprite = 0
        self.velocity = 15
        self.hitbox = (self.x +20,self.y,16,16)
        self.lives = 1
        self.alive = True

    def draw(self,window):
        if self.step_sprite + 1 >= 8:
            self.step_sprite = 0
        
        if self.left == True:
            window.blit(walk_left[self.step_sprite // 2],(self.x,self.y))
            self.step_sprite += 1
        elif self.right == True:
            window.blit(walk_right[self.step_sprite // 2],(self.x,self.y))
            self.step_sprite += 1
        else:
            window.blit(neutral,(self.x,self.y))
        self.hitbox = (self.x,self.y,16,16)
        #pygame.draw.rect(window,(255,0,0),self.hitbox,2)

    def hit(self):
        if self.lives > 0:
            self.lives -= 1
        else:
            self.alive = False


class enemy_1(object):
    logo = pygame.image.load('Harrow2.png')
    def __init__(self,x,y,width,height,end,velocity):
        self.x = x
        self.y = y
        self.width = width
        self.end = end
        self.velocity = velocity
        self.path = [x,end]
        self.sprite = 0
        self.hitbox = (self.x+20,self.y,16,16)

    def draw(self,window):
        self.move()
        window.blit(self.logo,(self.x,self.y))
        self.hitbox = (self.x,self.y,40,40)
        #pygame.draw.rect(window,(255,0,0),self.hitbox,2)
        pass

    def move(self):
        if self.velocity > 0:
            if self.x < self.path[1] +self.velocity:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.x += self.velocity
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
        pass

class enemy_2(object):
    logo = pygame.image.load('Winchester.png')
    def __init__(self,x,y,width,height,end,velocity):
        self.x = x
        self.y = y
        self.width = width
        self.end = end
        self.velocity = velocity
        self.path = [x,end]
        self.sprite = 0
        self.hitbox = (self.x+20,self.y,16,16)

    def draw(self,window):
        self.move()
        window.blit(self.logo,(self.x,self.y))
        self.hitbox = (self.x,self.y,40,40)
        #pygame.draw.rect(window,(255,0,0),self.hitbox,2)
        pass

    def move(self):
        if self.velocity > 0:
            if self.x < self.path[1] +self.velocity:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.x += self.velocity
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.velocity = self.velocity * -1
        pass

walk_right = [pygame.image.load('r1.png'),pygame.image.load('r2.png'),pygame.image.load('r3.png'),pygame.image.load('r4.png')]
walk_left = [pygame.image.load('l1.png'),pygame.image.load('l2.png'),pygame.image.load('l3.png'),pygame.image.load('l4.png')]
neutral = pygame.image.load('r4.png')

clock = pygame.time.Clock()

def game_over(score):
    window.fill((255,255,255))
    font = pygame.font.Font(None, 50)
    text = font.render('GAME OVER - SCORE:' + score,1,(1,1,1))
    textpos = text.get_rect()
    textpos.center = (250,500)
    window.blit(text, textpos)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
def redraw_window(seconds,score):
    global h2_spawn
    window.fill((255,255,255))
    font = pygame.font.Font(None, 36)
    text = font.render('Score:' + score,1,(1,1,1))
    textpos = text.get_rect()
    textpos.centerx = 60
    window.blit(text, textpos)

    text_1 = font.render('YOU HAVE ONE LIFE, DODGE HARROW AND WINCHESTER TO GAIN POINTS(1/10s)',1,(1,1,1))
    textpos_1 = text.get_rect()
    textpos_1.center = (55,100)
    window.blit(text_1, textpos_1)

    mario.draw(window)
    harrow.draw(window)
    if seconds > 10 and h2_spawn == False:
        h2_spawn = True
    if h2_spawn == True:
        harrow_2.draw(window)
    if seconds > 20 and w_spawn == False:
        winchester.draw(window)
    if seconds > 30 and w2_spawn == False:
        winchester_2.draw(window)

    pygame.display.update()

mario = player(100,410,16,16)
harrow = enemy_1(200,387,40,40,960,10)
harrow_2 = enemy_1(0,387,40,40,960,20)
winchester = enemy_2(0,345,40,40,960,20)
winchester_2 = enemy_2(0,345,40,40,960,30)
w_spawn = False
w2_spawn = False
h2_spawn = False

run = True
start_ticks = pygame.time.get_ticks()
while run:
    seconds = (pygame.time.get_ticks()-start_ticks)/1000
    score = str(int(seconds // 10))
    clock.tick(48) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_LEFT] and mario.x >= mario.velocity:
        mario.x -= mario.velocity
        mario.left = True
        mario.right = False
    elif keys_pressed[pygame.K_RIGHT] and mario.x < (screen_length - mario.width - mario.velocity):
        mario.x += mario.velocity
        mario.right = True
        mario.left = False
    else:
        mario.left = False
        mario.right = False
        mario.step_sprite = 0

    if (mario.jump) == False:
        if keys_pressed[pygame.K_UP]:
            mario.jump = True
            mario.left = False
            mario.right = False
            mario.step_sprite = 0
    else:
        if mario.jump_constant >= -7:
            negative = 1
            if mario.jump_constant < 0:
                negative = -1
            mario.y -= ((mario.jump_constant**2) * 0.5 * negative)
            mario.jump_constant -= 1
        else:
            mario.jump = False
            mario.jump_constant = 7

    if mario.hitbox[1] < harrow.hitbox[1] + harrow.hitbox[3] and mario.hitbox[1] + mario.hitbox[3] > harrow.hitbox[1]:
        if mario.hitbox[0] + mario.hitbox[2] > harrow.hitbox[0] and mario.hitbox[0] < harrow.hitbox[0] + harrow.hitbox[2]:
            mario.hit()
    if mario.hitbox[1] < harrow_2.hitbox[1] + harrow_2.hitbox[3] and mario.hitbox[1] + mario.hitbox[3] > harrow_2.hitbox[1]:
        if mario.hitbox[0] + mario.hitbox[2] > harrow_2.hitbox[0] and mario.hitbox[0] < harrow_2.hitbox[0] + harrow_2.hitbox[2]:
            mario.hit()
    if mario.hitbox[1] < winchester.hitbox[1] + winchester.hitbox[3] and mario.hitbox[1] + mario.hitbox[3] > winchester.hitbox[1]:
        if mario.hitbox[0] + mario.hitbox[2] > winchester.hitbox[0] and mario.hitbox[0] < winchester.hitbox[0] + winchester.hitbox[2]:
            mario.hit()
    if mario.hitbox[1] < winchester_2.hitbox[1] + winchester_2.hitbox[3] and mario.hitbox[1] + mario.hitbox[3] > winchester_2.hitbox[1]:
        if mario.hitbox[0] + mario.hitbox[2] > winchester_2.hitbox[0] and mario.hitbox[0] < winchester_2.hitbox[0] + winchester_2.hitbox[2]:
            mario.hit()

    if mario.alive == False:
        game_over(score)

    redraw_window(seconds,score)

pygame.quit()
