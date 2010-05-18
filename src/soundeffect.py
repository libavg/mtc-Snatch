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


class SoundEffect():
    ##   Constructor
    #    @param self object pointer.
    #    @param game pointer of the game instance
    #    @param source path to the audio file
    #    @param loop 1 for True; 0 for False
    #    @param state True for play; False for pause
    def __init__(self, game, source, loop, state):
        ## pointer of the game instance
        self.__game = game
        ## 1 or 0
        self.__loop = loop
        ## path to the audio file
        self.__source = source
        ## play or pause
        self.__state = state
        self.__createNode()
    
    ##   initialize Sound 
    #    add Node to the AVGTree
    def __createNode(self):
        ## DivNode for the field
        self.__area = self.__game.player.getElementByID("active_area")  
        ## Sound 
        self.sound = self.__game.player.createNode('sound', {                                       
                                               "href":self.__source,
                                               "loop":self.__loop})   
        self.__area.appendChild(self.sound)
        
        if self.__state:
            self.sound.play()
        else:
            self.sound.pause()
