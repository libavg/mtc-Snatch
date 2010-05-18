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
import math
import helpful, collision, game, soundeffect
import animation
from useful import *

class Animal:
    ##Constructor
    #@param self The object pointer.
    #@param source gives the path to video for the own state .
    #@param sourceShoot gives the path to video for the Shoot state.
    #@param sourceStab gives the path to video for the special state.
    #@param game The pointer of the game instance
    #@param x Coordinate of Node Position horizontal
    #@param y Coordinate of Node Position vertical  
    def __init__(self, source, sourceShoot, sourceStab, game, x, y):       
#------------------------------- state definition
        ## State Variable for the animal can contain OWN,SHOOT,CAUGHT,DRAGGED
        self.state = OWN
        ## variable which points on the game instance
        self.game = game
        ## marker for which wall is hit
        self.bounceX = -1
        ## variable that only one Event can happen on an Node
        self.__cursorID = None
        ##rember down event
        self.__offset = None
        ## get set when 2 animals collide
        self.animalCollision = False
        ## positon of the animal in the global List
        self.animalIndex = None 
        ##rember the last Down of an Node, in FrameTime
        self.__lastMouseDownFrameTime = 0
        ##rembers bounce events in FrameTime
        self.timeCollisionObj = []
        ##Pointer of the Animal to bounce with
        self.collisionObj = None
        ##get set when an animal hits an wall
        self.wallBounce=False
        ## rembers the last Up event in FrameTime
        self.__lastUpEvent=None
        ##rembers the goal in witch the animal is caught until an UP event happens 
        self.stateReminderCaught = -1
        ## time for next special attack (Hedgehog)
        self.cooldown = self.game.player.getFrameTime()
        ##rembers if an doubleEvent takes place
        self.doubleEvent = False
        self.__createNodes(source, sourceShoot, sourceStab, x, y)
        self.animalIndex = collision.pushNode(self)
        self.startCollision()
        game.player.setOnFrameHandler(self.__collisionException)
        game.player.setOnFrameHandler(self.__reduceSpeed)
        self.startMove()      
        ## rembers the last 5 positions of the animal
        self.queue=[self.animal.pos, self.animal.pos, self.animal.pos, self.animal.pos, self.animal.pos, self.animal.pos]
        ##the point where the animal moves to
        self.destinationPoint = self.newDestinationPoint(self.animal)
        ##the move - vector of the animal including the speed
        self.__speedVector = helpful.normalize(self.destinationPoint - self.animal.pos)
       

    ##moves the animal depending on his state over the screen on Frame
    def __move(self):
        collsionmerker=self.collisionObj
        if self.state == OWN:
            if self.__lastUpEvent <= self.game.player.getFrameTime() and self.__lastUpEvent !=None:
                self.stateReminderCaught = -1
                self.__lastUpEvent =None
            if collision.isCaught(self):
               self.destinationPoint = self.newDestinationPoint(self.animal)
            if self.animal.x <= self.destinationPoint[0]+self.__speedVector[0] and self.animal.x >= self.destinationPoint[0]-self.__speedVector[0]:
                self.destinationPoint = self.newDestinationPoint(self.animal)
            else:    
                self.animal.pos += self.__speedVector                
        if self.state == DRAGGED:
            self.animal.x = int(self.movePos[0])
            self.animal.y = int(self.movePos[1])  
        if self.state == SHOOT:
               if collision.isCaught(self):
                  collision.catchedControl(self, True)
               if self.__lastUpEvent <= self.game.player.getFrameTime() and self.__lastUpEvent!=None:
                    self.stateReminderCaught = -1
                    self.__lastUpEvent =None 
               self.animal.pos += self.__speedVector               
        if self.wallBounce == True: 
               if self.bounceX != -1:
                   NewWallBouncePoint=helpful.wallBouncing(self.animal,self.queue,self.bounceX,self.__speedVector)
                   self.destinationPoint=NewWallBouncePoint[1]
                   self.__speedVector = NewWallBouncePoint[0]
                   self.bounceX = -1                  
               self.wallBounce = False
               self.animal.pos += self.__speedVector      
               
               
        if self.animalCollision==True:
               if self.collisionObj != None :
                   NewPoint=helpful.AnimalBounce(self.animal,self.queue,self.__speedVector,self.collisionObj.animal,self.collisionObj.queue,self.collisionObj.__speedVector)
                   if self.collisionObj.__moveID != None:                     
                       if self.state == SHOOT:
                            self.collisionObj.state = SHOOT
                            self.collisionObj.manageAnimation("shoot")
                       self.collisionObj.destinationPoint=avg.Point2D(NewPoint[1][0],NewPoint[1][1])
                       self.collisionObj.__speedVector = avg.Point2D(NewPoint[1][2],NewPoint[1][3])
                       result = helpful.batch(self.animal,self.collisionObj.animal)
                       self.collisionObj.animal.pos -= result
                   self.destinationPoint = avg.Point2D(NewPoint[0][0],NewPoint[0][1])
                   self.__speedVector = avg.Point2D(NewPoint[0][2],NewPoint[0][3])                  
                   self.animal.pos += result     
                   self.animalCollision = False
                   self.collisionObj = None                            
        self.animal.angle=helpful.drehung(self.animal, self.queue)
        self.queue.append(self.animal.pos)
        self.queue.pop(0)
      
    ##Eventhandler for Down events
    #@param Event Parameter from the avg              
    def __onMouseDown(self, Event):
        if Event.source==avg.TOUCH or Event.source==avg.MOUSE:
            if self.game.animalSounds[self.type] != None:
                self.game.animalSounds[self.type].sound.play()
            if self.__offset == None:
                if self.state == CAUGHT:        
                    collision.catchedControl(self, False)
                    self.startCollision()
            self.startMove()
                    self.bounceX=-1
                if self.state != CAUGHT:
                    if (self.game.player.getFrameTime() - self.__lastMouseDownFrameTime) < 500 and self.type == IGEL and self.cooldown <= self.game.player.getFrameTime():
                                       
                        
                        animation.animate(self)                   
                self.__lastMouseDownFrameTime = self.game.player.getFrameTime()
                self.__offset = avg.Point2D(self.animal.getRelPos((Event.x, Event.y)))
                self.animal.setEventCapture(Event.cursorid)
                self.__cursorID = Event.cursorid
        
    ##Eventhandler for Move events
    #@param Event Parameter from the avg    
    def __onMouseMove(self, Event):
        if self.__offset != None and self.__cursorID==Event.cursorid:
            self.state = DRAGGED
            if self.doubleEvent !=True:          
                self.manageAnimation("caught")
            ##    remind the dragged position
            self.movePos = Event.x - self.__offset[0], Event.y - self.__offset[1]
            
    ##Eventhandler for Up events
    #@param Event Parameter from the avg    
    def __onMouseUp(self, Event):
        if self.__offset != None and self.__cursorID==Event.cursorid:
            self.__offset = None
            self.animal.releaseEventCapture(self.__cursorID)
            if collision.isCaught(self):
                self.state = CAUGHT 
                self.stopCollision()
        self.stopMove()
                self.manageAnimation("caught")
                collision.catchedControl(self, True)                                      
            else:
                speed = Event.speed
                upPos = self.animal.pos
                if (speed[0]> 1)| (speed[0]< -1) | (speed[1] > 1) | (speed[1] < -1 ):              
                    self.__speedVector = helpful.normalize(upPos - self.queue[1]) 
                    self.__speedVector=self.__speedVector*20
                    self.state = SHOOT
                    self.manageAnimation("shoot")   
                    self.__lastUpEvent = self.game.player.getFrameTime() + 200
                    self.bounceX = -1
                else:    
                    self.destinationPoint = self.newDestinationPoint(self.animal)
                    self.state = OWN
                    if self.doubleEvent!=True:
                       self.manageAnimation("own")
                    self.__lastUpEvent = self.game.player.getFrameTime() + 200
                    self.__speedVector = self.__speedVector*1
                    
                    
        
    ##calculates the new DestinationPoint for the animal
    #@param node DivNode for the animal 
    #@return: destinationPoint     
    def newDestinationPoint(self, node):
        isInsideOfTable = False
        isInsideOfGoal = False
        
        destinationPoint = avg.Point2D((helpful.getRandomNumber(node.x - 300, node.x + 300)), (helpful.getRandomNumber(node.y - 300, node.y + 300)))
        slope = helpful.linearFunction(node.pos, destinationPoint)
        while destinationPoint[0] > 1200 or destinationPoint[0] < 20 or destinationPoint[1] > 700 or destinationPoint[1] < 20 or helpful.pointControl(destinationPoint) or abs(slope[0]) > 5:
            destinationPoint = avg.Point2D((helpful.getRandomNumber(node.x - 300, node.x + 300)), (helpful.getRandomNumber(node.y - 300, node.y + 300)))
            slope = helpful.linearFunction(node.pos, destinationPoint)
        self.__speedVector = helpful.normalize(destinationPoint - self.animal.pos)
        return destinationPoint
    
    ##removes the DivNode of the animal from the avg tree
    def delAnimal(self):
        self.stopMove()
        self.stopCollision()
        deleteNode(self.animal)
    
    ## stop the move methode     
    def stopMove(self):
        self.game.player.clearInterval(self.__moveID)
    
    ## start the move methode 
    def startMove(self):
        ##    remind id of frame handler
        self.__moveID = self.game.player.setOnFrameHandler(self.__move)
    
    ## stop the Collision methode    
    def stopCollision(self):
        self.game.player.clearInterval(self.__collisionID)
    
    ## start the Collision methode
    def startCollision(self):
        ##    remind id of frame handler
        self.__collisionID = self.game.player.setOnFrameHandler(lambda:collision.collision(self))
    
    ##clear the collsion array on Frame
    def __collisionException(self):
            tmpTime = self.game.player.getFrameTime()
            if self.timeCollisionObj.__len__() != 0:
                for i in  range (0, self.timeCollisionObj.__len__()):
                       if i < self.timeCollisionObj.__len__():
                           if  self.timeCollisionObj[i][1] <= tmpTime:
                               self.timeCollisionObj.pop(0)
    ##adapt velocity to the current state on Frame                      
    def __reduceSpeed(self):
        vX = self.__speedVector[0]
        vY = self.__speedVector[1]
        vecLength = math.sqrt((vX*vX)+(vY*vY))
        if vecLength <= 1:
            self.__speedVector*=1
        else:
            self.__speedVector*=0.99
        if self.state == SHOOT and vecLength <= 1:
            if collision.isCaught(self)!=True:                    
               self.state = OWN
               if self.doubleEvent!=True:
                        self.manageAnimation("own")
            
    ## initialize video Nodes for animal class
    #    add Node to the AVGTree
    #@param source gives the path to video for the own state .
    #@param sourceShoot gives the path to video for the Shoot state.
    #@param sourceStab gives the path to video for the special state.
    #@param x Coordinate for horizontal position 
    #@param y Coordinate for vertical position                         
    def __createNodes(self, sourceOwn, sourceShoot, sourceStab, x, y):
        ## DivNode for the field
        self.__area = self.game.player.getElementByID("active_area")
        ##    create parent DivNode for animal
        self.animal = self.game.player.createNode('div', {                                       
                                               "width":48, "height":48,
                                               "x":x, "y":y})   
        self.__area.appendChild(self.animal)
        ##    video node for OWN state
        self.__animalOwn = self.game.player.createNode('video', {                                       
                                               "opacity":1,
                                               
                                               "href":sourceOwn,
                                               "loop":1})   
        self.__animalOwn.play()
        self.animal.appendChild(self.__animalOwn)
        ##    video node for SHOOT state       
        self.__animalShoot = self.game.player.createNode('video', {                                          
                                               "opacity":0,
                                              
                                               "href":sourceShoot,
                                               "loop":1})   
        self.__animalShoot.stop()
        self.animal.appendChild(self.__animalShoot)
        ##    video node for SPECIAL Hedgehog state       
        self.__animalStab = self.game.player.createNode('video', {                                          
                                               "opacity":0,
                                               
                                               "href":sourceStab,
                                               "loop":0})   
        self.__animalStab.stop()
        self.animal.appendChild(self.__animalStab)              
        self.animal.setEventHandler(CURSORDOWN, MOUSE | TOUCH, self.__onMouseDown)
        self.animal.setEventHandler(CURSORMOTION, MOUSE | TOUCH, self.__onMouseMove)
        self.animal.setEventHandler(CURSORUP, MOUSE | TOUCH, self.__onMouseUp)

    ##match video to state
    #@param state the current state of the animal   
    def manageAnimation(self, state):       
        self.__animalOwn.pause()
        self.__animalOwn.opacity = 0        
        self.__animalShoot.pause()
        self.__animalShoot.opacity = 0        
        self.__animalStab.stop()
        self.__animalStab.opacity = 0        
        if state == "own":
            self.__animalOwn.play()
            self.__animalOwn.opacity = 1
        elif state == "shoot":
            self.__animalShoot.play()
            self.__animalShoot.opacity = 1
        elif state == "stab":
            #self.__animalOwn.opacity = 0
            self.__animalStab.play()
            self.__animalStab.opacity = 1
        elif state == "caught":
            #self.animalOwn.pause()
            self.__animalOwn.opacity = 1
            


