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
class randomObject(object):
    SIZE=(50,50)
    def __init__(self, x, y):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()

        self.x=x
        self.y=-y
        self.distX=0
        self.distY=0
        self.rect=pg.Rect((0,0), randomObject.SIZE)
        self.image=self.make_image()
        self.mask=self.make_mask()

    def make_image(self):
        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        pg.draw.ellipse(image, pg.Color("black"), image_rect)
        pg.draw.ellipse(image, pg.Color("red"), image_rect.inflate(-12, -12))
        return image

    def make_mask(self):
        """
        Create a collision mask slightly smaller than our sprite so that
        the sprite's head can overlap obstacles; adding depth.
        """
        mask_surface = pg.Surface(self.rect.size).convert_alpha()
        mask_surface.fill(TRANSPARENT)
        mask_surface.fill(pg.Color("white"), (10,20,30,30))
        mask = pg.mask.from_surface(mask_surface)
        self.mask=mask

    def update(self, playerX, playerY):
        self.distX=self.x-playerX
        self.distY=self.y+playerY

        #if distY<screen_rect.top-screen_rect.center:
         #   self.speed=
        self.printX=self.screen_rect.center[0]+self.distX
        self.printY=self.screen_rect.center[1]+self.distY
        self.rect.center=(self.printX,self.printY)

    def draw(self, surface):
        """
        Draws the player to the target surface.
        """
        surface.blit(self.image, self.rect)


class myShip(object):

    def __init__(self, center, speed):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.image = S_UP
        self.rect = self.image.get_rect()
        self.rect.center=self.screen_rect.center
        self.x=0
        self.y=0
        self.speed=speed
        self.degLast=0
        self.lastVecNonZero=(0,-1)
        self.rotated=0
        self.mask=None
        self.make_mask()

    def make_mask(self):
        """
        Create a collision mask slightly smaller than our sprite so that
        the sprite's head can overlap obstacles; adding depth.
        """
        mask_surface = pg.Surface(self.rect.size).convert_alpha()
        mask_surface.fill(TRANSPARENT)
        mask_surface.fill(pg.Color("white"), (10,20,30,30))
        mask = pg.mask.from_surface(mask_surface)
        self.mask=mask

    def draw(self, surface):
        """Draw method seperated out from update."""
        surface.blit(self.image, self.rect)

    def update(self, screen_rect, keys, dt):
        """
        Updates our player appropriately every frame.
        """
        vector = [0, 0]
        for key in DIRECT_DICT:
            if keys[key]:
                vector[0] += DIRECT_DICT[key][0]
                vector[1] += DIRECT_DICT[key][1]
        factor = (ANGLE_UNIT_SPEED if all(vector) else 1)
        frame_speed = self.speed*factor*dt
        self.x += vector[0]*frame_speed
        self.y -= vector[1]*frame_speed

        a=(0,-1)
        if vector[0] or vector[1]:
            b=(vector[0], vector[1])
            self.lastVecNonZero=b
        else:
            b=self.lastVecNonZero
        deg = math.degrees(math.atan2(a[0]*b[1] - a[1]*b[0], a[0]*b[0] + a[1]*b[1] ))

        if (deg != self.degLast):
            self.changeImage(deg)
        self.rotated=deg
        self.degLast=deg

    def changeImage(self, deg):
        if deg==0:
            self.image=S_UP
        elif deg==45:
            self.image=S_UPRIGHT
        elif deg==90:
            self.image=S_RIGHT
        elif deg==135:
            self.image=S_DOWNRIGHT
        elif deg==180:
            self.image=S_DOWN
        elif deg==-45:
            self.image=S_UPLEFT
        elif deg==-90:
            self.image=S_LEFT
        elif deg==-135:
            self.image=S_DOWNLEFT
        self.rect=self.image.get_rect()
        self.rect.center=self.screen_rect.center
        self.make_mask()

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
        self.obj = randomObject(-200,200)
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
        self.player.draw(self.screen)
        self.obj.draw(self.screen)
        textsurface_x = myfont.render('x:' + str(self.player.x), False, (0, 0, 0))
        self.screen.blit(textsurface_x,(0,0))
        textsurface_y = myfont.render('y:' + str(self.player.y), False, (0, 0, 0))
        self.screen.blit(textsurface_y,(0,30))
        textsurface_r = myfont.render('r:' + str(self.player.rotated), False, (0, 0, 0))
        self.screen.blit(textsurface_r,(0,60))


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

            self.obj.update(self.player.x, self.player.y)

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

    S_UP = pg.image.load("up.png").convert()
    S_UPLEFT = pg.image.load("upLeft.png").convert()
    S_LEFT = pg.image.load("left.png").convert()
    S_DOWNLEFT = pg.image.load("downLeft.png").convert()
    S_DOWN = pg.image.load("down.png").convert()
    S_DOWNRIGHT = pg.image.load("downRight.png").convert()
    S_RIGHT = pg.image.load("right.png").convert()
    S_UPRIGHT = pg.image.load("upRight.png").convert()



    App().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
