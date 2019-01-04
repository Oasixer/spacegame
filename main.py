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

addMod={"nCheck":False, "nProts":0, "killAll":False, "typ":"", "x":0, "y":0, "protsDispl":False}
mx=0
my=0
gobble={"x":0,"y":0,"add":False}

status="original"

class eatCircle(pg.sprite.Sprite):
    SIZE=(50,50)
    def __init__(self, x, y, typ="struct"):
        pg.sprite.Sprite.__init__(self)
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.x=x
        self.y=-y
        self.distX=0
        self.distY=0
        self.rect=pg.Rect((0,0), eatCircle.SIZE)
        self.image=self.make_image()
        self.mask=self.make_mask()
        self.typ=typ

    def make_image(self):

        if self.typ=="struct":
            color="red"
        elif self.typ=="gun0":
            color="blue"

        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        pg.draw.ellipse(image, pg.Color("black"), image_rect)
        pg.draw.ellipse(image, pg.Color(color), image_rect.inflate(-12, -12))
        return image

    def make_mask(self):
        mask = pg.mask.from_surface(self.image)
        self.rect=self.image.get_rect()
        return mask

    def update(self, playerX, playerY, mods):
        self.distX=self.x-playerX
        self.distY=self.y+playerY
        self.printX=self.screen_rect.center[0]+self.distX
        self.printY=self.screen_rect.center[1]+self.distY
        self.rect.center=(self.printX,self.printY)
        if pg.sprite.spritecollide(self, mods, False):
            global addMod, gobble
            gobble["add"]=True
            gobble["x"]=self.x
            gobble["y"]=-self.y+100
            addMod["nProts"]+=1
            addMod["nCheck"]=True
            addMod["typ"]=self.typ
            #print ("stat: "+status+".Gobble killing self. nCheck=True. Prots(just added):"+str(addMod["nProts"])+"\n") #DEBUG
            self.kill()

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

