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

from libavg import avg
from game import Game

mtc = True
ShowFingers = False
filenum = 0

def flipBitmap(Node):
    Grid = Node.getOrigVertexCoords()
    Grid = [ [ (pos[0], 1-pos[1]) for pos in line ] for line in Grid]
    Node.setWarpedVertexCoords(Grid)



def updateBitmap(TrackerID):
  
    Bitmap = Tracker.getImage(TrackerID)
    Node = Player.getElementByID("fingers")
    Node.setBitmap(Bitmap)
    Node.width = 1280
    Node.height = 800
    flipBitmap(Node)   
        
def activateFingers():
    global Tracker
    global ShowFingers
    if ShowFingers:
        Player.getElementByID("fingers").active = 1
    else:
        Player.getElementByID("fingers").active = 0
    Tracker.setDebugImages(False, ShowFingers)

def dump():
    global filenum

    Player.screenshot().save('dump/dmp-%04d.tga' %filenum)
    filenum+=1

    

Player = avg.Player.get()  
Player.loadFile("snatch.avg")
Wiese = Player.getElementByID("gras")
if mtc:
    Tracker = Player.addTracker("avgtrackerrc")
    Player.setResolution(1,0,0,0)
    Player.setOnFrameHandler(lambda:updateBitmap(avg.IMG_FINGERS))
    #Player.setOnFrameHandler(dump)
    activateFingers()
    
else:
    Player.setResolution(0,0,0,0)
Game(Player,3)

Player.setVBlankFramerate(5)
Player.play()

