#################################################################################
# CREATOR INFO:
################################################################################

#Name: Colin May
#Andrew Id: cmmay
#Term Project 15-112 Fall 2020

################################################################################
################################################################################


import math, random

class Ai(object):


    #ai constructor
    def __init__(self, name, color, row, col, worldMap):
        self.name = name 
        self.color = color
        self.row = row #these will change
        self.col = col
        self.initialRow = row #these will remain constant 
        self.initialCol = col
        self.worldMap = worldMap

        self.mapRows = len(worldMap)
        self.mapCols = len(worldMap[0])

        self.dx = 0 
        self.dy = 0
        self.isAlive = True

        self.aiImageCx = None
        self.aiImageCy = None
        self.aiImageWidth = 200
        self.aiImageHeight = 200
        self.imageX0X1 = (None,None)
        self.imageY0Y1 = (None,None)
        self.transformedY = None


        #A* PATHFINDING ALGORITHM STUFF:
        self.allVerticesDict = self.initializeAllVerticesDict()
        self.lastDirectionMoved = None
        
        #gameplay
        self.isReporting = False
        self.isVoting = False
        self.personVotingFor = None #'player' or aiName
        self.stuckInLoop = False

        #task stuff for both imp and crew
        self.unVisitedTasks = ['N','V','F','W']
        self.visitedTasks = []
        self.currTask = None
        self.currTaskPath = None
        self.currEndVertex = None
        self.isSettingCurrEndVertex = False
        self.isGoingToCurrTask = False
        self.arrivedAtCurrEndVertex = False

        self.arrivedAtCurrTask = False
        self.isSettingCurrTaskPath = False

        #voting
        self.numSelfVotes = 0
        self.personWhoVotedForSelf = None
        
    ############################################################################
    # Raycasting:
    ############################################################################
    #returns true if ray is at ai position along with y coord
    def isRayRowColInAiPosition(self, app, x, rayRow,rayCol):
        mapMargin = 50
        #check if rayMapRow & rayMapCol at that x
        #is touching the center of an ai row,col
        if (rayRow,rayCol) == (self.row,self.col): #if in square
            #check if in center of square
            aiX0,aiY0,aiX1,aiY1 = self.getCellBounds(app,self.row,self.col,mapMargin)
            aiCx = (aiX1+aiX0)//2
            aiCy = (aiY1-aiY0)//2
            if aiCx-500 <= x <= aiCx+500:
                return (True, aiCy+300)
        return (False,None)

    

    ############################################################################
    # MOVEMENT :
    ############################################################################
  
    #returns true and the vertex if at vertex; otherwise false & none
    def isAtVertex(self):
        for vertex in self.allVerticesDict:
            vRow,vCol = self.allVerticesDict.get(vertex)[0]
            if (self.row, self.col) == (vRow,vCol): #vertex position
                return (True, vertex[0])
        return (False, None)
    

    #FOR MOVING TO GIVEN ROW,COL (imposter uses this mainly):
    #THIS UPDATES/MOVES AI Row, Col:
    #moves ai one step - figures out best next step to get to goalRow,goalCol
    def doStep_MoveThroughGridTowardRowCol(self, goalRow,goalCol):
        #while self.stuckInLoop: #my fix for when ais get stuck
        shortestDist = None
        shortestDx = None
        shortestDy = None

        currRow,currCol = self.row, self.col #-current ai position
        endRow,endCol = goalRow,goalCol
                #right    left     up     down
        sideDirs = [(+1,0), (-1,0), (0,+1), (0,-1)]
        

        #loop through each direction & determine which one is shortest to end
        for dx,dy in sideDirs:
            dRow,dCol = currRow+dy,currCol+dx
            #bounds check:
            if (self.worldMap[dRow][dCol] != 0 or
                (dRow >= self.mapRows or dRow < 0) or
                (dCol >= self.mapCols or dCol < 0)):
                continue
            
            #if reach this point: square is valid
            #calculate distance to end for square
            currDistToEnd = self.calculatePointsEuclideanDistance(
                                    dRow, dCol, endRow, endCol)
            
            #find shortest distance
            if shortestDist == None or currDistToEnd < shortestDist:
                shortestDist = currDistToEnd
                shortestDx = dx
                shortestDy = dy
            
        #move, use shortest row and col square
        if shortestDx != None and shortestDy != None:
            if self.lastDirectionMoved != None and self.isInALoop(dx,dy)[0]:
                fixedDx,fixedDy = self.isInALoop(dx,dy)[2],self.isInALoop(dx,dy)[1]
                print('\t\t\t\t\tIN A LOOP')
                self.row += self.isInALoop(dx,dy)[1]
                self.col += self.isInALoop(dx,dy)[2]
                #self.stuckInLoop = F
                self.lastDirectionMoved = (dx,dy)

            else:
                self.lastDirectionMoved = (dx,dy)
                self.row += shortestDy
                self.col += shortestDx
                #self.stuckInLoop = False
            
        
        if (self.row,self.col) == (endRow,endCol):
            self.arrivedAtGoalRowCol = True

    #FOR MOVING TO GIVEN VERTEX:
    #THIS UPDATES/MOVES AI Row, Col:
    #moves ai one step - figures out best next step to get to endVertex
    def doStep_MoveThroughGrid(self, endVertex):
        #while self.stuckInLoop: #my fix for when ais get stuck
        shortestDist = None
        shortestDx = None
        shortestDy = None

        currRow,currCol = self.row, self.col #-current ai position
        endRow,endCol = self.allVerticesDict.get(endVertex)[0]
                #right    left     up     down
        sideDirs = [(+1,0), (-1,0), (0,+1), (0,-1)]
        
        

        #loop through each direction & determine which one is shortest to end
        for dx,dy in sideDirs:
            dRow,dCol = currRow+dy,currCol+dx
            #bounds check:
            if (self.worldMap[dRow][dCol] != 0 or
                (dRow >= self.mapRows or dRow < 0) or
                (dCol >= self.mapCols or dCol < 0)):
                continue
            
            #if reach this point: square is valid
            #calculate distance to end for square
            currDistToEnd = self.calculatePointsEuclideanDistance(
                                    dRow, dCol, endRow, endCol)
            
            #find shortest distance
            if shortestDist == None or currDistToEnd < shortestDist:
                shortestDist = currDistToEnd
                shortestDx = dx
                shortestDy = dy
            
        #move, use shortest row and col square
        if shortestDx != None and shortestDy != None:
            if self.lastDirectionMoved != None and self.isInALoop(dx,dy)[0]:
                fixedDx,fixedDy = self.isInALoop(dx,dy)[2],self.isInALoop(dx,dy)[1]
                print('\t\t\t\t\tIN A LOOP')
                self.row += self.isInALoop(dx,dy)[1]
                self.col += self.isInALoop(dx,dy)[2]
                #self.stuckInLoop = F
                self.lastDirectionMoved = (dx,dy)

            else:
                self.lastDirectionMoved = (dx,dy)
                self.row += shortestDy
                self.col += shortestDx
                self.stuckInLoop = False
            
        
        if (self.row,self.col) == (endRow,endCol):
            self.arrivedAtCurrEndVertex = True #arrived
            

    #returns true if in a loop, and if so, the fixed direction to move
    def isInALoop(self, currDx,currDy):
        left = (-1,0)
        right = (+1,0)
        currDTuple = (currDx,currDy)
        #self.lastDirectionMoved = (dx,dy)
        if self.lastDirectionMoved == left and currDTuple == right:
            fixedDx,fixedDy = left[0], left[1]
            nextDRow = currRow+currDy+fixedDy
            nextDCol = currCol+currDx+fixedDx
            #bounds check:
            if (self.worldMap[nextDRow][nextDCol] != 0 or
                (nextDRow >= self.mapRows or nextDRow < 0) or
                (nextDCol >= self.mapCols or nextDCol < 0)):
                fixedDx,fixedDy = currDx,currDy #didn't work -go back to normal
            return (True,fixedDy,fixedDx)
        elif self.lastDirectionMoved == right and currDTuple == left:
            fixedDx,fixedDy = right[0], right[1]
            nextDRow = currRow+currDy+fixedDy
            nextDCol = currCol+currDx+fixedDx
            #bounds check:
            if (self.worldMap[nextDRow][nextDCol] != 0 or
                (nextDRow >= self.mapRows or nextDRow < 0) or
                (nextDCol >= self.mapCols or nextDCol < 0)):
                fixedDx,fixedDy = currDx,currDy#didn't work -go back to normal
            return (True,fixedDy,fixedDx)

        return (False,0,0)



    #pathagorean distance between 2 points    
    def calculatePointsEuclideanDistance(self, firstRow,firstCol,secRow,secCol):
        #pathagorean theorem to estimate euclidean distance (straight line)
        
        xLength = abs(secCol-firstCol)
        yLength = abs(secRow-firstRow)
        
        #pathagorean theorem
        dist = math.sqrt((xLength**2) + (yLength**2))
        return dist        

    #sets ai direction to given dx,dy           
    def updateDxDy(self, dx,dy):
        self.dx = dx
        self.dy = dy

    #moves the ai to given row,col            
    def updateRowCol(self, row, col):
        self.row = row
        self.col = col  

  


    ############################################################################
    # A* Pathfinding Algorithm:
    ############################################################################
    #define vertices for ai movement
    def initializeAllVerticesDict(self):
        #key:
            #g = distance from startVertex
            #h = heuristic (straight line) distance from endVertex
            #f = g + h
            #iRow/iCol = initial row/col
        iRow,iCol = self.initialRow, self.initialCol #so each ai can start at their respective A
        allVerticesDict = { 
        #Vertex | MapPos | isTask | Neighbor V's   |  g  |  h  |  f  | Previous vertex
            'A':  [  (iRow,iCol),  False,  ['T','K','B','V'],     None, None, None, None  ],
            'B':  [  (6,66),  False,  ['A','C'],         None, None, None, None  ],
            'C':  [  (11,66), False,  ['B','E','F'],       None, None, None, None  ],
            #'D':  [  (12,59), False,  ['C','E'],           None, None, None, None  ],
            'E':  [  (14,73), False,  ['C','F','G'],  None, None, None, None  ],
            'F':  [  (13,82), True,   ['E','C'],           None, None, None, None  ],
            'G':  [  (26,67), False,  ['E','H'],         None, None, None, None  ],
            'H':  [  (26,59), False,  ['G','U','Y'],         None, None, None, None  ],
            'I':  [  (28,44), False,  ['W','U','M'],     None, None, None, None  ],
            'J':  [  (16,46), False,  ['K','L','W'],   None, None, None, None  ],
            'K':  [  (15,50), False,   ['A','J','L'],         None, None, None, None  ],
            'L':  [  (20,55), False,  ['J','K'],         None, None, None, None  ],
            'M':  [  (27,27), False,  ['X','I','N'],       None, None, None, None  ],
            'N':  [  (16,31), True,   ['M','X'],           None, None, None, None  ],
            'O':  [  (23,16), False,  ['P','X'],         None, None, None, None  ],
            'P':  [  (13,16), False,  ['O','Z','Q'],     None, None, None, None  ],
            'Q':  [  (13,6),  False,  ['P','Z'],           None, None, None, None  ],
            #'R':  [  (10,25), False,  ['P','Z'],           None, None, None, None  ],
            'S':  [  (5,16),  False,  ['Z','T'],         None, None, None, None  ],
            'T':  [  (6,32),  False,  ['S','V','A'],       None, None, None, None  ],
            #didn't use U
            'U': [ (26,58), False, ['I','H','Y'],       None, None, None, None],
            'V':  [  (2,41),  True,   ['T','A'],         None, None, None, None  ],
            'W':  [  (21,43), True,  ['I','J'],         None, None, None, None  ],
            'X':  [  (27,26), False,  ['O','N','M'],           None, None, None, None  ],
            'Y':  [  (30,57), False,  ['U','H'],           None, None, None, None  ],
            'Z': [ (12,17), False, ['S','Q','P'], None, None, None, None],
        }
        return allVerticesDict

    #this is the A* pathfinding algorithm between map vertices:
    def getPathFromTwoVertices(self, startVertex, endVertex):
        #I learned the conceptual from https://www.youtube.com/watch?v=eSOJ3ARN5FM
        #however, I FIGURED IT OUT ON MY OWN!
        #key: 
            # g = distance from startVertex
            # h = heuristic distance -> euclidean distance from endVertex
            # f = g + h
        self.allVerticesDict = self.initializeAllVerticesDict()

        openList = []
        closedList = []
        lowestNeighborF = None
        bestCurrVertex = None
        lowestCurrVertex = None
        currNumSteps = None
        lowestNumSteps = 1000 #high value so it gets new one

        #bestCurrVertex = currVertex
        g = 0
        h = self.calculateVertexEuclideanDistance(startVertex, endVertex)
        f = h + g
        self.setGHFAtVertex(startVertex, g, h, f)
        closedList.append(startVertex)

        currVertex = startVertex
        #openList.append(currVertex)
        while currVertex != endVertex:
            lowestNeighborF  = None
            currNumSteps = 0
            #print('\ncurrVertex: ', currVertex)
            neighborVList = self.allVerticesDict.get(currVertex)[2]
            for neighborVertex in neighborVList:  
                if  (neighborVertex not in closedList and 
                    neighborVertex not in openList):
                    openList.append(neighborVertex)
             
            for openVertex in openList:
                self.setPrevVertex(openVertex, currVertex)
                #calculate g
                g = 0
                currTempVertex = openVertex 
                prevTempVertex = self.allVerticesDict.get(currTempVertex)[6] 
                currNumSteps = 0
                while prevTempVertex != None: 
                    currNumSteps += 1
                    g += self.calculateVertexEuclideanDistance(currTempVertex, prevTempVertex)
                    currTempVertex = prevTempVertex 
                    prevTempVertex = self.allVerticesDict.get(currTempVertex)[6]

                #g = self.getAdjacentDistance()
                h = self.calculateVertexEuclideanDistance(openVertex, endVertex)#currVertex, endVertex)
                f = g + h
                self.setGHFAtVertex(openVertex, g, h, f)
          
            
                #want lowest f value to be next step in path
                if lowestNeighborF == None or f <= lowestNeighborF:
                    if f == lowestNeighborF: #if equal F's
                        #this is finding the more direct path if F's equal
                        if openVertex == endVertex: #if at end, choose end
                            lowestCurrVertex = openVertex
                        elif (openVertex == lowestCurrVertex and 
                            lowestCurrVertex not in openList):
                            lowestCurrVertex = openVertex
                        elif currNumSteps == lowestNumSteps: #same F, same steps
                            # --> random path for variety
                            #50% chance for each path
                            randInt = random.randint(1,2)
                            if randInt == 1: #choose current
                                lowestCurrVertex = openVertex
                    else:
                        lowestCurrVertex = openVertex
                        lowestNumSteps = currNumSteps
                    lowestNeighborF = f
                        
                    
                    lowestCurrVertex = openVertex
               
            #add to closed lsit
            closedList.append(lowestCurrVertex)
            openList.remove(lowestCurrVertex)
            currVertex = lowestCurrVertex
            
            
            
        if closedList != [startVertex]:
            vertexPath = self.getPathFromClosedList(closedList, startVertex, endVertex)
            return vertexPath
        else: #startVertex = endVertex
            return startVertex

    #get path from list from a* algorithm
    def getPathFromClosedList(self, closedList, startVertex, endVertex):
        #traverse backwards using previous vertexes
        vertexPath = []
        vertexPath.append(endVertex)
        prevVertex = self.allVerticesDict[endVertex][6]
        vertexPath.append(prevVertex)
        while prevVertex != startVertex:
            prevVertex = self.allVerticesDict[prevVertex][6]
            vertexPath.append(prevVertex)
        
        #then reverse it to get proper order
        vertexPath = vertexPath[::-1]
        return vertexPath

    #set heuristic values from a* algorithm
    def setGHFAtVertex(self, vertex, g, h, f):
        #set g
        self.allVerticesDict[vertex][3] = g
        #set h
        self.allVerticesDict[vertex][4] = h
        #set f
        self.allVerticesDict[vertex][5] = f

    #set previous vertex, for algorithms
    def setPrevVertex(self, vertex, prevVertex):
        #set previous vertex
        self.allVerticesDict[vertex][6] = prevVertex

    #pathagorean distance
    def calculateVertexEuclideanDistance(self, firstVertex, secondVertex):
        #pathagorean theorem to estimate euclidean distance (straight line)
        firstX = self.allVerticesDict.get(firstVertex)[0][0]
        firstY = self.allVerticesDict.get(firstVertex)[0][1]
        secondX = self.allVerticesDict.get(secondVertex)[0][0]
        secondY = self.allVerticesDict.get(secondVertex)[0][1]
        
        xLength = abs(secondX-firstX)
        yLength = abs(secondY-firstY)

        #pathagorean theorem
        dist = math.sqrt((xLength**2) + (yLength**2))
        return int(dist)


    ############################################################################
    # GET/SET VALUES:
    ############################################################################
    #getters/setters
    #voting
    def addOneNumSelfVotes(self):
        self.numSelfVotes += 1
    def getNumSelfVotes(self):
        return self.numSelfVotes
    def getPersonWhoVotedForSelf(self):
        return self.personWhoVotedForSelf
    def setPersonWhoVotedForSelf(self, person):
        self.personWhoVotedForSelf = person
    
    #images
    def setImageX0X1(self,x0,x1):
        self.imageX0X1 = (x0,x1)
    def setImageY0Y1(self,y0,y1):
        self.imageY0Y1 = (y0,y1)
    def getImageX0X1(self):
        return self.imageX0X1
    def getImageY0Y1(self):
        return self.imageY0Y1
    def getTransformedY(self):
        return self.transformedY
    def setTransformedY(self, y):
        self.transformedY = y
    def setAiImageCx(self, cx):
        self.aiImageCx = cx
    def setAiImageCy(self, cy):
        self.aiImageCy = cy
    def getAiImageCx(self):
        return self.aiImageCx
    def getAiImageCy(self):
        return self.aiImageCy
    def setAiImageHeight(self, height):
        self.aiImageHeight = height
    def setAiImageWidth(self, width):
        self.aiImageWidth = width
    def getAiImageHeight(self):
        return self.aiImageHeight
    def getAiImageWidth(self):
        return self.aiImageWidth
    
    
    #voting/reporting
    def getPersonVotingFor(self):
        return self.personVotingFor
    def setPersonVotingFor(self,person):
        self.personVotingFor = person #person= 'player' or aiName
    
    def getIsVoting(self):
        return self.isVoting
    def setIsVoting(self, boolVal):
        self.isVoting = boolVal

    def getIsReporting(self):
        return self.isReporting
    def setIsReporting(self, boolVal):
        self.isReporting = boolVal
    
    #is alive or dead
    def getIsAlive(self):
        return self.isAlive
    def setIsAlive(self, boolVal):
        self.isAlive = boolVal

    #row,col,initialrow,initialcol
    def getInitialRow(self):
        return self.initialRow
    def getInitialCol(self):
        return self.initialCol
    def setRow(self, row):
        self.row = row
    def setCol(self, col):
        self.col = col

    #returns ai name/id
    def getName(self):
        return self.name
    #returns center x
    def getRow(self):
        return self.row
    #returns center y
    def getCol(self):
        return self.col
    #returns color
    def getColor(self):
        return self.color
    #returns direction x
    def getDx(self):
        return self.dx
    #returns direction y
    def getDy(self):
        return self.dy

    #finds and returns ai cx and cy (on map)
    def findCxAndCy(self, app, margin):
        #mapMargin = #same as in main app.mapMargin
        x0,y0,x1,y1 = self.getCellBounds(app, self.row, self.col, margin)
        cx = (x0+x1) / 2
        cy = (y0+y1) / 2
        return (cx, cy)

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
    
    #task stuff - imposter fakes tasks, crewmate does tasks
    def getCurrTask(self):
        return self.currTask

    def getIsGoingToCurrTask(self):
        return self.isGoingToCurrTask
    def setIsGoingToCurrTask(self, boolVal):
        self.isGoingToCurrTask = boolVal
    
    def getArrivedAtCurrTask(self):
        return self.arrivedAtCurrTask
    def setArrivedAtCurrTask(self, boolVal):
        self.arrivedAtCurrTask = boolVal
    
    def getIsSettingCurrTaskPath(self):
        return self.isSettingCurrTaskPath
    def setIsSettingCurrTaskPath(self, boolVal):
        self.isSettingCurrTaskPath = boolVal

    def getArrivedAtCurrEndVertex(self):
        return self.arrivedAtCurrEndVertex
    def setArrivedAtCurrEndVertex(self, boolVal):
        self.arrivedAtCurrEndVertex = boolVal

    def getIsSettingCurrEndVertex(self):
        return self.isSettingCurrEndVertex
    def setIsSettingCurrEndVertex(self, boolVal):
        self.isSettingCurrEndVertex = boolVal
    
    #TASK GAMEPLAY STUFF USED BY BOTH
    def markCurrTaskComplete(self):
        self.unVisitedTasks.remove(self.currTask)
        self.visitedTasks.append(self.currTask)


    def markCurrEndVertexReached(self):
        self.currTaskPath.remove(self.currEndVertex)
    
    def setCurrTaskPath(self):
        if self.isAtVertex()[0]: #should be at vertex, so should be true
            currVertex = self.isAtVertex()[1]
            taskVertex = self.currTask #currTask is a vertex

        path = self.getPathFromTwoVertices(currVertex, taskVertex) #A* pathfinding
        self.currTaskPath = path
        self.currTaskPath.pop(0) #remove starting position - don't need it here


    def setCurrEndVertex(self):
        #Path Example: ['A'(removed), 'K', 'J', 'W', 'I']
        
        self.currEndVertex = self.currTaskPath[0]
    
    def checkIfArrivedAtCurrTask(self):
        if self.currTaskPath == []: #if reached end of path
            return True

    def doStep_TowardsCurrEndVertex(self):
        #currTask = self.currTask #this is a vertex
        self.doStep_MoveThroughGrid(self.currEndVertex)

    def setCurrTaskRandomly(self):
        #check if all completed
        # if self.unVisitedTasks == []:
        #     self.isAllTasksCompleted = True

        #get random unvisited task location
        randUnVisitedIndex = random.randint(0,len(self.unVisitedTasks)-1)
        randUnVisitedTaskVertex = self.unVisitedTasks[randUnVisitedIndex]
        #set task
        self.currTask = randUnVisitedTaskVertex

    def checkIfAllTasksCompleted(self):
        print('unVisited Tasks: ', self.unVisitedTasks)
        if self.unVisitedTasks == []:
            return True


