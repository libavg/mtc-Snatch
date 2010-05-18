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

from libavg import*
import animal, helpful
import math
from useful import *
counter=1

#@return return list 
def getList():
    return list
##push a node to the global list
#@param animal the node of an animal
#@return animalIndex return the index of the animal 
def pushNode(animal):
    animal.game.animals.append(animal)
    animal.game.animalIndex +=1
    return animal.game.animalIndex

## proves if an animal is caught
#@param animal the node of an animal
#@return True when its inside a goal
def isCaught(animal):
    for i in range (animal.game.playerAmount.__len__()):
        if animal.game.playerAmount[i]:
            if helpful.isInGoal(animal, animal.game.goals[i].midPoint[0], animal.game.goals[i].midPoint[1]):
                return True
##handling for the catching of an animal
#@param animal the node of an animal 
#@param event Up or Down   
def catchedControl(animal, event):    
    if helpful.isInGoal(animal, animal.game.goals[0].midPoint[0], animal.game.goals[0].midPoint[1]) and animal.game.playerAmount[0]:
        if event:
            animal.game.playerNames[0].controlAnimalsUp(animal)
             
            animal.stateReminderCaught = 0
        else:
            animal.game.playerNames[0].controlAnimalsDown(animal) 
    elif helpful.isInGoal(animal, animal.game.goals[1].midPoint[0], animal.game.goals[1].midPoint[1]) and animal.game.playerAmount[1]:
        if event:
            animal.game.playerNames[1].controlAnimalsUp(animal) 
            animal.stateReminderCaught = 1
        else:
            animal.game.playerNames[1].controlAnimalsDown(animal)      
    elif helpful.isInGoal(animal, animal.game.goals[2].midPoint[0], animal.game.goals[2].midPoint[1]) and animal.game.playerAmount[2]:
        if event:
            animal.game.playerNames[2].controlAnimalsUp(animal) 
            animal.stateReminderCaught = 2
        else:
            animal.game.playerNames[2].controlAnimalsDown(animal)
    elif helpful.isInGoal(animal, animal.game.goals[3].midPoint[0], animal.game.goals[3].midPoint[1]) and animal.game.playerAmount[3]:
        if event:
            animal.game.playerNames[3].controlAnimalsUp(animal) 
                       
            animal.stateReminderCaught = 3
        else:
            animal.game.playerNames[3].controlAnimalsDown(animal) 
    
##proves if the requirements for creating a BlackSheep are given
#@param animalObj1 node of an animal
#@param animalObj2 node of an animal
#@return True 
def testSheepCollision(animalObj1, animalObj2):
      if animalObj1.stateReminderCaught != -1 and animalObj2.stateReminderCaught != -1:
        if animalObj1.stateReminderCaught != animalObj2.stateReminderCaught:    
            return True   
