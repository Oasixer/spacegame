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
               pg.K_d: ( 1, 0),
               pg.K_w: ( 0,-1),
               pg.K_s: ( 0, 1)}

ANGLE_UNIT_SPEED = math.sqrt(2)/2

class myShip(object):
    SIZE = (100, 100)

    def __init__(self, center, speed, direction=pg.K_RIGHT):
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.rect = pg.Rect((0,0), self.SIZE)
        self.rect.center=self.screen_rect.center
        self.image = self.make_image()
        self.x=0
        self.y=0
        self.speed=speed

    def make_mask(self):
        """
        Create a collision mask slightly smaller than our sprite so that
        the sprite's head can overlap obstacles; adding depth.
        """
        mask_surface = pg.Surface(self.rect.size).convert_alpha()
        mask_surface.fill(TRANSPARENT)
        mask_surface.fill(pg.Color("white"), (10,20,30,30))
        mask = pg.mask.from_surface(mask_surface)
        return mask

    def make_image(self):
        """
        Creates our hero (a red circle/ellipse with a black outline).
        """
        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        pg.draw.ellipse(image, pg.Color("black"), image_rect)
        pg.draw.ellipse(image, pg.Color("red"), image_rect.inflate(-12, -12))
        return image

    def draw(self, surface):
        """
        Draws the player to the target surface.
        """
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
        #self.x+=1#TEMPPPPPPPP
        self.y += vector[1]*frame_speed

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
        self.player = myShip(self.screen_rect.center, 190)

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
            self.render()
            dt = self.clock.tick(self.fps)/1000.0


def main():
    """
    Prepare our environment, create a display, and start the program.
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    App().main_loop()
    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()
