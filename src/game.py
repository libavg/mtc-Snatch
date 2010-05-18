# -*- coding: utf-8 -*-
# Copyright (C) 2009
#    Lusia Erldorfer, <Lusia dot Erldorfer at student dot HTW minus Berlin dot de>
#    Annette Hameister, <annettehameister at gmail dot com>
#    Martin Hauffe, <martinhauffe at googlemail dot com>
#    Katrin Koehler, <katrin dot koehler at student dot HTW minus Berlin dot de>
#    Hans Pfau, <H_Pfau at web dot de>
#    Nancy Wuttke, <nancy.wuttke at gmx dot de>
#    
#
# This file is part of snatchem.
#
# snatchem is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# snatchem is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with snatchem.  If not, see <http://www.gnu.org/licenses/>.

from libavg import *
from libavg import button
import helpful, useful, collision, sys
import teammate, animal, score, startButton, soundeffect, goal, collision, highscore
from useful import *


id = 0

class Game:
    ##   Constructor
    #    @param player avg Player
    #    @param index initial amount of animals
    def __init__(self, player, index):    
        ##    pointer to the player
        self.player = player
        ##    init amount of animals 
        self.animalAmount = index
        ##    animal amount of non caught animals
        self.freeAnimal  = index 
        ##    global animal reminder
        self.animals = []
        ##    list index for the animals
        self.animalIndex = -1   
        ##    reminder for the rounds
        self.__round = 0
        ##    reminder for the play time
        self.__highscoreTime = None
        ##    reminder for the displayed play time
        self.__highscoreSecondes = None
        ##    button in the middle of the field
        self.__mainButton = None
        ##    button to go back to the menu
        self.__againButton = None
        ##    reminder for the moles
        self.__moleObj = []
        ##    set True if moles are created
        self.__isUsed = False
        ## goal instance left 
        self.__goal1 = goal.Goal("goal1", self, -171, 300, 1.57, avg.Point2D(-100, 330), 0, 360, avg.Point2D(12, 239), avg.Point2D(12, 297), avg.Point2D(12, 353), avg.Point2D(12, 415), avg.Point2D(12, 475))
        ## goal instance top 
        self.__goal2 = goal.Goal("goal2", self, 370, 0, 3.14, avg.Point2D(640, -95), 550, 80, avg.Point2D(713, 7), avg.Point2D(652, 7), avg.Point2D(594, 7), avg.Point2D(535, 7), avg.Point2D(487, 7))
        ## goal instance right 
        self.__goal3 = goal.Goal("goal3", self, 940, 300, -1.57, avg.Point2D(1310, 390), 1100, 360, avg.Point2D(1218, 470), avg.Point2D(1218, 413), avg.Point2D(1218, 356), avg.Point2D(1218, 299), avg.Point2D(1218, 260))
        ## goal instance bottom 
        self.__goal4 = goal.Goal("goal4", self, 370, 631, 0, avg.Point2D(580, 755), 560, 690, avg.Point2D(487, 735), avg.Point2D(541, 735), avg.Point2D(600, 735), avg.Point2D(659, 735), avg.Point2D(715, 735))
        ##    all possible animals
        self.__animalArray = [animal.Hedgehog, animal.Snail, animal.Turtle, animal.Sheep, animal.Rabbit]     
        ##    count the activated players
        self.__countPlayer = 0
        ##    reminder for the activated players 
        self.playerAmount = [False, False, False, False]
        ##    reminder for the players        
        self.playerNames = ["player1", "player2", "player3", "player4"]
        ##    reminder for the goal instances
        self.goals = [self.__goal1, self.__goal2, self.__goal3, self.__goal4] 
        ## DivNode for the field
        self.__area = self.player.getElementByID("active_area")
        ##    reminder for animal production on the moles
        self.__moleActive = False
        ##    highscore instance
        self.__highScore = None
        ##    reminder for the start buttons of each teammate
        self.__startButtonsPlayer = []   
        ##    tutorial Node
        self.__tutorial = None
        ##    credits Node
        self.__credits = None
        ##    count the init frequency
        self.__countInit = 0

        self.__loadSounds()
        self.__initGame(None)
        

    ##    creates the start buttons and the main button and resets the game
    #     @param event avg event
    def __initGame(self, event):
        if self.__countInit > 0:
            self.__resetGame()
        self.__countInit += 1
        self.soundBg[0].sound.play()  
        self.__createMenu()
        
    
    ##    starts a new round
    def __startGame(self): 
        ##    reminder for the frame time at the beginning of each round
        self.__startTime = self.player.getFrameTime()     
        for i in range (self.playerAmount.__len__()):
            if self.playerAmount[i] == False:
               #print "i",i 
               self.__startButtonsPlayer[i].delStartButton()
        self.__startButtonsPlayer = []  
               
        if self.__testPlayerAmount():
            self.__highscoreTime = None 
            self.__highscoreSecondes = None  
            ##    0 or 1 for left or right mole activation                     
            self.__quadrant = helpful.getRandomNumber(0, 1) 
            if self.__quadrant == 1:
                self.__moleActive = True
            else:
                self.__moleActive = False     
            self.soundBg[0].sound.stop()
            self.soundBg[1].sound.play()                     
            self.freeAnimal = self.animalAmount    
            self.__createAnimal(self.animalAmount)
            self.__highscoreTime = self.player.getFrameTime()
            self.__round += 1
            ##    reminder for the handler id of animal manager
            self.__createID = self.player.setOnFrameHandler(self.__createAnimalManager)
            ##    reminder for the handler id of the score
            self.__displayScore = self.player.setInterval(1000, self.__updateScore) 
        else:
            self.__initGame(None)
    
    ##    terminates the current round
    def stopGame(self):
        self.soundBg[1].sound.stop()
        self.soundBg[0].sound.play()
        self.__deleteAllAnimals()
        self.__disableGoals()
        self.player.clearInterval(self.__displayScore)
        self.__highscoreTime = self.player.getFrameTime()-self.__highscoreTime
        self.__highScore = None
        self.__highScore = highscore.Highscore("winner1", self, 485, 320, self.__highscoreTime)
        self.directory = self.__highScore.get_Directory()
        if self.__highScore.isInHighscore()==True:
            self.__highScore.createHighscore(485,320,0)
            self.__highScore.displayHighscore(None)
        else:
            self.__highScore.HighscorePosition = None
            self.__highScore.displayHighscore("keks")  
    
    
     ## set the game to default
    def __resetGame(self):
        self.animalIndex = -1
        self.animals = []
        
        self.__disableGoals()
        self.__deleteAllPlayer() 
        self.__backToMenu()
        self.__resetScreen()
        
        self.__moleObj = []
        self.__isUsed = False
        self.__moleActive = False
        self.__mainButton = None
        self.__highscoreButton = None 
        self.__tutorialButton = None
        self.__creditsButton = None
        self.__exitButton = None
        
        self.__highscoreTime = None
        self.__highscoreSecondes= None
        self.__countPlayer = 0
        
    ##    reset screen after highscore 
    def __resetScreen(self):
        if self.__againButton != None:
            self.__againButton.delStartButton() 
            self.__againButton = None
        if self.__highScore != None:
           self.__highScore.deletehighscore()
           self.__highScore = None 
    if self.__tutorial != None:
        self.tutorialSound.sound.stop()
            useful.deleteNode(self.__tutorial)
        self.__tutorialVideo.stop()
            self.__tutorial = None
        if self.__credits != None:
            useful.deleteNode(self.__credits)
            self.__credits = None        
    self.__deleteMenu()
        
    
