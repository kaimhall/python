import pygame, sys
from pygame.locals import *
import random
import time

# Robo class for player.
class Robo(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.surf = surface
        self.rect = self.surf.get_rect()
        self.pos = vec((320 , SCREEN_HEIGHT - offset))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False         

    def move(self):
        self.acc = vec(0,0.5)
        pressed_keys = pygame.key.get_pressed()
        
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        
        if self.pos.x > SCREEN_WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_WIDTH
     
        self.rect.midbottom = self.pos

    def update(self):      
        collisions = pygame.sprite.spritecollide(r1 , blocks, False)  
        if r1.vel.y > 0:
            if collisions:
                if self.pos.y < collisions[0].rect.bottom:               
                    self.pos.y = collisions[0].rect.top +1
                    self.vel.y = 0
                    self.jumping = False
                
    def jump(self):
        collisions = pygame.sprite.spritecollide(r1 , blocks, False)  
        if collisions and not self.jumping:
            self.jumping = True
            self.vel.y = -15
    
    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

## Block class for platforms. No methods.
class Block(pygame.sprite.Sprite):
    def __init__(self,surface):
        super().__init__()
        self.surf = surface
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center=(random.randint(0,SCREEN_WIDTH-10), random.randint(0, SCREEN_HEIGHT-30)))
        self.speed = random.randint(-1, 1)
        self.moving = True   

# Monster class for enemies.
class Monster(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.surf = surface
        cntr = get_monster_stand()
        self.rect = self.surf.get_rect(center = cntr)
        self.speed = 1         

    def update(self):
        self.rect.move_ip( 0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            pass

def new_robo():
    robo = pygame.image.load('src/robo.png')
    return Robo(robo)
     
def new_block():
    block = pygame.Surface((random.randint(50,100), 12))
    return Block(block)

def get_monster_stand():
    for block in blocks:
        return (block.rect.x + block.surf.get_width() / 2, block.rect.y - block.surf.get_height() - offset)

def new_monster():
    monster = pygame.image.load('src/hirvio.png')
    return Monster(monster)

def get_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_SPACE or event.key == K_LSHIFT or event.key == K_RSHIFT:
                r1.jump()

        if event.type == KEYUP:
            if event.key == K_SPACE or event.key == K_LSHIFT or event.key == K_RSHIFT:
                r1.cancel_jump()

def block_gen():
    while len(blocks) < 7 :
        width = random.randrange(50,80)
        b  = new_block()
        C = True
        while C:             
            b.rect.center = (random.randrange(0, SCREEN_WIDTH - width),
                                random.randrange(100, 400))
            C = check(b, blocks)
        blocks.add(b)
        all_sprites.add(b, blocks)

def check(block, grouped):
    if pygame.sprite.spritecollideany(block, grouped):
        return True
    else:
        for entity in blocks:
            if entity == Block:
                continue
            if (abs(block.rect.top - entity.rect.bottom) < 50) and (abs(block.rect.bottom - entity.rect.top) < 50):
                return True
        C = False

def game_loop():
        while True:        
            get_events()

            r1.move()
            r1.update() 

            screen.fill((255,255,255))
            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)    
            
            pygame.display.update()
            clk.tick(30)

if __name__ == '__main__':
    
    pygame.init()   
    clk = pygame.time.Clock()
    vec = pygame.math.Vector2
    offset = 13
    
    ACC = 0.5
    FRIC = -0.12
    FPS = 60

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480 

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game")

    monsters = []
    coins = []

    r1 = new_robo()
    blk0= pygame.Surface((SCREEN_WIDTH, 20))
    blk0 = Block(blk0)
    blk0.rect = blk0.surf.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT - 10))
    blk0.moving = False

    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    all_sprites.add(r1)
    all_sprites.add(blk0)
    blocks.add(blk0)

    for blk in range(random.randint(5, 7)):
        block_gen()
        
    
    game_loop()    