import os
import sys
import math
import pygame as pg

#Space Game!
#Based on pygame-samples by Mekire (https://github.com/Mekire)


pg.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pg.font.SysFont('Comic Sans MS', 30)

CAPTION="FUCK"
SCREEN_SIZE = (1303, 719)

TRANSPARENT = (0, 0, 0, 0)

DIRECT_DICT = {pg.K_a: (-1, 0),
               pg.K_d: (1, 0),
               pg.K_w: (0,-1),
               pg.K_s: (0, 1)}

ANGLE_UNIT_SPEED = math.sqrt(2)/2

MODSIZE=(20,20)

neighborCheck=False
prototypes=0

class eatCircle(pg.sprite.Sprite):
    SIZE=(50,50)
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.colliding="0"
        self.x=x
        self.y=-y
        self.distX=0
        self.distY=0
        self.rect=pg.Rect((0,0), eatCircle.SIZE)
        self.image=self.make_image()
        self.mask=self.make_mask()

    def make_image(self, color="red"):
        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        pg.draw.ellipse(image, pg.Color("black"), image_rect)
        pg.draw.ellipse(image, pg.Color(color), image_rect.inflate(-12, -12))
        return image

    def make_mask(self):
        mask = pg.mask.from_surface(self.image)
        self.rect=self.image.get_rect()
        olist = mask.outline()
        pg.draw.lines(self.image,pg.Color("green"),1,olist)
        return mask

    def update(self, playerX, playerY, mods):
        self.distX=self.x-playerX
        self.distY=self.y+playerY
        self.printX=self.screen_rect.center[0]+self.distX
        self.printY=self.screen_rect.center[1]+self.distY
        self.rect.center=(self.printX,self.printY)
        if pg.sprite.spritecollide(self, mods, False):
            self.kill()
            global prototypes, neighborCheck
            prototypes+=1
            neighborCheck=True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class myShip(object):
    def __init__(self, center, speed):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.x=0
        self.y=0
        self.speed=speed
        self.degLast=0
        self.lastVecNonZero=(0,-1)

    def update(self, screen_rect, keys, dt):
        vector = [0, 0]
        for key in DIRECT_DICT:
            if keys[key]:
                vector[0] += DIRECT_DICT[key][0]
                vector[1] += DIRECT_DICT[key][1]
        factor = (ANGLE_UNIT_SPEED if all(vector) else 1)
        frame_speed = self.speed*factor*dt
        self.x += vector[0]*frame_speed
        self.y -= vector[1]*frame_speed