#===============================================================================
# 
#===============================================================================
       
  
    
      
    ##    create button instances for the menu
    def __createMenu(self):  
       self.__highScore = highscore.Highscore("winner1", self, 485, 320, self.__highscoreTime)  
       self.__mainButton = startButton.StartButton(self, self.__showActivateButtons, 590, 340,"../img/buttonstart.png", 0,160, 85, False)
       self.__highscoreButton = startButton.StartButton(self, self.__highScore.displayHighscore, 390, 240,"../img/highscorebutton.png", 0,160, 85, False)
       self.__tutorialButton = startButton.StartButton(self, self.__displayTutorial, 790, 240,"../img/tutorial.png", 0,160, 85, False)
       self.__creditsButton = startButton.StartButton(self, self.__displayCredits, 390, 440,"../img/credits.png", 0,160, 85, False)
       self.__exitButton = startButton.StartButton(self, self.__exitGame, 790, 440,"../img/exit.png", 0,160, 85, False)
    
    ##    initialize again/back button
    def createPlayAgainB(self):
           ##    back button
           self.__againButton = startButton.StartButton(self, self.__initGame, 900, 620,"../img/buttonagain.png", 0,160,85,False)    

   ##    delete the five buttons of the menu
    def __deleteMenu(self):
    if self.__mainButton != None:
        self.__mainButton.delStartButton()
        self.__highscoreButton.delStartButton()
        self.__tutorialButton.delStartButton()
        self.__creditsButton.delStartButton()
        self.__exitButton.delStartButton()
     
    ##    delete all possible displayed Nodes
    def __backToMenu(self):

        if self.__tutorial != None:
        self.tutorialSound.sound.stop()
            useful.deleteNode(self.__tutorial)
        self.__tutorialVideo.stop()
            self.__tutorial = None
        if self.__credits != None:
            useful.deleteNode(self.__credits)
            self.__credits = None
        if self.__highScore != None:
            self.__highScore.deletehighscore()
            self.__highScore = None
 