class Turtle(Animal):
    ##Constructor
    #@param game The pointer of the game instance
    #@param x Coordinate of Node Position horizontal
    #@param y Coordinate of Node Position vertical
    #@param id index 
    def __init__(self, game, x, y, id):
        source = "../img/schildie_own.mov"
        sourceShoot = "../img/schildie_schuss.mov"
        sourceStab = "../img/schildie_sterne.mov"
        ## defines a name for the instance
        self.__name = "Turtle" 
        ##    defines the type for the instance 
        self.type = SCHILDKROETE
        ##    unique index
        self.id = id         
        Animal.__init__(self, source, sourceShoot, sourceStab, game, x, y)
        

class Sheep(Animal):
    ##Constructor
    #@param game The pointer of the game instance
    #@param x Coordinate of Node Position horizontal
    #@param y Coordinate of Node Position vertical
    #@param id index 
    def __init__(self, game, x, y, id):
        source = "../img/schaf_weiss_own.mov" 
        sourceShoot = "../img/schaf_weiss_schuss.mov" 
        sourceStab = "../img/schaf_weiss_sterne.mov"
        ## defines a name for the instance
        self.__name = "Sheep" 
        ##    defines the type for the instance
        self.type = SCHAF
        ##    unique index
        self.id = id          
        Animal.__init__(self, source, sourceShoot, sourceStab, game, x, y)
       
        
