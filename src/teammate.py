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
import helpful, animal, useful, collision, startButton
from useful import *


class Teammate:
    ## Constructor
    #  @param self object pointer.
    #  @param game pointer of the game instance
    #  @param score pointer of the score instance
    #  @param goal pointer of the goal instance
    def __init__(self, name, game, score, goal):
        ##    pointer to the goal instance
        self.__goal = goal
        ##    counter for the animals collected
        self.__animalCollected = 0
        ##    remind for animals in goal
        self.__collected = [[None, 0], [None, 0], [None, 0], [None, 0], [None, 0]]
        ##    defines a name for the instance
        self.__name = name
        ##    pointer to the game instance
        self.__game = game
        ##    pointer to the score instance
        self.score = score
          
  
    ##    show the score for the winner
    def __displayScore(self):
        ##    node for the winner time
        self.winnerTime = self.game.player.createNode('words', { "text":str(self.score.points), "color":"661b25", "fontsize":36}) 
        self.score.score.appendChild(self.winnerTime)
        self.score.score.x = self.__goal.winner.x + 50
        self.score.score.y = self.__goal.winner.y + 50
    
    ##    stops the game if five animals are collected
    def __gamePointCounter(self): 
        if self.__animalCollected == 5:
           #self.__displayScore()
           self.__game.hideScore()
           self.__goal.winner.opacity = 1
           self.__game.specialSounds[3].sound.play()
           self.__game.stopGame()
           
    ##   remove the animal from the goal  
    #    @param animalObject pointer to the animal instance
    def controlAnimalsDown(self, animalObject):
       if self.__collected[animalObject.type][0] != None:
           if self.__collected[animalObject.type][0].id == animalObject.id and collision.isCaught(animalObject):
               self.__goal.placesTaken[self.__collected[animalObject.type][1]] = False
               self.__collected[animalObject.type][0] = None   
               self.__collected[animalObject.type][1] = 0
               self.__animalCollected -= 1
               self.__game.freeAnimal += 1 
  
   ##    handle animal collection
   #    @param animalObject pointer to the animal instance
    def controlAnimalsUp(self, animalObject):  
        if animalObject.state != OWN:
            if animalObject.type == 5:
                self.__game.specialSounds[2].sound.play()
                x = 0
                list = []             
                list.append(animalObject.animalIndex)
                animalReminder = None
                animalObject.delAnimal()
                for i in range (self.__collected.__len__()):
                        if  self.__collected[i][0] == None:
                            animalReminder = x
                        elif self.__collected[i][0] != None :
                           if x != animalReminder:
                               x += 1
                               if list[x-1]<self.__collected[i][0].animalIndex:
                                  list.append(self.__collected[i][0].animalIndex)
                               else:
                                   rem = None
                                   rem = list[x-1]
                                   list[x-1] = self.__collected[i][0].animalIndex
                                   list.append(rem)
                                           
                           animalReminder = None 
                             
                           self.__collected[i][0].delAnimal()
                           self.__collected[i][0] = None
                           self.__animalCollected -= 1
                           self.__goal.placesTaken[i] = False 
                           self.__collected[i][1] = 0  
                self.__game.popAnimals(None,None,list)
            elif self.__collected[animalObject.type][0] != None and animalObject.id != self.__collected[animalObject.type][0].id:
               self.__goal.placesTaken[self.__collected[animalObject.type][1]] = False  
               self.__game.popAnimals(self.__collected[animalObject.type][0].animalIndex,animalObject.animalIndex,None)
               #self.__goal.placesTaken[self.__collected[animalObject.type][1]] = False   
               self.__collected[animalObject.type][1] = 0                        
               self.__collected[animalObject.type][0].delAnimal()  
               self.__collected[animalObject.type][0] = None 
               animalObject.delAnimal() 
               self.__animalCollected -= 1
               self.__game.freeAnimal -= 1    
            else:    
                if animalObject.state != SHOOT:    
                    self.__collected[animalObject.type][0] = animalObject 
                    self.__collected[animalObject.type][1] = self.__goal.findPosition(animalObject)
                    self.__animalCollected += 1
                    self.__game.freeAnimal -= 1
            self.__gamePointCounter()     
  
