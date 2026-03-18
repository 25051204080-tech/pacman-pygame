from board import boards
import pygame
import sys
import random

pygame.init()
WIDTH=600
HEIGHT=630

screen=pygame.display.set_mode((WIDTH,HEIGHT))
timer=pygame.time.Clock()
font = pygame.font.SysFont("Arial",20)
fps=60
pygame.display.set_caption("Praktikum PBO - Pacman")
BG=(222,184,135)
BALL=(255,255,255)
LINE=(160,82,45)
anim_counter=0
flick_counter=0
flicker=False
score=0
powerup=False
power_counter=0
power_time=300

class MAP:
    def __init__(self,level):
        self.level=level
        self.line1=pygame.transform.scale(pygame.image.load("assets/line/line1.png"),(20,20))
        self.line2=pygame.transform.scale(pygame.image.load("assets/line/line1.png"),(40,40))
        self.line3=pygame.transform.scale(pygame.image.load("assets/line/line3.png"),(20,20))
        self.line4=pygame.transform.scale(pygame.image.load("assets/line/line4.png"),(20,20))
        self.line5=pygame.transform.scale(pygame.image.load("assets/line/line5.png"),(20,20))
        self.line6=pygame.transform.scale(pygame.image.load("assets/line/line6.png"),(20,20))
        self.line7=pygame.transform.scale(pygame.image.load("assets/line/line7.png"),(20,20))
        self.line8=pygame.transform.scale(pygame.image.load("assets/line/line8.png"),(20,20))

    def draw_board(self):
        tile_w = WIDTH // len(self.level[0])
        tile_h = (HEIGHT-30) // len(self.level)

        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                x = j *tile_w
                y = i *tile_h
                if self.level[i][j]==1:
                    screen.blit(self.line1,(x,y))
                if self.level[i][j]==2 and not flicker:
                    screen.blit(self.line2,(x-10,y-10))
                if self.level[i][j]==3:
                    screen.blit(self.line3,(x,y))
                if self.level[i][j]==4:
                    screen.blit(self.line4,(x,y))
                if self.level[i][j]==5:
                    screen.blit(self.line5,(x,y))          
                if self.level[i][j]==6:
                    screen.blit(self.line6,(x,y))          
                if self.level[i][j]==7:
                    screen.blit(self.line7,(x,y))          
                if self.level[i][j]==8:
                    screen.blit(self.line8,(x,y))          
board=MAP(boards)