class Snail(Animal):
    ##Constructor
    #@param game The pointer of the game instance
    #@param x Coordinate of Node Position horizontal
    #@param y Coordinate of Node Position vertical
    #@param id index 
    def __init__(self, game, x, y, id):      
       source = "../img/schnecke_own.mov"  
       sourceShoot = "../img/schnecke_schuss.mov" 
       sourceStab = "../img/schnecke_sterne.mov"
       ## defines a name for the instance
       self.__name = "Snail"
       ##    defines the type for the instance
       self.type = SCHNECKE
       ##    unique index
       self.id = id    
       Animal.__init__(self, source, sourceShoot, sourceStab, game, x, y)
       

class Rabbit(Animal):
    ##Constructor
    #@param game The pointer of the game instance
    #@param x Coordinate of Node Position horizontal
    #@param y Coordinate of Node Position vertical
    #@param id index 
    def __init__(self, game, x, y, id):      
       source = "../img/hase_own.mov"   
       sourceShoot = "../img/hase_schuss.mov" 
       sourceStab = "../img/hase_sterne.mov"
       ## defines a name for the instance
       self.__name = "Rabbit"
       ##    defines the type for the instance
       self.type = HASE
       ##    unique index
       self.id = id   
       Animal.__init__(self, source, sourceShoot, sourceStab, game, x, y)
      