#subclass of Ai --> crewmate
class AiCrewmate(Ai):
    def __init__(self, name, color, row, col, worldMap):
        super().__init__(name, color, row, col, worldMap)

        self.impStatus = 'crewmate'
        self.isMoving = True
        
        self.crewSpeed = 15 #lower is faster
        #tasks:
        #self.taskLocations = ['N','V','F','W']
        self.numTasksCompleted = 0
        
        self.unVisitedTasks = ['N','V','F','W']
        self.visitedTasks = []

        self.shouldFindNewTaskNow = True

        self.currTask = None
        self.currTaskPath = None
        self.currEndVertex = None
        self.isSettingCurrEndVertex = False
        self.isGoingToCurrTask = False
        self.arrivedAtCurrEndVertex = False

        self.arrivedAtCurrTask = False
        self.isSettingCurrTaskPath = False

        self.isAllTasksCompleted = False

        # self.isReporting = False
        # self.isVoting = False
        # self.personVotingFor = None #'player' or aiName
    ############################################################################
    # GET/SET VALUES:
    ############################################################################
    
    #get/set values, speed
    def getCrewSpeed(self):
        return self.crewSpeed

    #tasks 
    def getNumTasksCompleted(self):
        return self.numTasksCompleted
    def addOneToNumTasksCompleted(self):
        self.numTasksCompleted += 1
    
    #movement / ai
    def getImpStatus(self):
        return self.impStatus
    
    def getIsMoving(self):
        return self.isMoving
    def setIsMoving(self, boolVal):
        self.isMoving = boolVal
    
    #tasks
    def getIsAllTasksCompleted(self):
        return self.isAllTasksCompleted
    def setIsAllTasksCompleted(self, boolVal):
        self.isAllTasksCompleted = boolVal

    def getShouldFindNewTaskNow(self):
        return self.shouldFindNewTaskNow
    def setShouldFindNewTaskNow(self, boolVal):
        self.shouldFindNewTaskNow = boolVal


    ############################################################################
    # GAMEPLAY:
    ############################################################################
   

