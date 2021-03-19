# This file contains all the intermediate screens/tabs in the game, such as
# the start screen, the end screen, the rules screen, and scores screen
# All citations for pictures are in modalApp.py

from cmu_112_graphics import *

#The first screen that pops up when you load the app
class SplashScreen(Mode):
    #Initializes the main menu
    def appStarted(mode):
        mode.buttons = [(mode.width/2, 200, 'New Game'), (mode.width/2, 300, 'Rules'),
                                                (mode.width/2, 400, 'Highscores')]
        mode.buttonL = 200
        mode.buttonH = 30
        

    #Checks to see where the user clicked and which button it is
    def mousePressed(mode, event):
        for button in mode.buttons:
            if ((button[0]-mode.buttonL <= event.x <= button[0]+mode.buttonL) and
            (button[1]-mode.buttonH <= event.y <= button[1]+mode.buttonH)):
                if mode.buttons.index(button) == 0:
                    #Start the game with the user's name and number of levels they want
                    name = mode.getUserInput('Enter Your Name')
                    levels = mode.getUserInput('How many Levels do you want?')
                    if (name == ''):
                        mode.app.showMessage('Your Score will not be saved')
                    elif (name == None) or (levels == None) or (levels == '') or(int(levels) <= 0) :
                        mode.app.showMessage('Enter a name or valid number of levels')
                        mode.app.resetApp()
                        break
                    else:
                        mode.app.name = name
                    mode.app.loadLevels(int(levels))
                    print('Loading Level 1')
                    mode.app.level += 1
                    mode.app.setActiveMode(mode.app.levelList[mode.app.level-1])
                elif mode.buttons.index(button) == 1:
                    #Load the rules screen
                    mode.app.setActiveMode(mode.app.rulesScreen)
                else:
                    mode.app.setActiveMode(mode.app.scoresScreen)

    #Draws the three buttons in the menu
    def drawButtons(mode, canvas):
        for button in mode.buttons:
            canvas.create_rectangle(button[0] -mode.buttonL, button[1]-mode.buttonH,
                                button[0] + mode.buttonL, button[1] + mode.buttonH,
                                fill = 'darkgreen')
            canvas.create_text(button[0], button[1], text = f'{button[2]}', 
                                                    font = 'Arial 30 bold')
    #Draws the main menu
    def redrawAll(mode, canvas):
        canvas.create_image(mode.app.width//2,mode.app.height//2,image = ImageTk.PhotoImage(mode.app.background))
        mode.drawButtons(canvas)
        canvas.create_text(mode.width/2, 50,text = 'The Trials', font = 'Arial 60 bold')

class RulesScreen(Mode):
    
    def keyPressed(mode, event):
        if event.key == 'Enter':
            #Go back to the main menu
            mode.app.setActiveMode(mode.app.firstScreen)

    #Draw the rules screen
    def redrawAll(mode, canvas):
        margin = 50
        canvas.create_image(mode.width//2,mode.height//2,image = ImageTk.PhotoImage(mode.app.background))
        canvas.create_rectangle(margin, margin, mode.width - margin, mode.height - margin,
                        fill = 'steelblue1', stipple = 'gray50')
        canvas.create_text(mode.width/2, margin + 40, font = 'Arial 40 bold', text = 'Rules')
        canvas.create_image(margin + 100, margin + 140, image = ImageTk.PhotoImage(mode.app.arrowkeys))
        canvas.create_text(mode.width-margin-200, margin+140, text = 'Movement', font = 'Arial 15 bold')
        canvas.create_image(margin + 100, margin + 240, image = ImageTk.PhotoImage(mode.app.pause))
        canvas.create_text(mode.width-margin-200, margin +240, text = 'Pause', font = 'Arial 15 bold')
        canvas.create_text(mode.width/2, margin + 340, font = 'Arial 13 bold', 
                            text = 'Attacks automatically occur when you are not moving')
        canvas.create_text(mode.width/2, margin + 390, font = 'Arial 15 bold',
                                text = 'Press Enter to return')

class EndScreen(Mode):
    
    #checks to see if you clicked to go back to main menu
    def mousePressed(mode,event):
        if (mode.app.width//2 - 100 <= event.x <= mode.app.width//2 + 100 and
            mode.app.height//2 + 20 <= event.y <= mode.app.height//2 + 60):
            #save the score of the winner
            mode.app.saveScore()
            #return to the main menu
            mode.app.resetApp()

    #Draws the end screen
    def redrawAll(mode,canvas):
        canvas.create_image(mode.app.width//2, mode.app.height//2, 
                    image = ImageTk.PhotoImage(mode.app.background))
        canvas.create_text(mode.app.width//2, mode.app.height//2-60, text = 'Congratulations, You Win!',
                        font = 'Arial 30 bold')
        canvas.create_text(mode.app.width//2-10, mode.app.height//2 -20,
                        text = f'Final Score: {mode.app.score}', font = 'Arial 20 bold')
        canvas.create_rectangle(mode.app.width//2 -100 , mode.app.height//2 +20, 
                        mode.app.width//2+100,mode.height//2+60, fill = 'darkgreen')
        canvas.create_text(mode.app.width//2, mode.app.height//2 +40, 
                        text = 'Main Menu', font = 'Arial 20 bold' )

class ScoresScreen(Mode):
    #Initializes the scores
    def appStarted(mode):
        mode.scorefile = open('scores.txt', 'r')
        mode.rawdata = []
        mode.lines = mode.scorefile.read().splitlines()
        for line in mode.lines:
            nameScore = line.split(':')
            name = nameScore[0]
            score = int(nameScore[1])
            mode.rawdata.append((name,score))
        #Citation for lambda help: https://realpython.com/python-sort/#ordering-values-with-sort
        mode.data = sorted(mode.rawdata, key = lambda score: score[1], reverse = True)
        mode.scorefile.close()
    
    def keyPressed(mode, event):
        if event.key == 'Enter':
            mode.app.setActiveMode(mode.app.firstScreen)
    
    def redrawAll(mode, canvas):
        margin = 50
        canvas.create_image(mode.width//2,mode.height//2,image = ImageTk.PhotoImage(mode.app.background))
        canvas.create_rectangle(margin, margin, mode.width - margin, mode.height - margin,
                        fill = 'tomato2', stipple = 'gray50')
        canvas.create_text(mode.width//2, 30, text = 'Highscores', font ='Arial 30 bold')
        canvas.create_text(mode.width//2, mode.height - margin- 30, text = 'Press Enter to return',
                                font = 'Arial 20 bold')
        if len(mode.data) <= 10:
            for i in range(len(mode.data)):
                place = i+1
                name = mode.data[i][0]
                score = mode.data[i][1]   
                canvas.create_text(margin + 40, margin + (i+1)*40, text =f'{str(place)}',
                                    font = 'Arial 15 bold') 
                canvas.create_text(mode.width//2, margin + (i+1)*40, text =f'{name}',
                                    font = 'Arial 15 bold')
                canvas.create_text(mode.width-margin-40, margin + (i+1)*40, text = f'{score}',
                                    font = 'Arial 15 bold')        

        else:
            for i in range(10):
                place = i+1
                name = mode.data[i][0]
                score = mode.data[i][1]   
                canvas.create_text(margin + 20, margin + (i+1)*40, text =f'{str(place)}', font = 'Arial 15 bold') 
                canvas.create_text(mode.width//2, margin + (i+1)*40, text =f'{name}', font = 'Arial 15 bold')
                canvas.create_text(mode.width-margin-20, margin + (i+1)*40, text = f'{score}', font = 'Arial 15 bold')        
    
        









