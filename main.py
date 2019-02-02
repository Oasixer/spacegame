import os
import sys
import math
import random
import pygame as pg

#Space Game!
#Based on pygame-samples by Mekire (https://github.com/Mekire)


pg.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pg.font.SysFont('Comic Sans MS', 30)

CAPTION="FUCK"
SCREEN_SIZE = (1303, 719)
NUM_PROT_UPGRADES=3
TRANSPARENT = (0, 0, 0, 0)

DIRECT_DICT = {pg.K_a: (-1, 0),
               pg.K_d: (1, 0),
               pg.K_w: (0,-1),
               pg.K_s: (0, 1)}
FIRE_KEY=pg.K_SPACE

ACTIVE_BOX=800

SHIPSPEED = 500
ANGLE_UNIT_SPEED = math.sqrt(2)/2

MODSIZE=(20,20)

add_mod={"nCheck":False, "nProts":0, "killAll":False, "typ":"", "x":0, "y":0, "protsDispl":False, "add":False, "direct":"up"}
mx=0
my=0
gobble={"x":0,"y":0,"add":False,"typ":"", "diam":30}
status="original"
add_enemy={"add":True, "lvl": 0}

class Eat_Circle(pg.sprite.Sprite):
    def __init__(self, x, y, diam=30, type_one_param="struct"):
        pg.sprite.Sprite.__init__(self)
        self.x=x
        self.y=-y
        self.dist_x=0
        self.dist_y=0
        self.diam=diam
        self.rect=pg.Rect((0,0), (diam,diam))
        self.type_one_param=type_one_param
        self.image=self.make_image()
        self.mask=self.make_mask()

    def make_image(self):

        if self.type_one_param=="struct":
            color="red"
        elif self.type_one_param=="gun0":
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

    def update(self, mods, projectiles):
        self.dist_x=self.x-Player.get_x()
        self.dist_y=self.y+Player.get_y()
        self.print_x=App.SCREEN_RECT.center[0]+self.dist_x
        self.print_y=App.SCREEN_RECT.center[1]+self.dist_y
        self.rect.center=(self.print_x,self.print_y)
        global ACTIVE_BOX
        if pg.sprite.spritecollide(self, mods, False):# or pg.sprite.spritecollide(self,projectiles,False):
            global add_mod, gobble
            gobble["add"]=True
            gobble["x"]=self.x
            gobble["y"]=-self.y+200
            gobble["diam"]=self.diam
            gobble["typ"]=self.type_one_param
            add_mod["nProts"]+=1
            add_mod["nCheck"]=True
            add_mod["typ"]=self.type_one_param
            App.enemies.add(Enemy(0, 100, Player.level))
            #print("gobbled. typ="+self.typ+"x,y="+str(self.x)+", "+str(self.y))
            #print ("stat: "+status+".Gobble killing self. nCheck=True. Prots(just added):"+str(addMod["nProts"])+"\n") #DEBUG
            self.kill()
        elif abs(self.dist_x)>ACTIVE_BOX or abs(self.dist_y)>ACTIVE_BOX:
            gobble["add"]=True
            gobble["x"]=self.x
            gobble["y"]=-self.y+200
            gobble["diam"]=self.diam
            gobble["typ"]=self.type_one_param
            self.kill()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(object):
    x=0
    y=0
    level=0
    def __init__(self, center, speed):
        self.speed=speed
        self.degLast=0
        self.lastVecNonZero=(0,-1)

    def update(self, keys, dt):
        vector = [0, 0]
        for key in DIRECT_DICT:
            if keys[key]:
                vector[0] += DIRECT_DICT[key][0]
                vector[1] += DIRECT_DICT[key][1]
        factor = (ANGLE_UNIT_SPEED if all(vector) else 1)
        frame_speed = self.speed*factor*dt
        Player.x += vector[0]*frame_speed
        Player.y -= vector[1]*frame_speed

    @classmethod
    def get_x(cls):
        return Player.x

    @classmethod
    def get_y(cls):
        return Player.y

