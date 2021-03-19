from cmu_112_graphics import *
import time,random



#This file contains all the information for the 3 enemy classes(enemy,ranged.mortar),
# as well as the fireabll and rock classes which the enemies use


class Enemy():
    def __init__(self, health, position, app):
        self.x = position[0]
        self.y = position[1]
        self.initialHealth = health
        self.health = health
        self.dead = False
        self.damage = 60

        #initialize the move sprites
        self.fmoveSprite = app.app.fmoveSprite
        self.bmoveSprite = app.app.bmoveSprite

        #initialize the ghost move sprites
        self.fghostmoveSprite = app.app.fghostmoveSprite
        self.bghostmoveSprite = app.app.bghostmoveSprite

        #initialize the attack sprites
        self.attackSprites = app.app.attackSprites
        

        #backward attack sprites 
        self.attackRSprites = app.app.attackRSprites
        
        
        self.attackSpritesCounter = 0
        self.isAttacking = False
        self.attackTime = time.time()
        self.isGhost = True
        self.canHit = False
        self.orientation = 'Backward'
        
    #Changes the health of the enemy, and kills it if it's below 0
    def changeHealth(self, damage, app):
        if not self.dead:
            self.health -= damage
            if self.health <= 0:
                self.dead = True
                app.enemies.remove(self)
                app.app.score += 80

    def distance(self,x0,y0,x1,y1):
        return ((x1-x0)**2 + (y1-y0)**2)**0.5
    
    #If within range, attacks the player
    def attack(self, app):
        if not self.dead:
            if self.distance(self.x, self.y, app.player.x, app.player.y) <= 25:
                #Cooldown
                if time.time() - self.attackTime > 2:
                    self.attackTime = time.time()
                    app.player.changeHealth(self.damage)
                    self.attackSpritesCounter += 1
    
    #Moves the enemy towards the player
    def move(self, app):
        if not self.dead:
            dist = self.distance(app.player.x, app.player.y, self.x, self.y)
            tempx,tempy = self.x,self.y
            dx = app.player.x - self.x
            dy = app.player.y - self.y
            self.x += dx/30
            self.y += dy/30

            if self.x < app.player.x:
                self.orientation = 'Forward'
            else:
                self.orientation = 'Backward'
            
            erow, ecol = app.getCell(self.x,self.y)
            #Toggles the ghost mode of the enemy
            if (erow,ecol) in app.positions or dist > 200:
                self.isGhost = True
                self.canHit = False
            elif dist <= 200:
                self.isGhost = False
                self.canHit = True
            self.attack(app)

    #Draws the enemy in the correct orientation
    def drawEnemy(self, canvas, scroll):
        if not self.dead:
            if self.isAttacking:
                if self.orientation == 'Forward':
                    sprite = self.attackSprites[self.attackSpritesCounter%len(self.attackSprites)]
                    canvas.create_image(self.x-scroll, self.y, image = ImageTk.PhotoImage(sprite))
                else:
                    sprite = self.attackRSprites[self.attackSpritesCounter%len(self.attackRSprites)]
                    canvas.create_image(self.x-scroll, self.y, image = ImageTk.PhotoImage(sprite))
                    
            elif self.isGhost:
                if self.orientation == 'Forward':
                    sprite = self.fghostmoveSprite
                    canvas.create_image(self.x,self.y, image = ImageTk.PhotoImage(sprite) )
                    
                else:
                    sprite = self.bghostmoveSprite
                    canvas.create_image(self.x-scroll,self.y, image = ImageTk.PhotoImage(sprite) )
            else:
                sprite = self.fmoveSprite if self.orientation == 'Forward' else self.bmoveSprite
                canvas.create_image(self.x-scroll,self.y, image = ImageTk.PhotoImage(sprite))
            healthbar = 60 * self.health//self.initialHealth
            canvas.create_rectangle(self.x-25-scroll, self.y-35, 
                                self.x-25-scroll + healthbar, self.y-25,
                                fill = 'chartreuse2', width= 0)

class Rock():
    def __init__(self,x,y,dx,dy,origin,app):
        #Initializes position and direction
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.damage = 80
        self.hit = False
        self.origin = origin

    def move(self,app):
        #disappears after 5 seconds
        if time.time() - self.origin.attackTime > 5:
            self.origin.rocks = 0
        else:
            tempx,tempy = self.x,self.y
            self.x += (self.dx/10)
            self.y += (self.dy/10)
            brow, bcol = app.getCell(self.x,self.y)
            #Goes out of bounds
            if (self.x < 0 or self.x > app.width + app.extra or self.y < 0 or self.y > app.height):
                self.hit = True
                self.origin.rocks = 0
            #Colision with player
            elif app.player.distance(self.x, self.y, app.player.x, app.player.y) <= 25:
                app.player.changeHealth(self.damage)
                self.hit = True
                self.origin.rocks = 0
            elif (brow,bcol) in app.positions:
                #Ricochet the rock
                x0,y0,x1,y1 = app.getCellBounds(brow,bcol)
                #rock is above or below the cell
                if (self.y - self.dy/10) <= y0 or (self.y-self.dy/10) >= y1:
                    self.dy = -1*self.dy
                #rock is right or left the cell
                elif (self.x-self.dx/10) <= x0 or (self.x-self.dx/10) >= x1:
                    self.dx = -1*self.dx

