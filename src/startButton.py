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

class StartButton(button.Button):
    ##   Constructor
    #    @param self object pointer
    #    @param game pointer to the game instance
    #    @param onClick call back function for click events
    #    @param x coordinate for the horizontal position
    #    @param y coordinate for the vertical position
    #    @param source path to the image file
    #    @param angle display angle for the button
    #    @param width set width for the DivNode
    #    @param height set height for the DivNode
    #    @param on True for Countdown (3, 2, 1); False for normal button
     def __init__(self, game, onClick, x, y, source, angle, width, height, on):
         ## pointer to the game instance
         self.game = game
         ## display angle for the button 
         self.__angle = angle
         ## True or False
         self.__on = on
         ## position of the button
         #self.__pos = avg.Point2D(x, y)
         ## width and height
         self.__size = avg.Point2D(width, height)
         ## DivNode for the field
         self.__area = game.player.getElementByID("active_area")
         ## DivNode for the button
         self.start_button = game.player.createNode('div', {                                       
                                               "width":self.__size[0], "height":self.__size[1],
                                               "x":x, "y":y, 
                                               "angle":self.__angle}) 
         self.__area.appendChild(self.start_button)
         self.__img1 = game.player.createNode('image', { "href":source}) 
         self.start_button.appendChild(self.__img1)
         self.__img2 = game.player.createNode('image', { "href":source}) 
         self.start_button.appendChild(self.__img2)
         self.__img3 = game.player.createNode('image', { "href":source}) 
         self.start_button.appendChild(self.__img3)
         self.__img4 = game.player.createNode('image', { "href":source}) 
         self.start_button.appendChild(self.__img4)
         
         if (self.__on):
            self.__countdown = Countdown(self, self.__angle)
         
         button.Button.__init__(self, self.start_button, onClick)
         
     ##    remove the DivNode from the tree   
     def delStartButton(self):
         useful.deleteNode(self.start_button)
         if (self.__on):
            self.__countdown.deleteCountdown()
            
     
         
         
class Countdown:
    ##   Constructor
    #    @param self object pointer
    #    @param startButton pointer to the StartButton instance
    #    @param angle display angle
    def __init__(self, startButton, angle):
        ## pointer to the StartButton instance
        self.__startButton = startButton
        ## display angle
        self.__angle = angle
        if self.__angle == -1.57:
            ## position for the highscore
            self.__pos = avg.Point2D(self.__startButton.start_button.x+125, self.__startButton.start_button.y-25)
        elif self.__angle == 1.57:
            self.__pos = avg.Point2D(self.__startButton.start_button.x-100, self.__startButton.start_button.y-40)
        elif self.__angle == 3.14:
            self.__pos = avg.Point2D(self.__startButton.start_button.x+25, self.__startButton.start_button.y-140)
        else:
            self.__pos = avg.Point2D(self.__startButton.start_button.x+15, self.__startButton.start_button.y+80)
        ## DivNode for the field
        self.__area = self.__startButton.game.player.getElementByID("active_area")
         ## DivNode contains images for the countdown
        self.__countdownNode = self.__startButton.game.player.createNode('div', {                                       
                                               "width":100, "height":134,
                                               "x":self.__pos[0], "y":self.__pos[1], 
                                               "angle":angle}) 
        self.__area.appendChild(self.__countdownNode)
        ##    Image node 1
        self.__img1 = self.__startButton.game.player.createNode('image', { "href":"../img/1_.png", "opacity": 0}) 
        self.__countdownNode.appendChild(self.__img1)
        ##    Image node 2
        self.__img2 = self.__startButton.game.player.createNode('image', { "href":"../img/2_.png", "opacity": 0}) 
        self.__countdownNode.appendChild(self.__img2)
        ##    Image node 3
        self.__img3 = self.__startButton.game.player.createNode('image', { "href":"../img/3_.png", "opacity": 0}) 
        self.__countdownNode.appendChild(self.__img3)
        
        #if (self.__startButton.on):
        self.__startContdown()
            
    ##    remove the DivNode from the tree    
    def deleteCountdown(self):
        useful.deleteNode(self.__countdownNode)
        
    ##    set image opacity to 0
    def __hideImages(self):
        self.__img1.opacity = 0
        self.__img2.opacity = 0
        self.__img3.opacity = 0
        
    ##    show current cipher
    #     @param image 
    def __displayImage(self, image):
        self.__hideImages()   
        image.opacity = 1
    
    ## start countdown 
    def __startContdown(self):
        self.__startButton.game.player.setTimeout(2000, lambda:self.__displayImage(self.__img3))
        self.__startButton.game.player.setTimeout(3000, lambda:self.__displayImage(self.__img2))
        self.__startButton.game.player.setTimeout(4000, lambda:self.__displayImage(self.__img1))
        #self.startButton.game.player.setTimeout(5000, self.startButton.game.startGame)
        
        