class Hedgehog(Animal):
    ##Constructor
    #@param game The pointer of the game instance
    #@param x Coordinate of Node Position horizontal
    #@param y Coordinate of Node Position vertical
    #@param id index 
    def __init__(self, game, x, y, id):
        source = "../img/igel_own.mov"  
        sourceShoot = "../img/igel_schuss.mov"
        sourceStab = "../img/igel_nackt.mov"   
        ## defines a name for the instance 
        self.__name = "Hedgehog"
        ##    defines the type for the instance
        self.type = IGEL
        ##    unique index
        self.id = id           
        Animal.__init__(self, source, sourceShoot, sourceStab, game, x, y)

        
class BlackSheep(Animal):
    ##Constructor
    #@param game The pointer of the game instance
    #@param x Coordinate of Node Position horizontal
    #@param y Coordinate of Node Position vertical
    #@param id index 
    def __init__(self, game, x, y, id):
        source = "../img/schaf_schwarz_own.mov"  
        sourceShoot = "../img/schaf_schwarz_schuss.mov"
        sourceStab = "../img/schaf_schwarz_sterne.mov" 
        ##    defines a name for the instance
        self.__name = "BlackSheep"
        ##    defines the type for the instance
        self.type = SCHAFSCHWARZ
        ##    unique index
        self.id = id           
        Animal.__init__(self, source, sourceShoot, sourceStab, game, x, y)
        
class Mole():
    ##Constructor
    #@param game The pointer of the game instance
    #@param x Coordinate of Node Position horizontal
    #@param y Coordinate of Node Position vertical
    #@param id index
    #@param angle display angle
    def __init__(self, game, x, y, id, angle):
        ##    pointer to the game instance
        self.__game = game
        source = "../img/maulwurf.mov"
        ## DivNode for the field
        self.__area = self.__game.player.getElementByID("active_area")
        ##    create parent DivNode for Mole
        self.mole = self.__game.player.createNode('div', {                                       
                                               "width":50, "height":58,
                                               "x":x, "y":y,
                                               "angle": angle})   
        self.__area.appendChild(self.mole)
        ##    Video node for the mole
        self.__moleVideo = self.__game.player.createNode('video', {                                       
                                               "opacity":1,
                                               "href":source,
                                               "loop":0})   
        self.__moleVideo.play()
        self.mole.appendChild(self.__moleVideo)
        
    ##delete the mole node    
    def delete(self):
        deleteNode(self.mole)
        
        
