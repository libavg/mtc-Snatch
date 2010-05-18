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

class Goal():
    ##   Constructor
    #    @param self object pointer
    #    @param name defines a name for the instance
    #    @param game pointer of the game instance
    #    @param x coordinate for the horizontal position
    #    @param y coordinate for the vertical position
    #    @param angle display angle for the goal
    #    @param midPoint pivotX and pivotY 
    #    @param xWinner x coordinate for the winner image
    #    @param yWinner y coordinate for the winner image
    #    @param place1 position for the first animal in goal
    #    @param place2 position for the first animal in goal
    #    @param place3 position for the first animal in goal
    #    @param place4 position for the first animal in goal
    #    @param place5 position for the first animal in goal
     def __init__(self, name, game, x, y, angle, midPoint, xWinner, yWinner, place1, place2, place3, place4, place5):
         ## defines a name for the instance
         self.__name = name
         ## pointer of the game instance
         self.__game = game
         ## defines pivotX and pivotY of the goal
         self.midPoint = midPoint
         self.__createGoal(x, y, angle, xWinner, yWinner)
         ## x coordinate for the horizontal position
         self.x = x
         ## y coordinate for the vertical position
         self.y = y
         ## reminder for the coordinates of the places
         self.__places = [place1, place2, place3, place4, place5]
         ## reminder for taken places
         self.placesTaken = [False, False, False, False, False]
    
    ##   initialize node for goal
    #    add Node to the AVGTree
    #    @param x coordinate for the horizontal position
    #    @param y coordinate for the vertical position
    #    @param angle display angle for the goal
    #    @param xWinner x coordinate for the winner image
    #    @param yWinner y coordinate for the winner image  
     def __createGoal(self, x, y, angle, winnerX, winnerY):
        ## DivNode for the field
        self.__area = self.__game.player.getElementByID("active_area")
        ##    Image for the goal
        self.goal = self.__game.player.createNode('image', { 
                                               "width":500, "height":159,
                                               "opacity":0,
                                               "href":"../img/tor.png",
                                               "angle":angle,
                                               "x":x, "y":y,})   
        self.__area.appendChild(self.goal)
        ## Image for the winner
        self.winner = self.__game.player.createNode('image', { 
                                               "width":155, "height":22,
                                               "href":"../img/gewonnen.png",
                                               "angle":angle,
                                               "opacity": 0,
                                               "x":winnerX, "y":winnerY})
        self.__area.appendChild(self.winner)
        
        
     ##   looks for the next free position in goal
     #    @param animalObj animal instance
     #    @return place in goal
     def findPosition(self, animalObj):
        for place in range (0, self.placesTaken.__len__()):
            if self.placesTaken[place] == False:
                self.placesTaken[place] = True
                animalObj.animal.x = self.__places[place][0]
                animalObj.animal.y = self.__places[place][1]
                animalObj.animal.angle = self.goal.angle
                return place
                break;
            
     ##   set places to default values
     def resetPlacesTaken(self):
        self.placesTaken = [False, False, False, False, False]
                
        
