#################################################################################
# CREATOR INFO:
################################################################################

#Name: Colin May
#Andrew Id: cmmay
#Term Project 15-112 Fall 2020

################################################################################
################################################################################


import math

class Player(object):


    #player constructor
    def __init__(self, color, row, col, dirRow, dirCol): 
        self.color = color
        self.row = row #can be decimal i think
        self.col = col #can be decimal i think
        self.dirRow = dirRow #-1,0,1 i think
        self.dirCol = dirCol #-1,0,1 i think
        #self.impStatus = impStatus #string --> 'imposter' or 'crewmate'
        self.initialRow = row
        self.initialCol = col
        self.initialDirRow = dirRow
        self.initialDirCol = dirCol
        
        self.fovPlaneX = 0 #best angle for 1st person games
        self.fovPlaneY = 0.66 #best angle for 1st person games
        self.initialFOVPlaneX = self.fovPlaneX
        self.initialFOVPlaneY = self.fovPlaneY
        self.moveSpeed = 0.15 # squares per second (.10-.20)
        self.rotSpeed = 0.12 #radians per second

        self.isMovingForward = False
        self.isMovingBackward = False
        self.isRotatingLeft = False
        self.isRotatingRight = False

        #self.isPromptingReport = False
        #self.canMove = True
        self.isMoving = True
        self.isPromptingReport = False
        self.isAlive = True
        self.numSelfVotes = 0
        self.personWhoVotedForSelf = None

    ############################################################################
    # GET/SET VALUES:
    ############################################################################
    #voting
    def addOneNumSelfVotes(self):
        self.numSelfVotes += 1
    def getNumSelfVotes(self):
        return self.numSelfVotes
    def getPersonWhoVotedForSelf(self):
        return self.personWhoVotedForSelf
    def setPersonWhoVotedForSelf(self, person):
        self.personWhoVotedForSelf = person
    
    #fov plane
    def getFOVPlaneX(self):
        return self.fovPlaneX
    def getFOVPlaneY(self):
        return self.fovPlaneY
    def setFOVPlaneX(self, fovPlaneX):
        self.fovPlaneX = fovPlaneX
    def setFOVPlaneY(self, fovPlaneY):
        self.fovPlaneY = fovPlaneY
    #initial fov plane
    def setInitialFOVPlaneY(self,fovPlaneY):
        self.fovPlaneY = fovPlaneY
    def setInitialFOVPlaneX(self,fovPlaneX):
        self.fovPlaneX = fovPlaneX
    def getInitialFOVPlaneY(self):
        return self.initialFOVPlaneY
    def getInitialFOVPlaneX(self):
        return self.initialFOVPlaneX

    #alive status
    def getIsAlive(self):
        return self.isAlive
    def setIsAlive(self, boolVal):
        self.isAlive = boolVal
    #prompt report
    def setIsPromptingReport(self, boolVar):
        self.isPromptingReport = boolVar
    def getIsPromptingReport(self, boolVar):
        self.isPromptingReport = boolVar
    
 
    #moving and position values in following functions
    def getIsMoving(self):
        return self.isMoving
    def setIsMoving(self, boolVal):
        self.isMoving = boolVal

    def getInitialRow(self):
        return self.row
    def getInitialCol(self):
        return self.col

    def getInitialDirRow(self):
        return self.initialDirRow
    def getInitialDirCol(self):
        return self.initialDirCol
    def setInitialDirRow(self, dirRow):
        self.initialDirRow = dirRow
    def setInitialDirCol(self, dirCol):
        self.initialDirCol = dirCol
    def setDirRow(self, row):
        self.dirRow = row
    def setDirCol(self, col):
        self.dirCol = col
   
    #player speed
    def setPlayerSpeed(self, speed):
        self.moveSpeed = speed

    #returns the x0,y0,x1,y1 of a given row,col & margin
    #source: 112 website, I modified it partially for my use.
    #https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
    def getCellBounds(self, app, row, col, margin):
        gridWidth = app.width - 2*margin
        gridHeight = app.height - 2*margin
        cellWidth = gridWidth / app.mapCols
        cellHeight = gridHeight / app.mapRows

        x0 = margin + cellWidth * col
        y0 = margin + cellHeight * row
        x1 = margin + cellWidth * (col+1)
        y1 = margin + cellHeight * (row+1)
        return x0,y0,x1,y1
    
    #returns player cx and cy (on map)
    def findCxAndCy(self, app, margin):
        x0,y0,x1,y1 = self.getCellBounds(app, self.row, self.col, margin)
        pCx = (x0+x1) / 2
        pCy = (y0+y1) / 2
        return (pCx, pCy)

    #returns direction vector, in x
    def getDirRow(self):
        return self.dirRow
    #returns direction vector, in y
    def getDirCol(self):
        return self.dirCol
    #returns player color
    def getColor(self):
        return self.color
    #returns player row (on map)
    def getRow(self):
        return self.row
    #returns player col (on map)
    def getCol(self):
        return self.col
    def setRow(self, row):
        self.row = row
    def setCol(self, col):
        self.col = col

    #returns fovPlaneX (used in vertLines algorithm)
    def getFovPlaneX(self):
        return self.fovPlaneX
    #returns fovPlaneY (used in vertLines algorithm)
    def getFovPlaneY(self):
        return self.fovPlaneY

    #these four return the player's isMoving booleans
    def getIsMovingForward(self):
        return self.isMovingForward
    def getIsMovingBackward(self):
        return self.isMovingBackward
    def getIsRotatingLeft(self):
        return self.isRotatingLeft
    def getIsRotatingRight(self):
        return self.isRotatingRight

    #these four set the player's isMoving booleans to a given value
    def setIsMovingForward(self, value):
        self.isMovingForward = value
    def setIsMovingBackward(self, value):
        self.isMovingBackward = value
    def setIsRotatingLeft(self, value):
        self.isRotatingLeft = value
    def setIsRotatingRight(self, value):
        self.isRotatingRight = value
    
    #these two set / get isPromptingReport variable
    def setIsPromptingReport(self, boolVar):
        self.isPromptingReport = boolVar
    def getIsPromptingReport(self):
        return self.isPromptingReport

    ############################################################################
    # MOVEMENT:
    ############################################################################

    #move player forward if no wall, use moveSpeed
    def moveForward(self, worldMap):
        #player position is vector, so check row/col of both vectors
        #this is partially from this source:
        #https://lodev.org/cgtutor/raycasting.html (raycasting tutorial)
        xNextRow = int(self.row + self.dirRow * self.moveSpeed)
        xNextCol = int(self.col)
        yNextRow = int(self.row)
        yNextCol = int(self.col + self.dirCol * self.moveSpeed)

        if worldMap[xNextRow][xNextCol] == 0: #no wall in x vector
            self.row += self.dirRow * self.moveSpeed
        if worldMap[yNextRow][yNextCol] == 0: #no wall in y vector
            self.col += self.dirCol * self.moveSpeed
    
    #move player backward if no wall, use moveSpeed
    def moveBackward(self, worldMap):
        #player position is vector, so check row/col of both vectors
        #this is partially from this source:
        #https://lodev.org/cgtutor/raycasting.html (raycasting tutorial)
        xNextRow = int(self.row - self.dirRow * self.moveSpeed)
        xNextCol = int(self.col)
        yNextRow = int(self.row)
        yNextCol = int(self.col - self.dirCol * self.moveSpeed)

        if worldMap[xNextRow][xNextCol] == 0: #no wall in x vector
            self.row -= self.dirRow * self.moveSpeed
        if worldMap[yNextRow][yNextCol] == 0: #no wall in y vector
            self.col -= self.dirCol * self.moveSpeed

    #rotate player right, use rotSpeed
    def rotateRight(self):
        #source: https://lodev.org/cgtutor/raycasting.html (raycasting tutorial)
        #source provided: math explanation/example c++ code for 3d rotating
        #source explains: to rotate a vector, multiply it with rotation matrix:
            #rot matrix:        [ cos(a) -sin(a)]
            #                   [ sin(a) cos(a) ]

        #rotate player direction (rotSpeed in radians)
        oldDirRow = self.dirRow
        self.dirRow = ( self.dirRow * math.cos(-self.rotSpeed)
                        - self.dirCol * math.sin(-self.rotSpeed) )
        self.dirCol = ( oldDirRow * math.sin(-self.rotSpeed)
                        + self.dirCol * math.cos(-self.rotSpeed))

        #rotate player FOV plane
        oldPlaneX = self.fovPlaneX
        self.fovPlaneX = ( self.fovPlaneX * math.cos(-self.rotSpeed)
                            - self.fovPlaneY * math.sin(-self.rotSpeed) )
        self.fovPlaneY = ( oldPlaneX * math.sin(-self.rotSpeed) 
                            + self.fovPlaneY * math.cos(-self.rotSpeed))

    #rotate player left, use rotSpeed
    def rotateLeft(self):
        #source: https://lodev.org/cgtutor/raycasting.html (raycasting tutorial)
        #source provided: math explanation/example c++ code for 3d rotating
        #source explains: to rotate a vector, multiply it with rotation matrix:
            #rot matrix:        [ cos(a) -sin(a)]
            #                   [ sin(a) cos(a) ]
        
        #rotate player direction (rotSpeed in radians)
        oldDirRow = self.dirRow
        self.dirRow = ( self.dirRow * math.cos(self.rotSpeed)
                        - self.dirCol * math.sin(self.rotSpeed) )
        self.dirCol = ( oldDirRow * math.sin(self.rotSpeed)
                        + self.dirCol * math.cos(self.rotSpeed))

        #rotate player FOV plane
        oldPlaneX = self.fovPlaneX
        self.fovPlaneX = ( self.fovPlaneX * math.cos(self.rotSpeed)
                            - self.fovPlaneY * math.sin(self.rotSpeed) )
        self.fovPlaneY = ( oldPlaneX * math.sin(self.rotSpeed) 
                            + self.fovPlaneY * math.cos(self.rotSpeed))

   




