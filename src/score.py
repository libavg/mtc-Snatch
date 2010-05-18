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
import helpful, useful, collision

class Score:
    ## Constructor
    #  @param self object pointer.
    #  @param game pointer of the game instance
    #  @param x x coordinate for the node
    #  @param y coordinate for the node
    #  @param angle angle for the node
    def __init__(self, game, x, y, angle):
        ## current points of the score
        self.points = 0
        ## pointer of the game instance
        self.__game = game
        ## DivNode for the field
        self.__area = game.player.getElementByID("active_area")
        ## DivNode for the score
        self.score = game.player.createNode('div', {                                       
                                               "width":80, "height":50,
                                               "x":x, "y":y,
                                               "angle":angle}) 
        self.__area.appendChild(self.score)
        ## Node display the points
        self.text = game.player.createNode('words', { "text":str(self.points), 
                                                      "color":"661b25", 
                                                      "size":36}) 
        self.score.appendChild(self.text)
    

    
    ##    display new amount 
    def update(self):
        useful.deleteNode(self.text)
        self.text = self.__game.player.createNode('words', { "text":str(self.points), "color":"661b25", "size":36}) 
        self.score.appendChild(self.text)
     
    ##    remove the DivNode from the tree
    def deleteScore(self):
        useful.deleteNode(self.score)
        
