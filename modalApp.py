from cmu_112_graphics import *
from Screens import *
from levelGenerator import *

#############################################################
#Citation for enemy sprites: https://craftpix.net/freebies/free-wraith-tiny-style-2d-sprites/
#Citation for player and bullet: https://www.gameart2d.com/the-robot---free-sprites.html
#Citation for mortar: https://pnghut.com/png/uzTb9CRnqq/clash-royale-of-clans-download-game-tool-mortar-transparent-png
# Citation for Rock: https://www.vexels.com/png-svg/preview/145826/round-rock 
#Citation for obstacle: https://ftbwiki.org/Concrete_(Minecraft)
#Citation for the portal: https://freepngimg.com/png/27516-portal-photos
#Citation for the fireball: https://toppng.com/free-image/fireball-png-PNG-free-PNG-Images_120800
#Citation for background: https://www.pinterest.com/pin/233413193166744150/
# Citation for other background: https://www.istockphoto.com/illustrations/forrest 
# Citation for rules image: https://www.iconexperience.com/v_collection/icons/?icon=keyboard_key_p
# Citation for rules image: https://www.clipartmax.com/middle/m2i8i8K9H7G6G6G6_computer-keyboard-arrow-keys-clip-art-computer-keyboard-arrow-keys-clip-art/
# Citation for all the colors: http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

#This file is the modalApp and is the one that will be run. This loads all the images, saves scores, and runs the app

#Initializes all the modes of the app
class myModalApp(ModalApp):
    def appStarted(app):
        app.loadImages()
        app.firstScreen = SplashScreen()
        app.rulesScreen = RulesScreen()
        app.endScreen = EndScreen()
        app.scoresScreen = ScoresScreen()
        app.resetApp()

    #Re-creates all the levels and resets the scores and users
    def resetApp(app):
        app.score = 0
        app.name = ''
        app.level = 0
        app.levelList = []
        app.scoresScreen = ScoresScreen()
        app.setActiveMode(app.firstScreen)
    
    #Creates the levels
    def loadLevels(app, number):
        for i in range(number):
            enemies, obstacles = app.generateNumbers(i+1)
            level = Level(enemies, obstacles)
            app.levelList.append(level)
    
    #Defines the number of obstacles and enemies for each level
    def generateNumbers(app, levelNum):
        #The first three levels are to get used to the different types of monsters
        if levelNum == 1:
            return ((3,0,0),5)
        elif levelNum == 2:
            return ((0,3,0),20)
        elif levelNum == 3:
            return ((0,0,2),5)
        else:
            while True:
                normal = random.randint(levelNum - 1, levelNum + 2)
                ranged = random.randint(levelNum - 2, levelNum + 2)
                mortar = random.randint(max(levelNum-10,2), min(levelNum-2,10))

                if normal + ranged + mortar >= levelNum * 3:
                    continue
                else:
                    return ((normal,ranged,mortar),random.randint(5, 25))

    #Saves the score after a player loses or wins
    def saveScore(app):
        if app.name != '':
            scoreFile = open('scores.txt', 'a') 
            scoreFile.write(f'{app.name}:{app.score}\n')
            scoreFile.close()
        

    def loadImages(app):
        image = app.loadImage('Sprites/StartScreenPicture.png')
        app.background = image.resize((app.width,app.height), Image.ANTIALIAS)

        image = app.loadImage('Sprites/arrowkeys.png')
        app.arrowkeys = image.resize((80,80), Image.ANTIALIAS)
        image = app.loadImage('Sprites/pause.png')
        app.pause = image.resize((80,80), Image.ANTIALIAS)

        image = app.loadImage('Sprites/Obstacle.png')
        app.obstacle = image.resize((50,50), Image.ANTIALIAS)

        image = app.loadImage('Sprites/endPiece.png')
        app.endPiecePicture = image.resize((50,50), Image.ANTIALIAS)

        image = app.loadImage('Sprites/level.jpg')
        app.levelBackground = image.resize((app.width,app.height), Image.ANTIALIAS)

        image = app.loadImage('Sprites/Bullet.png')
        app.bullet = image.resize((25,25), Image.ANTIALIAS)

        #initialize the moving sprites
        app.moveSprites = []
        for i in range(1,9):
            image = app.loadImage(f'Sprites/PlayerSprite/Run ({i}).png')
            scaledImage = image.resize((50,50), Image.ANTIALIAS)
            app.moveSprites.append(scaledImage)
        

        #initialize the shoot sprites
        app.shootSprites = []
        for i in range(1,5):
            image = app.loadImage(f'Sprites/PlayerSprite/Shoot ({i}).png')
            scaledImage = image.resize((50,50), Image.ANTIALIAS)
            app.shootSprites.append(scaledImage)
        

        #initialize the dead sprites
        app.deadSprites = []
        for i in range(1,11):
            image=app.loadImage(f'Sprites/PlayerSprite/Dead ({i}).png')
            scaledImage = image.resize((50,50), Image.ANTIALIAS)
            app.deadSprites.append(scaledImage)
        

        #initialize the end Sprites
        app.endSprites = []
        for i in range(1,6):
            image = app.loadImage(f'Sprites/PlayerSprite/JumpShoot ({i}).png')
            scaledImage = image.resize((50,50), Image.ANTIALIAS)
            app.endSprites.append(scaledImage)
        


        #initialize the enemy move sprites
        image = app.loadImage('Sprites/Enemy Sprites/Walking/Wraith_01_Moving Forward_000.png')
        app.fmoveSprite = image.resize((50,50), Image.ANTIALIAS)
        image = app.loadImage('Sprites/Enemy Sprites/Walking/Wraith_01_Moving Backward_000.png')
        app.bmoveSprite = image.resize((50,50), Image.ANTIALIAS)

        #initialize the ghost move sprites
        image = app.loadImage('Sprites/Enemy Sprites/Walking/Wraith_03_Moving Forward_000.png')
        app.fghostmoveSprite = image.resize((50,50), Image.ANTIALIAS)
        image = app.loadImage('Sprites/Enemy Sprites/Walking/Wraith_03_Moving Backward_000.png')
        app.bghostmoveSprite = image.resize((50,50), Image.ANTIALIAS)

        #initialize the enemy attack sprites
        app.attackSprites = []
        for i in range(0,12):
            image = app.loadImage(f'Sprites\Enemy Sprites\Attacking\Wraith_01_Attack_0{i//10}{i%10}.png')
            scaledImage = image.resize((50,50), Image.ANTIALIAS)
            app.attackSprites.append(scaledImage)

        #backward attack sprites 
        app.attackRSprites = []
        for i in range(0,12):
            image = app.loadImage(f'Sprites\Enemy Sprites\Attacking\Wraith_01_AttackR_0{i//10}{i%10}.png')
            scaledImage = image.resize((50,50), Image.ANTIALIAS)
            app.attackRSprites.append(scaledImage)
        
        image = app.loadImage('Sprites/Ranged.png')
        app.fRangedSprite = image.resize((50,50), Image.ANTIALIAS)
        image = app.loadImage('Sprites/RangedR.png')
        app.bRangedSprite = image.resize((50,50), Image.ANTIALIAS)
        image = app.loadImage('Sprites/rock.png')
        app.rockSprite = image.resize((25,25), Image.ANTIALIAS)

        image = app.loadImage('Sprites/Fireball.png')
        app.fireballSprite = image.resize((25,25), Image.ANTIALIAS)

        image = app.loadImage('Sprites/mortar.jpg')
        app.mortarSprite = image.resize((50,50), Image.ANTIALIAS)

app = myModalApp(width = 600, height = 600)
        
        