#subclass of player --> crewmate
class PlayerCrewmate(Player): 
    def __init__(self, color, row, col, dirRow, dirCol):
        super().__init__(color, row, col, dirRow, dirCol)

        self.impStatus = 'crewmate'

        #bool for if near a task, prompt 'use' button if true
        self.isPromptingUse = False
        self.isDoingTask = False
        self.currTask = None
        self.currTaskLocation = None

        self.isDoingWiresTask = False
        self.wiresTaskWallLocationCoords = dict()
        self.wiresTaskWallLocationCoords = \
                        self.initializeWiresTaskWallLocationCoords()

        self.numWiresTasksCompleted = 0
        

    ############################################################################
    # GET/SET VALUES:
    ############################################################################
    
    #imposter status - crewmate or imposter
    def getImpStatus(self):
        return self.impStatus

    #these two set / get isPromptingUse variable
    def setIsPromptingUse(self, boolVar):
        self.isPromptingUse = boolVar
    def getIsPromptingUse(self):
        return self.isPromptingUse
    

    #these two set / get isDoingTask variable
    def setIsDoingTask(self, boolVar):
        self.isDoingTask = boolVar
    def getIsDoingTask(self):
        return self.isDoingTask
    
    #sets/returns the name of the task, or None. Ex: "wires"
    def setCurrTask(self, taskName):
        self.currTask = taskName
    def getCurrTask(self):
        return self.currTask
    
    #sets/returns the name of the task, or None. Ex: "wires"
    def setCurrTaskLocation(self, taskLocationName):
        self.currTaskLocation = taskLocationName
    def getCurrTaskLocation(self):
        return self.currTaskLocation

    #WIRES task:
    #these two set / get isDoingWiresTask variable
    def setIsDoingWiresTask(self, boolVar):
        self.isDoingWiresTask = boolVar
    def getIsDoingWiresTask(self):
        return self.isDoingWiresTask
    #add to wires
    def addOneToNumWiresTasksCompleted(self):
        self.numWiresTasksCompleted += 1
    def getNumWiresTasksCompleted(self):
        return self.numWiresTasksCompleted
    
    ############################################################################
    # GAMEPLAY:
    ############################################################################
    #set for player wires task locations on map, with names
    def initializeWiresTaskWallLocationCoords(self):
        wiresTaskWallLocationCoords = {
                                        'electrical': (15,31),
                                        'storage': (20,43),
                                        #'admin':  (14,50),
                                        'navigation': (13,83),
                                        'cafeteria': (0,41),
                                        #'security': (10,26),
                                       }
        return wiresTaskWallLocationCoords


    #returns mapRow,mapCol for given task and location
    def getTaskMapCoords(self, taskName, location):
        if taskName == 'wires':
            mapRow,mapCol = self.wiresTaskWallLocationCoords.get(location, 
                                "invalid wires loc name")
            return mapRow, mapCol

    #returns true if player's position is on a wire task
    #also returns the location of the wire task they are on
    def isPlayerNearWiresTask(self):
        if (15 <= self.row <= 17) and (30 <= self.col <= 32):
            return (True, 'electrical')
        elif (20 <= self.row <= 22) and (42 <= self.col <= 44):
            return (True, 'storage')
        # elif (14 <= self.row <= 16) and (49 <= self.col <= 51):
        #     return (True, 'admin')
        elif (12 <= self.row <= 14) and (82 <= self.col <= 84):
            return (True, 'navigation')
        elif (0 <= self.row <= 2) and (40 <= self.col <= 42):
            return (True, 'cafeteria')
        # elif (9 <= self.row <= 11) and (24 <= self.col <= 26):
        #     return (True, 'security')
        else:
            return (False, None) 






#subclass of player --> imposter
class PlayerImposter(Player): 
    def __init__(self, color, row, col, dirRow, dirCol):
        super().__init__(color, row, col, dirRow, dirCol)

        self.impStatus = 'imposter'

        self.isPromptingKill = False
        self.isPromptingVent = False
        self.isKilling = False 
        self.isAlive = True 

    def getImpStatus(self):
        return self.impStatus

    ############################################################################
    # GET/SET Values:
    ############################################################################
    
    def getIsPromptingKill(self):
        return self.isPromptingKill
    def setIsPromptingKill(self, boolVal):
        self.isPromptingKill = boolVal

    def getIsKilling(self):
        return self.isKilling
    def setIsKilling(self, boolVal):
        self.isKilling = boolVal

    ############################################################################
    # GAMEPLAY:
    ############################################################################

    #returns true if the player's position is on a vent
    # def isPlayerOnVent(self):
    #     if self.row == 10 and self.col == 14:
    #         return True
    #     #can add more vent locations here
    #     else:
    #         return False

