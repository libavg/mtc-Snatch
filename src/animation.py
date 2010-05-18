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
import collision
import animal, helpful
import math
from useful import *

def animate(animalObject):
    print animalObject.type
    newList=[]
    if animalObject.type == 0 :
        list=animalObject.game.animals       
        index = animalObject.animalIndex
        if list[index] != None:
            x = list[index].animal.x
            y = list[index].animal.y
            print "erstens"
            #animalObject.cooldown = True
            animalObject.manageAnimation("stab")
            animalObject.doubleEvent=True
            #animal.stopCollision()
            #animal.stopMove()
            animalObject.game.specialSounds[1].sound.play()
            
           
            
            
            
            newList.append(list[index])
            for j in range (0, list.__len__()):
                if list[j] != None:
                    if (list[j].animalIndex != index):
                        jx = list[j].animal.x
                        jy = list[j].animal.y
                        if math.sqrt((x - jx) * (x - jx) + (y - jy) * (y - jy)) < 300:
                            if list[j].state != CAUGHT and list[j].type != IGEL:
                                if list[j].doubleEvent == False:
                                    newList.append(list[j])
                                    list[j].doubleEvent = True
                                    list[j].manageAnimation("stab")
                                    list[j].stopCollision()
                                    list[j].stopMove()
                            #list[j].game.player.setTimeout(1000, lambda:list[j].manageAnimation("stab"))
                            #list[j].game.player.setTimeout(1000, list[j].stopCollision)
                            #list[j].game.player.setTimeout(1000, list[j].stopMove)
            
            #list[index].manageAnimation("stab")             
            list[index].game.player.setTimeout(2000,lambda:reactivateAnimals(newList,index,animalObject))
            list[index].cooldown = list[index].game.player.getFrameTime() + 4000
                            #UrchinStabs(list[j])
                            
                            
                            #print list[index].cooldown
                            
def reactivateAnimals(list, index,animalObject):
    animalObject.manageAnimation("own")
    #animalObject.cooldown = False     
    #animal.startMove()
    #animal.startCollision()
   
    animalObject.doubleEvent=False
    for j in range (0, list.__len__()):
                if list[j] != None:
                    if (list[j].animalIndex != index):                
                            list[j].manageAnimation("own")
                            list[j].doubleEvent = False
                            list[j].startMove()
                            list[j].startCollision()
