import math
from cmu_112_graphics import *
import time

#This file conatins information for the Player and Bullet object

class Player(object):
    x = 0
    y = 0

    def __init__(self, health, x,y, app):
        #initialize the moving sprites
        self.moveSprites = app.app.moveSprites
        self.movespriteCounter = 0

        #initialize the shoot sprites
        self.shootSprites = app.app.shootSprites
        self.shootSpritesCounter = 0

        #initialize the dead sprites
        self.deadSprites = app.app.deadSprites
        self.deadSpritesCounter = 0

        #initialize the end Sprites
        self.endSprites = app.app.endSprites
        self.endSpritesCounter = 0
            
        self.levelCleared = False

        self.isMoving = False
        Player.x = x
        Player.y = y
        self.health = health
        self.dead = False
        
    def __repr__(self):
        return f'player with {self.health} hp'

    @staticmethod
    def distance(x0,y0,x1,y1):
        return ((x1-x0)**2 + (y1-y0)**2)**0.5

    def attack(self, app):
        #Find nearest enemy
        if len(app.enemies) != 0:
            closest = None
            minDistance = 10**10
            for enemy in app.enemies:
                dist = Player.distance(Player.x, Player.y, enemy.x, enemy.y)
                if dist < minDistance:
                    minDistance = dist
                    closest = enemy
            
            dx = closest.x - Player.x
            dy = closest.y - Player.y
            
            #create a weapon that is shooting in that direction
            return Bullet(dx, dy, minDistance, self.x + dx/50, self.y + dy/50, closest,app)
    
    #Changes the health and if its below 0, kills the player
    def changeHealth(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.dead = True

    #Draws the player
    def drawPlayer(self, canvas, scroll):
        if self.dead:
            for deadSprite in self.deadSprites:
            # deadSprite = self.deadSprites[self.deadSpritesCounter%len(self.deadSprites)]
                canvas.create_image(Player.x - scroll,Player.y,image=ImageTk.PhotoImage(deadSprite))
        elif self.isMoving:
            moveSprite = self.moveSprites[self.movespriteCounter%len(self.moveSprites)]
            canvas.create_image(Player.x - scroll, Player.y, image = ImageTk.PhotoImage(moveSprite))
        elif not self.isMoving:
            for shootSprite in self.shootSprites:
                canvas.create_image(Player.x - scroll, Player.y, image = ImageTk.PhotoImage(shootSprite))
        elif self.levelCleared:
            endSprite = self.endSprites[self.endSpritesCounter%len(self.endSprites)]
            canvas.create_image(Player.x - scroll, Player.y, image = ImageTk.PhotoImage(endSprite))

        canvas.create_text(self.x - scroll, self.y-30 , text = f'{self.health} hp', font = 'Arial 10 bold')



class Bullet(object):
    number = 0

    def __init__(self, dx,dy, distance, x, y, enemy,app):
        #Initializes the position and direction of the bullet
        self.distance = distance
        self.dx = dx/8
        self.dy = dy/8
        self.x = x
        self.y = y
        self.target = enemy
        self.hitTarget = False
        self.hitObstacle = False
        self.damage = 50
        self.picture = app.app.bullet
    
    #Moves the bullet and checks for collisions
    def move(self, app):
        self.x = self.x + (self.dx)
        self.y = self.y + (self.dy)
        brow, bcol = app.getCell(self.x,self.y)
        dist = Player.distance(self.x, self.y, self.target.x, self.target.y)
        if  dist <= 35:
            if self.target.canHit:
                self.hitTarget = True
                self.target.changeHealth(self.damage,app)
        elif(self.x < 0 or self.x > app.width + app.extra or self.y < 0 or self.y > app.height
            or (brow,bcol) in app.positions):
            self.hitObstacle = True

    #Draws bullet on screen
    def drawBullet(self, canvas, scroll):
        if not (self.hitObstacle or self.hitTarget):
            canvas.create_image(self.x-scroll, self.y, image = ImageTk.PhotoImage(self.picture))
            


