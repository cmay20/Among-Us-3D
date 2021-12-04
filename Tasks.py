#################################################################################
# CREATOR INFO:
################################################################################

#Name: Colin May
#Andrew Id: cmmay
#Term Project 15-112 Fall 2020

################################################################################
################################################################################


from cmu_112_graphics import *
import random

class Tasks (object):

    def __init__(self, appWidth, appHeight):
        #wires
        self.appWidth = appWidth
        self.appHeight = appHeight
        


#WiresTask is subclass of Tasks
class WiresTask(Tasks):
    def __init__(self, appWidth, appHeight, imageSize):
        super().__init__(appWidth, appHeight)
        
        #wires image
        #self.wiresImage = self.getWiresImage()
        self.wiresImageWidth, self.wiresImageHeight = imageSize

        #initialize task
        self.initializeWiresTask()
        # self.isThisLocationCompleted = False
    
  
    ############################################################################
    # INITIALIZE stuff:
    ############################################################################
    
    #initializes wire task variables
    def initializeWiresTask(self):
        #all wires
        self.setWireStartButtonsDimensions()
        self.setWireEndButtonsDimensions()

        #first wire
        self.drawingFirstWire = False
        self.stickFirstWireInRed = False
        self.stickFirstWireInBlue = False
        self.stickFirstWireInYellow = False
        self.stickFirstWireInPink = False
        self.releasedInFirstWire = False
        self.firstWireIsStuck = False

        #second wire
        self.drawingSecondWire = False
        self.stickSecondWireInRed = False
        self.stickSecondWireInBlue = False
        self.stickSecondWireInYellow = False
        self.stickSecondWireInPink = False
        self.releasedInSecondWire = False
        self.secondWireIsStuck = False

        #third wire
        self.drawingThirdWire = False
        self.stickThirdWireInRed = False
        self.stickThirdWireInBlue = False
        self.stickThirdWireInYellow = False
        self.stickThirdWireInPink = False
        self.releasedInThirdWire = False
        self.thirdWireIsStuck = False

        #fourth wire
        self.drawingFourthWire = False
        self.stickFourthWireInRed = False
        self.stickFourthWireInBlue = False
        self.stickFourthWireInYellow = False
        self.stickFourthWireInPink = False
        self.releasedInFourthWire = False
        self.fourthWireIsStuck = False
        
        #wire color order
        self.setRandomWireOrder()

    ############################################################################
    # GET/SET stuff:
    ############################################################################
  
    
    #these four (below)return stickwireInColor values for each wire
    def getStickFirstWireInColor(self, color):
        if color == 'red':
            return self.stickFirstWireInRed
        elif color == 'blue':
            return self.stickFirstWireInBlue
        elif color == 'yellow':
            return self.stickFirstWireInYellow
        elif color == 'pink':
            return self.stickFirstWireInPink
    def getStickSecondWireInColor(self, color):
        if color == 'red':
            return self.stickSecondWireInRed
        elif color == 'blue':
            return self.stickSecondWireInBlue
        elif color == 'yellow':
            return self.stickSecondWireInYellow
        elif color == 'pink':
            return self.stickSecondWireInPink
    def getStickThirdWireInColor(self, color):
        if color == 'red':
            return self.stickThirdWireInRed
        elif color == 'blue':
            return self.stickThirdWireInBlue
        elif color == 'yellow':
            return self.stickThirdWireInYellow
        elif color == 'pink':
            return self.stickThirdWireInPink
    def getStickFourthWireInColor(self, color):
        if color == 'red':
            return self.stickFourthWireInRed
        elif color == 'blue':
            return self.stickFourthWireInBlue
        elif color == 'yellow':
            return self.stickFourthWireInYellow
        elif color == 'pink':
            return self.stickFourthWireInPink

    #these four (below) return each wire's isStuck variable
    def getIsFirstWireStuck(self):
        return self.firstWireIsStuck
    def getIsSecondWireStuck(self):
        return self.secondWireIsStuck
    def getIsThirdWireStuck(self):
        return self.thirdWireIsStuck
    def getIsFourthWireStuck(self):
        return self.fourthWireIsStuck

    #these four (below) set the drawing variables to a given bool for each wire
    def setDrawingFirstWire(self, boolVal):
        self.drawingFirstWire = boolVal
    def setDrawingSecondWire(self, boolVal):
        self.drawingSecondWire = boolVal
    def setDrawingThirdWire(self, boolVal):
        self.drawingThirdWire = boolVal
    def setDrawingFourthWire(self, boolVal):
        self.drawingFourthWire = boolVal
    
    #these four (below) return the drawing variables for each wire
    def getDrawingFirstWire(self):
        return self.drawingFirstWire
    def getDrawingSecondWire(self):
        return self.drawingSecondWire
    def getDrawingThirdWire(self):
        return self.drawingThirdWire
    def getDrawingFourthWire(self):
        return self.drawingFourthWire 
    
    #these four (below) return each wire color
    def getFirstWireColor(self):
        return self.firstWireColor
    def getSecondWireColor(self):
        return self.secondWireColor
    def getThirdWireColor(self):
        return self.thirdWireColor
    def getFourthWireColor(self):
        return self.fourthWireColor

    #these four (below) check if each wire is on correct ending wire
        #if so, it sets the appropriate values
    def checkSetFirstOnCorrectEndWire(self, x, y): #x, y are event.x, event.y
        self.drawingFirstWire = False
        if (self.firstWireColor == 'red' and
                self.isReleasedInFirstWireEnd(x, y)):
            self.stickFirstWireInRed = True
            self.firstWireIsStuck = True

        elif (self.firstWireColor == 'blue' and
                self.isReleasedInSecondWireEnd(x, y)):
            self.stickFirstWireInBlue = True
            self.firstWireIsStuck = True

        elif (self.firstWireColor == 'yellow' and
                self.isReleasedInThirdWireEnd(x, y)):
            self.stickFirstWireInYellow = True
            self.firstWireIsStuck = True

        elif (self.firstWireColor == 'pink' and
                self.isReleasedInFourthWireEnd(x, y)):
            self.stickFirstWireInPink = True
            self.firstWireIsStuck = True
    def checkSetSecondOnCorrectEndWire(self, x, y): #x, y are event.x, event.y
        self.drawingSecondWire = False
        if (self.secondWireColor == 'red' and
                self.isReleasedInFirstWireEnd(x, y)):
            self.stickSecondWireInRed = True
            self.secondWireIsStuck = True
            
        elif (self.secondWireColor == 'blue' and
                self.isReleasedInSecondWireEnd(x, y)):
            self.stickSecondWireInBlue = True
            self.secondWireIsStuck = True

        elif (self.secondWireColor == 'yellow' and
                self.isReleasedInThirdWireEnd(x, y)):
            self.stickSecondWireInYellow = True
            self.secondWireIsStuck = True

        elif (self.secondWireColor == 'pink' and
                self.isReleasedInFourthWireEnd(x, y)):
            self.stickSecondWireInPink = True
            self.secondWireIsStuck = True
    def checkSetThirdOnCorrectEndWire(self, x, y): #x, y are event.x, event.y
        self.drawingThirdWire = False
        if (self.thirdWireColor == 'red' and
                self.isReleasedInFirstWireEnd(x, y)):
            self.stickThirdWireInRed = True
            self.thirdWireIsStuck = True 

        elif (self.thirdWireColor == 'blue' and
                self.isReleasedInSecondWireEnd(x, y)):
            self.stickThirdWireInBlue = True
            self.thirdWireIsStuck = True

        elif (self.thirdWireColor == 'yellow' and
                self.isReleasedInThirdWireEnd(x, y)):
            self.stickThirdWireInYellow = True
            self.thirdWireIsStuck = True

        elif (self.thirdWireColor == 'pink' and
                self.isReleasedInFourthWireEnd(x, y)):
            self.stickThirdWireInPink = True
            self.thirdWireIsStuck = True
    def checkSetFourthOnCorrectEndWire(self, x, y): #x, y are event.x, event.y
        self.drawingFourthWire = False
        if (self.fourthWireColor == 'red' and
                self.isReleasedInFirstWireEnd(x, y)):
            self.stickFourthWireInRed = True
            self.fourthWireIsStuck = True
            
        elif (self.fourthWireColor == 'blue' and
                self.isReleasedInSecondWireEnd(x, y)):
            self.stickFourthWireInBlue = True
            self.fourthWireIsStuck = True

        elif (self.fourthWireColor == 'yellow' and
                self.isReleasedInThirdWireEnd(x, y)):
            self.stickFourthWireInYellow = True
            self.fourthWireIsStuck = True

        elif (self.fourthWireColor == 'pink' and
                self.isReleasedInFourthWireEnd(x, y)):
            self.stickFourthWireInPink = True
            self.fourthWireIsStuck = True
    
    ############################################################################
    # GAMEPLAY stuff:
    ############################################################################

    #return true if all wires are stuck
    def isAllWiresCompleted(self):
        if (self.firstWireIsStuck and self.secondWireIsStuck and
            self.thirdWireIsStuck and self.fourthWireIsStuck):
            return True
        return False

    #sets wire colors from randomly generated ordered list of wire colors
    def setRandomWireOrder(self):
        #red, yellow, pink, blue
        colorNumDict = { 0: 'red',
                        1: 'yellow',
                        2: 'pink',
                        3: 'blue'
                    }

        numSet = { 0, 1, 2, 3}
        orderedWireList = []
        while(len(numSet) > 0):
            currNum = random.randint(min(numSet), max(numSet))
            if currNum in numSet:
                orderedWireList.append(colorNumDict.get(currNum, 'invalid_wire_num'))
                numSet.remove(currNum)

        #set wire colors
        self.firstWireColor = orderedWireList[0]
        self.secondWireColor = orderedWireList[1]
        self.thirdWireColor = orderedWireList[2]
        self.fourthWireColor = orderedWireList[3]
    
   

    ############################################################################
    # WIRE BUTTON stuff:
    ############################################################################
    #initialize first wire Start button dimensions
    def setWireStartButtonsDimensions(self):
        cx,cy = self.appWidth//2, self.appHeight//2

        halfImgWidth = self.wiresImageWidth/2
        halfImgHeight = self.wiresImageHeight/2
        fifthOfImageHeight = self.wiresImageHeight * 1/5.5

        x0 = cx - halfImgWidth + 3
        y0 = cy - halfImgHeight + fifthOfImageHeight
        x1 = x0 + 40
        y1 = y0 + 20

        #set first wire
        self.firstWireSButtonLeftX = x0
        self.firstWireSButtonRightX = x1
        self.firstWireSButtonLeftY = y0
        self.firstWireSButtonRightY = y1

        #set second wire
        self.secondWireSButtonLeftX = x0
        self.secondWireSButtonRightX = x1
        self.secondWireSButtonLeftY = y0 + fifthOfImageHeight + 15
        self.secondWireSButtonRightY = y1 + fifthOfImageHeight + 15

        #set third wire
        self.thirdWireSButtonLeftX = x0
        self.thirdWireSButtonRightX = x1
        self.thirdWireSButtonLeftY = y0 + 2*fifthOfImageHeight + 25
        self.thirdWireSButtonRightY = y1 + 2*fifthOfImageHeight + 25

        #set fourth wire
        self.fourthWireSButtonLeftX = x0
        self.fourthWireSButtonRightX = x1
        self.fourthWireSButtonLeftY = y0 + 3*fifthOfImageHeight + 35
        self.fourthWireSButtonRightY = y1 + 3*fifthOfImageHeight + 35

    #these four (below) return the start (left side) wire button dimensions
    def getFirstWireSButtonDims(self):
        return (self.firstWireSButtonLeftX, self.firstWireSButtonLeftY,
                self.firstWireSButtonRightX, self.firstWireSButtonRightY)
    def getSecondWireSButtonDims(self):
        return (self.secondWireSButtonLeftX, self.secondWireSButtonLeftY,
                self.secondWireSButtonRightX, self.secondWireSButtonRightY)
    def getThirdWireSButtonDims(self):
        return (self.thirdWireSButtonLeftX, self.thirdWireSButtonLeftY,
                self.thirdWireSButtonRightX, self.thirdWireSButtonRightY)
    def getFourthWireSButtonDims(self):
        return (self.fourthWireSButtonLeftX, self.fourthWireSButtonLeftY,
                self.fourthWireSButtonRightX, self.fourthWireSButtonRightY)

    #these four (below) return true if player click in start wire buttons
    def isClickInFirstWireStart(self, x, y):
        if ((self.firstWireSButtonLeftX <= x <= self.firstWireSButtonRightX) and
            (self.firstWireSButtonLeftY <= y <= self.firstWireSButtonRightY)):
            return True
        return False
    def isClickInSecondWireStart(self, x, y):
        if ((self.secondWireSButtonLeftX <= x <= self.secondWireSButtonRightX) and
            (self.secondWireSButtonLeftY <= y <= self.secondWireSButtonRightY)):
            return True
        return False
    def isClickInThirdWireStart(self, x, y):
        if ((self.thirdWireSButtonLeftX <= x <= self.thirdWireSButtonRightX) and
            (self.thirdWireSButtonLeftY <= y <= self.thirdWireSButtonRightY)):
            return True
        return False
    def isClickInFourthWireStart(self, x, y):
        if ((self.fourthWireSButtonLeftX <= x <= self.fourthWireSButtonRightX) and
            (self.fourthWireSButtonLeftY <= y <= self.fourthWireSButtonRightY)):
            return True
        return False

    #initialize first wire end button dimensions
    def setWireEndButtonsDimensions(self):
        cx,cy = self.appWidth//2, self.appHeight//2 

        halfImgWidth = self.wiresImageWidth/2
        halfImgHeight = self.wiresImageHeight/2
        fifthOfImageHeight = self.wiresImageHeight * 1/5.5

        x0 = cx + halfImgWidth - 3
        y0 = cy - halfImgHeight + fifthOfImageHeight
        x1 = x0 - 40
        y1 = y0 + 20

        #set first wire
        self.firstWireEButtonLeftX = x0
        self.firstWireEButtonRightX = x1
        self.firstWireEButtonLeftY = y0
        self.firstWireEButtonRightY = y1

        #set second wire
        self.secondWireEButtonLeftX = x0
        self.secondWireEButtonRightX = x1
        self.secondWireEButtonLeftY = y0 + fifthOfImageHeight + 15
        self.secondWireEButtonRightY = y1 + fifthOfImageHeight + 15

        #set third wire
        self.thirdWireEButtonLeftX = x0
        self.thirdWireEButtonRightX = x1
        self.thirdWireEButtonLeftY = y0 + 2*fifthOfImageHeight + 25
        self.thirdWireEButtonRightY = y1 + 2*fifthOfImageHeight + 25

        #set fourth wire
        self.fourthWireEButtonLeftX = x0
        self.fourthWireEButtonRightX = x1
        self.fourthWireEButtonLeftY = y0 + 3*fifthOfImageHeight + 35
        self.fourthWireEButtonRightY = y1 + 3*fifthOfImageHeight + 35

    #these four (below) return the end (right side) wire button dimensions
    def getFirstWireEButtonDims(self):
        return (self.firstWireEButtonLeftX, self.firstWireEButtonLeftY,
            self.firstWireEButtonRightX, self.firstWireEButtonRightY)
    def getSecondWireEButtonDims(self):
        return (self.secondWireEButtonLeftX, self.secondWireEButtonLeftY,
                self.secondWireEButtonRightX, self.secondWireEButtonRightY)
    def getThirdWireEButtonDims(self):
        return (self.thirdWireEButtonLeftX, self.thirdWireEButtonLeftY,
                self.thirdWireEButtonRightX, self.thirdWireEButtonRightY)
    def getFourthWireEButtonDims(self):
        return (self.fourthWireEButtonLeftX, self.fourthWireEButtonLeftY,
                self.fourthWireEButtonRightX, self.fourthWireEButtonRightY)

    #these four (below) return true if player click/release in end wire buttons
    def isReleasedInFirstWireEnd(self, x, y):
        #caution, leftx and rightx are flipped
        if ((self.firstWireEButtonLeftX >= x >= self.firstWireEButtonRightX) and
            (self.firstWireEButtonLeftY <= y <= self.firstWireEButtonRightY)):
            return True
        return False
    def isReleasedInSecondWireEnd(self, x, y):
        #caution, leftx and rightx are flipped
        if ((self.secondWireEButtonLeftX >= x >= self.secondWireEButtonRightX) and
            (self.secondWireEButtonLeftY <= y <= self.secondWireEButtonRightY)):
            return True
        return False
    def isReleasedInThirdWireEnd(self, x, y):
        #caution, leftx and rightx are flipped
        if ((self.thirdWireEButtonLeftX >= x >= self.thirdWireEButtonRightX) and
            (self.thirdWireEButtonLeftY <= y <= self.thirdWireEButtonRightY)):
            return True
        return False
    def isReleasedInFourthWireEnd(self, x, y):
        #caution, leftx and rightx are flipped
        if ((self.fourthWireEButtonLeftX >= x >= self.fourthWireEButtonRightX) and
            (self.fourthWireEButtonLeftY <= y <= self.fourthWireEButtonRightY)):
            return True
        return False


    