#subclass of Ai --> imposter
class AiImposter(Ai):
    def __init__(self, name, color, row, col, worldMap):
        super().__init__(name, color, row, col, worldMap)

        self.impStatus = 'imposter'
        self.isMoving = True
        self.isHunting = False
        self.isFaking = True
        self.shouldFindNewFakeTaskNow = True
        #self.isKilling = True

        self.unVisitedTasks = ['N','V','F','W']
        self.visitedTasks = []
        
        self.impSpeed = 12 #slightly faster than crew

        self.currTask = None
        self.currTaskPath = None
        self.currEndVertex = None
        self.isSettingCurrEndVertex = False
        self.isGoingToCurrTask = False
        self.arrivedAtCurrEndVertex = False

        self.arrivedAtCurrTask = False
        self.isSettingCurrTaskPath = False
        
        self.isAllTasksCompleted = False #fake tasks


    ############################################################################
    # GET/SET VALUES:
    ############################################################################
    
    #speed
    def getImpSpeed(self):
        return self.impSpeed
    
    #fake tasks
    def getShouldFindNewFakeTaskNow(self):
        return self.shouldFindNewFakeTaskNow
    def setShouldFindNewFakeTaskNow(self, boolVal):
        self.shouldFindNewFakeTaskNow = boolVal
    
    #imp status - imposter! or crewmate
    def getImpStatus(self):
        return self.impStatus
    
    #movement
    def getIsMoving(self):
        return self.isMoving
    def setIsMoving(self, boolVal):
        self.isMoving = boolVal
    
    #hunting crewmates or faking tasks
    def getIsHunting(self):
        return self.isHunting
    def getIsFaking(self):
        return self.isFaking

    ############################################################################
    # GAMEPLAY:
    ############################################################################
    #decide when to hunt or fake, rand chance
    def setHuntingOrFaking(self):
        chooseHuntingChance = random.randint(1,3)
        if chooseHuntingChance == 1: 
            #then go hunting
            self.isHunting = True
            self.isFaking = False
        else:
            #fake tasks
            self.isFaking = True
            self.isHunting = False
            