class Projectile(pg.sprite.Sprite):
    def __init__(self, x, y, diam, direct, playerX, playerY, typ="bullet"):
        global MODSIZE
        pg.sprite.Sprite.__init__(self)
        self.screen = pg.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.direct=direct
        self.distX=0
        self.distY=0
        self.rect=pg.Rect((0,0), size)
        self.rect.center=(x*MODSIZE, -y*MODSIZE)
        self.image=self.make_image()
        self.mask=self.make_mask()
        self.typ=typ

    def make_image(self):

        if self.typ=="bullet":
            color="blue"

        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        pg.draw.ellipse(image, pg.Color(color), image_rect)
        pg.draw.ellipse(image, pg.Color(color), image_rect.inflate(self.diam/3,self.diam/3))
        return image

    def make_mask(self):
        mask = pg.mask.from_surface(self.image)
        self.rect=self.image.get_rect()
        return mask

    def update(self, playerX, playerY, mods):
        self.distX=self.x-playerX
        self.distY=self.y+playerY
        self.printX=self.screen_rect.center[0]+self.distX
        self.printY=self.screen_rect.center[1]+self.distY
        self.rect.center=(self.printX,self.printY)
        if pg.sprite.spritecollide(self, mods, False):
            global addMod, gobble
            gobble["add"]=True
            gobble["x"]=self.x
            gobble["y"]=-self.y+100
            addMod["nProts"]+=1
            addMod["nCheck"]=True
            #print ("stat: "+status+".Gobble killing self. nCheck=True. Prots(just added):"+str(addMod["nProts"])+"\n") #DEBUG
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Mod(pg.sprite.Sprite):
    def __init__(self, x, y, typ, size=MODSIZE):
        pg.sprite.Sprite.__init__(self)
        self.typ=typ
        self.layout_x=x
        self.layout_y=y
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
        return (self.screen_rect.center[0]+self.layout_x*self.size[0],self.screen_rect.center[1]-self.layout_y*self.size[1])

    def make_image(self):
        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()

        if self.typ[0]=="struct":
            pg.draw.rect(image, pg.Color("black"), image_rect)
            pg.draw.rect(image, pg.Color("red"), image_rect.inflate(-int(self.size[0]/2), -int(self.size[1]/2)))

        elif self.typ[0]=="thrust":
            pg.draw.rect(image,pg.Color("black"), image_rect)
            pg.draw.rect(image, pg.Color("white"), image_rect.inflate(-int(self.size[0]/2), -int(self.size[1]/2)))

        elif self.typ[0]=="prot":
            pg.draw.rect(image,pg.Color("gray"), image_rect)
            pg.draw.rect(image, pg.Color("green"), image_rect.inflate(-int(self.size[0]/3), -int(self.size[1]/3)))

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
        global addMod
        if addMod["nCheck"] and not self.typ[0]=="flame" and not self.typ[0]=="prot":
            self.neighborCheck(mods)
            #print("(NCHECKING)")

        if addMod["nProts"] and self.typ[0]=="prot":
            self.prototypeWatch()


    def prototypeWatch(self):
        global mx, my, addMod, status
        mx, my = pg.mouse.get_pos()
        clicks= pg.mouse.get_pressed()

        #c=self.rect.center

        if (mx>(self.rect.centerx-self.size[0]/2)) and (mx < (self.rect.centerx+self.size[0]/2))and (my>(self.rect.centery-self.size[1]/2)) and (my < (self.rect.centery+self.size[1]/2)) and clicks[0]:
            #print("\n\njust detected a hover. original status:\n")
            #print ("stat: "+status+". neighCheck="+str(addMod["nCheck"])+" Prots:"+str(addMod["nProts"])+"\n") #DEBUG
            addMod["nProts"] -= 1
            if not addMod["nProts"]:
                addMod["killAll"] = True
            #addMod["nCheck"] = True
            addMod["typ"] = "struct"
            addMod["x"] = self.layout_x
            addMod["y"] = self.layout_y
            status+="-delProt"
            #print("new stat: "+status+". neighCheck="+str(addMod["nCheck"])+". Prots:"+str(addMod["nProts"])+"\n") #DEBUG
            self.kill()

    def neighborCheck(self, mods):
        for key in self.neighbors:
            self.neighbors[key]=False
        modList=mods.sprites()
        for i in modList: #MAKE SURE THE OTHER COORDINATE IS THE SAME!!!!!
            if i.layout_x-self.layout_x==1 and i.layout_y==self.layout_y:
                self.neighbors["right"]=True
            if i.layout_x-self.layout_x==-1 and i.layout_y==self.layout_y:
                self.neighbors["left"]=True
            if i.layout_y-self.layout_y==1 and i.layout_x==self.layout_x:
                self.neighbors["top"]=True
            if i.layout_y-self.layout_y==-1 and i.layout_x==self.layout_x:
                self.neighbors["bot"]=True

            print("done nCheck from: "+i.typ[0]+": " + str(i.layout_x)+", "+str(i.layout_y))
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
        objects=[eatCircle(0,100)]
        return pg.sprite.Group(objects)

    def make_mods(self):
        mods=[Mod(-2,0,["flame","right"]),Mod(-1,1, ["flame","down"]),Mod(-1,0,["thrust",""]),Mod(0,0,["struct",""]),Mod(1,0,["thrust",""]),Mod(2,0,["flame","left"]), Mod(1,-1, ["flame", "up"])]
        return pg.sprite.Group(mods)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type in (pg.KEYUP, pg.KEYDOWN):
                self.keys = pg.key.get_pressed()

    def render(self):
        self.screen.fill(pg.Color("white"))
        self.objects.draw(self.screen)
        self.mods.draw(self.screen)
        global addMod, mx, my
        textsurface_x = myfont.render('neighborCheck: ' + str(addMod["nCheck"]) +', prototypes: '+ str(addMod["nProts"]), False, (0, 0, 0))
        self.screen.blit(textsurface_x,(0,0))
        textsurface_y = myfont.render('mx:' + str(mx) + ' my: ' + str(my), False, (0, 0, 0))
        self.screen.blit(textsurface_y,(0,30))
        pg.display.update()

    def main_loop(self):
        self.clock.tick(self.fps)/1000.0
        dt = 0.0
        while not self.done:
            global addMod, status
            self.event_loop()
            self.player.update(self.screen_rect, self.keys, dt)
            self.mods.update(self.keys, self.mods)
            #print ("stat: "+status+". UPDATING MODS. neighChk:"+str(addMod["nCheck"])+", Prots:"+str(addMod["nProts"])+"\n") #DEBUG
            if addMod["nCheck"]:
                addMod["nCheck"]=False
                #print ("stat: "+status+". Turning off neighborcheck-literally nothing else. Prots:"+str(addMod["nProts"])+"\n") #DEBUG
            if addMod["nProts"] and not addMod["protsDispl"]:
                #print ("stat: "+status+". Displaying prots. Just turned neighCheck off. Prots:"+str(addMod["nProts"])+"\n") #DEBUG
                modList=self.mods.sprites()
                for i in modList:
                    if not (i.typ[0]=="prot" or i.typ[0]=="flame"):
                        if not i.neighbors["top"]:
                            self.mods.add(Mod(i.layout_x, i.layout_y+1, ["prot",""]))
                            print("adding top from: "+i.typ[0]+": "+ str(i.layout_x)+", "+str(i.layout_y))
                        if not i.neighbors["bot"]:
                            self.mods.add(Mod(i.layout_x, i.layout_y-1, ["prot",""]))
                            print("adding bot from: "+i.typ[0]+": " + str(i.layout_x)+", "+str(i.layout_y))
                        if not i.neighbors["right"]:
                            self.mods.add(Mod(i.layout_x+1, i.layout_y, ["prot",""]))
                            print("adding right from: "+i.typ[0]+": " + str(i.layout_x)+", "+str(i.layout_y))
                        if not i.neighbors["left"]:
                            self.mods.add(Mod(i.layout_x-1, i.layout_y, ["prot",""]))
                            print("adding left from: "+i.typ[0]+": " + str(i.layout_x)+", "+str(i.layout_y))
                        print("done checking from: "+i.typ[0]+": " + str(i.layout_x)+", "+str(i.layout_y))
                print("done displaying prots\n")

                addMod["protsDispl"]=True
                #print ("stat: "+status+". Just displayed prots. Also neighCheck is still off. Prots:"+str(addMod["nProts"])+"\n") #DEBUG
            if addMod["killAll"]:
                addMod["protsDispl"]=False
                #print ("stat: "+status+". Killing prots. Also neighCheck is still off. Prots:"+str(addMod["nProts"])+"\n") #DEBUG
                for i in self.mods.sprites():
                    if i.typ[0]=="prot":
                        i.kill()
                    addMod["killAll"]=False
            if addMod["typ"]:
                status+="+adSeg"
                #print ("ADDING SEGMENT. stat: "+status+". neighCheck=True  Prots:"+str(addMod["nProts"])+"\n") #DEBUG
                self.mods.add(Mod(addMod["x"],addMod["y"],[addMod["typ"],""]))
                #addMod["nCheck"]=True
                addMod["typ"]=""

            self.objects.update(self.player.x, self.player.y, self.mods)
            global gobble
            if gobble["add"]:
                self.objects.add(eatCircle(gobble["x"],gobble["y"]))
                gobble["add"]=False
                #addMod["nCheck"]=True
                #print ("stat: "+status+". Adding gobble. neighCheck=True. Prots:"+str(addMod["nProts"])+"\n") #DEBUG
            self.render()
            dt = self.clock.tick(self.fps)/1000.0

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(CAPTION)
    pg.display.set_mode(SCREEN_SIZE)
    App().main_loop()
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