#===============================================================================
# 
#===============================================================================
            
    ##    reset players
    def __deleteAllPlayer(self):
        for i in range (self.playerAmount.__len__()):
            if self.goals[i] != None:
                self.goals[i].winner.opacity = 0    
                self.goals[i].resetPlacesTaken()
                if self.playerAmount[i]:
                    self.playerNames[i].score.deleteScore() 
                self.playerAmount[i] = False
                self.playerNames[i] = ""
                
   
    ##    hide the displayed time 
    def hideScore(self):
        for i in range (self.playerAmount.__len__()):
            if type(self.playerNames[i]) != str:
                self.playerNames[i].score.text.opacity = 0
        
    
            
    ##    hide goals
    def __disableGoals(self):
        self.goals[0].goal.opacity = 0
        self.goals[1].goal.opacity = 0
        self.goals[2].goal.opacity = 0
        self.goals[3].goal.opacity = 0
    

  
    ##   update highscore for all goals 
    def __updateScore(self):
        self.__highscoreSecondes = self.player.getFrameTime() - self.__startTime
        for i in range (self.playerNames.__len__()):
            if type(self.playerNames[i]) != str:
                self.playerNames[i].score.points = self.__highscoreSecondes/1000 
                self.playerNames[i].score.update()
  
 
#===============================================================================
# 
#===============================================================================
         
    ##    initialize the start buttons for the goals and set the timeout to start the game
    #     @param avg event
    def __showActivateButtons(self, event):
        ##    remind timeout id 
    #
    self.__deleteMenu()
    self.player.setTimeout(400,self.__resetScreen)
        self.__startGameID = self.player.setTimeout(5000, self.__startGame) 
        
    #self.__backToMenu() 
        self.__startButtonsPlayer.append(startButton.StartButton(self, self.__onClickPlayer1, 140, 340, "../img/button.png", 1.57, 132, 65, True))
        self.__startButtonsPlayer.append(startButton.StartButton(self, self.__onClickPlayer2, 580, 150, "../img/button.png", 3.14, 132, 65, True))
        self.__startButtonsPlayer.append(startButton.StartButton(self, self.__onClickPlayer3, 990, 340, "../img/button.png", -1.57, 132, 65, True))
        self.__startButtonsPlayer.append(startButton.StartButton(self, self.__onClickPlayer4, 580, 560,"../img/button.png", 0, 132, 65, True))
              
                                   
    ##    call back for player 1
    #     @param event avg event
    def __onClickPlayer1(self, event):
        self.goals[0].goal.opacity = 1
        self.playerNames[0] = teammate.Teammate("Player1", self, score.Score(self, -10, 610, 1.57), self.goals[0])   
        self.playerAmount[0] = True
        self.__startButtonsPlayer[0].delStartButton() 
        if self.__mainButton == None:
            self.__mainButton = startButton.StartButton(self, self.__startGame, 590, 340,"../img/buttonstart.png", 0,160,85,False)
    
    ##    call back for player 2
    #     @param event AVG Event
    def __onClickPlayer2(self, event):
        self.goals[1].goal.opacity = 1 
        self.playerNames[1] = teammate.Teammate("Player2", self, score.Score(self, 320, 2, 3.14), self.goals[1]) 
        self.playerAmount[1] = True
        self.__startButtonsPlayer[1].delStartButton()
        if self.__mainButton == None:
            self.__mainButton = startButton.StartButton(self, self.__startGame, 590, 340,"../img/buttonstart.png", 0,160,85,False)
                 
    ##    call back for player 3
    #     @param event AVG Event
    def __onClickPlayer3(self, event):
        self.goals[2].goal.opacity = 1
        self.playerNames[2] = teammate.Teammate("Player3", self, score.Score(self, 1200, 100, -1.57), self.goals[2])
        self.playerAmount[2] = True
        self.__startButtonsPlayer[2].delStartButton()
        if self.__mainButton == None:
            self.__mainButton = startButton.StartButton(self, self.__startGame, 590, 340,"../img/buttonstart.png", 0,160,85,False)  
   
    ##    call back for player 4
    #     @param event AVG Event
    def __onClickPlayer4(self, event):
        self.goals[3].goal.opacity = 1
        self.playerNames[3] = teammate.Teammate("Player4", self, score.Score(self, 840, 740, 0), self.goals[3])
        self.playerAmount[3] = True
        self.__startButtonsPlayer[3].delStartButton()
        if self.__mainButton == None:
            self.__mainButton = startButton.StartButton(self, self.__startGame, 590, 340,"../img/buttonstart.png", 0,160,85,False) 
                 
    
    ##    create Nodes to display credits
    #     @param event AVG Event
    def __displayCredits(self, event):
        if self.__credits == None:        
            ##    create parent DivNode for animal
            self.__credits = self.player.createNode('div', {                                       
                                                   "width":298, "height":463,
                                                   "x":500, "y":191})   
            self.__area.appendChild(self.__credits)
            ##    video node for OWN state
            self.__creditImage = self.player.createNode('image', {                                       
                                                   "opacity":1,
                                                   
                                                   "href":"../img/credits_image.png",})   
            self.__credits.appendChild(self.__creditImage)
            self.createPlayAgainB()
            self.__deleteMenu()
            
            
    ##    create Nodes to display Tutorial
    #     @param event AVG Event
    def __displayTutorial(self, event):
        if self.__tutorial == None:
            ##    create parent DivNode for animal
            self.__tutorial = self.player.createNode('div', {                                       
                                                   "width":1280, "height":800,
                                                   "x":0, "y":0})   
            self.__area.appendChild(self.__tutorial)
            ##    video node for OWN state
            self.__tutorialVideo = self.player.createNode('video', {                                       
                                                   "opacity":1,
                                                   "width":1280, "height":800,
                                                   "href":"../img/t11.avi",
                                                   "loop":0})   
            self.__tutorialVideo.play()
            self.__tutorial.appendChild(self.__tutorialVideo)
            self.createPlayAgainB()
        self.soundBg[0].sound.stop()
            self.__deleteMenu()
        self.tutorialSound = soundeffect.SoundEffect(self, "../sound/tsound03.wav", 0, False)
            self.tutorialSound.sound.play()            

    ##    count the amount of activated players
    #     @return True if enough player are activated
    def __testPlayerAmount(self):
        for i in range (self.playerAmount.__len__()):
            if self.playerAmount[i] == True:
                self.__countPlayer += 1
        if self.__countPlayer < 2:
            return False
        else:
            return True
          
    ##    terminates the application
    def __exitGame(self, event):
        sys.exit()