class Player:
    def __init__ (self, x, y):
        self.x=x
        self.y=y
        self.speed=2
        self.height=30
        self.width=30
        self.direction=0

        self.player_images=[]
        for i in range(1,4):
            img = pygame.image.load(f"assets/player_images/{i}.png")
            img = pygame.transform.scale(img,(self.height,self.width))
            self.player_images.append(img)

    def check_collision(self,new_x,new_y,level):
        row= ((HEIGHT-30)//32)
        col= (WIDTH//30)

        grid_x =int((new_x + self.width//2) // col)
        grid_y =int((new_y + self.height//2) // row)

        if 0 <= grid_y < len(level) and 0 <= grid_x < len(level[0]):
            if level[grid_y][grid_x] <3:
                return True
        
        return False
    
    def makan(self,new_x,new_y,level):
        global score, powerup, power_counter
        row = ((HEIGHT-30)//32)
        col = (WIDTH//30)

        grid_x =int((new_x + self.width//2) // col)
        grid_y =int((new_y + self.height//2) // row)
        if level[grid_y][grid_x] == 1:
            level[grid_y][grid_x] = 0
            score+=5
        if level[grid_y][grid_x] == 2:
            level[grid_y][grid_x] = 0
            score+=20
            powerup=True
            power_counter=0
        
    def move(self, keys):
            global anim_counter
            if keys[pygame.K_RIGHT]:
                new_x=self.x + self.speed
                if self.check_collision(new_x, self.y,boards):
                    self.x=new_x
                    self.direction=0
                self.makan(new_x, self.y,boards)
            if keys[pygame.K_LEFT]:
                new_x=self.x - self.speed
                if self.check_collision(new_x, self.y,boards):
                    self.x=new_x
                    self.direction=1
                self.makan(new_x, self.y,boards)
            if keys[pygame.K_UP]:
                new_y=self.y - self.speed
                if self.check_collision(self.x, new_y,boards):
                    self.y=new_y
                    self.direction=2
                self.makan(self.x, new_y,boards)
            if keys[pygame.K_DOWN]:
                new_y=self.y + self.speed
                if self.check_collision(self.x, new_y,boards):
                    self.y=new_y
                    self.direction=3
                self.makan(self.x, new_y,boards)
            if anim_counter <20:
                anim_counter+=1
            else:
                anim_counter=0
    
    def draw(self,screen):
        #0-kanan, 1-kiri, 2-atas,3-bawah
        frame = self.player_images[(anim_counter//5) % len(self.player_images)]
        if self.direction==0:
            screen.blit(frame,(self.x,self.y))
        if self.direction ==1:
            screen.blit(pygame.transform.flip(frame,True,False), (self.x,self.y))
        if self.direction==2:
            screen.blit(pygame.transform.rotate(frame,90), (self.x,self.y))
        if self.direction==3:
            screen.blit(pygame.transform.rotate(frame,270), (self.x,self.y))
        if self.x<0:
            self.x=0
        if self.x>WIDTH-self.width:
            self.x=WIDTH-self.width
        if self.y<0:
            self.y=0
        if self.y>HEIGHT-self.height:
                self.y=590-self.height

player = Player(289, 418)

class ghost:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.speed=2
        self.height=30
        self.width=30
        self.direction=0

    def position(self, new_x, new_y, level):
        turns = [False, False, False, False]

        row_size = ((HEIGHT - 30) // 32)
        col_size = (WIDTH // 30)
        center_x = new_x + self.width // 2
        center_y = new_y + self.height // 2
        grid_x = int(center_x // col_size)
        grid_y = int(center_y // row_size)

        if grid_x + 1 < len(level[0]):
            if level[grid_y][grid_x + 1] < 3:
                turns[0] = True
        if grid_x - 1 >= 0:
            if level[grid_y][grid_x - 1] < 3:
                turns[1] = True
        if grid_y - 1 >= 0:
            if level[grid_y - 1][grid_x] < 3:
                turns[2] = True
        if grid_y + 1 < len(level):
            if level[grid_y + 1][grid_x] < 3:
                turns[3] = True
        return turns

    def move(self):
        turns = self.position(self.x, self.y, boards)
        if not turns[self.direction]:
            self.direction = random.randint(0,3)
        if self.direction==0 and turns[0]:
            self.x+=self.speed
        elif self.direction==1 and turns[1]:
            self.x-=self.speed
        elif self.direction==2 and turns[2]:
            self.y-=self.speed
        elif self.direction==3 and turns[3]:
            self.y+=self.speed
    def check_player(self, player):
        ghost_rect = pygame.Rect(self.x,self.y,self.width,self.height)
        player_rect = pygame.Rect(player.x,player.y,player.width,player.height)
        return ghost_rect.colliderect(player_rect)
    
class Pinky(ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image1 = pygame.transform.scale(pygame.image.load("assets/ghost/ghost1.png"),(self.height,self.width))
        self.image2 = pygame.transform.scale(pygame.image.load("assets/ghost/ghost4.png"),(self.height,self.width))
    def draw(self):
        if not powerup:
            screen.blit(self.image1,(self.x,self.y))
        else:
            screen.blit(self.image2,(self.x,self.y))
    def go(self):
        self.move()
class Greeny(ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image1 = pygame.transform.scale(pygame.image.load("assets/ghost/ghost2.png"),(self.height,self.width))
        self.image2 = pygame.transform.scale(pygame.image.load("assets/ghost/ghost4.png"),(self.height,self.width))
    def draw(self):
        if not powerup:
            screen.blit(self.image1,(self.x,self.y))
        else:
            screen.blit(self.image2,(self.x,self.y))
    def go(self):
        self.move()
class Bluey(ghost):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image1 = pygame.transform.scale(pygame.image.load("assets/ghost/ghost3.png"),(self.height,self.width))
        self.image2 = pygame.transform.scale(pygame.image.load("assets/ghost/ghost4.png"),(self.height,self.width))
    def draw(self):
        if not powerup:
            screen.blit(self.image1,(self.x,self.y))
        else:
            screen.blit(self.image2,(self.x,self.y))
    def go(self):
        self.move()

def cek_win(level):
    for row in level:
        if 1 in row or 2 in row:
            return False
    return True  

pinky=Pinky(330,270)
greeny=Greeny(285,270)
bluey=Bluey(240,270)

game_over=False
you_win=False
running = True
while running:
    timer.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if flick_counter<13:
        flicker=True
        flick_counter+=1
    else:
        flicker=False
        flick_counter=0

    if not game_over:
        keys = pygame.key.get_pressed()
        player.move(keys)
        pinky.go()
        greeny.go()
        bluey.go()

    screen.fill(BG)
    board.draw_board()
    player.draw(screen)
    pinky.draw()
    greeny.draw()
    bluey.draw()
    
    if powerup:
       power_counter += 1
       if power_counter >= power_time:
            powerup = False
            power_counter = 0
    if pinky.check_player(player):
        if powerup:
            score += 100
            pinky.x = 330
            pinky.y = 270
        else:
            game_over = True
    if greeny.check_player(player):
        if powerup:
            score += 100
            greeny.x = 285
            greeny.y = 270
        else:
            game_over = True
    if bluey.check_player(player):
        if powerup:
            score += 100
            bluey.x = 240
            bluey.y = 270
        else:
            game_over = True
    if cek_win(boards):
        you_win = True
        game_over = True

    score_text = font.render(f"Score: {score}", True, (0,0,0))
    screen.blit(score_text,(10,600))
    font02=pygame.font.SysFont("None",50)
    if game_over and not you_win:
        text = font02.render("GAME OVER", True, (0,0,0))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)

    if you_win:
        text = font02.render("YOU WIN!", True, (0,0,0))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()