## calculates if two animal nodes touch each other 
#calculates if an animal hit a wall
#@param animal the node of an animal   
def collision(animal):
        global counter
        index = animal.animalIndex
        
        if index < animal.game.animals.__len__():
            if animal.game.animals[index] != None:
                x = animal.game.animals[index].animal.x
                y = animal.game.animals[index].animal.y
                #print animal.game.animals[index].bounceX, animal.game.animals[index].animal.pos, animal.game.animals[index].state
                if animal.game.animals[index].state!=DRAGGED:
                   #print animal.game.animals[index].bounceX, animal.game.animals[index].animal.pos
                   if animal.game.animals[index].bounceX==-1:
                   
                        if animal.game.animals[index].animal.y<=0:
                            animal.game.animals[index].bounceX = 0
                            animal.game.animals[index].wallBounce=True
                            animal.game.animals[index].animal.y=5
                            
                            #print "top hit"
                        if animal.game.animals[index].animal.y>=735:
                            animal.game.animals[index].bounceX = 1 
                            animal.game.animals[index].wallBounce=True
                            animal.game.animals[index].animal.y=730
                            #print "bottom hit"
                        if animal.game.animals[index].animal.x<=0:
                            animal.game.animals[index].bounceX = 2
                            animal.game.animals[index].wallBounce=True 
                            animal.game.animals[index].animal.x=5
                            #print "left hit"
                        if animal.game.animals[index].animal.x>=1215:
                            animal.game.animals[index].bounceX = 3
                            animal.game.animals[index].wallBounce=True 
                            animal.game.animals[index].animal.x=1210
                            #print "right hit"
                   for j in range (0, animal.game.animals.__len__()):
                        if animal.game.animals[j] != None:
                            if (animal.game.animals[j].animalIndex != index):
                               
                                jx = animal.game.animals[j].animal.x
                                jy = animal.game.animals[j].animal.y
                                     
                                if math.sqrt((x - jx) * (x - jx) + (y - jy) * (y - jy)) < 40:
                                #-------- Sheep collision   
                                    if animal.game.animals[j].type == SCHAF and animal.game.animals[index].type == SCHAF:   
                                        if testSheepCollision(animal.game.animals[j], animal.game.animals[index]):  
                                           #print "jez ein schwarez schaf bitte"
                                           createBlackSheep(animal.game.animals[j])
                                           animal.game.animals[j].delAnimal()
                                           animal.game.animals[index].delAnimal()
                                           animal.game.popAnimals(animal.game.animals[j].animalIndex,animal.game.animals[index].animalIndex,None)
                                           animal.game.freeAnimal -= 2 
                                           break                                       
                                    getroffen =False
                                 #   print "gr",animal.game.animals[index].timeCollisionObj.__len__()
                                    for n in range (0,animal.game.animals[index].timeCollisionObj.__len__()):
                                          if animal.game.animals[j]==animal.game.animals[index].timeCollisionObj[n][0]: 
                                             getroffen =True
                                    
                                    #print "GETROFFEN", getroffen         
                                    if getroffen== False: 
                                        
                                        
                                        if animal.game.animals[j].state != DRAGGED and  animal.game.animals[j].state != CAUGHT and  animal.game.animals[index].state != CAUGHT:
                    #----------------------- Crash laesst eine wolke einblenden solange die Tiere kollidieren!!!!
                                            Crash(animal.game.animals[index])
                                          #  print "Es treffen sich 2 Tiere"
                                           # print "animal ", index, " bounce on ", animal.game.animals[j].animalIndex
                                            animal.game.animals[index].animalCollision = True
                                            animal.game.animals[index].collisionObj = animal.game.animals[j]
                                            timeObjCombiner=[animal.game.animals[j],animal.game.animals[j].game.player.getFrameTime() + 100]
                                            animal.game.animals[index].timeCollisionObj.append(timeObjCombiner)
                                            timeObjCombiner=[animal.game.animals[index],animal.game.animals[index].game.player.getFrameTime() + 100]
                                            animal.game.animals[j].timeCollisionObj.append(timeObjCombiner)   
## creates a BlackSheep
#@param aniObjectJ node of an animal 
def createBlackSheep(aniObjectJ):
    animal.BlackSheep(aniObjectJ.game, aniObjectJ.animal.x, aniObjectJ.animal.y, 100)
            
class Crash:
    ##Constructor
    #@param animal node of an animal  
    def __init__(self, animal):
        ##variable for the animal
        self.__animal = animal
        ##DivNode for the field
        self.__area = animal.game.player.getElementByID("active_area")
        ## Image Node for the Cloud
        self.__cloud = animal.game.player.createNode('<image href="../img/crash.png" />')
      
        self.__area.appendChild(self.__cloud)
        self.__cloud.x = animal.animal.x-30
        self.__cloud.y = animal.animal.y-30
        self.__cloud.width = animal.animal.width*2
        self.__cloud.height = animal.animal.width*2
        
        self.__animal.game.player.setTimeout(10,self.__stop)
    
    ##deletes the node of the cloud 
    def __stop(self):
        deleteNode(self.__cloud)


        
              
