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
import useful,startButton
import Image, ImageDraw
import os
class Highscore():
     ##Constructor
     #@param self The object pointer.
     #@param name defines a name for the instance
     #@param game The pointer of the game instance
     #@param x Coordinate of Node Position horizontal
     #@param y Coordinate of Node Position vertical
     #@param time
     def __init__(self, name, game, x, y,time):
         ## variable for the name of the instance
         self.__name = name
         ## variable which points on the game instance
         self.__game = game
         ##variable for the time of the winner
         self.__high= time
         ##variable for drawing canvas
         self.__winnerCanvas = None
         ##variable for the canvas Background
         self.__canvasBackground = None
         ##variable for the position of the canvas node horizontal
         self.__gloX=x+18
         ##variable for the position of the canvas node vertical
         self.__gloY=y+57
         ##position in Highscore list
         self.HighscorePosition = None
         ## variable that only one Event can happen on an Node
         self.__cursorID = None
         ##rember down event
         self.__offset = None
         ##color variable includes 3 int
         self.__black = (0, 0, 0)
         ##color variable includes 3 int 
         self.__white= (255,255,255)
         ##rembers a down event for drawing
         self.__firstDown = False
         ##remindes for the horizontal coordinate of the last frame
         self.__xold = None
         ##remindes for the vertical coordinate of the last frame
         self.__yold = None
         ##variable for PIL Image used for saving
         self.__image1 = Image.new("RGB", (300, 150), self.__white)
         ##variable for PIL Memory-DrawImage used for saving 
         self.__draw = ImageDraw.Draw(self.__image1)
         ##list which inculdes the lines to be drawn when saving
         self.__drawList= []
         ## DivNode for the field
         self.__area = self.__game.player.getElementByID("active_area")
         ## list with the Positons of the Highscore members 
         self.__highscorePos = [avg.Point2D(70, 23), avg.Point2D(70, 108), avg.Point2D(70, 194), avg.Point2D(70, 278), avg.Point2D(70, 366),avg.Point2D(70, 23), avg.Point2D(70, 108), avg.Point2D(70, 194), avg.Point2D(70, 278), avg.Point2D(70, 366)]
         self.__placebgLeft = None
         self.__placebgRight = None
         self.__leftPosFar = [140,137]
         self.__rightPosFar = [800,137] 
         self.__leftPosNear = [325,137]
         self.__rightPosNear = [650,137]       

     ##Create the Canvas + Background and the Save and Cancel Button
     #@param x Coordinate of Node Position horizontal
     #@param y Coordinate of Node Position vertical
     #@param angle Angle of node
     def createHighscore(self, x, y, angle):
         __root = self.__game.player.getElementByID("root")
         self.__canvasBackground = self.__game.player.createNode('image', { 
                                               "width":325, "height":213,
                                               "href":"../img/drawpanel.png",
                                               "angle":angle,
                                               "opacity": 1,
                                               "x":x, "y":y,})
         __root.appendChild(self.__canvasBackground)
         self.__winnerCanvas = self.__game.player.createNode('div', { 
                                                       "width":284, "height":139,
                                                       "angle":angle,
                                                       "opacity": 1,
                                                       "x":self.__gloX, "y":self.__gloY})
                                                      
         __root.appendChild(self.__winnerCanvas)
         self.__saveButton = startButton.StartButton(self.__game,self.__savePicture,750,265,"../img/ok.png",0,40,53,False)   
         self.__cancelButton = startButton.StartButton(self.__game,self.__resetPicture,670,265,"../img/cancel.png",0,51,48,False)
         self.__winnerCanvas.setEventHandler(CURSORDOWN, MOUSE | TOUCH, self.onMouseDownCanvas)
         self.__winnerCanvas.setEventHandler(CURSORMOTION, MOUSE | TOUCH, self.onMouseMoveCanvas)
         self.__winnerCanvas.setEventHandler(CURSORUP, MOUSE | TOUCH, self.onMouseUpCanvas)  
     
     ## reads the files from an given Directory
     #@return false if the Directory is empty
     #@return list includes the names of the files inside the Directory
     def get_Directory(self):
         list = []
         ausgefuehrt = False
         for filename in os.listdir("../highscore/"):
             if filename[0] != '.':
                 list.append(filename)
                 ausgefuehrt = True 
         if ausgefuehrt ==False:
             return False
         else:  
             print "SORTED: ", list.sort()
             #list.sort()
             return list
     
     ##proves if the winner is inside the Highscore 
     #@return True the winner is in the Highscore
     #@return False the winner is not in the Highscore 
     def isInHighscore(self):
         time= str(self.__high)
         underlinehit = False
         getroffen= False
         
         dirList= self.get_Directory()          
         if dirList!=False:
             for i in range (0,dirList.__len__()):
                tmp=dirList[i]
                underlinehit = False
                laenge=-1
                a=-1
                for x in range (0,len(tmp)):
                     if underlinehit!=False:  
                        if laenge==(len(time)+4):
                            a+=1
                            if tmp[x]>time[a]:
                               getroffen= True 
                               break;
                            elif tmp[x]<time[a]:
                               getroffen=False
                               break;
                            elif tmp[x]==time[a]:
                               print "equal"
                        elif laenge>(len(time)+4):
                            getroffen= True 
                            break;
                        elif laenge<(len(time)+4):
                            getroffen= False 
                            break;
                     if tmp[x]=="_":
                        underlinehit= True
                        laenge=len(tmp)-(x+1)
                if getroffen==True:
                       self.HighscorePosition = i 
                       return True
                elif getroffen==False:
                        print "next round"
         else:
            self.HighscorePosition = 0 
            return True
         if dirList.__len__()<10:
             self.HighscorePosition = dirList.__len__()
             return True 
         return False
     
     ##separate the File-Time from the Filename
     #@param dirList list with the filenames in it
     #@return fileTime list with the File-Time          
     def __get_FileTime(self,dirList):
        fileTime = []
        for i in range (0,dirList.__len__()):
            tmp=dirList[i]
            str=None
            underlinehit=False
            for x in range (0,len(tmp)):
             if underlinehit==True:
                 if str!=None:
                    str+=tmp[x]
                 else:
                    str=tmp[x]   
             if tmp[x]=="_":
                underlinehit=True
            fileTime.append(str)
            print "STRING DER APPENEDED",str
        return fileTime
     

     ##displays the Highscore
     #@param directory list of Filenames from the highscore folder 
     #@param leftPos the Position for the Left Background
     #@param rightPos the Position for the Right Background                      
     #def displayHighscore(self, directory,leftPos,rightPos):
     def displayHighscore(self, event):
        directory = self.get_Directory()
        if event != None:
            leftPos = self.__leftPosNear
            rightPos = self.__rightPosNear
            self.__game.createPlayAgainB()
        else:
            leftPos = self.__leftPosFar
            rightPos = self.__rightPosFar

        self.__placebgLeft = self.__game.player.createNode('div', {                                       
                                               "width":335, "height":463,
                                               "x": leftPos[0], "y": leftPos[1],"opacity":1}) 
        self.__area.appendChild(self.__placebgLeft)
        self.__highscoreImageLeft = self.__game.player.createNode('image', { "href": "../img/highscore1.png", "x": 0, "y": 0, "width": 335, "height": 463, "opacity": 1})
        self.__placebgLeft.appendChild(self.__highscoreImageLeft)
        self.__placebgRight = self.__game.player.createNode('div', {                                       
                                               "width":335, "height":463,
                                               "x": rightPos[0], "y": rightPos[1],"opacity":1}) 
        self.__area.appendChild(self.__placebgRight)
        self.__highscoreImageRight = self.__game.player.createNode('image', { "href": "../img/highscore2.png", "x": 0, "y": 0, "width": 335, "height": 463, "opacity": 1})
        self.__placebgRight.appendChild(self.__highscoreImageRight)
        marker = False
        if directory!=False:
            time = self.__get_FileTime(directory)
            for i in range(0,directory.__len__()):
                print "DIR",directory[i]
                print "TIME",time[i]
                if self.HighscorePosition!=None:
                    #print "HIGH",self.HighscorePosition,"III",i
                    if self.HighscorePosition == i:
                         marker=True
                         #print "MARKER GESETZT"
                    if marker ==True:
                        if i+1>=10:
                            break;
                        else:
                            #print "ddddddddrin"  
                            self.__createDrawingNodes(directory,time[i],i,i+1)
                            
                    else: 
                        #print "MARKER NICHT GETROFFEN"
                        self.__createDrawingNodes(directory,time[i],i,i)      
                        
                else:
                     self.__createDrawingNodes(directory,time[i],i,i)
                     
     ## create the nodes necessary for the Highscore
     #@param directory list of Filenames from the highscore folder
     #@param time string including FileTime
     #@param i index of the position in the list directory
     #@param x index of the position in the list __highscorePos
     def __createDrawingNodes(self,directory,time,i, x):
         self.__name = self.__game.player.createNode('image', { "href": "../highscore/" + directory[i], "x": self.__highscorePos[x][0], "y": self.__highscorePos[x][1], "width": 150, "height": 75,"opacity":1})
         intTime=float(time[0:-4])/1000
         time = str(intTime)
         self.__time = self.__game.player.createNode('words', { "text":time, 
                    "color":"661b25", "fontsize":20 ,
                    "x": self.__highscorePos[x][0]+165,"y": self.__highscorePos[x][1]+10})
         if x<=4:                
            self.__placebgLeft.appendChild(self.__name)
            self.__placebgLeft.appendChild(self.__time)
         else:
            self.__placebgRight.appendChild(self.__name)
            self.__placebgRight.appendChild(self.__time)
     
     ## renames Files in the higscore folder
     #@param x start positon for renaming
     #@param dirList list of the File - Names from the highscore Folder                     
     def __renameFiles(self,x,dirList):
         self.HighscorePosition = x
         fileTime=self.__get_FileTime(dirList)
         #print "laenge",dirList.__len__(),"XXX",x
         for i in range (dirList.__len__(),x,-1):
           if i == 10:
               os.remove("../highscore/"+str(i)+"_"+fileTime[i-1])
           elif i<10:   
               im = Image.open("../highscore/"+"0"+str(i)+"_"+fileTime[i-1])
               if (i+1)!= 10:
                   im.save("../highscore/"+"0"+str(i+1)+"_"+fileTime[i-1])
               else:
                   im.save("../highscore/"+str(i+1)+"_"+fileTime[i-1])         
               im=None
               os.remove("../highscore/"+"0"+str(i)+"_"+fileTime[i-1])
               
               
     ##EventHandler function for the Save Button
     #@param Event Parameter from the avg        
     def __savePicture(self,event):
         anim.fadeOut(self.__canvasBackground, 500)
         anim.fadeOut(self.__winnerCanvas, 500)
         directorList = self.get_Directory()
         if directorList!=False:
             self.__renameFiles(self.HighscorePosition,directorList)
         time= str(self.__high)
         if self.HighscorePosition+1 ==10:   
            filename = "../highscore/"
         else:
            filename = "../highscore/"+"0"  
         position=str(self.HighscorePosition+1)
         filename+=position
         filename+="_"
         filename+=time
         filename+=".png"
         self.__image1.save(filename)
         self.__name = self.__game.player.createNode('image', { "href": filename, "x": self.__highscorePos[self.HighscorePosition][0], "y": self.__highscorePos[self.HighscorePosition][1], "width": 150, "height": 75,"opacity":0})
         intTime = float(time)/1000
         time = str(intTime)
         self.__time = self.__game.player.createNode('words', { "text":time,
                "color":"661b25", "fontsize":20 ,
                "x": self.__highscorePos[self.HighscorePosition][0]+165,
                "y": self.__highscorePos[self.HighscorePosition][1]+10,"opacity":0})
         if self.HighscorePosition<=4:                
            self.__placebgLeft.appendChild(self.__name)
            self.__placebgLeft.appendChild(self.__time)
         else:
           self.__placebgRight.appendChild(self.__name)
           self.__placebgRight.appendChild(self.__time)    
         anim.fadeIn(self.__name, 1000)
         anim.fadeIn(self.__time,1000)
         self.__game.player.setTimeout(2000, self.__slideHighscore)
         self.__game.player.setTimeout(3000, self.__game.createPlayAgainB)      
         self.__cancelButton.delStartButton()   
         self.__saveButton.delStartButton()
     
     ##EventHandler function for the Cancel Button
     #@param Event Parameter from the avg    
     def __resetPicture(self,event):
        for i in range (0,self.__winnerCanvas.getNumChildren()):
            self.__winnerCanvas.removeChild(0)      
        self.__image1 = None
        self.__draw = None
        self.__image1 = Image.new("RGB", (300, 150), self.__white)
        self.__draw = ImageDraw.Draw(self.__image1)
        
    ## slides the Highscore together
     def __slideHighscore(self):
        anim.LinearAnim(self.__placebgLeft, "x", 500, self.__placebgLeft.x, 325)
        anim.LinearAnim(self.__placebgRight, "x", 500, self.__placebgRight.x, 650)
     
     ##Eventhandler for Down events
     #@param Event Parameter from the avg
     def onMouseDownCanvas(self,Event):
          self.__winnerCanvas = Event.node
          if  Event.source==avg.TOUCH or  Event.source==avg.MOUSE:
              if self.__offset == None:
                  self.__offset = self.__winnerCanvas.getRelPos((Event.x-self.__gloX, Event.y-self.__gloY))
                  self.__firstDown= True
                  self.__winnerCanvas.setEventCapture(Event.cursorid)
                  self.__cursorID = Event.cursorid 
                   
     ##Eventhandler for Move events
     #@param Event Parameter from the avg             
     def onMouseMoveCanvas(self,Event):
              self.__winnerCanvas = Event.node    
              if self.__offset != None and self.__cursorID==Event.cursorid:
                  xmove = Event.x-self.__gloX
                  ymove = Event.y-self.__gloY
                  if self.__firstDown == True:
                    line = self.__game.player.createNode("line", {
                        "pos1":(self.__offset[0], self.__offset[1]),
                        "pos2":(self.__offset[0], self.__offset[1]),
                        "strokewidth":4,"color":"FF0000"})
                    self.__drawList.append((self.__offset[0]+self.__gloX,self.__offset[1]+self.__gloY))
                    self.__drawList.append((self.__offset[0]+self.__gloX,self.__offset[1]+self.__gloY))
                    self.__winnerCanvas.appendChild(line)
                    #list.append((offset[0], offset[1]))
                    self.__firstDown=False
                  else:
                    line = self.__game.player.createNode("line", {
                        "pos1":(self.__xold, self.__yold), 
                        "pos2":(xmove, ymove),
                        "strokewidth":4,"color":"FF0000"})
                    self.__drawList.append((self.__xold,self.__yold))
                    self.__drawList.append((xmove,ymove))
                   
                    
                    self.__winnerCanvas.appendChild(line)
                  self.__xold=xmove
                  self.__yold=ymove
      
     ##Eventhandler for Up events
     #@param Event Parameter from the avg   
     def onMouseUpCanvas(self,Event):
              self.__winnerCanvas = Event.node
              if self.__offset != None and self.__cursorID==Event.cursorid:
                  self.__draw.line(self.__drawList,self.__black)
                  self.__drawList = [] 
                  self.__winnerCanvas.releaseEventCapture( self.__cursorID)
                  self.__offset = None;
                  
     ##deletes the complete Highscore nodes     
     def deletehighscore(self):
         if self.__winnerCanvas != None and  self.__canvasBackground != None:
             useful.deleteNode(self.__winnerCanvas)
             useful.deleteNode(self.__canvasBackground)
         if self.__placebgLeft != None:
            useful.deleteNode(self.__placebgLeft)
            useful.deleteNode(self.__placebgRight)
     
