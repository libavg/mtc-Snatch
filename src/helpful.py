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
import math, random

##calculates if an Point is inside a goal
#@param point destination point of an animal
#@param x horizontal mid Point of an goal
#@param y vertical mid Point of an goal
#@return isInside True when the Point is inside False when not
def isPointInGoal(point, x, y):
    isInside = False
    x = x
    y = y
    rad = 300
    dx = point[0] - x
    dy = point[1] - y
    if dx*dx + dy*dy < rad*rad:
        isInside = True
    return isInside
##controles the call for the isInside calculation
#@param point destination point of an animal
#@return true when the node is inside one of the goals
def pointControl(point):
    if isPointInGoal(point, 640, 0) or isPointInGoal(point, 0, 350) or isPointInGoal(point, 1280, 350) or isPointInGoal(point, 640, 720):
        return True

##calculates if an Point is inside a goal
#@param point Position of an animal Node
#@param x horizontal mid Point of an goal
#@param y vertical mid Point of an goal
#@return isInside True when the Point is inside False when not
def isInGoal(animal, x, y):
    isInside = False
    x = x
    y = y
    rad = 205
    dx = animal.animal.x - x
    dy = animal.animal.y - y
    if dx*dx + dy*dy < rad*rad:
        isInside = True
    return isInside

## get an random Number
#@param start value
#@param ende value
#@return a random number between start / end parameter
def getRandomNumber(start, end):
    num = abs(random.randint(int(start), int(end)))
    return num
## calculates a vector between given parameter
#@param PosA avg.Point2D Point 
#@param PosB avg.Point2D Point
#@return a vector 
def linearFunction(PosA, PosB):
    if (PosB[0]-PosA[0]) == 0:
        m = (PosB[1]-PosA[1])/0.01
    else:
        m = (PosB[1]-PosA[1])/(PosB[0]-PosA[0])
    n = -1*(m*PosA[0])+(PosA[1])
    #xnull=((n/m)*-1)
    a=[m,n]
    return a

## calculates the vector length of 2 Points
#@param PosA avg.Point2D Point 
#@param PosB avg.Point2D Point
#@return a vector 
def pointCalc(PosA, PosB):
    deltaX=PosB[0]-PosA[0]
    deltaY=PosB[1]-PosA[1]
    po=avg.Point2D(PosB[0]+deltaX,PosB[1]+deltaY)
    return po
## caluclates the turn of an node
#@param Node the node of an animal
#@param queue list including the last 5 Posititions of the animal
#@return angle the calculated angle   
def drehung(Node, queue):
     a=queue[0]
     ax=a[0]
     b=queue[0]
     by=a[1]

     if Node.x==ax and Node.y>by:
        angle=math.pi
          #nach oben   
     elif Node.x==ax and Node.y<by:
             angle=0
              
     elif Node.x==ax and Node.y==by:
             angle=0;
     elif Node.x<ax and Node.y==by:             
             angle=-math.pi/2
          
     elif Node.x<ax:
             angle= (math.atan((Node.y-by)/(Node.x-ax))-(math.pi/2))
     else:
             angle= math.atan((Node.y-by)/(Node.x-ax))+(math.pi/2)
 #    print "angle:  ",angle
     return angle     
## normalizes the Point
#@param point avg.Point2D
#@return point normalized point  
def normalize(point):
     return point / math.sqrt((point[0]*point[0]) + (point[1]*point[1]))
## square root of an given variable
#@param num Number (int,float etc.)
#@return num Number (int,float etc.)
def quad(num):
    return num*num
##caluclates the new Vector of two animal when they bounce
#@param Animal1 node of an animal
#@param queue1 list including the last 5 Posititions of the animal
#@param Vector1 vector of an animal
#@param Animal2 node of an animal
#@param queue2 list including the last 5 Posititions of the animal
#@param Vector2 vector of an animal
#@return point include the vector of both animals 
def AnimalBounce(Animal1,queue1,Vector1,Animal2,queue2,Vector2):
    
    m1x=Vector1[0]
    m1y=Vector1[1]
    #--------------Tier 2 L    
    m2x=Vector2[0]
    m2y=Vector2[1]
    tx= Animal1.x - Animal2.x
    ty= Animal1.y - Animal2.y
    t = math.sqrt(tx*tx + ty*ty)
    if t==0:
        t=1 
    m1ux = (m1x*tx + m1y*ty)*tx/(t*t)
    m1uy = (m1x*tx + m1y*ty)*ty/(t*t)
    m1vx = m1x-m1ux
    m1vy = m1y-m1uy
    m2ux = (m2x*tx + m2y*ty)*tx/(t*t)
    m2uy = (m2x*tx + m2y*ty)*ty/(t*t)
    m2vx = m2x-m2ux
    m2vy = m2y-m2uy
   # if abfrageX>=0 or abfrageY>=0:
    new1x= Animal1.x + (m2vx - m1ux)*10
    new1y= Animal1.y + (m2vy - m1uy)*10
    
    new2x= Animal2.x + (m1vx - m2ux)*10
    new2y= Animal2.y + (m1vy - m2uy)*10
      
    
    Tier1=[new1x,new1y,m2vx - m1ux,m2vy - m1uy]
    Tier2=[new2x,new2y,m1vx - m2ux,m1vy - m2uy]
    #print "TIER1 :", Tier1
    #print "TIER2 :", Tier2
    point=[Tier1,Tier2]
    return point

##calculates the new DestinationPoint and Vector for the animal    
#@param Animal node of an animal 
#@param queue list including the last 5 Posititions of the animal
#@param bounceX includes an number which defines on which wall the touch happen 
#@param Vector vector of an animal
#@return result the Vector (index 0) and new DestinationPoint (index 1)      
def wallBouncing(Animal,queue,bounceX,Vector):
    x=Vector[0]
    y=Vector[1]
    if bounceX==0 or bounceX==1:
        y = y*(-1)
        
    if bounceX==2 or bounceX==3:
        x = x*(-1)
    Vec= avg.Point2D(x,y)
    Dest= Animal.pos+(Vec*20) 
    destX = Dest[0]
    destY = Dest[1]
    if Dest[0] > 1260 or Dest[1] > 700:
        
        destX = destX*0.8
        destY = destY*0.8
    
    newDest = avg.Point2D(destX, destY)    
    #print "DESTI",Dest    
    result=[Vec,newDest]
    
    return result

## calucaltes new Positon for the animal prevents double bouncing
#@param Animal1 node of an animal
#@param Animal2 node of an animal 
#@return result new Pos for the animals  
def batch(animal1,animal2):
    Vec = animal1.pos - animal2.pos
    Vectorlength = Vec.getNorm()
    Vecsave = Vec/Vectorlength
    result = (Vecsave*25)-(Vec/2.)
    return result