class Projectile(pg.sprite.Sprite):
    def __init__(self, x, y, diam, time, speed_factor, type_one_param="bullet", direct_vect=(0,0), center=None):
        #REMEMBER TO MOVE THE INPUTS FROM DIRECT STRING TO DIRECT VECT
        global MODSIZE
        pg.sprite.Sprite.__init__(self)
        #print("projectile created. x="+str(x)+", y="+str(y))
        self.speed_factor=speed_factor
        self.init_time=time
        self.type_one_param=type_one_param
        self.diam=diam
        if direct_string=="up":
            self.direct_vect=(0,1)
        elif direct_string=='down':
            self.direct_vect=(0,-1)
        elif direct_string=='left':
            self.direct_vect=(1,0)
        elif direct_string=='right':
            self.direct_vect=(-1,0)
        else:
            self.direct_vect=direct_vect
        self.dist_x=0
        self.dist_y=0
        self.rect=pg.Rect((0,0), (diam,diam))
        self.image=self.make_image()
        self.mask=self.make_mask()
        if direct_string:
            self.rect.center=(int(App.SCREEN_RECT.center[0]+Player.get_x()+(x-self.direct_vect[0])*MODSIZE[0]), int(App.SCREEN_RECT.center[1]-Player.get_y()+(-y-self.direct_vect[1])*MODSIZE[1]))
        else:
            self.rect.center=center
            print("particle c" +str(center[0]) + ", " +str(center[1]))
        self.origin=self.rect.center

    def make_image(self):

        if self.type_one_param=="bullet":
            color="blue"
        else:
            color="green"

        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        pg.draw.ellipse(image, pg.Color(color), image_rect)
        pg.draw.ellipse(image, pg.Color(color), image_rect.inflate(self.diam/3,self.diam/3))
        return image

    def make_mask(self):
        mask = pg.mask.from_surface(self.image)
        return mask

    def update(self, time):
        factor= (time - self.init_time)*self.speed_factor
        self.dist_x=int(Player.x+self.direct_vect[0]*factor)
        self.dist_y=int(Player.y-self.direct_vect[1]*factor)
        self.print_x=self.origin[0]-self.dist_x
        self.print_y=self.origin[1]+self.dist_y
        self.rect.center=(self.print_x,self.print_y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Enemy(pg.sprite.Sprite):
    number_of_enemies=0
    def __init__(self, init_x_rel, init_y_rel, level):
        pg.sprite.Sprite.__init__(self)
        global ENEMY_DATA
        self.level=level+1
        self.move_speed=self.level#TODO:USE
        self.gun_type=self.level#TEMP
        self.image=ENEMY_DATA[0][self.level][0]
        self.rect=ENEMY_DATA[1][self.level]
        self.accel_vec=[0,0]
        p_x, p_y = Player.get_x(), Player.get_y()
        self.r_x, self.r_y = init_x_rel, init_y_rel
        self.e_x, self.e_y = p_x + self.r_x, p_y + self.r_y
        c_x, c_y = App.SCREEN_RECT.centerx, App.SCREEN_RECT.centery
        self.print_x = c_x + self.r_x
        self.print_y = c_y - self.r_y
        self.rect.center=(self.print_x,self.print_y)
        self.rotation_angle=0
        self.move_vec=[0,0]
        self.p=0.0005
        self.d=0
        self.projectile_diameter=7
        self.projectile_speed=0
        self.projectile_type="bullet"
        print("created lvl:"+str(self.level)+" x:"+str(self.e_x)+"y"+str(self.e_y))

    def update(self):
        self.move()
        self.rotate_image()
        self.shoot()
        #print("updated. x:"+str(self.rel_x)+", "+str(self.print_x)+", y"+str(self.rel_y)+", "+str(self.print_y))
        #self.check_boundaries()

    def get_dist(self, vector):
        return math.sqrt(vector[0]**2+vector[1]**2)

    def move(self):
        r_x_last=self.r_x
        r_y_last=self.r_y
        p_x=Player.get_x()
        p_y=Player.get_y()
        self.r_x, self.r_y = self.e_x-p_x, self.e_y-p_y

        px=self.p*-self.r_x
        dx=self.d*-(self.r_x-r_x_last)
        py=self.p*-self.r_y
        dy=self.d*-(self.r_y-r_y_last)

        accel_vec=[px+dx, py+dy]
        if accel_vec[0]>3:
            accel_vec[0]=3
        elif accel_vec[0]< -3:
            accel_vec[0]=-3
        if accel_vec[1]>3:
            accel_vec[1]=3
        elif accel_vec[1]< -3:
            accel_vec[1]=-3

        #print("accel vec:" + str(accel_vec))

        self.move_vec[0]+=accel_vec[0]
        self.move_vec[1]+=accel_vec[1]
        self.accel_vec=accel_vec
        #TEMP
        #self.move_vec=[px-dx,py-dy]



        self.e_x+=self.move_vec[0]#TODO, UPDATE MOVE VEC FIRST
        self.e_y+=self.move_vec[1]#TODO, UPDATE MOVE VEC FIRST
        p_x, p_y = Player.get_x(), Player.get_y()
        c_x, c_y = App.SCREEN_RECT.centerx, App.SCREEN_RECT.centery
        self.print_x = c_x + self.r_x
        self.print_y = c_y - self.r_y
        self.rect.centerx=self.print_x
        self.rect.centery=self.print_y
        print("enemy c:" + str(self.rect.centerx) + ", " + str(self.rect.centery))

    def rotate_image(self):
        angle=int(round(math.degrees(math.atan2(self.accel_vec[1],self.accel_vec[0]))))
        angle-=0
        if angle<0:
            angle+=360
        global ENEMY_DATA
        self.image=ENEMY_DATA[0][self.level][angle]
        center=self.rect.center
        self.rect=self.image.get_rect()
        self.rect.center=center
        #TEMPORARY

    def shoot(self):
        App.projectiles.add(Projectile(0,0, self.projectile_diameter, "", pg.time.get_ticks(), self.projectile_speed, self.projectile_type, (self.accel_vec[0]/self.get_dist(self.accel_vec),self.accel_vec[1]/self.get_dist(self.accel_vec)), self.rect.center))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Mod(pg.sprite.Sprite):
    def __init__(self, layout_x, layout_y, type_two_param, size=MODSIZE):
        pg.sprite.Sprite.__init__(self)
        self.type_two_param=type_two_param
        #if typ[0]=="struct":
            #print("adding struct: layX="+str(x)+", layY="+str(y))
        self.layout_x=layout_x
        self.layout_y=layout_y
        self.size=size
        self.rect=pg.Rect((0,0), size)
        self.rect.center=self.find_position()
        self.image=self.make_image()
        self.mask=self.make_mask()
        self.rect.center=self.find_position()
        self.firing=False
        self.neighbors = {"top":None, "left":None, "right":None, "bot":None}
        self.last_shot_time=0
        self.add_shot={"add":False, "origin_Layout":(0,0), "typ":"", "diam":0, "direct":"", "speedFactor":10}
        self.priority=""

    def find_position(self):
        return (App.SCREEN_RECT.center[0]+self.layout_x*self.size[0],App.SCREEN_RECT.center[1]-self.layout_y*self.size[1])

    def make_image(self):
        image = pg.Surface(self.rect.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        #print("imaging")

        if self.type_two_param[0]=="struct":
            pg.draw.rect(image, pg.Color("black"), image_rect)
            pg.draw.rect(image, pg.Color("red"), image_rect.inflate(-int(self.size[0]/2), -int(self.size[1]/2)))

        elif self.type_two_param[0]=="thrust":
            pg.draw.rect(image,pg.Color("black"), image_rect)
            pg.draw.rect(image, pg.Color("white"), image_rect.inflate(-int(self.size[0]/2), -int(self.size[1]/2)))

        elif self.type_two_param[0]=="prot":
            pg.draw.rect(image,pg.Color("gray"), image_rect)
            pg.draw.rect(image, pg.Color("green"), image_rect.inflate(-int(self.size[0]/3), -int(self.size[1]/3)))

        elif self.type_two_param[0]=="gun0":
            pg.draw.rect(image,pg.Color("gray"), image_rect)

        return image

    def make_mask(self):
        mask = pg.mask.from_surface(self.image)
        self.rect=self.image.get_rect()
        return mask

    def update(self, keys, mods, time):
        vector = [0, 0]
        for key in DIRECT_DICT:
            if keys[key]:
                vector[0] += DIRECT_DICT[key][0]
                vector[1] -= DIRECT_DICT[key][1]
        if self.type_two_param[0]=="flame":
            if self.type_two_param[1]=="down":
                if self.firing==False:
                    if vector[1]<0:
                        self.thrust(True,"down")
                else:
                    if vector[1]>=0:
                        self.thrust(False,"down")
            elif self.type_two_param[1]=="up":
                if self.firing==False:
                    if vector[1]>0:
                        self.thrust(True,"up")
                else:
                    if vector[1]<=0:
                        self.thrust(False,"up")
            elif self.type_two_param[1]=="left":
                if self.firing==False:
                    if vector[0]<0:
                        self.thrust(True,"left")
                else:
                    if vector[0]>=0:
                        self.thrust(False,"left")
            elif self.type_two_param[1]=="right":
                if self.firing==False:
                    if vector[0]>0:
                        self.thrust(True,"right")
                else:
                    if vector[0]<=0:
                        self.thrust(False,"right")

        elif self.type_two_param[0]=="gun0":
            #print("i am a gun facing: "+self.typ[1])
            global FIRE_KEY
            if keys[FIRE_KEY] and time-self.last_shot_time>300:
                #print("FIREKEY DETECTED")
                self.add_shot["add"]=True
                self.add_shot["direct"]=self.type_two_param[1]
                self.add_shot["origin_Layout"]=(self.layout_x,self.layout_y)
                self.add_shot["typ"]="bullet"
                self.add_shot["diam"]=10
                self.add_shot["speedFactor"]=0.3
                self.last_shot_time=time

        global add_mod
        if add_mod["nCheck"] and not self.type_two_param[0]=="flame" and not self.type_two_param[0]=="prot":
            self.neighbor_check(mods)
            #print("(NCHECKING)")

        if add_mod["nProts"] and self.type_two_param[0]=="prot":
            self.prototypeWatch(mods)


    def prototypeWatch(self, mods):
        global mx, my, add_mod, status
        mx, my = pg.mouse.get_pos()
        clicks= pg.mouse.get_pressed()

        #c=self.rect.center

        if (mx>(self.rect.centerx-self.size[0]/2)) and (mx < (self.rect.centerx+self.size[0]/2))and (my>(self.rect.centery-self.size[1]/2)) and (my < (self.rect.centery+self.size[1]/2)) and clicks[0]:
            self.neighbor_check(mods, True)
            #print(self.neighbors["bot"])
            #print("\n\njust detected a hover. original status:\n")
            #print ("stat: "+status+". neighCheck="+str(addMod["nCheck"])+" Prots:"+str(addMod["nProts"])+"\n") #DEBUG
            add_mod["nProts"] -= 1
            if not add_mod["nProts"]:
                add_mod["killAll"] = True
            #addMod["nCheck"] = True
            add_mod["x"] = self.layout_x
            add_mod["y"] = self.layout_y
            add_mod["add"] = True

            if self.priority:
                add_mod["direct"]=self.priority
            elif self.neighbors["top"]:
                add_mod["direct"]="down"
            elif self.neighbors["bot"]:
                add_mod["direct"]="up"
            elif self.neighbors["left"]:
                add_mod["direct"]="right"
            else:
                add_mod["direct"]="left"
            #print("y:"+str(self.layout_y))
            status+="-delProt"
            #print("new stat: "+status+". neighCheck="+str(addMod["nCheck"])+". Prots:"+str(addMod["nProts"])+"\n") #DEBUG
            self.kill()

    def neighbor_check(self, mods, rotation_check=False):
        for key in self.neighbors:
            self.neighbors[key]=False
        modList=mods.sprites()
        for i in modList: #MAKE SURE THE OTHER COORDINATE IS THE SAME!!!!!
            if (not rotation_check) or ((not i.type_two_param[0]=="flame") and (not i.type_two_param[0]=="prot")):
                if i.layout_x-self.layout_x==1 and i.layout_y==self.layout_y:
                    self.neighbors["right"]=True
                    if i.type_two_param[0]=="struct" and rotation_check:
                        self.priority="left"
                if i.layout_x-self.layout_x==-1 and i.layout_y==self.layout_y:
                    self.neighbors["left"]=True
                    if i.type_two_param[0]=="struct" and rotation_check:
                        self.priority="right"
                if i.layout_y-self.layout_y==1 and i.layout_x==self.layout_x:
                    self.neighbors["top"]=True
                    if i.type_two_param[0]=="struct" and rotation_check:
                        self.priority="down"
                if i.layout_y-self.layout_y==-1 and i.layout_x==self.layout_x:
                    self.neighbors["bot"]=True
                    if i.type_two_param[0]=="struct" and rotation_check:
                        self.priority="up"
                    #print("Im a "+str(self.typ[0])+" and found a "+str(i.typ[0]))

            #print("done nCheck from: "+i.typ[0]+": " + str(i.layout_x)+", "+str(i.layout_y))
    def thrust(self, firing, direct_string):
        self.firing= not self.firing
        image = pg.Surface(self.size).convert_alpha()
        image.fill(TRANSPARENT)
        image_rect = image.get_rect()
        image_rect = image_rect.inflate(-6,-6)

        if firing:
            if direct_string=="down":
                pg.draw.polygon(image, pg.Color("red"), (image_rect.bottomleft, image_rect.midtop, image_rect.bottomright))
            elif direct_string == "up":
                pg.draw.polygon(image, pg.Color("red"), (image_rect.topleft, image_rect.midbottom, image_rect.topright))
            elif direct_string == "left":
                pg.draw.polygon(image, pg.Color("red"), (image_rect.topleft, image_rect.bottomleft, image_rect.midright))
            elif direct_string == "right":
                pg.draw.polygon(image, pg.Color("red"), (image_rect.topright, image_rect.bottomright, image_rect.midleft))
        else:
            image.fill(pg.Color("white"))
        self.image=image

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#class Background():
#    global BACKGROUND_IMAGE
#    self.image=

class App(object):
    """
    A class to manage our event, game loop, and overall program flow.
    """
    projectiles=pg.sprite.Group()
    enemies=pg.sprite.Group()
    SCREEN=None
    SCREEN_RECT=None
    def __init__(self):
        """
        Get a reference to the display surface; set up required attributes;
        and create a Player instance.
        """
        self.clock = pg.time.Clock()
        App.SCREEN=pg.display.get_surface()
        App.SCREEN_RECT=App.SCREEN.get_rect()
        self.fps = 60
        self.done = False
        self.keys = pg.key.get_pressed()
        global SHIPSPEED
        self.player = Player(App.SCREEN_RECT.center, SHIPSPEED)
        self.objects = self.make_objects()
        self.struct_upgrades = pg.sprite.Group()
        self.generate_struct_upgrades()
        self.mods = self.make_mods()

    def make_objects(self):
        #objects = [randomObject(400,400), randomObject(300,270), randomObject(150,170)]
        #objects.append(randomObject(0,150))
        objects=[Eat_Circle(0,100,30), Eat_Circle(-100,0,30,"gun0")]
        return pg.sprite.Group(objects)

    def generate_struct_upgrades(self):
        global NUM_PROT_UPGRADES
        while(len(self.struct_upgrades.sprites())<NUM_PROT_UPGRADES):
            #print("adding")
            global ACTIVE_BOX
            p_x=int(Player.get_x())
            p_y=int(Player.get_y())
            newObject=Eat_Circle(random.randint(p_x-ACTIVE_BOX, p_x+ACTIVE_BOX), random.randint(p_y-ACTIVE_BOX, p_y+ACTIVE_BOX),30,"struct")
            self.struct_upgrades.add(newObject)
            self.objects.add(newObject)

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
        self.SCREEN.fill(pg.Color("white"))
        self.objects.draw(App.SCREEN)
        self.mods.draw(App.SCREEN)
        App.projectiles.draw(App.SCREEN)
        App.enemies.draw(App.SCREEN)
        global add_mod, mx, my
        textsurface_x = myfont.render('prototypes: '+ str(add_mod["nProts"]), False, (0, 0, 0))
        App.SCREEN.blit(textsurface_x,(0,0))
        #textsurface_y = myfont.render('mx:' + str(mx) + ' my: ' + str(my), False, (0, 0, 0))
        #self.screen.blit(textsurface_y,(0,30))
        pg.display.update()

    def main_loop(self):
        self.clock.tick(self.fps)/1000.0
        dt = 0.0
        while not self.done:
            global add_mod, status, add_enemy
            current_time=pg.time.get_ticks()
            self.event_loop()
            App.enemies.update()
            self.player.update(self.keys, dt)
            self.mods.update(self.keys, self.mods, current_time)
            #print ("stat: "+status+". UPDATING MODS. neighChk:"+str(addMod["nCheck"])+", Prots:"+str(addMod["nProts"])+"\n") #DEBUG

            for mod in self.mods:
                if mod.add_shot["add"]:
                    App.projectiles.add(Projectile(mod.add_shot["origin_Layout"][0],mod.add_shot["origin_Layout"][1],mod.add_shot["diam"],mod.add_shot["direct"], current_time, mod.add_shot["speedFactor"], mod.add_shot["typ"]))
                    mod.add_shot["add"]=False

            App.projectiles.update(current_time)

            if add_mod["nCheck"]:
                add_mod["nCheck"]=False
                #print ("stat: "+status+". Turning off neighborcheck-literally nothing else. Prots:"+str(addMod["nProts"])+"\n") #DEBUG
            if add_mod["nProts"] and not add_mod["protsDispl"]:
                #print ("stat: "+status+". Displaying prots. Just turned neighCheck off. Prots:"+str(addMod["nProts"])+"\n") #DEBUG
                mod_list=self.mods.sprites()
                for i in mod_list:
                    if not (i.type_two_param[0]=="prot" or i.type_two_param[0]=="flame"):
                        if not i.neighbors["top"]:
                            self.mods.add(Mod(i.layout_x, i.layout_y+1, ["prot",""]))
                            #print("adding top from: "+i.typ[0]+": "+ str(i.layout_x)+", "+str(i.layout_y))
                        if not i.neighbors["bot"]:
                            self.mods.add(Mod(i.layout_x, i.layout_y-1, ["prot",""]))
                            #print("adding bot from: "+i.typ[0]+": " + str(i.layout_x)+", "+str(i.layout_y))
                        if not i.neighbors["right"]:
                            self.mods.add(Mod(i.layout_x+1, i.layout_y, ["prot",""]))
                            #print("adding right from: "+i.typ[0]+": " + str(i.layout_x)+", "+str(i.layout_y))
                        if not i.neighbors["left"]:
                            self.mods.add(Mod(i.layout_x-1, i.layout_y, ["prot",""]))
                            #print("adding left from: "+i.typ[0]+": " + str(i.layout_x)+", "+str(i.layout_y))
                        #print("done checking from: "+i.typ[0]+": " + str(i.layout_x)+", "+str(i.layout_y))
                #print("done displaying prots\n")

                add_mod["protsDispl"]=True
                #print ("stat: "+status+". Just displayed prots. Also neighCheck is still off. Prots:"+str(addMod["nProts"])+"\n") #DEBUG
            if add_mod["killAll"]:
                add_mod["protsDispl"]=False
                #print ("stat: "+status+". Killing prots. Also neighCheck is still off. Prots:"+str(addMod["nProts"])+"\n") #DEBUG
                for i in self.mods.sprites():
                    if i.type_two_param[0]=="prot":
                        i.kill()
                    add_mod["killAll"]=False
            if add_mod["add"]:
                status+="+adSeg"
                #print ("ADDING SEGMENT.") #DEBUG
                self.mods.add(Mod(add_mod["x"],add_mod["y"],[add_mod["typ"],add_mod["direct"]]))
                #addMod["nCheck"]=True
                add_mod["typ"]=""
                add_mod["add"]=False
                add_mod["killAll"]=True

            self.objects.update(self.mods, self.projectiles)
            global gobble
            if gobble["add"]:
                if gobble["typ"]=="struct":
                    self.generate_struct_upgrades()
                else:
                    self.objects.add(Eat_Circle(gobble["x"],gobble["y"],gobble["diam"],gobble["typ"]))
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

    ENEMY_IMAGES_BASE=[pg.image.load("enemy_0.png").convert_alpha(),pg.image.load("enemy_1.png").convert_alpha()]
    global ENEMY_DATA

    ENEMY_DATA=[[],[]]
    for enemy_type in range(len(ENEMY_IMAGES_BASE)):
        ENEMY_DATA[0].append([])

    for enemy_type in range(len(ENEMY_IMAGES_BASE)):
        ENEMY_DATA[1].append(ENEMY_IMAGES_BASE[enemy_type].get_rect())
        for angle in range(360):
            ENEMY_DATA[0][enemy_type].append(rot_center(ENEMY_IMAGES_BASE[enemy_type],angle))

    App().main_loop()
    pg.quit()
    sys.exit()

def rot_center(image, angle):
    rect=image.get_rect()
    rot_image = pg.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image

if __name__ == "__main__":

    main()