#===============================================================================
# 
#===============================================================================
        
        
     ##    initialize animals
    #     @param amount 
    def __initAnimal(self, amount):
        global id
        for Index in range(0, amount):
            ani = self.__animalArray[helpful.getRandomNumber(0, (len(self.__animalArray)-1))]
            if self.__moleActive == True: 
                instance = ani(self, self.__pos1[0], self.__pos1[1], id)
                self.__moleActive = False
            else:
                instance = ani(self, self.__pos2[0], self.__pos2[1], id)
                self.__moleActive = True
            id += 1     
        
            
    ##    initialize mole 
    #    @param amount
    def __createAnimal(self, amount):
        global id
        ##    position of the left mole
        self.__pos1 = avg.Point2D(380, 340)
        ##    position for the right mole
        self.__pos2 = avg.Point2D(840, 340)
        if self.__isUsed == False:  
            self.__moleObj.append(animal.Mole(self, self.__pos1[0], self.__pos1[1], id, 0))
            self.__moleObj.append(animal.Mole(self, self.__pos2[0], self.__pos2[1], id, 3.14))
            self.player.setTimeout(2000, lambda:self.__initAnimal(amount))
            self.__isUsed = True 
        else:
           self.__initAnimal(amount) 
        
    ##    keep track of the animal production
    def __createAnimalManager(self):
        if(self.freeAnimal < 3):
            amount = helpful.getRandomNumber(1,3)
            self.__createAnimal(amount)
            self.freeAnimal += amount

    ##   delete all animals in the game   
    def __deleteAllAnimals(self):
        self.player.clearInterval(self.__createID)
        self.freeAnimal = 0
        collision.animalIndex = -1
        for i in range (self.animals.__len__()):
            if self.animals[i] != None:
                self.animals[i].delAnimal() 
        for i in range (self.__moleObj.__len__()):
            self.__moleObj[i].delete()

    ##   handle remove of animals from the animal list
    #    @param animalID1 id from an animal instance
    #    @param animalID2 id from an animal instance
    #    @param listOfAnimals list of animal id's to remove
    def popAnimals(self, animalID1, animalID2, listOfAnimals):
        reminder = None
        if listOfAnimals==None:
            if animalID1>animalID2:
               self.animals.pop(animalID1)
               self.animals.pop(animalID2)
               reminder=animalID2
            else:
               self.animals.pop(animalID2)
               self.animals.pop(animalID1)
               reminder=animalID1
        else:  
            for i in range (0,listOfAnimals.__len__()-1):
                self.animals.pop(listOfAnimals[i])
            reminder = listOfAnimals.__len__()-1              
        self.updateAnimals(reminder)
        
    ##    adapt animal list to changes
    #    @param start position in animal list
    def updateAnimals(self, start):   
        for start in range (0,self.animals.__len__()):           
            self.animals[start].animalIndex = start 
        self.animalIndex = self.animals.__len__()-1

#===============================================================================
# 
#===============================================================================

    ##    initialize all sounds
    def __loadSounds(self):
        ##    initialize sound nodes for animal sounds
        self.animalSounds = [soundeffect.SoundEffect(self, "../sound/igel.aif", 0, False), soundeffect.SoundEffect(self, "../sound/schnecke.wav", 0, False), None, soundeffect.SoundEffect(self, "../sound/schaf.wav", 0, False), soundeffect.SoundEffect(self, "../sound/hase.wav", 0, False), None]
        ##    initialize sound nodes for special effects
        self.specialSounds = [soundeffect.SoundEffect(self, "../sound/tor_collision.wav", 0, False), soundeffect.SoundEffect(self, "../sound/igel_special.wav", 0, False), soundeffect.SoundEffect(self, "../sound/tor_schaf_schwarz.wav", 0, False), soundeffect.SoundEffect(self, "../sound/winner.wav", 0, False)]
        ##    initialize sound nodes for background 
        self.soundBg = [soundeffect.SoundEffect(self, "../sound/bg.wav", 1, False), soundeffect.SoundEffect(self, "../sound/wiese_bg.wav", 1, False)]
    


