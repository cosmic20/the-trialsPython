from cmu_112_graphics import *
import random
from Person import Player
from Person import Bullet
from Opponent import Enemy,Ranged,Mortar

#This file contains all the interactions for a level, and is responsible for all the logic inside


#Class for obstacles and the endPiece to the level
class Square():
    width = 50
    def __init__(self, rx,ry,app):
        self.rx = rx
        self.ry = ry
       

#Class for the wall at the start and end of the level
class Wall():
    width = 100
    def __init__(self,x0,y0):
        self.x0 = x0
        self.y0 = y0
    
    def drawWall(self,canvas, app):
        canvas.create_rectangle(self.x0-app.scrollX, self.y0, self.x0+self.width-app.scrollX, app.height,
                    fill = 'black')

#Class for each level
class Level(Mode):

    #Takes the values of the number of enemies, how many of each kind, and 
    #the number of obstacles
    def __init__(self,enemies,obstacles):
        super().__init__()
        self.numEnemy = enemies[0]
        self.numRanged = enemies[1]
        self.numMortar = enemies[2]
        self.totalEnemies = enemies[0]+enemies[1]+enemies[2]
        self.totalObstacles = obstacles
        Bullet.number = 0

    def appStarted(self):
        #Initialize the level
        self.margin = 50
        self.extra = 200
        self.rows = (self.height-2*self.margin)//Square.width
        self.cols = (self.width+self.extra-2*self.margin)//Square.width
        self.endPiece = Square(self.cols-1, self.rows//2, self)
        self.obstacles = self.generateObstacles()
        self.startWall = Wall(-100,0)
        self.endWall = Wall(self.width+self.extra+10, 0)

        #Initialize the player and enemies
        x0,y0,x1,y1 = self.getCellBounds(self.rows//2, 0)
        self.player = Player(1000, (x0+x1)//2, (y0+y1)//2, self)
        self.scrollX = 0 
        self.scrollMargin = 50
        self.enemies = self.generateEnemies()
        self.paused = False
        self.canDrawBullet = False
    
    #Generates each type of enemy
    def generateEnemies(self):
        enemies = []
        self.generateEnemyType(enemies, self.numEnemy, 0)
        self.generateEnemyType(enemies,self.numRanged, 1)
        self.generateEnemyType(enemies,self.numMortar, 2)   
        return enemies
    
    #Places the enemies, given a certain type. The counter specifies which enemy 
    # is being created
    def generateEnemyType(self,enemies, number, counter):
        for i in range(number):
            while True:
                position = (random.randint(60,self.width+self.extra-20),
                                        random.randint(60,self.height-60))
                row,col = self.getCell(position[0],position[1])
                overlap = False
                #Checks if the enemy was placed on an obstacle
                if (row,col) in self.positions:
                    overlap = True
                playerRow, playerCol = self.getCell(Player.x, Player.y)
                if (not overlap):
                    #Make a normal enemy
                    if counter%3 == 0:
                        health = 250
                        enemy = Enemy(health,position,self)
                        enemies.append(enemy)
                    #Make a ranged enemy
                    elif counter%3 == 1:
                        health = 200
                        enemy = Ranged(health,position,self)
                        enemies.append(enemy)
                    #Make a mortar enemy
                    else:
                        health = 450
                        enemy = Mortar(health,position,self)
                        enemies.append(enemy)   
                    break
                else:
                    #Try placing the enemy again
                    continue
        
    #citation: https://www.cs.cmu.edu/~112/notes/notes-animations-part3.html#sidescrollerExamples
    # Makes the player be seen to simulate the scrolling
    def makePlayerVisible(self):
        # scroll to make player visible as needed
        if (self.player.x < self.scrollX + self.scrollMargin):
            self.scrollX = self.player.x - self.scrollMargin
        if (self.player.x > self.scrollX + self.width - self.scrollMargin):
            self.scrollX = self.player.x - self.width + self.scrollMargin

    #Changes position given the direction
    def movePlayer(self, dx, dy):
        if not self.paused:
            if not self.player.dead:
                tempx, tempy = Player.x, Player.y
                Player.x += dx
                Player.y += dy
                playerRow, playerCol = self.getCell(Player.x, Player.y)
                #Passed the x bounds
                if Player.x <= self.startWall.x0 + Wall.width or Player.x >=self.endWall.x0:
                    Player.x = tempx
                #Passed the y bounds
                if Player.y <= 0 or Player.y >= self.height:
                    Player.y = tempy
                #Hit an obstacle
                if (playerRow,playerCol) in self.positions:
                    Player.x = tempx
                    Player.y = tempy
                #Change the spritecounter to animate the movement
                self.player.movespriteCounter += 1
                playerRow, playerCol = self.getCell(Player.x, Player.y)
                #Advance to next level if all the enemies are dead and player is at the endPiece
                if playerRow == self.endPiece.ry and playerCol == self.endPiece.rx:
                    if len(self.enemies) == 0:
                        self.player.levelCleared = True
                        self.app.level += 1
                        if self.app.level <= len(self.app.levelList):
                            print(f'loading Level {self.app.level}')
                            Bullet.number = 0
                            self.app.setActiveMode(self.app.levelList[self.app.level-1])
                        else:
                            self.app.setActiveMode(self.app.endScreen)
                self.makePlayerVisible()
    
        
    #citation: https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCell(self, x, y):
        gridWidth  = self.width + self.extra - 2*self.margin
        gridHeight = self.height - 2*self.margin
        cellWidth  = gridWidth / self.cols
        cellHeight = gridHeight / self.rows
        row = int((y - self.margin) / cellHeight)
        col = int((x - self.margin) / cellWidth)

        return (row, col)
        
    #citation:https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCellBounds(self, row, col):
        gridWidth  = self.width + self.extra - 2*self.margin
        gridHeight = self.height - 2*self.margin
        x0 = self.margin + gridWidth * col / self.cols
        x1 = self.margin + gridWidth * (col+1) / self.cols
        y0 = self.margin + gridHeight * row / self.rows
        y1 = self.margin + gridHeight * (row+1) / self.rows
        return (x0, y0, x1, y1)

    #citation: https://www.cs.cmu.edu/~112/notes/notes-recursion-part2.html#memoization 
    def memoized(f):
        import functools
        cachedResults = dict()
        @functools.wraps(f)
        def wrapper(*args):
            if args not in cachedResults:
                cachedResults[args] = f(*args)
            return cachedResults[args]
        return wrapper 
    
    #creates the obstacles and makes sure they aren't overlapping and 
    #checks if there is a solution from one end of the level to the other end
    def generateObstacles(self):
        obstacleList = []
        numObstacles = self.totalObstacles
        i=0
        tries = 0
        while (tries<1000):
            while(i<numObstacles):
                #Randomly place the obstacle
                rx = random.randint(0,self.cols-1)
                ry = random.randint(0,self.rows-1)
                square = Square(rx, ry, self)
                intersects = False
                #Check if the obstacle is overlapping an existing obstacle
                for oSquare in obstacleList:
                    if ((square.rx == oSquare.rx and square.ry == oSquare.ry)
                        or (square.rx == self.endPiece.rx and square.ry == self.endPiece.ry) or
                        (square.rx == 0 and square.ry == self.rows//2)):
                        intersects = True
                if intersects:
                    #PLace the obstacle again
                    continue
                else:
                    #Add it to the list of all obstacles
                    obstacleList.append(square)
                    i += 1 
            #make a list of the positions of the squares
            positions = []
            for square in obstacleList:
                positions.append((square.ry,square.rx))
            self.positions = set(positions)
            #check if you can go from the player start to the endpiece
            path = self.isPath(self.rows//2, 0, self.endPiece.ry, self.endPiece.rx, 
                                                            self.rows//2, 0)
            if path:
                return obstacleList
            else:
                #Place all the obstacles in different locations
                tries += 1
                obstacleList = []
                i= 0
                continue
        #If after 999 tries there is no path from start to finish, 
        # move the end piece to where the player starts to guarantee a solution
        #This very rarely will run since almost all the time there is a path
        if tries > 999:
            prow, pcol = self.getCell(50,self.app.height//2)
            self.endPiece.ry = prow
            self.endPiece.rx = pcol
            if (prow,pcol) in self.positions:
                self.positions.remove((prow,pcol))
                obstacleList.remove((prow,pcol))
            return obstacleList
    
    #Recursively checks if there is a path from a given (row,col) to a target (row,col)
    def isPath(self, row, col, trow, tcol, prow, pcol):
        if (not ((0<=row<=self.rows-1) and (0<=col<=self.cols-1)) or 
                                                    (row,col) in self.positions):
            return False
        if row == trow and col == tcol:
            return True
        else:
            dirs = [(0,1), (1,0), (-1,0), (0,-1)]
            for drow,dcol in dirs:
                newRow = row + drow
                newCol = col + dcol
                if newRow == prow and newCol == pcol:
                    return False
                if self.isPath(newRow,newCol,trow,tcol, row, col):
                    return True
            return False

    #Checks if any shortcut keys were pressed or movement keys
    def keyPressed(self, event):
        if event.key == 'p' :
            self.paused = not self.paused
        elif event.key == 'd':
            Bullet.number = 0
            self.player.dead = True
        elif event.key == 'e':
            self.app.setActiveMode(self.app.endScreen)
        elif event.key == 's':
            self.app.level += 1
            if self.app.level <= len(self.app.levelList):
                print(f'loading Level {self.app.level}')
                Bullet.number = 0
                self.app.setActiveMode(self.app.levelList[self.app.level-1])
            else:
                self.app.setActiveMode(self.app.endScreen)

        elif event.key == 'Up':
            if not self.paused:
                self.player.isMoving = True
                self.movePlayer(0,-10)
        elif event.key == 'Down':
            if not self.paused:
                self.player.isMoving = True
                self.movePlayer(0,10)
        elif event.key == 'Left':
            if not self.paused:
                self.player.isMoving = True
                self.movePlayer(-10,0)
        elif event.key == 'Right':
            if not self.paused:
                self.player.isMoving = True
                self.movePlayer(10,0)

    #Moves each enemy
    def moveEnemies(self):
        for enemy in self.enemies:
            enemy.move(self)

    #Allows the player to start attacking again 
    def keyReleased(self, event):  
        if (event.key == 'Up' or event.key == 'Down' or event.key == 'Right' or
            event.key == 'Left'):
            self.player.isMoving = False  

    #Checks if the player clicked the main menu button post death 
    def mousePressed(self,event):
        if self.player.dead:
            if (self.app.width//2 -100 <= event.x <= self.app.width//2 + 100 and
                self.app.height//2 +20 <= event.y <= self.app.height//2 +60):
                Bullet.number =0
                #Saves player score
                self.app.saveScore()
                #Resets the app
                self.app.resetApp()


    def timerFired(self):
        if not self.paused:
            if not self.player.dead:
                #If the level is cleared, do not move any  bullets
                if self.player.levelCleared:
                    self.canDrawBullet = False
                #Move the bullet if it exists, otherwise make a bullet
                else:
                    if len(self.enemies) != 0:
                        if Bullet.number == 0:
                            self.bullet = self.player.attack(self)
                            self.bullet.move(self)
                            Bullet.number += 1
                            self.canDrawBullet = True
                        else:
                            self.bullet.move(self)
                            if self.bullet.hitTarget or self.bullet.hitObstacle:
                                Bullet.number -= 1
                                self.canDrawBullet = False
                #Move the enemies
                self.moveEnemies()

    def redrawAll(self, canvas):
        #Draw Pause screen
        if self.paused:
            canvas.create_image(self.app.width//2, self.app.height//2, 
                        image = ImageTk.PhotoImage(self.app.background))
            canvas.create_text(self.app.width//2, self.app.height//2-60, text = 'Game is Paused',
                                font = 'Arial 30 bold')
            canvas.create_text(self.app.width//2-10, self.app.height//2 -20,
                                text = 'Press p to return to game', font = 'Arial 20 bold')
                
            
        else:
            #Draw the dead screen
            if self.player.dead:
                canvas.create_image(self.app.width//2, self.app.height//2, 
                        image = ImageTk.PhotoImage(self.app.background))
                canvas.create_text(self.app.width//2, self.app.height//2-60, text = 'You Lose! :(',
                                font = 'Arial 30 bold')
                canvas.create_text(self.app.width//2-10, self.app.height//2 -20,
                                text = f'Final Score: {self.app.score}', font = 'Arial 20 bold')
                canvas.create_rectangle(self.app.width//2 -100 , self.app.height//2 +20, 
                                self.app.width//2+100,self.height//2+60, fill = 'darkgreen')
                canvas.create_text(self.app.width//2, self.app.height//2 +40, 
                                text = 'Main Menu', font = 'Arial 20 bold' )

            else:

                #draw background
                canvas.create_image(self.app.width//2, self.app.height//2, 
                            image = ImageTk.PhotoImage(self.app.background))

                canvas.create_text(self.app.width//2 - self.scrollX, 20,
                                            text = f'Level {self.app.level}', font = 'Arial 20 bold')
                canvas.create_text(self.app.width - 30 - self.scrollX, 20,
                            text = f'Score: {self.app.score}', font = 'Arial 20 bold')

                #draw obstacles
                for square in self.obstacles:
                    x0,y0,x1,y1 = self.getCellBounds(square.ry,square.rx)
                    canvas.create_image((x0+x1)/2 - self.scrollX, (y0+y1)/2, 
                            image = ImageTk.PhotoImage(self.app.obstacle))
                
                #draw endPiece
                x2,y2,x3,y3 = self.getCellBounds(self.endPiece.ry, self.endPiece.rx)
                canvas.create_image((x2+x3)/2-self.scrollX,(y2 +y3)/2, 
                        image  = ImageTk.PhotoImage(self.app.endPiecePicture))

                #draw start Wall
                self.startWall.drawWall(canvas,self)

                #draw the end Wall
                self.endWall.drawWall(canvas,self)

                #draw Enemies
                for enemy in self.enemies:
                    enemy.drawEnemy(canvas, self.scrollX)
                
                #draw Player
                self.player.drawPlayer(canvas, self.scrollX)
                
                if self.canDrawBullet:
                    self.bullet.drawBullet(canvas, self.scrollX)






