class Ranged(Enemy):

    def __init__(self, health, position, app):
        #initializes the ranged enemy
        self.x = position[0]
        self.y = position[1]
        self.initialHealth = health
        self.health = health
        self.dead = False
        self.orientation = 'Backward'
        self.fSprite = app.app.fRangedSprite
        self.bSprite = app.app.bRangedSprite
        self.rockSprite = app.app.rockSprite
        self.rocks = 0
        self.canHit = True

    def move(self, app):
        #Flips orientation of the enemy 
        if not self.dead:
            if app.player.x - self.x <= 0:
                self.orientation = 'Backward'
            else:
                self.orientation = 'Forward'
            
            self.attack(app)

    def attack(self, app):
        if not self.dead:
            #Throws a rock at the player if no rock exists, or moves an existing rock
            if self.rocks == 0:
                self.attackTime = time.time()
                dx = app.player.x - self.x
                dy = app.player.y - self.y  
                self.rock = Rock(self.x +dx/50,self.y+dy/50,dx,dy,self,app)
                self.rocks = 1
            else:
                self.rock.move(app)

        
    #Draws the enemy
    def drawEnemy(self,canvas,scroll):
        if not self.dead:
            if self.orientation == 'Forward':
                canvas.create_image(self.x-scroll, self.y, image=ImageTk.PhotoImage(self.fSprite))
            else:
                canvas.create_image(self.x-scroll, self.y, image=ImageTk.PhotoImage(self.bSprite))
            
            healthbar = 60 * self.health//self.initialHealth
            canvas.create_rectangle(self.x-25-scroll, self.y-35, 
                                self.x-25-scroll + healthbar, self.y-25,
                                fill = 'chartreuse2', width= 0)
            
            if self.rocks == 1:
                canvas.create_image(self.rock.x-scroll, self.rock.y, image = ImageTk.PhotoImage(self.rockSprite))

class Fireball():
    def __init__(self,x,y,origin,target,app):
        #Initializes the position and direction of fireball
        self.x = x
        self.y = y
        self.origin = origin
        self.target = target
        self.picture = app.app.fireballSprite
        self.launchTime = time.time()

    def move(self,app):
        #shoot straight up and leave the screen in 2 seconds using d =rt, so r= d/t
        if time.time() - self.launchTime <= 2:
            distance = -100 - self.y
            timeNeeded = 4 
            dy = distance/timeNeeded
            self.y += dy
        #stay in the air for 2 seconds, and come back down in 2 seconds
        elif time.time() - self.launchTime >= 4:
            distance = self.target[1] -self.y
            timeNeeded = 2 
            self.x = self.target[0]
            dy = distance/timeNeeded
            self.y += dy
        #If it lands, calculate the damage done ot player if player is nearby
        if self.x == self.target[0] and self.target[1] -10 <= self.y <= self.target[1] + 10:
            dist = app.player.distance(self.x,self.y,app.player.x,app.player.y)
            self.origin.fireballs = 0
            if dist <= 30:
                #The closer you are to the center, more damage taken
                damage = 500 - int((dist**2)//3)
                app.player.changeHealth(damage)
               
class Mortar(Enemy):

    def __init__(self,health,position,app):
        #Initializes the Mortar enemy
        self.x = position[0]
        self.y = position[1]
        self.dead = False
        self.health = health
        self.initialHealth = health
        self.sprite = app.app.mortarSprite
        self.attackTime = time.time()
        self.fireballs = 0
        self.canHit = True


    def move(self, app):
        if not self.dead:
            self.attack(app)
    
    def attack(self, app):
        #launch an attack that throws a bomb into an area of radius 50
        if not self.dead:
            #Creates a fireball or moves an existing one
            if self.fireballs == 0:
                #Cooldown on the attack
                if time.time() - self.attackTime > 5:
                    self.attackTime = time.time()
                    targetx = app.player.x + random.randint(-40,40)
                    targety = app.player.y + random.randint(-40,40)
                    self.fireball = Fireball(self.x,self.y, self, (targetx, targety), app )
                    self.fireballs = 1
            else:
                self.fireball.move(app)

    #Draws the mortar
    def drawEnemy(self, canvas,scroll):
        if not self.dead:
            canvas.create_image(self.x-scroll, self.y, image = ImageTk.PhotoImage(self.sprite))
            healthbar = 60 * self.health//self.initialHealth
            canvas.create_rectangle(self.x-25-scroll, self.y-35, 
                                self.x-25-scroll + healthbar, self.y-25,
                                fill = 'chartreuse2', width= 0)
            if self.fireballs == 1:
                canvas.create_image(self.fireball.x - scroll, self.fireball.y, 
                            image = ImageTk.PhotoImage(self.fireball.picture))
                canvas.create_oval(self.fireball.target[0]-25-scroll, self.fireball.target[1]-25,
                                    self.fireball.target[0]+25-scroll, self.fireball.target[1]+25, 
                                                                fill ='coral2')
                canvas.create_oval(self.fireball.target[0]-20-scroll, self.fireball.target[1]-20,
                                    self.fireball.target[0]+20-scroll, self.fireball.target[1]+20,
                                    fill = 'white')
                canvas.create_oval(self.fireball.target[0]-5-scroll, self.fireball.target[1]-5,
                                    self.fireball.target[0]+5-scroll, self.fireball.target[1]+5,
                                                        fill = 'coral2')



        