class mod(pg.sprite.Sprite):

    def __init__(self, x, y, typ, size=MODSIZE):
        pg.sprite.Sprite.__init__(self)
        self.typ=typ
        self.layout_x=x
        self.layout_y=-y
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.size=size
        self.rect=pg.Rect((0,0), size)
        self.image=self.make_image()
        self.mask=self.make_mask()
        self.rect.center=self.findPosition()
        self.firing=False
        self.neighbors = {"top":None, "left":None, "right":None, "bot":None}

    def findPosition(self):
        return (self.screen_rect.center[0]+self.layout_x*self.size[0],self.screen_rect.center[1]+self.layout_y*self.size[1])

    def make_image(self):
        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()

        if self.typ[0]=="struct":
            pg.draw.rect(image, pg.Color("black"), image_rect)
            pg.draw.rect(image, pg.Color("red"), image_rect.inflate(-12, -12))
        elif self.typ[0]=="thrust":
            pg.draw.rect(image,pg.Color("black"), image_rect)
            pg.draw.rect(image, pg.Color("white"), image_rect.inflate(-12, -12))
        elif self.typ[0]=="prot":
            pg.draw.rect(image,pg.Color("black"), image_rect)
            pg.draw.rect(image, pg.Color("green"), image_rect.inflate(-12, -12))

        return image

    def make_mask(self):
        mask = pg.mask.from_surface(self.image)
        self.rect=self.image.get_rect()
        return mask

    def update(self, keys, mods):
        vector = [0, 0]
        for key in DIRECT_DICT:
            if keys[key]:
                vector[0] += DIRECT_DICT[key][0]
                vector[1] -= DIRECT_DICT[key][1]
        if self.typ[0]=="flame":
            if self.typ[1]=="down":
                if self.firing==False:
                    if vector[1]<0:
                        self.thrust(True,"down")
                else:
                    if vector[1]>=0:
                        self.thrust(False,"down")
            elif self.typ[1]=="up":
                if self.firing==False:
                    if vector[1]>0:
                        self.thrust(True,"up")
                else:
                    if vector[1]<=0:
                        self.thrust(False,"up")
            elif self.typ[1]=="left":
                if self.firing==False:
                    if vector[0]<0:
                        self.thrust(True,"left")
                else:
                    if vector[0]>=0:
                        self.thrust(False,"left")
            elif self.typ[1]=="right":
                if self.firing==False:
                    if vector[0]>0:
                        self.thrust(True,"right")
                else:
                    if vector[0]<=0:
                        self.thrust(False,"right")

        global neighborCheck, prototypes
        if neighborCheck:
            self.neighborCheck(mods)

    def neighborCheck(self, mods):
        modList=mods.sprites()
        for i in modList: #MAKE SURE THE OTHER COORDINATE IS THE SAME!!!!!
            if i.layout_x-self.layout_x==1 and i.layout_y==self.layout_y:
                self.neighbors["right"]=True
            if i.layout_x-self.layout_x==-1 and i.layout_y==self.layout_y:
                self.neighbors["left"]=True
            if i.layout_y-self.layout_y==-1 and i.layout_x==self.layout_x:
                self.neighbors["top"]=True
            if i.layout_y-self.layout_y==1 and i.layout_x==self.layout_x:
                self.neighbors["bot"]=True

    def thrust(self, firing, direct):
        self.firing= not self.firing
        image = pg.Surface(self.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        image_rect = image_rect.inflate(-6,-6)

        if firing:
            if direct=="down":
                pg.draw.polygon(image, pg.Color("red"), (image_rect.bottomleft, image_rect.midtop, image_rect.bottomright))
            elif direct == "up":
                pg.draw.polygon(image, pg.Color("red"), (image_rect.topleft, image_rect.midbottom, image_rect.topright))
            elif direct == "left":
                pg.draw.polygon(image, pg.Color("red"), (image_rect.topleft, image_rect.bottomleft, image_rect.midright))
            elif direct == "right":
                pg.draw.polygon(image, pg.Color("red"), (image_rect.topright, image_rect.bottomright, image_rect.midleft))
        else:
            image.fill(pg.Color("white"))
        self.image=image

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class App(object):
    """
    A class to manage our event, game loop, and overall program flow.
    """
    def __init__(self):
        """
        Get a reference to the display surface; set up required attributes;
        and create a Player instance.
        """
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60
        self.done = False
        self.keys = pg.key.get_pressed()
        self.player = myShip(self.screen_rect.center, 100)
        self.objects = self.make_objects()
        self.mods = self.make_mods()

    def make_objects(self):
        #objects = [randomObject(400,400), randomObject(300,270), randomObject(150,170)]
        #objects.append(randomObject(0,150))
        objects=[eatCircle(0,300)]
        return pg.sprite.Group(objects)

    def make_mods(self):
        mods=[mod(-2,0,["flame","right"]),mod(-1,1, ["flame","down"]),mod(-1,0,["thrust",""]),mod(0,0,["struct",""]),mod(1,0,["thrust",""]),mod(2,0,["flame","left"]), mod(1,-1, ["flame", "up"])]
        return pg.sprite.Group(mods)

    def event_loop(self):
        """
        One event loop. Never cut your game off from the event loop.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type in (pg.KEYUP, pg.KEYDOWN):
                self.keys = pg.key.get_pressed()

    def render(self):
        """
        Perform all necessary drawing and update the screen.
        """
        self.screen.fill(pg.Color("white"))
        self.objects.draw(self.screen)
        self.mods.draw(self.screen)
        textsurface_x = myfont.render('x:' + str(self.player.x), False, (0, 0, 0))
        self.screen.blit(textsurface_x,(0,0))
        textsurface_y = myfont.render('y:' + str(self.player.y), False, (0, 0, 0))
        self.screen.blit(textsurface_y,(0,30))

        pg.display.update()

    def main_loop(self):
        """
        One game loop. Simple and clean.
        """
        self.clock.tick(self.fps)/1000.0
        dt = 0.0
        while not self.done:
            self.event_loop()
            self.player.update(self.screen_rect, self.keys, dt)
            self.mods.update(self.keys, self.mods)
            global neighborCheck, prototypes
            if neighborCheck:
                neighborCheck=False
            if prototypes:
                modList=self.mods.sprites()
                for i in modList:
                    if not (i.typ[0]=="prot" or i.typ[0]=="flame"):
                        if not i.neighbors["top"]:
                            self.mods.add(mod(i.layout_x, i.layout_y+1, ["prot",""]))
                        if not i.neighbors["bot"]:
                            self.mods.add(mod(i.layout_x, i.layout_y-1, ["prot",""]))
                        if not i.neighbors["right"]:
                            self.mods.add(mod(i.layout_x+1, i.layout_y, ["prot",""]))
                        if not i.neighbors["left"]:
                            self.mods.add(mod(i.layout_x-1, i.layout_y, ["prot",""]))
            self.objects.update(self.player.x, self.player.y, self.mods)

            self.render()
            dt = self.clock.tick(self.fps)/1000.0


def main():

    global S_UP, S_UPLEFT, S_LEFT, S_DOWNLEFT, S_DOWN, S_DOWNRIGHT, S_RIGHT, S_UPRIGHT
    """
    Prepare our environment, create a display, and start the program.
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)

    S_UP = pg.image.load("t_up.png").convert_alpha()
    S_UPLEFT = pg.image.load("t_upLeft.png").convert_alpha()
    S_LEFT = pg.image.load("t_left.png").convert_alpha()
    S_DOWNLEFT = pg.image.load("t_downLeft.png").convert_alpha()
    S_DOWN = pg.image.load("t_down.png").convert_alpha()
    S_DOWNRIGHT = pg.image.load("t_downRight.png").convert_alpha()
    S_RIGHT = pg.image.load("t_right.png").convert_alpha()
    S_UPRIGHT = pg.image.load("t_upRight.png").convert_alpha()



    App().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
