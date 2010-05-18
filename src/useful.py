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

##    type for the Hedgehog instance
IGEL = 0
##    type for the Snail instance
SCHNECKE = 1
##    type for the Turtle instance
SCHILDKROETE = 2
##    type for the Sheep instance
SCHAF = 3
##    type for the Rabbit instance
HASE = 4
##    type for the BlackSheep instance
SCHAFSCHWARZ = 5


##    state for default move of the animal instance
OWN = 1
##    state for dragged move of the animal instance
DRAGGED = 2
##    state for bounced move of the animal instance
BOUNCED = 3
##    state for caught move of the animal instance
CAUGHT = 4
##    state for shoot move of the animal instance
SHOOT = 5

##    initialize state of the game
INIT = 0
##    play state of the game
PLAY = 1

##    remove the given node from the tree
#     @param node AVGNode to remove
def deleteNode(node):
    parent=node.getParent()
    if parent != None:
        pos=parent.indexOf(node)
        parent.removeChild(pos) 
