
#################################################################################
# CREATOR INFO:
################################################################################

#Name: Colin May
#Andrew Id: cmmay
#Term Project 15-112 Fall 2020

################################################################################
################################################################################
#GAME INSPIRATION SOURCE: MY PROJECT - AMONG US 3D - IS BASED OFF OF THE ORIGINAL 
    #"AMONG US" 2D ONLINE GAME. THE MAP & SPRITES ARE BASED OFF OF THAT GAME
        #http://www.innersloth.com/index.php 
################################################################################
################################################################################

from cmu_112_graphics import *
from Player import *
from Ai import *
from myAmongUsSounds import *
from Tasks import *
from tkinter import *
import random, math, time



#initializes/resets entire game state
def appStarted(app):
    app.timerDelay = 0 #adjust as necessary
    app.timerVotingFor = False

    #tkinter:
    app.drawingTkSpConfigWindow = False
    setUpSpConfigWindowAndHide(app)
    app.runningVoteTkWindow = False
    app.drawingTkVotingWindow = False
    

    #sounds
    app.mySounds = Sounds()
    app.mySounds.playMainTitleScreenMusic() #initially start title music
    
    #images
    setAllImages(app)

    #SPLASH SCREENS:
    #title screen
    app.drawingEjectedScreen = False
    app.stars = []
    initializeTitleScreenStars(app)
    app.drawingATitleScreen = True #used for all
    app.drawingMainTitleScreen = True
    setSinglePlayerButtonDimensions(app)
    #single player screen
    app.drawingSinglePlayerScreen = False
    setConfigSPButtonDimensions(app)
    setSPPlayButtonDimensions(app)

    app.drawingCrewWinScreen = False
    app.drawingImpWinScreen = False
    setPlayAgainButtonDimensions(app)
    
    

    #map
    mapFileName = "AmongUsWorldMap.txt" #map based off original "Among Us"
    app.worldMap = getMapFromFile(mapFileName) #2d list of digits 
    app.mapRows = len(app.worldMap)
    app.mapCols = len(app.worldMap[0])
    app.isMapOpen = False
    app.mapMargin = 50 #dont change this
    app.mapCircleRadius = 10

    #player
    app.numPlayers = 1 #single player
    app.startingSPImpStatus = 'crewmate'
    app.startingSPPlayerspeed = 0.15
    app.playerViewAIsOnMap = False
    app.drawingPlayerDiedText = False
    

    #Tasks
    app.numTasks = 4 #change as add more tasks to map
    app.numTasksCompleted = 0 #change to be for each player (multiplayer)
    initializeWiresTasksObjects(app)

    #AI
    app.numAIs = 2 #MUST BE GREATER THAN 1 for game
    app.maxNumAIs = 5
    app.timerCount = 0
    app.isGetStartAiTaskTime = False
    app.startAiTaskTime = None
    app.changeDecisionTimerCount = 0
    app.isIMPGetStartAiTaskTime = False
    app.startIMPAiTaskTime = None
    app.IMPTimerCount = 0
    app.killIMPTime = 0

    app.killCoolDownDone = False
    app.impReportTimeDone = False

    #ray casting
    app.vertLineDimensions = dict() #contains { x: (pxLineBottom, pxLineTop, 
    app.vertLinePerpDistance = dict() #contains perpendicular distances from player
                                        #to walls at [x] on screen#   color) }
    app.sortedAiDistList = []
    app.aiRowColDistDict = dict()
    app.canCreateImage = False
    app.aiXDistDict = dict()
    app.needToSaveDistance = False
    app.sortedAiDistListPlusExtra = []

    #gameplay
    app.distToKill = 4
    app.deadBodyLocations = [] #(row,col) locations of dead bodies 
    app.aiReported = False
    app.playerReported = False
    app.killCoolDownCurrTime = 15
    app.distToReport = 4
    app.reportWaitTimeCount = 0
    app.drawingTimerCount = 0
    app.drawingReportingScreen = False
    app.getStartTimeReportedScreen = False
    
    #voting
    setVoteButtonDimensions(app)
    app.showingVotes = False
    app.largestVotes = None
    app.mostVotedPlayer = None
    #app.mostVotedPerson = None
    #app.largestVotes = None
    #app.numAiPlayerAlive = app.numAIs + app.numPlayers
    #setUpVotingWindowAtStartAndHide(app)
    app.drawingVotingScreen = False
    app.boolVal = True
    #app.promptVent = False


    
    



def setUpSinglePlayer(app):
    createNewPlayer(app) #sets app.player (called again after hit play)
    app.aiDistancesFromPlayer = dict()
    setPlayerUseButtonDimensions(app)
    setPlayerReportButtonDimensions(app)
    setPlayerKillButtonDimensions(app)
    app.player.setPlayerSpeed(app.startingSPPlayerspeed)
    createStartingAIs(app)
    if app.player.getImpStatus() == 'crewmate':
        app.numTaskBarCols = (app.numPlayers + (app.numAIs-1)) * app.numTasks
    elif app.player.getImpStatus() == 'imposter':
        app.numTaskBarCols = ((app.numPlayers-1) + app.numAIs) * app.numTasks
################################################################################
# WIRES TASK:
################################################################################
#initialize the four wires tasks named with their location
def initializeWiresTasksObjects(app):
    wiresImageSize = app.wiresTaskImage.size
    #in electrical:
    app.elecWiresTaskObj = WiresTask(app.width, app.height, wiresImageSize)
    #in storage:
    app.storWiresTaskObj = WiresTask(app.width, app.height, wiresImageSize)
    #in nav:
    app.navWiresTaskObj = WiresTask(app.width, app.height, wiresImageSize)
    #in cafe:
    app.cafeWiresTaskObj = WiresTask(app.width, app.height, wiresImageSize)
        
#get the corresponding wires task object to given location
def getWiresTaskObjectFromLocation(app, currWiresLocation):
    if currWiresLocation == 'electrical':
        return app.elecWiresTaskObj
    elif currWiresLocation == 'storage':
        return app.storWiresTaskObj
    elif currWiresLocation == 'navigation':
        return app.navWiresTaskObj
    elif currWiresLocation == 'cafeteria':
        return app.cafeWiresTaskObj



################################################################################
# ADV TKINTER WINDOW STUFF:
################################################################################
#initializes tkinter single player configuration window
def setUpSpConfigWindowAndHide(app):
    #SETUP:
    app.spConfigTkWindow = Tk()
   
    app.spConfigTkWindow.geometry('200x300')
    app.spConfigTkWindow.configure(bg='dark gray')
    app.spConfigTkWindow.title("Game Settings")
    app.spConfigTkWindow.withdraw() #hide window at start

    #WIDGETS:
    
    app.speedText = Label(app.spConfigTkWindow, text="Player Speed", 
                        background='dark gray', font=('Helvetica', 14, 'bold'))
    app.speedText.grid(row=1, column=1, sticky=N)

    app.speedText1 = Label(app.spConfigTkWindow, text="fast", 
                        background='dark gray', font=('Helvetica', 12))
    app.speedText1.grid(row=2, column=2, sticky=W)

    app.speedText2 = Label(app.spConfigTkWindow, text="slow", 
                        background='dark gray', font=('Helvetica', 12))
    app.speedText2.grid(row=2, column=0, sticky=E)

    
    app.setSpeedSlider = Scale(app.spConfigTkWindow, from_=10, to=20, showvalue=0, 
                orient=HORIZONTAL, background='dark gray')
    app.setSpeedSlider.set(15)    
    app.setSpeedSlider.grid(row=2, column=1, sticky=N)


    app.statusText = Label(app.spConfigTkWindow, text="Imposter Status", 
                        background='dark gray', font=('Helvetica', 14, 'bold'))
    app.statusText.grid(row=3, column=1, sticky=N)

    app.statusVar = IntVar(app.spConfigTkWindow)    
    app.crewStatusRadioButton = Radiobutton(app.spConfigTkWindow, 
                                text='crewmate', variable=app.statusVar,
                                value=1, bg='dark gray', 
                                command=lambda: toggleRadioCrew(app))
    app.crewStatusRadioButton.grid(row=4, column=1, sticky=N)
    
    app.impStatusRadioButton = Radiobutton(app.spConfigTkWindow, 
                                text='imposter', variable=app.statusVar,
                                value=0, bg='dark gray')#, 
                                #command=lambda: toggleRadioCrew(app))
    app.impStatusRadioButton.grid(row=5, column=1, sticky=N)
    app.crewStatusRadioButton.select()

    #confirm button
    Button(app.spConfigTkWindow, text="Confirm",
        command=lambda:configConfirmButton(app)).grid(row=6, column=1, sticky=N)

#run / show window (loops)
def runSPConfigWindow(app):
    app.spConfigTkWindow.deiconify() #show window

#execute confirm button actions        
def configConfirmButton(app):
    if app.statusVar.get() == 1:
        app.startingSPImpStatus = 'crewmate'
    elif app.statusVar.get() == 0:
        app.startingSPImpStatus = 'imposter'
    
    app.startingSPPlayerspeed = app.setSpeedSlider.get() / 100
    
    #app.player.setPlayerSpeed(speed) #set speed

    app.spConfigTkWindow.withdraw()
    app.drawingTkSpConfigWindow = False


################################################################################
# IMAGE / SOUND STUFF:
################################################################################   
def setAllImages(app):
    #among us text title
    #free IMAGE SOURCE: https://www.citypng.com/show_download/stock/4733 
    fileName = 'gameImages/amongUsTitle.png'
    app.titleTextImage = app.loadImage(fileName)
    app.titleTextImage = app.scaleImage(app.titleTextImage, 1/4)
    
    #3d text image
    #free IMAGE SOURCE: 
        #https://cdn.freelogovectors.net/wp-content/uploads/2015/06/3d_10.png
    url = 'https://cdn.freelogovectors.net/wp-content/uploads/2015/06/3d_10.png'
    app.text3dImage = app.loadImage(url)
    app.text3dImage = app.scaleImage(app.text3dImage, 1/5)

    #crewmate USE button image + transparent image
    #free IMAGE SOURCE:
        #https://static.wikia.nocookie.net/among-us-wiki/images/1/15/Use.png/revision/latest?cb=20201002163154
    fileName = 'gameImages/Usebutton.png'
    app.useButtonImage = app.loadImage(fileName)
    app.useButtonImage = app.scaleImage(app.useButtonImage, 1 * 7/8)
    #transparency scale: 0 -> 100% transparent, 255 -> 0% transparent
    app.useButtonImageTrans = app.useButtonImage.copy()
    app.useButtonImageTrans.putalpha(15)
    app.useButtonImageWidth, app.useButtonImageHeight = app.useButtonImage.size
    
    #crewmate REPORT button image + transparent image
    #free IMAGE SOURCE:
        #https://among-us.fandom.com/wiki/Report?file=Report.png
    fileName = 'gameImages/reportButton.png'
    app.reportButtonImage = app.loadImage(fileName)
    app.reportButtonImage = app.scaleImage(app.reportButtonImage, 1 * 7/8)
    #transparency scale: 0 -> 100% transparent, 255 -> 0% transparent
    app.reportButtonImageTrans = app.reportButtonImage.copy()
    app.reportButtonImageTrans.putalpha(15)
    app.reportButtonImageWidth, app.reportButtonImageHeight = app.reportButtonImage.size


    #wires task image
    #free IMAGE SOURCE:
        #https://among-us.fandom.com/wiki/Fix_Wiring?file=Fix_Wiring_Backdrop.png
    fileName = 'gameImages/wiresTaskImage.png'
    app.wiresTaskImage = app.loadImage(fileName)
    app.wiresTaskImage = app.scaleImage(app.wiresTaskImage, 1)
    app.wiresTaskImageWidth, app.wiresTaskImageHeight = app.wiresTaskImage.size


    #task exclamation image
    #free IMAGE SOURCE:
    fileName = 'gameImages/taskExclamation.png'
    app.taskExclamationImage = app.loadImage(fileName)
    app.taskExclamationImage = app.scaleImage(app.taskExclamationImage, 1)
    app.taskExclamationImage.putalpha(150)

    #imposter kill image
    fileName = 'gameImages/Killimage.png'
    app.killButtonImage = app.loadImage(fileName)
    app.killButtonImage = app.scaleImage(app.killButtonImage, 1*7/8)
    app.killButtonImageTrans = app.killButtonImage.copy()
    app.killButtonImageTrans.putalpha(15)
    app.killButtonImageWidth, app.killButtonImageHeight = app.killButtonImage.size


    '''CHARACTER SPRITES:'''
    #SOURCE: https://among-us.fandom.com/wiki/Red #used for all colors

    #YELLOW ALIVE CHARACTER
    fileName = 'gameImages/yellowAlive.png'
    app.yellowAliveImage = app.loadImage(fileName)
    #YELLOW DEAD CHARACTER
    fileName = 'gameImages/yellowDeadImage.png'
    app.yellowDeadImage = app.loadImage(fileName)

    #ORANGE ALIVE CHARACTER
    fileName = 'gameImages/orangeAlive.png'
    app.orangeAliveImage = app.loadImage(fileName)
    #ORANGE DEAD CHARACTER
    fileName = 'gameImages/orangeDead.png'
    app.orangeDeadImage = app.loadImage(fileName)

    #BLUE ALIVE CHARACTER
    fileName = 'gameImages/blueAlive.png'
    app.blueAliveImage = app.loadImage(fileName)
    #BLUE DEAD CHARACTER
    fileName = 'gameImages/blueDead.png'
    app.blueDeadImage = app.loadImage(fileName)

    #GREEN ALIVE CHARACTER
    fileName = 'gameImages/greenAlive.png'
    app.greenAliveImage = app.loadImage(fileName)
    #GREEN DEAD CHARACTER
    fileName = 'gameImages/greenDead.png'
    app.greenDeadImage = app.loadImage(fileName)

    #RED ALIVE CHARACTER
    fileName = 'gameImages/redAlive.png'
    app.redAliveImage = app.loadImage(fileName)
    #RED DEAD CHARACTER
    fileName = 'gameImages/redDead.png'
    app.redDeadImage = app.loadImage(fileName)

    #reported screen
    fileName = 'gameImages/bodyReportedScreenImage.png'
    app.bodyReportedScreenImage = app.loadImage(fileName)

################################################################################
# SPLASH SCREEN STUFF:
################################################################################
#Set button dimensions & isClicked to use buttons:

def isClickInSinglePlayerButton(app, x, y):
    if ((app.spButtonLeftX <= x <= app.spButtonRightX) and
        (app.spButtonLeftY <= y <= app.spButtonRightY)):
        return True
    return False

def initializeTitleScreenStars(app):
    numStars = app.width // 10
    for _ in range(numStars):
        cx = random.randint(0, app.width)
        cy = random.randint(0, app.height)
        r = random.randint(1, 4)
        app.stars.append((cx, cy, r))

#need to fix this star effect for changing window sizes
def playScreenStarEffect(app):
    for i in range(len(app.stars)):
        cx, cy, r = app.stars[i]
        speed = random.randint(1,4)
        app.stars[i] = (cx+speed*.5, cy, r)
        if cx >= app.width:
            app.stars[i] = (0, cy, r)

def setSinglePlayerButtonDimensions(app):
    cx,cy = app.width//2, app.height//2.25
    #x1, y1 = x0 + 400, y0 + 100
    halfWidth = 175
    halfHeight = 30

    x0,y0,x1,y1 = cx-halfWidth, cy-halfHeight, cx+halfWidth, cy+halfHeight
    app.spButtonLeftX = x0
    app.spButtonLeftY = y0
    app.spButtonRightX = x1
    app.spButtonRightY = y1

def isClickInConfigureSPButton(app, x, y):
    if ((app.conButtonLeftX <= x <= app.conButtonRightX) and
        (app.conButtonLeftY <= y <= app.conButtonRightY)):
        return True
    return False

def setConfigSPButtonDimensions(app):
    cx,cy = app.width//2, app.height//2.25
    #x1, y1 = x0 + 400, y0 + 100
    halfWidth = 175
    halfHeight = 30

    x0,y0,x1,y1 = cx - halfWidth, cy-halfHeight, cx + halfWidth, cy + halfHeight
    app.conButtonLeftX = x0
    app.conButtonRightX = x1
    app.conButtonLeftY = y0
    app.conButtonRightY = y1

def isClickInSPPlayButton(app, x, y):
    if ((app.spPlayButtonLeftX <= x <= app.spPlayButtonRightX) and
        (app.spPlayButtonLeftY <= y <= app.spPlayButtonRightY)):
        return True
    return False

def setSPPlayButtonDimensions(app):
    cx,cy = app.width//2, app.height//1.25
    #x1, y1 = x0 + 400, y0 + 100
    halfWidth = 175
    halfHeight = 30

    x0,y0,x1,y1 = cx - halfWidth, cy-halfHeight, cx + halfWidth, cy + halfHeight
    app.spPlayButtonLeftX = x0
    app.spPlayButtonRightX = x1
    app.spPlayButtonLeftY = y0
    app.spPlayButtonRightY = y1

def isClickInPlayAgainButton(app, x, y):
    if ((app.playAgainButtonLeftX <= x <= app.playAgainButtonRightX) and
        (app.playAgainButtonLeftY <= y <= app.playAgainButtonRightY)):
        #print('in here')
        return True
    return False

def setPlayAgainButtonDimensions(app):
    #print('here')
    cx,cy = app.width//2, app.height//1.25
    #x1, y1 = x0 + 400, y0 + 100
    halfWidth = 175
    halfHeight = 30

    x0,y0,x1,y1 = cx - halfWidth, cy-halfHeight, cx + halfWidth, cy + halfHeight
    app.playAgainButtonLeftX = x0
    app.playAgainButtonRightX = x1
    app.playAgainButtonLeftY = y0
    app.playAgainButtonRightY = y1

def isClickInVoteButton(app, x, y):
    if ((app.voteButtonLeftX <= x <= app.voteButtonRightX) and
        (app.voteButtonLeftY <= y <= app.voteButtonRightY)):
        #print('in here')
        return True
    return False

def setVoteButtonDimensions(app):
    #print('here')
    cx,cy = app.width//2, app.height*(6/8)
    #x1, y1 = x0 + 400, y0 + 100
    halfWidth = 65
    halfHeight = 25

    x0,y0,x1,y1 = cx - halfWidth, cy-halfHeight, cx + halfWidth, cy + halfHeight
    app.voteButtonLeftX = x0
    app.voteButtonRightX = x1
    app.voteButtonLeftY = y0
    app.voteButtonRightY = y1

################################################################################
# MAP STUFF:
################################################################################

#returns the worldMap 2d list from file
def getMapFromFile(fileName):
    map2dList = []
    with open(fileName) as f: #"with open" learned from 112 website: 
            #https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
        mapString = f.read() #returns string

    #convert to list
    mapString.strip()
    for line in mapString.splitlines():
        lineList = []
        for valStr in line.split(','):
            lineList.append(int(valStr))
        map2dList.append(lineList)
    return map2dList



################################################################################
# PLAYER STUFF:
################################################################################

#sets largestVotes and person with most votes
def findLargestVotes(app):
    largestVotes = None
    for ai in app.allAIs:
        numVotes = ai.getNumSelfVotes()
        if largestVotes == None or numVotes > largestVotes:
            largestVotes = numVotes
            mostVotedPlayer = ai

    playerNumVotes = app.player.getNumSelfVotes()
    if playerNumVotes > largestVotes:
        largestVotes = playerNumVotes
        mostVotedPlayer = app.player
    
    app.largestVotes = largestVotes
    app.mostVotedPlayer = mostVotedPlayer

#move when hit report
def reportMoveEveryone(app):
    app.drawingReportScreen = True
    for ai in app.allAIs:
        #set ai positions to start
        ai.setRow(ai.getInitialRow())
        ai.setCol(ai.getInitialCol())
        ai.setIsMoving(False)

    app.player.setIsMoving(False)
    



#returns true if near deadbody, and if true return (name,color) of deadai
def playerIsNearDeadBody(app):
    pRow,pCol = app.player.getRow(),app.player.getCol()
    for (deadColor,dRow,dCol) in app.deadBodyLocations:
        if getEuclideanDistance(app,dRow,dCol,pRow,pCol) <= app.distToReport:
            return (True, deadColor)
    return (False,None,None)


 
#returns true if near alive ai, and return that ai object
def isPlayerImposterNearAliveAI(app):
    for ai in app.allAIs:
        if ai.getIsAlive():
            aiRow,aiCol = ai.getRow(),ai.getCol()
            pRow,pCol = app.player.getRow(),app.player.getCol()
            
            currDist = getEuclideanDistance(app,pRow,pCol,aiRow,aiCol)
            if currDist <= app.distToKill:
                closestAi = ai
                return (True,closestAi) #currently returns first check within 7
    return (False, None)



#pathagorean theorem
def getEuclideanDistance(app, firstRow,firstCol,secRow,secCol):
    xLength = abs(secCol-firstCol)
    yLength = abs(secRow-firstRow)
    
    #pathagorean theorem
    dist = math.sqrt((xLength**2) + (yLength**2))
    return dist  


#sets app.player to new Player (single player stuff in it)
def createNewPlayer(app):
    color = getRandPlayerColor(app) #initial random color
    startRow, startCol = 5, 40 #initial position vector
    faceDirectionX, faceDirectionY = -1, 0 #initial direction vector, can't change?

    if app.startingSPImpStatus == 'crewmate':
        app.player = (PlayerCrewmate(color, startRow, startCol, 
                        faceDirectionX, faceDirectionY)) #, impStatus))
    if app.startingSPImpStatus == 'imposter':
        app.player = (PlayerImposter(color, startRow, startCol, 
                        faceDirectionX, faceDirectionY))
    #rotate starting position
    rotatePlayerRightNTimes(app, 11)


def rotatePlayerRightNTimes(app, n): #right now only for single player
    for _ in range(n):
        app.player.rotateRight()   

#returns random color for player, can't repeat other player colors 
def getRandPlayerColor(app): 
    color = random.randint(1,5)
    colorChooser = {   #dict of player colors
                    1: "blue",
                    2: "orange",
                    3: "green",
                    4: "red",
                    5: "yellow",
                    # 6: "pink",
                    # 7: "purple",
                    # 8: "brown",
                    # 9: "lime",
                   }
    playerColor = colorChooser.get(color, "invalid playerColor")
    return playerColor

def distFormula(x1, y1, x2, y2): #did not use 112 website for this
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

#update distance from player to ai in dictionary
def updateDistanceToAIsDict(app):
    #might have to loop between each player, if have multiplayers
    pCx, pCy = app.player.findCxAndCy(app, app.mapMargin)

    for ai in app.allAIs:
        aiCx, aiCy = ai.findCxAndCy(app, app.mapMargin)
        dist = distFormula(pCx, pCy, aiCx, aiCy)
        aiNameId = ai.getName()
        app.aiDistancesFromPlayer[aiNameId] = dist


#below are more button dimensions and isclickinbuttons:
def isClickInUseButton(app, x, y):
    if ((app.useButtonLeftX <= x <= app.useButtonRightX) and
        (app.useButtonLeftY <= y <= app.useButtonRightY)):
        return True
    return False

def setPlayerUseButtonDimensions(app):
    cx,cy = app.width * 7.35/8, app.height * 7/8
    #x1, y1 = x0 + 400, y0 + 100
    halfWidth = app.useButtonImageWidth/2
    halfHeight = app.useButtonImageHeight/2

    x0,y0,x1,y1 = cx - halfWidth, cy-halfHeight, cx + halfWidth, cy + halfHeight
    app.useButtonCx = cx
    app.useButtonCy = cy

    app.useButtonLeftX = x0
    app.useButtonRightX = x1
    app.useButtonLeftY = y0
    app.useButtonRightY = y1


def isClickInReportButton(app, x, y):
    if ((app.reportButtonLeftX <= x <= app.reportButtonRightX) and
        (app.reportButtonLeftY <= y <= app.reportButtonRightY)):
        return True
    return False

def setPlayerReportButtonDimensions(app):
    cx,cy = app.width * 7.35/8, app.height * 5.5/8
    #x1, y1 = x0 + 400, y0 + 100
    halfWidth = app.reportButtonImageWidth/2
    halfHeight = app.reportButtonImageHeight/2

    x0,y0,x1,y1 = cx - halfWidth, cy-halfHeight, cx + halfWidth, cy + halfHeight
    app.reportButtonCx = cx
    app.reportButtonCy = cy

    app.reportButtonLeftX = x0
    app.reportButtonRightX = x1
    app.reportButtonLeftY = y0
    app.reportButtonRightY = y1

def isClickInKillButton(app, x, y):
    if ((app.killButtonLeftX <= x <= app.killButtonRightX) and
        (app.killButtonLeftY <= y <= app.killButtonRightY)):
        return True
    return False

def setPlayerKillButtonDimensions(app):
    cx,cy = app.width * 7.35/8, app.height * 7/8
    #x1, y1 = x0 + 400, y0 + 100
    halfWidth = app.useButtonImageWidth/2
    halfHeight = app.useButtonImageHeight/2

    x0,y0,x1,y1 = cx - halfWidth, cy-halfHeight, cx + halfWidth, cy + halfHeight
    app.killButtonCx = cx
    app.killButtonCy = cy

    app.killButtonLeftX = x0
    app.killButtonRightX = x1
    app.killButtonLeftY = y0
    app.killButtonRightY = y1


################################################################################
# AI STUFF:
################################################################################
#returns random color for player, can't repeat other player colors 
def getRandAIColor(app): 

    color = random.randint(1,5)
    colorChooser = {   #dict of player colors
                    1: "blue",
                    2: "orange",
                    3: "green",
                    4: "red",
                    5: "yellow",
                    # 6: "pink", #only have above^ color images
                    # 7: "purple",
                    # 8: "brown",
                    # 9: "lime",
                   }
    aiColor = colorChooser.get(color, "invalid playerColor")
    return aiColor

def createStartingAIs(app):
    #app.numAis MUST BE GREATER THAN 1 for game   & less than maxNumAis
    startPositionsDict = {
                            0: (1,47),
                            1: (2,48),
                            2: (3,49),
                            3: (4,50),
                            4: (5,49),
                            5: (6,48),
                            6: (7,47),
                            7: (3,47),
                            8: (5,47),
                         }
    app.allAIs = []
    takenColorsList = []
    
    if app.numAIs <= app.maxNumAIs:
        if app.player.getImpStatus() == 'crewmate': #if player is crewmate
            numAIs = app.numAIs-1
        elif app.player.getImpStatus() == 'imposter': #if player is imposter
            numAIs = app.numAIs

        #make crewmates
        for count in range(numAIs): 
            #do random imposter stuff here too
            color = getRandAIColor(app) 
            while color == app.player.getColor() or color in takenColorsList:
                color = getRandAIColor(app)
            takenColorsList.append(color)
            #A on testMap = (3,47)
            
            startRow,startCol = startPositionsDict[count]
            name = f"ai{count}"
            aiCrew = AiCrewmate(name,color,startRow,startCol,app.worldMap)
            app.allAIs.append(aiCrew)

        #make imposter if player crewmate
        if app.player.getImpStatus() == 'crewmate':
            print('make imposter')
            nameNum = app.numAIs-1 
            name = f"ai{nameNum}"
            startRow += 5
            startCol += 5

            color = getRandAIColor(app) 
            while color == app.player.getColor() or color in takenColorsList:
                color = getRandAIColor(app)
            takenColorsList.append(color)

            app.allAIs.append((AiImposter(name, color, startRow, startCol, app.worldMap)))
    else:
        #throw exception here
        print('TOO MANY IMPOSTERS, app.numAIs > app.maxNumAIs')

  
#move ais crewmates right now
def moveAIs(app):
    for ai in app.allAIs:
        #new thread
        if ai.getImpStatus() == 'crewmate':
            ai.runAiCrewmate()
        else:
            pass
            #ai.runAiImposter()

#returns true if near deadbody, and if true return nearest player/ai
def isAICrewNearDeadBody(app, ai):
    aiRow,aiCol = ai.getRow(),ai.getCol()
    for (deadColor,dRow,dCol) in app.deadBodyLocations:
        distToReport = 4
        if getEuclideanDistance(app,dRow,dCol,aiRow,aiCol) <= distToReport:
            nearestPerson,distToNearPerson = getNearestAlivePerson(app, ai)
            return (True,nearestPerson,deadColor,distToNearPerson)
    return (False, None)

#returns true if near deadbody, and if true return nearest player/ai
def isAIImpNearDeadBody(app, ai):
    aiRow,aiCol = ai.getRow(),ai.getCol()
    for (deadColor,dRow,dCol) in app.deadBodyLocations:
        distToReport = 4
        if getEuclideanDistance(app,dRow,dCol,aiRow,aiCol) <= distToReport:
            nearestPerson,distToNearPerson = getNearestAlivePerson(app, ai)
            return (True,nearestPerson,deadColor, distToNearPerson)
    return (False, None)

#returns closest alive person and their distance
def getNearestAlivePerson(app, ai):
    shortestPersonDist = None
    closestPerson = None
    aiRow,aiCol = ai.getRow(),ai.getCol()
    for loopAi in app.allAIs:
        if loopAi.getName() != ai.getName():
            if loopAi.getIsAlive():
                
                lRow,lCol = loopAi.getRow(),loopAi.getCol()
                currDist = getEuclideanDistance(app,lRow,lCol,aiRow,aiCol)
                if shortestPersonDist == None or currDist <= shortestPersonDist:
                    shortestPersonDist = currDist
                    closestPerson = loopAi
    #check player
    if app.player.getIsAlive():
        pRow,pCol = app.player.getRow(),app.player.getCol()
        playerDist = getEuclideanDistance(app,pRow,pCol,aiRow,aiCol)
        if shortestPersonDist == None or playerDist < shortestPersonDist:
            shortestPersonDist = playerDist
            closestPerson = 'player'
    
    return (closestPerson, shortestPersonDist)

################################################################################
# RAY CASTING:
################################################################################

#for every x on screen, calculates the height/color of each vert. line for walls
def setVertLinesDimensionsAlgorithm(app):
    #SOURCE URL: https://lodev.org/cgtutor/raycasting.html (raycasting tutorial)
    #SOURCE PROVIDED: explanations/derivations of the mathematical algorithms, 
            # & example codes/pseudocodes that I used to learn about raycasting
    #MORE SPECIFICALLY^: I used this source when learning 
        #about raycasting the walls, however, to raycast the AIs I DID NOT
        #use this source (used what i had learned about raycasting in general)

    #Note: Calculations are all 2d, so think about the math in 2d to understand
    #Note:  DDA = Digital Differential analysis mathematical algorithm- 
                #finds the grid squares a line hits.
            #-here, we use to find the map grid squares our ray hits & stop
            # algorithm once a wall grid square is hit. Then can find distance
            # to that square and heights of vert. lines, etc.

    
    #create short local variables of player values for clarity
    app.aiXDistDict = dict()
    pRow, pCol = app.player.getRow(), app.player.getCol()
    pDirRow, pDirCol = app.player.getDirRow(), app.player.getDirCol()
    pPlaneX = app.player.getFovPlaneX()
    pPlaneY = app.player.getFovPlaneY()


    '''Go through every vert line (x) in screen:'''
    for x in range(app.width): 
        
        '''Initialize variables necessary for DDA algorithm:'''

        #Get position/direction of actual ray for this x (vert. line):    
        cameraX = 2*x / app.width-1 #x-coordinate on camera plane (-1 to 1 ish)
        app.rayDirX = pDirRow + pPlaneX * cameraX
        app.rayDirY = pDirCol + pPlaneY * cameraX

        #Get map square the ray is in:
        rayMapRow = int(pRow) #mapX (in my original demo)
        rayMapCol = int(pCol) #mapY (in my original demo)

        #Get deltaDistX = distance between vert. grid column lines that ray hits
            # Note: abs(1/rayDirX) derived from pathagorean theorem
            # Note: do not allow division by zero
        if (app.rayDirY == 0):    deltaDistX = 0
        elif (app.rayDirX == 0):  deltaDistX = 1
        else:                 deltaDistX = abs(1 / app.rayDirX) 
        #Get deltaDistY = distance between horz. grid row lines that ray hits
            # Note: abs(1/rayDirY) derived from pathagorean theorem
            # Note: do not all division by zero
        if (app.rayDirX == 0):    deltaDistY = 0
        elif (app.rayDirY == 0):  deltaDistY = 1
        else:                 deltaDistY = abs(1 / app.rayDirY)

        #stepX/Y = direction to step in x or y-direction (+1 or -1)
        #sideDistX/Y = length of ray from current position to next x or y side
        if app.rayDirX < 0: 
            stepDirX = -1 #facing (-) dir -> step dir is (-)
            sideDistX = (pRow - rayMapRow) * deltaDistX 
        else: 
            stepDirX = 1 #facing (+) dir -> step dir is (+)
            sideDistX = (rayMapRow + 1 - pRow) * deltaDistX 
        if app.rayDirY < 0: 
            stepDirY = -1 #facing (-) dir -> step dir is (-)
            sideDistY = (pCol - rayMapCol) * deltaDistY 
        else: 
            stepDirY = 1 #facing (+) dir -> step dir is (+)
            sideDistY = (rayMapCol + 1 - pCol) * deltaDistY 


        ''' Perform DDA Algorithm:'''
        #basically, the adding variables here is extending the ray out
            #in the simulated 3d space. So, the ray will continue to extend
            #until it hits a wall. Then we can get the distance and position to 
            #that wall in relation to the player's position.

        hitWall = False
        while not hitWall:
            #jump to next map square by adding distances in x or y direction 
            if sideDistX < sideDistY: #then use graph side = 0 (left side)
                sideDistX += deltaDistX
                rayMapRow += stepDirX
                side = 0
            else: #then use graph side = 1 (right side)
                sideDistY += deltaDistY
                rayMapCol += stepDirY
                side = 1
            
            '''AI RAYCASTING : check if ray in ai position, if so,save dist'''
            #check if in ai cell
            for ai in app.allAIs:

                #get cell for ray - rayMapRow,rayMapCol
                if ai.isRayRowColInAiPosition(app,x,rayMapRow,rayMapCol)[0]:
                    
                    y = ai.isRayRowColInAiPosition(app,x,rayMapRow,rayMapCol)[1]
                    if side == 0:
                        distToAi = (rayMapRow-pRow+(1-stepDirX)/2) / app.rayDirX
                    else:
                        distToAi = (rayMapCol-pCol+(1-stepDirY)/2) / app.rayDirY 
                    if distToAi == 0:
                        distToAi = 0.01
                     

                    app.aiXDistDict[ai] = (x, y, distToAi)


            #check if ray has hit a wall!
            if app.worldMap[rayMapRow][rayMapCol] > 0:
                hitWall = True
        
        '''DDA done, now get distance of ray to the wall:'''
        #distToWall, is perpendicular distance from wall to player's 
            #camera plane -- this avoids a fisheye effect
        if side == 0:
            distToWall = (rayMapRow - pRow + (1 - stepDirX) / 2) / app.rayDirX
        else:
            distToWall = (rayMapCol - pCol + (1 - stepDirY) / 2) / app.rayDirY

        '''Now, get height of wall:'''
        #the wall height = inverse of the distance to wall
            #then multiply by app.height (height in px of screen) to 
            #convert the units to pixels

        if distToWall == 0:
            distToWall = 0.01
        wallHeightInPx = app.height // distToWall

        '''Need lowest/highest points (in px) of wall for drawing:'''
        wallBottomInPx = -wallHeightInPx / 2 + app.height / 2
        if wallBottomInPx < 0:
            wallBottomInPx = 0
        
        wallTopInPx = wallHeightInPx / 2 + app.height / 2
        if wallTopInPx >= app.height:
            wallTopInPx = app.height - 1
    


        '''Get color for wall:'''
        #darken certain walls for shadows

        if side == 0: #unshaded
            colorsDict = {
                            1: 'gray', #hallways
                            2: 'gold', #task
                            22: 'yellow', #near task
                            3: 'blue', #security
                            4: 'orange', #cafe & electrical
                            5: 'firebrick', #weapons
                            6: 'turquoise', #O2, medbay
                            7: 'slate blue', #nav, reactor, & admin
                            8: 'goldenrod', #shields
                            9: 'light sky blue', #comms
                            10: 'medium sea green', #storage
                            12: 'light pink', #engines
                         }
            color = colorsDict.get(app.worldMap[rayMapRow][rayMapCol],
                            "invalid_wall_color")
        else: #shaded (shadows)
            shadedColorsDict = {
                                1: 'dim gray', #hallways
                                2: 'gold', #task 
                                22: 'yellow', #near task
                                3: 'medium blue', #security
                                4: 'dark orange', #cafe & electrical
                                5: 'dark red', #weapons
                                6: 'dark turquoise', #O2, medbay
                                7: 'dark slate blue', #nav, reactor, & admin
                                8: 'dark goldenrod', #shields
                                9: 'sky blue', #comms
                                10: 'seagreen', #storage
                                12: 'pink', #engines

                               }
            color = shadedColorsDict.get(app.worldMap[rayMapRow][rayMapCol],
                            "invalid_wall_color")
        
        '''Finally, put what learned into list'''
        app.vertLineDimensions[x] = (wallBottomInPx, wallTopInPx, 
                                                color, distToWall)

    #### END OF vert lines FUNCTION

#AI RAYCASTING helper/sorting aspect
def sortAndGetHeightAIRayCasting(app):
    # Note: While I referenced https://lodev.org/cgtutor/raycasting.html for
        #CONCEPTUAL, I ONLY USED THE CONCEPTUAL and figured out the entire ray
            #casting sprites ON MY OWN. This source only provided conceptual
            #how ray casting sprites works, I learned how it works, and then 
            #figured out how to implement it.
    
    
    app.sortedAiDistList = []
    app.sortedAiDistListPlusExtra = []
    for ai in app.aiXDistDict:
        x, y, distToAi = app.aiXDistDict.get(ai)
        app.sortedAiDistList.append(distToAi)


    #SORT AI sprites from FAR to CLOSE, looked in python documentation for 
                            # reverse parameter
    app.sortedAiDistList.sort(reverse=True) #sorts & reverses

    for ai in app.aiXDistDict:
        for distToAi in app.sortedAiDistList:
            x, y, distToAi = app.aiXDistDict.get(ai)
            app.sortedAiDistListPlusExtra.append((ai,x,y,distToAi))

    '''alternate method i was close to implementing:'''
    #set player values to local variables for clarity
    # pX = app.player.getRow()
    # pY = app.player.getCol()
    # pDirX, pDirY = app.player.getDirRow(), app.player.getDirCol()
    # pPlaneX = app.player.getFovPlaneX()
    # pPlaneY = app.player.getFovPlaneY()
    
    #get height
    #draw height, 
    
    #after sorting ais, do projection
    # for ai in app.sortedAiDistList: #O(N) 
    #     ai,x,distToAi = app.aiRowColDistDict.get(distToAi)
        #translate ai viewed position to player plane perspective
        # aiX = aiRow #change local name to match my other variable formats,x/y
        # aiY = aiCol 
        # aiX -= pX #might have to flip these
        # aiY -= pY

        #transform ai sprite position relative to camera
        #multiply^ with inverse of 2x2 camera matrix to put in camera perspective
        #USED https://www.youtube.com/watch?v=y4B_EC5MNS8&feature=emb_logo 
            #and https://www.youtube.com/watch?v=IKFlUVIDOWQ 
            # to learn inverse matrices & multiplication of 2x2 matrices
        #orig matrix =  [ pPlaneX  pDirX]
        #               [ pPlaneY  pDirY], so I take inverse of this:
        #origMDeterminant = abs(pPlaneX*pDirY - pPlaneY*pDirX)
        #inverse Matrix formula = (1/origMDeterminant) * [pDirY -pPlaneY]
        #                                                   [-pDirX pPlaneX]
        #knowing above: transform sprite pos ^ using inverse matrix:
        #just like player movement, I must do both x and y for ai
        #I use ai's x: aiX, instead of the player's plane because 
            #im transforming it from player to ai plane, for x: use formula:
        #aiTransformedX = (1/origMDeterminant) * (aiX*pDirY - ((aiY)*(pDirX)))
        # for y (which is simulated z depth on 2d screen), we do same thing
            #with formula but replacing pDirY with plane,need plane for depth
        #aiTransformedY = (1/origMDeterminant) * (pPlaneX*aiY - ((pPlaneY)*(aiX)))
        
        #print(aiTransformedX, aiTransformedY)
        #transformedYDict[distToAi] = aiTransformedY
        #project onto screen
        #raycasting source explains conceptual idea that in order to project 
            #anything onto raycasted screen, you divide x through depth & 
            #translate/scale it so its in pixel coordinates
        #so, here I used the transformed x & transformed y (zdepth) to get new X
            #for screen
        # aiScreenX = (aiTransformedX+1) / aiTransformedY
        # aiScreenX *= app.width/                         2 #translate to pixel
        # #to use for image, dont have floats (like below):
        # aiScreenX = int(aiScreenX)

        # #calculate height of the ai 
        # aiHeight = 1+app.height / aiTransformedY #just height over y
        #     #realized need to make height int for creating image:
        # aiHeight = abs(int(aiHeight))
        # aiWidth = aiHeight #width same as height

        # #for image creation, we need cx and cy, translate into pixel
        # aiImageX0,aiImageY0 = aiScreenX - aiWidth/2, app.height/2 - aiHeight/2
        # aiImageX1, aiImageY1 = aiScreenX + aiWidth/2, app.height/2 + aiHeight/2
        
        # aiImageCx, aiImageCy = (aiImageX0+aiImageX1)/2, (aiImageY0+aiImageY1)/2
        # #print(aiImageCx,aiImageCy)
        # #give image cx & cy to ai for drawing
        # ai.setAiImageCx(aiScreenX)
        # ai.setAiImageCy(aiImageCy)
        # #print('here')
        # # ai.setImageX0X1(aiImageX0,aiImageX1)
        # # ai.setImageY0Y1(aiImageY0,aiImageY1)
        # #give image height & width to ai for drawing
        # ai.setAiImageHeight(aiHeight)
        # ai.setAiImageWidth(aiWidth)
        # #ai.setTransformedY(aiTransformedY)
        # #print('calculated')
        # #app.aiTransformedY = aiTransformedY

#pathagorean theorem
def getEuclideanDistanceFromPlayer(app, aiRow, aiCol):
    pRow,pCol = app.player.getRow(), app.player.getCol()
    xLength = abs(aiCol-pCol)
    yLength = abs(aiRow-pRow)
    
    #pathagorean theorem
    dist = math.sqrt((xLength**2) + (yLength**2))
    return dist


################################################################################
# CONTROLLERS:
################################################################################
#responds to mousePressed event
def mousePressed(app, event):
    if app.drawingATitleScreen: #drawing title screen
        #main title
        if app.drawingMainTitleScreen: #main title screen
            if isClickInSinglePlayerButton(app, event.x, event.y):
                app.mySounds.playButtonClickSound()
                app.drawingMainTitleScreen = False
                app.drawingSinglePlayerScreen = True
            #elif click in multiplayer button
                #mainScreen = false
                #multiplayerScreen = true
        elif app.drawingSinglePlayerScreen: #single player screen
            if isClickInSPPlayButton(app, event.x, event.y): 
                app.mySounds.playButtonClickSound()
                app.drawingSinglePlayerScreen = False
                app.drawingATitleScreen = False #start game
                setUpSinglePlayer(app) 
                setUpVotingWindowAtStartAndHide(app)
                app.mySounds.stopIfPlayingMainTitleScreenMusic() # stop title music
                app.mySounds.playGameMusic()
                
                #moveAIs(app)
            elif isClickInConfigureSPButton(app, event.x, event.y):
                app.mySounds.playButtonClickSound()
                app.drawingTkSpConfigWindow = True

        elif app.drawingCrewWinScreen or app.drawingImpWinScreen:
            if isClickInPlayAgainButton(app, event.x, event.y):
                appStarted(app) #prob gonna have to clear way more than this
                #app.drawingATitleScreen = True
        elif app.drawingVotingScreen:
            if app.showingVotes == False:
                if isClickInVoteButton(app, event.x, event.y):
                    app.runningVoteTkWindow = not app.runningVoteTkWindow

    else: #not drawing title screen
        
        if app.player.getIsPromptingReport() and app.playerReported == False:
                #if near dead body bool here & prompt report
                if isClickInReportButton(app, event.x, event.y):
                        app.mySounds.playReportSound()
                        app.playerReported = True
                        app.getStartTimeReportedScreen = True
        #CREWMATE:
        if app.player.getImpStatus() == 'crewmate': 
            if app.player.getIsPromptingUse(): #if can click use button
                if isClickInUseButton(app, event.x, event.y):
                    currBool = app.player.getIsDoingTask()
                    app.player.setIsDoingTask(not currBool) #toggle
            
            #TASKS:
            #wires task:
            if app.player.getIsDoingWiresTask():
                #check what start wire player clicks in:
                if app.currWiresTaskObj.isClickInFirstWireStart(event.x, event.y):
                    app.currWiresTaskObj.setDrawingFirstWire(True)
                    app.wiresFirstCurrMouseX = event.x + 20
                    app.wiresFirstCurrMouseY = event.y 
                elif app.currWiresTaskObj.isClickInSecondWireStart(event.x, event.y):
                    app.currWiresTaskObj.setDrawingSecondWire(True)
                    app.wiresSecondCurrMouseX = event.x + 20
                    app.wiresSecondCurrMouseY = event.y
                elif app.currWiresTaskObj.isClickInThirdWireStart(event.x, event.y):
                    app.currWiresTaskObj.setDrawingThirdWire(True)
                    app.wiresThirdCurrMouseX = event.x + 20
                    app.wiresThirdCurrMouseY = event.y
                elif app.currWiresTaskObj.isClickInFourthWireStart(event.x, event.y):
                    app.currWiresTaskObj.setDrawingFourthWire(True)
                    app.wiresFourthCurrMouseX = event.x + 20
                    app.wiresFourthCurrMouseY = event.y

        elif app.player.getImpStatus() == 'imposter':
            if app.player.getIsPromptingKill():
                if isClickInKillButton(app, event.x, event.y):
                    app.player.setIsKilling(True)
                    app.mySounds.playKillSound()

                
#responds to mouseDragged event
def mouseDragged(app, event):
    #wires task:
    if not app.drawingATitleScreen:
        if app.player.getImpStatus() == 'crewmate':
            if app.player.getIsDoingWiresTask(): #crewmate doing wires
                if app.currWiresTaskObj.getDrawingFirstWire():
                    app.wiresFirstCurrMouseX = event.x
                    app.wiresFirstCurrMouseY = event.y
                if app.currWiresTaskObj.getDrawingSecondWire():
                    app.wiresSecondCurrMouseX = event.x
                    app.wiresSecondCurrMouseY = event.y
                if app.currWiresTaskObj.getDrawingThirdWire():
                    app.wiresThirdCurrMouseX = event.x
                    app.wiresThirdCurrMouseY = event.y
                if app.currWiresTaskObj.getDrawingFourthWire():
                    app.wiresFourthCurrMouseX = event.x
                    app.wiresFourthCurrMouseY = event.y


#responds to mouseReleased event
def mouseReleased(app, event):
    if not app.drawingATitleScreen:
        if app.player.getImpStatus() == 'crewmate' and app.player.getIsAlive():
                #wires task:
            if app.player.getIsDoingWiresTask(): 
                #check what end wire player releases in:
                if app.currWiresTaskObj.getDrawingFirstWire():
                    app.currWiresTaskObj.checkSetFirstOnCorrectEndWire(event.x, event.y)
                    if app.currWiresTaskObj.isAllWiresCompleted():
                        app.numTasksCompleted += 1
                        app.player.addOneToNumWiresTasksCompleted()
                elif app.currWiresTaskObj.getDrawingSecondWire():
                    app.currWiresTaskObj.checkSetSecondOnCorrectEndWire(event.x, event.y)
                    if app.currWiresTaskObj.isAllWiresCompleted():
                        app.numTasksCompleted += 1
                        app.player.addOneToNumWiresTasksCompleted()
                elif app.currWiresTaskObj.getDrawingThirdWire():
                    app.currWiresTaskObj.checkSetThirdOnCorrectEndWire(event.x, event.y)
                    if app.currWiresTaskObj.isAllWiresCompleted():
                        app.numTasksCompleted += 1
                        app.player.addOneToNumWiresTasksCompleted()
                elif app.currWiresTaskObj.getDrawingFourthWire():
                    app.currWiresTaskObj.checkSetFourthOnCorrectEndWire(event.x, event.y)
                    if app.currWiresTaskObj.isAllWiresCompleted():
                        app.numTasksCompleted += 1
                        app.player.addOneToNumWiresTasksCompleted()

    
    

#responds to keyPressed event
def keyPressed(app, event):
    if not app.drawingATitleScreen: #and app.player.getIsAlive():
        # if event.key == 't': #TESTING TELEPORT/vent IDEA - works
        #     app.player.row = 8
        #     app.player.col = 10
        if event.key == 'Tab': #hold to open map
            app.isMapOpen = True
        if app.isMapOpen:
            if event.key == 'v': #view ai's on the map
                app.playerViewAIsOnMap = not app.playerViewAIsOnMap
        #player movement:
        if app.player.getIsAlive():
            if event.key == 'w' or event.key == 'Up':
                app.player.setIsMovingForward(True) 
            elif event.key == 's' or event.key == 'Down':
                app.player.setIsMovingBackward(True) 
        if event.key == 'a' or event.key == 'Left':
            app.player.setIsRotatingLeft(True) 
        elif event.key == 'd' or event.key == 'Right':
            app.player.setIsRotatingRight(True) 

#responds to keyReleased event
def keyReleased(app, event):
    if not app.drawingATitleScreen:
        if event.key == 'Tab': #release to close map
            app.isMapOpen = False

        #player movement:
        if app.player.getIsAlive():
            if event.key == 'w' or event.key == 'Up':
                app.player.setIsMovingForward(False) 
            elif event.key == 's' or event.key == 'Down':
                app.player.setIsMovingBackward(False) 
        if event.key == 'a' or event.key == 'Left':
            app.player.setIsRotatingLeft(False) 
        elif event.key == 'd' or event.key == 'Right':
            app.player.setIsRotatingRight(False) 

#called every tick/timerFired
def timerFired(app):
    app.drawingTimerCount += 1
    if not app.drawingATitleScreen: #not drawing title screen
        #raycasting
        setVertLinesDimensionsAlgorithm(app) #sets app.vertLineDimensions each frame
        #updateDistanceToAIsDict(app)
      
        sortAndGetHeightAIRayCasting(app)

        #player movement (workaround for unsupported multi-key press):
        if app.player.getIsMovingForward(): app.player.moveForward(app.worldMap)
        if app.player.getIsMovingBackward(): app.player.moveBackward(app.worldMap)
        if app.player.getIsRotatingLeft(): app.player.rotateLeft()
        if app.player.getIsRotatingRight(): app.player.rotateRight()
        
        #gameplay
        # if app.player.isPlayerOnVent(): #check if player on vent
        #     app.promptVent = True
        # else:
        #     app.promptVent = False
        
        #Player CREWMATE
        if app.player.getImpStatus() == 'crewmate':
            if app.player.getIsAlive() == False: # if dead
                app.drawingPlayerDiedText = True
                app.player.setIsMovingForward(False)
                app.player.setIsMovingBackward(False)
            else:
                app.drawingPlayerDiedText = False

            #use/report buttons
            setPlayerReportButtonDimensions(app)
            setPlayerUseButtonDimensions(app)
            #REPORTING
            if playerIsNearDeadBody(app)[0] and app.player.getIsAlive():
                app.player.setIsPromptingReport(True)
            else:
                app.player.setIsPromptingReport(False)

                # app.deadColor = playerIsNearDeadBody(app)[1]
                # app.deadLocation = playerIsNearDeadBody(app)[2]
            #TASKS:
            #wires
            if app.player.isPlayerNearWiresTask()[0]: #for multi, loop through each player
                app.player.setIsPromptingUse(True) #prompt if near
                #if actually doing wires task:
                if app.player.getIsDoingTask():
                    currWiresLocation = app.player.isPlayerNearWiresTask()[1]
                    app.player.setCurrTask('wires')
                    app.player.setCurrTaskLocation(currWiresLocation)
                    app.player.setIsDoingWiresTask(True)
                    #get current wiresTask object:
                        #should prob convert this to inside player obj for multi
                    app.currWiresTaskObj = getWiresTaskObjectFromLocation(app, currWiresLocation)
                    
                    #setup current wireTask start/end buttons:
                    app.currWiresTaskObj.setWireStartButtonsDimensions() 
                    app.currWiresTaskObj.setWireEndButtonsDimensions() 

            #will need to do elifs for other tasks here
            
            else: #not near any tasks 
                app.player.setCurrTask(None)
                app.player.setCurrTaskLocation(None)
                app.player.setIsPromptingUse(False)
                app.player.setIsDoingTask(False)
                app.player.setIsDoingWiresTask(False)
                #app.currWiresTaskObj = None        
        
        #player IMPOSTER
        elif app.player.getImpStatus() == 'imposter':
            if playerIsNearDeadBody(app)[0]:
                app.player.setIsPromptingReport(True)
            else:
                app.player.setIsPromptingReport(False)
            if isPlayerImposterNearAliveAI(app)[0] == True:# and 
                #app.killCoolDownCurrTime == 0:
                app.player.setIsPromptingKill(True)
                if app.player.getIsKilling():
                    app.mySounds.playKillSound()
                    deadAi = isPlayerImposterNearAliveAI(app)[1]
                    deadAi.setIsAlive(False)
                    deadAi.setIsMoving(False)
                    deadAiRow,deadAiCol = deadAi.getRow(),deadAi.getCol()
                    #killingTimerCount = 0 #play sound using this method, to stop lag
                    deadAiColor = deadAi.getColor()
                    app.deadBodyLocations.append((deadAiColor,deadAiRow,
                                                    deadAiCol))#,deadAiLoc))
                    #app.numTaskBarCols -= 1 * app.numTasks #change tasks when kill somehow
                    #ejectPlayer(app, deadAi)
                    app.player.setIsKilling(False)
                    app.player.setIsPromptingKill(False)
            else:
                app.player.setIsPromptingKill(False)
                # if app.isGetStartAiTaskTime == True: #KILL COOLDOWN STUFF
                #         print('got start time')
                #         app.startAiTaskTime = time.time()
                #         app.isGetStartAiTaskTime = False

        #if report happened
        app.reportWaitTimeCount += 1      
        if app.aiReported:
            #app.drawingATitleScreen = True
            app.drawingReportingScreen = True
            reportMoveEveryone(app)
            if app.reportWaitTimeCount % 30 == 0:
                app.drawingReportingScreen = False
                app.drawingATitleScreen = True
                app.drawingVotingScreen = True             
                app.aiReported = False
        elif app.playerReported:
            app.drawingReportingScreen = True
            reportMoveEveryone(app)
            if app.reportWaitTimeCount % 30 == 0:
                app.drawingReportingScreen = False
                app.drawingATitleScreen = True
                app.drawingVotingScreen = True              
                app.playerReported = False
        # if app.drawingReportingScreen: 
        #     if app.getStartTimeReportedScreen:
        #         app.startReportingTime = time.time()
        #         app.getStartTimeReportedScreen = False
        #     if time.time() - app.startReportingTime > 2:
        #         app.drawingReportingScreen = False
        #         app.drawingReportingScreen = False

        # AIs
        for ai in app.allAIs:
            
            #AI CREWMATE
            if ai.getImpStatus() == 'crewmate':
                if ai.getIsMoving(): #if is moving (not in a meeting)
                    app.timerCount += 1 #timer for ai fps movement
                    
                    if (isAICrewNearDeadBody(app,ai)[0] and ai.getIsAlive() and
                        app.aiReported == False):
                        closestPerson = isAICrewNearDeadBody(app,ai)[1]
                        ai.setPersonVotingFor(closestPerson)
                        app.timerVotingFor = True
                        if app.timerVotingFor:
                            if ai.getPersonVotingFor() != None:
                                personVotingFor = ai.getPersonVotingFor()
                                if personVotingFor == 'player':
                                    personVotingFor = app.player
                                #print(personVotingFor)
                                personVotingFor.addOneNumSelfVotes()
                            app.timerVotingFor = False
                        if closestPerson == 'player':
                            app.player.addOneNumSelfVotes()
                        else:
                            closestPerson.addOneNumSelfVotes()
                        #ai.setIsReporting(True)
                        
                        if app.timerCount % 60 == 0: #wait a bit before reporting
                            app.mySounds.playReportSound()
                            app.aiReported = True
                        #ai.setIsMoving(False)

                    if app.aiReported == False:
                        #tasks:
                        if (ai.isAtVertex()[0] and ai.getIsAllTasksCompleted() == False 
                        and ai.getShouldFindNewTaskNow()):
                            #app.taskTimerCount = 0
                            # if ai.getNextTask() != None: #theres a prev task set
                            #     #mark prev task complete
                            #     ai.markNextTaskComplete()
                            #set next random task
                            ai.setCurrTaskRandomly() #set task
                            ai.setIsSettingCurrTaskPath(True)
                            ai.setIsGoingToCurrTask(True)
                            ai.setShouldFindNewTaskNow(False)
                            #print('found new task') #these prints are helpful
                        if ai.getIsSettingCurrTaskPath(): #if setting current path
                            ai.setCurrTaskPath() #set path
                            ai.setIsSettingCurrEndVertex(True)
                            ai.setIsSettingCurrTaskPath(False)
                            #print('set current task path')
                        if ai.getIsGoingToCurrTask(): #is going to curr task
                            if ai.getIsSettingCurrEndVertex(): #if setting new curr end vertex
                                ai.setCurrEndVertex() #set curr end vertex
                                ai.setIsSettingCurrEndVertex(False)
                                #print('set current end vertex')
                            if app.timerCount % ai.getCrewSpeed() == 0: #speed = 15 fps
                                if ai.getCurrTask() != None: #theres a task set to go to
                                    ai.doStep_TowardsCurrEndVertex() #move ai one step
                                    #print('**stepped towards end vertex**')
                                    #print('\t\t\t',ai.getRow(), ai.getCol())
                            if ai.getArrivedAtCurrEndVertex(): #arrived at curr end vertex
                                ai.markCurrEndVertexReached()
                                if ai.checkIfArrivedAtCurrTask() == True:#
                                    #print('arrived at current task')
                                    ai.setArrivedAtCurrTask(True)
                                    app.isGetStartAiTaskTime = True
                                else:
                                    #print('set new end vertex')
                                    ai.setIsSettingCurrEndVertex(True) #set new one
                                ai.setArrivedAtCurrEndVertex(False)
                                #print('arrived at current end vertex')
                        if ai.getArrivedAtCurrTask(): #arrived at task
                            #print('in here')
                            #app.GetStartAiTaskTime = True
                            if app.isGetStartAiTaskTime == True:
                                #print('got start time')
                                app.startAiTaskTime = time.time()
                                app.isGetStartAiTaskTime = False
                            ai.setIsGoingToCurrTask(False)
                            #startTime = time.time()
                            #print(app.startAiTaskTime, time.time())
                            if time.time() - app.startAiTaskTime > 5: #wait 5 seconds at task
                                #mark completed task and find new task
                                #if hard mode, go to random spot
                                
                                #print('done waiting')
                                ai.markCurrTaskComplete()
                                #ai.setShouldFindNewTaskNow(True)
                                if ai.checkIfAllTasksCompleted() == True:
                                    ai.setIsAllTasksCompleted(True)
                                    app.isGetStartAiTaskTime = False
                                else:
                                    #print('should find new task')
                                    ai.setShouldFindNewTaskNow(True)
                                    app.isGetStartAiTaskTime = False

                                ai.addOneToNumTasksCompleted()#add one to task count
                                app.numTasksCompleted += 1#add one to overall count
                                ai.setArrivedAtCurrTask(False)
                                #ai.setShouldFindNewTaskNow(False)
                        if ai.getIsAllTasksCompleted():
                            #go back and wait in original spot in cafe
                            ai.setIsMoving(False)
                            ai.setRow(ai.getInitialRow())
                            ai.setCol(ai.getInitialCol())
                            #print('all tasks completed')
                            #or can have random chance of searching for bodies
                    
            elif ai.getImpStatus() == 'imposter':
                if ai.getIsMoving():
                    app.IMPTimerCount += 1
                    app.changeDecisionTimerCount += 1
                    #note: imposter fakes tasks at start of game to avoid suspicion
                    #decides if hunting or faking every little while:
                    if app.changeDecisionTimerCount % 80 == 0:
                        ai.setHuntingOrFaking()#random chance
                    
                    #if near dead body, decide if self report or not
                    if app.IMPTimerCount % 150 == 0:
                        app.impReportTimeDone = True
                    if isAIImpNearDeadBody(app, ai)[0] and app.impReportTimeDone:
                        if isAIImpNearDeadBody(app, ai)[3] < 10: #distToNearPerson
                            chanceOfSelfReport = random.randint(1,6) #1/6 chance if close
                            if chanceOfSelfReport == 1:
                                closestPerson = isAICrewNearDeadBody(app,ai)[1]
                                ai.setPersonVotingFor(closestPerson)
                                if closestPerson == 'player':
                                    app.player.addOneNumSelfVotes()
                                else:
                                    closestPerson.addOneNumSelfVotes()
                                if app.IMPTimerCount % 60 == 0: #wait a bit before reporting
                                    app.aiReported = True
                                    app.mySounds.playReportSound()
                                    app.impReportTimeDone = False
                    
                    #actions for hunting players
                    if ai.getIsHunting():   
                        #hunt closest players and kill

                        if app.IMPTimerCount % 125 == 0:
                            app.killCoolDownDone = True

                        nearestPerson,nearDist = getNearestAlivePerson(app, ai)
                        if nearestPerson != None and nearDist != None:
                            if nearestPerson == 'player':
                                nearestPerson = app.player
                                goalRow = app.player.getRow()
                                goalCol = app.player.getCol()
                            else: #its an ai
                                #for closeAi in app.allAIs:
                                    #if closeAi.getName() == nearestPerson:
                                goalRow = nearestPerson.getRow()
                                goalCol = nearestPerson.getCol()
                                #nearestPerson = closeAi
                            #move/step toward player  
                            if app.IMPTimerCount % ai.getImpSpeed() == 0:          
                                ai.doStep_MoveThroughGridTowardRowCol(goalRow,goalCol)

                            #check if close enough to kill - kill if close
                            if (nearDist <= app.distToKill and 
                                app.killCoolDownDone): 
                                #kill that person
                                
                                app.mySounds.playKillSound()
                                nearestPerson.setIsAlive(False)
                                nearestPerson.setIsMoving(False)
                                nearestPersonRow = nearestPerson.getRow()
                                nearestPersonCol = nearestPerson.getCol()
                                nearestPersonColor = nearestPerson.getColor()
                                app.deadBodyLocations.append((nearestPersonColor,
                                        nearestPersonRow,nearestPersonCol))
                                #ejectPlayer(app, nearestPerson)
                                app.killCoolDownDone = False

                        
                    #actions for faking tasks
                    elif ai.getIsFaking():
                        #print('IMPOSTER IS FAKING')
                        if (ai.isAtVertex()[0] and ai.getShouldFindNewFakeTaskNow()):
                            #app.taskTimerCount = 0
                            # if ai.getNextTask() != None: #theres a prev task set
                            #     #mark prev task complete
                            #     ai.markNextTaskComplete()
                            #set next random task
                            ai.setCurrTaskRandomly() #set task
                            ai.setIsSettingCurrTaskPath(True)
                            ai.setIsGoingToCurrTask(True)
                            ai.setShouldFindNewFakeTaskNow(False)
                            #print('imp: found new fake task') #prints are helful
                        if ai.getIsSettingCurrTaskPath(): #if setting current path
                            ai.setCurrTaskPath() #set path
                            ai.setIsSettingCurrEndVertex(True)
                            ai.setIsSettingCurrTaskPath(False)
                            #print('imp: set current fake task path')
                        if ai.getIsGoingToCurrTask(): #is going to curr task
                            if ai.getIsSettingCurrEndVertex(): #if setting new curr end vertex
                                ai.setCurrEndVertex() #set curr end vertex
                                ai.setIsSettingCurrEndVertex(False)
                                #print('imp: set current end vertex')
                            if app.IMPTimerCount % ai.getImpSpeed() == 0: #speed = 15 fps
                                if ai.getCurrTask() != None: #theres a task set to go to
                                    ai.doStep_TowardsCurrEndVertex() #move ai one step
                                    #print('imp: **stepped towards end vertex**')
                                    #print('\t\t\t',ai.getRow(), ai.getCol())
                            if ai.getArrivedAtCurrEndVertex(): #arrived at curr end vertex
                                ai.markCurrEndVertexReached()
                                if ai.checkIfArrivedAtCurrTask() == True:#
                                    #print('imp: arrived at current fake task')
                                    ai.setArrivedAtCurrTask(True)
                                    app.isIMPGetStartAiTaskTime = True
                                else:
                                    #print('imp: set new end vertex')
                                    ai.setIsSettingCurrEndVertex(True) #set new one
                                ai.setArrivedAtCurrEndVertex(False)
                                #print('imp: arrived at current end vertex')
                        if ai.getArrivedAtCurrTask(): #arrived at task
                            #print('in here')
                            #app.GetStartAiTaskTime = True
                            if app.isIMPGetStartAiTaskTime == True:
                                #print('imp: got start time')
                                app.startIMPAiTaskTime = time.time()
                                app.isIMPGetStartAiTaskTime = False
                            ai.setIsGoingToCurrTask(False)
                            #startTime = time.time()
                            #print(app.startIMPAiTaskTime, time.time())
                            if time.time() - app.startIMPAiTaskTime > 5: #wait 5 seconds at task
                                #mark completed task and find new task
                                #if hard mode, go to random spot
                                
                                #print('imp: done waiting')
                              
                                # else:
                                #print('imp: should find new fake task')
                                ai.setShouldFindNewFakeTaskNow(True)
                                app.isIMPGetStartAiTaskTime = False

                                #ai.addOneToNumTasksCompleted()#add one to task count
                                #app.numTasksCompleted += 1#add one to overall count
                                ai.setArrivedAtCurrTask(False)
                                #ai.setShouldFindNewTaskNow(False)
                        # if ai.getIsAllTasksCompleted():
                        #     #go back and wait in original spot in cafe
                        #     ai.setIsMoving(False)
                        #     ai.setRow(ai.getInitialRow())
                        #     ai.setCol(ai.getInitialCol())
                        #     print('all tasks completed')
                            #or can have random chance of searching for bodies

                        

                  
                    

        #test if people won:
        if app.numTasksCompleted >= app.numTaskBarCols: #crewmate win
            #print('CREWMATES WIN!') #draw win screen here
            app.drawingCrewWinScreen = True
            app.drawingATitleScreen = True
        elif len(app.deadBodyLocations) == (app.numPlayers + app.numAIs)-1:
            #print('IMPOSTER WINS!') #draw win screen
            app.drawingImpWinScreen = True
            app.drawingATitleScreen = True
            

    else: #a title screen is being drawn
        playScreenStarEffect(app)
        if app.drawingMainTitleScreen:
            setSinglePlayerButtonDimensions(app)
        if app.drawingSinglePlayerScreen:
            setConfigSPButtonDimensions(app)
            setSPPlayButtonDimensions(app)
            if app.drawingTkSpConfigWindow:
                runSPConfigWindow(app)
        if app.drawingCrewWinScreen or app.drawingImpWinScreen:
            pass
        if app.drawingVotingScreen:
            if app.showingVotes:
                # if app.boolVal:
                #     if app.player.getIsAlive():
                        
                findLargestVotes(app)

                if time.time() - app.voteWaitTimer > 5:
                    app.drawingVotingScreen = False
                    app.drawingEjectedScreen = True
                    app.ejectedWaitTimer = time.time()
                    app.showingVotes = False
            else: #not showing votes
                if app.runningVoteTkWindow:
                    runVoteWindow(app)
        if app.drawingEjectedScreen:
            if time.time() - app.ejectedWaitTimer > 3:
                if app.mostVotedPlayer.getImpStatus() == 'imposter':
                    ejectPlayer(app, app.mostVotedPlayer)
                    app.drawingEjectedScreen = False
                    app.drawingCrewWinScreen = True
                else:
                    ejectPlayer(app, app.mostVotedPlayer) 
                    app.drawingEjectedScreen = False
                    app.drawingATitleScreen = False
                
                
            #setPlayAgainButtonDimensions(app)
            #if clicked in mouse pressed (calls appstarted & rests game)

def ejectPlayer(app, player):
    player.setIsAlive(False)
    app.deadBodyLocations.append((player.getColor(),player.getRow(),
                                    player.getCol()))
    # if player in app.allAIs:
    #     app.allAIs.remove(player)
    
################################################################################
# DRAWING:
################################################################################

#returns the x0,y0,x1,y1 of a given row,col & margin
#source: 112 website, I modified it partially for my use.
    #https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getCellBounds(app, row, col, margin): 
    gridWidth = app.width - 2*margin
    gridHeight = app.height - 2*margin
    cellWidth = gridWidth / app.mapCols
    cellHeight = gridHeight / app.mapRows

    x0 = margin + cellWidth * col
    y0 = margin + cellHeight * row
    x1 = margin + cellWidth * (col+1)
    y1 = margin + cellHeight * (row+1)
    return x0,y0,x1,y1

#returns the row,col of a given x,y & margin
#source: 112 website, I modified it partially for my use.
    #https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html#exampleGrids
def getCell(app, x, y, margin):
    gridWidth = app.width - 2*margin
    gridHeight = app.height - 2*margin
    cellWidth = gridWidth / app.mapCols
    cellHeight = gridHeight / app.mapRows

    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)

#ceiling and floor, not raycasted (I tried to raycast, but tkinter couldnt handle it)
def drawCeilingAndFloor(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height/2, fill="black")
    canvas.create_rectangle(0,app.height/2,app.width,app.height,
                                fill="silver")
    
#draws each verticle line (draws the raycasting effect)
def drawVertLines(app, canvas):
    #loop through dictionary of x's
    for x in app.vertLineDimensions: 
        lowerY, upperY, color, distToWall = app.vertLineDimensions[x]
        canvas.create_line(x, lowerY, x, upperY, fill=color)

#draws the vent text prompt
def drawVentPrompt(app, canvas):
    canvas.create_text(app.width//2, app.height//2, 
                        text="Enter vent?", font="Helvetica, 30 bold")

#draws player circle on map
def drawPlayerOnMap(app, canvas):
    #app.player = (Player(color, startRow, startCol, 
     #                   faceDirectionX, faceDirectionY))
    pRowX = app.player.getRow()
    pColY = app.player.getCol()
    r = app.mapCircleRadius
    pCx, pCy = app.player.findCxAndCy(app, app.mapMargin)
    # margin = app.mapMargin
    # x0,y0,x1,y1 = getCellBounds(app, pRowX, pColY, margin)
    # pCx = (x0+x1) / 2
    # pCy = (y0+y1) / 2

    color = app.player.getColor() 
    canvas.create_oval(pCx-r, pCy-r, pCx+r, pCy+r, fill=color)


    pDirRowX = app.player.getDirRow()
    pDirColY = app.player.getDirCol()
    pPlaneX = app.player.getFovPlaneX()
    pPlaneY = app.player.getFovPlaneY()

    #center line
    x = app.width//2
    midCameraX = (2*x) / app.width-1 #x-coordinate on camera plane (-1 to 1 ish) 
    midRayDirX = pDirColY + pPlaneX * midCameraX
    midRayDirY = pDirRowX + pPlaneY * midCameraX
    centerX = pCx + 20*midRayDirX   
    centerY = pCy + 20*midRayDirY
    canvas.create_line(pCx, pCy, centerX, centerY, fill=app.player.getColor())

    
    
#draws each map location label 
def drawMapLabels(app, canvas):
    fontSize = str(app.width//65) #might want to include app.height here
    font = 'helvetica ' + fontSize
    margin = app.mapMargin

    #cafeteria
    x,y = 3, 46.5 
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="Cafeteria", fill='white',font=font)

    #weapons
    x,y = 4, 68 
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="Weapons", fill='white',font=font)

    #O2
    x,y = 11, 62
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="O2", fill='white',font=font)

    #navigation
    x,y = 13, 80
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="Navigation", fill='white',font=font)

    #shields
    x,y = 26, 68
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="Shields", fill='white',font=font)

    #storage
    x,y = 26, 43
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="Storage", fill='white',font=font)

    #communications
    x,y = 30, 57
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="Communications", fill='white',font=font)

    #admin
    x,y = 16, 55
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="Admin", fill='white',font=font)

    #electrical
    x,y = 18, 30
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="Electrical", fill='white',font=font)

    #medbay
    x,y = 10, 32
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="Medbay", fill='white',font=font)

    #lower engine
    x,y = 23, 15
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="Lower Engine", fill='white',font=font)

    #upper engine
    x,y = 4, 15
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="Upper Engine", fill='white',font=font)

    #reactor
    x,y = 12, 6
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="Reactor", fill='white',font=font)

    #security
    x,y = 12, 22
    x0,y0,x1,y1 = getCellBounds(app, x, y, margin)
    cx, cy = (x0+x1) / 2, (y0+y1) / 2
    canvas.create_text(cx, cy, text="Security", fill='white',font=font)

#draws the map grid
def drawMap(app, canvas):
    margin = app.mapMargin
    for row in range(app.mapRows):
        for col in range(app.mapCols):
            x0,y0,x1,y1 = getCellBounds(app, row, col, margin)
            if app.worldMap[row][col] == 0: #floor
                color = 'cyan'
                canvas.create_rectangle(x0,y0,x1,y1, fill=color, width=0)
            #can hardcode here for colored ones you still want to show on map

#draws the ai circles on the map
def drawAiOnMap(app, canvas):
    r = app.mapCircleRadius
    
    for ai in app.allAIs:
        row, col, dx, dy = ai.getRow(), ai.getCol(), ai.getDx(), ai.getDy() 
        color = ai.getColor()
        cx, cy = ai.findCxAndCy(app, app.mapMargin)
        #print('trying to draw')
        #draw circle
        if ai.getImpStatus() == 'crewmate':
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color)
        elif ai.getImpStatus() == 'imposter':
            canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color)
            #imposter labeled with X
            x0,y0 = cx-(r*5/8), cy-(r*5/8)
            x1,y1 = cx+(r*5/8), cy+(r*5/8)
            canvas.create_line(x0,y0,x1,y1,fill='black', width=2)
            x0,y0 = cx-(r*5/8), cy+(r*5/8)
            x1,y1 = cx+(r*5/8), cy-(r*5/8)
            canvas.create_line(x0,y0,x1,y1,fill='black', width=2)



def drawScreenStarEffect(app, canvas):
    for (cx, cy, r) in app.stars:
        canvas.create_oval(cx-r,cy-r,cx+r,cy+r, fill='white')


def drawTitleScreen(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill='black')
    #star effect
    drawScreenStarEffect(app, canvas)
    
    #among us title text
    offset = 100
    titleX = app.width//2 - offset
    canvas.create_image(titleX, app.height//5, image=ImageTk.PhotoImage(app.titleTextImage))
    
    #3d text image
    offset = 185
    text3dX = app.width//2 + offset
    canvas.create_image(text3dX, app.height//5, image=ImageTk.PhotoImage(app.text3dImage))


def drawTitleSinglePlayerButton(app, canvas):
    # cx,cy = app.width//2, app.height//2.25

    x0,y0 = app.spButtonLeftX, app.spButtonLeftY
    x1, y1 = app.spButtonRightX, app.spButtonRightY
   
    canvas.create_rectangle(x0,y0,x1,y1, fill='white')
    canvas.create_rectangle(x0+3,y0+3,x1-3,y1-3, fill='black')
    canvas.create_text((x0+x1)//2, (y0+y1)//2, text='SINGLE PLAYER', 
                        font='impact 32', fill='white')

def drawSinglePlayerScreen(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill='black')
    drawScreenStarEffect(app, canvas)
    font = 'impact 72 bold'
    canvas.create_text(app.width//2, app.height//6, text='Single Player', 
                        font=font, fill='lime')

def drawConfigureSPButton(app, canvas):
    x0,y0 = app.conButtonLeftX, app.conButtonLeftY
    x1, y1 = app.conButtonRightX, app.conButtonRightY

    canvas.create_rectangle(x0,y0,x1,y1, fill='white')
    canvas.create_rectangle(x0+3,y0+3,x1-3,y1-3, fill='black')
    canvas.create_text((x0+x1)//2, (y0+y1)//2, text='Configure Game Settings', 
                        font='impact 28', fill='white')

def drawSPPlayButton(app, canvas):
    x0,y0 = app.spPlayButtonLeftX, app.spPlayButtonLeftY
    x1, y1 = app.spPlayButtonRightX, app.spPlayButtonRightY

    canvas.create_rectangle(x0,y0,x1,y1, fill='white')
    canvas.create_rectangle(x0+3,y0+3,x1-3,y1-3, fill='black')
    canvas.create_text((x0+x1)//2, (y0+y1)//2, text='Begin Mission', 
                        font='impact 28', fill='white')

def drawPlayAgainScreen(app, canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill='black')
    drawScreenStarEffect(app, canvas)
    font = 'impact 72 bold'
    if app.drawingCrewWinScreen:
        if app.player.getImpStatus() == 'crewmate':
            canvas.create_text(app.width//2, app.height//6, text='Victory', 
                        font=font, fill='blue')
        elif app.player.getImpStatus() == 'imposter':
            canvas.create_text(app.width//2, app.height//6, text='Defeat', 
                        font=font, fill='red')
    elif app.drawingImpWinScreen:
        if app.player.getImpStatus() == 'crewmate':
            canvas.create_text(app.width//2, app.height//6, text='Defeat', 
                        font=font, fill='blue')
        elif app.player.getImpStatus() == 'imposter':
            canvas.create_text(app.width//2, app.height//6, text='Victory', 
                        font=font, fill='red')

def drawPlayAgainButton(app, canvas):
    x0,y0 = app.playAgainButtonLeftX, app.playAgainButtonLeftY
    x1, y1 = app.playAgainButtonRightX, app.playAgainButtonRightY

    canvas.create_rectangle(x0,y0,x1,y1, fill='white')
    canvas.create_rectangle(x0+3,y0+3,x1-3,y1-3, fill='black')
    canvas.create_text((x0+x1)//2, (y0+y1)//2, text='Play Again', 
                        font='impact 28', fill='white')

def drawVoteButton(app, canvas):
    x0,y0 = app.voteButtonLeftX, app.voteButtonLeftY
    x1, y1 = app.voteButtonRightX, app.voteButtonRightY

    canvas.create_rectangle(x0,y0,x1,y1, fill='blue')
    canvas.create_rectangle(x0+3,y0+3,x1-3,y1-3, fill='black')
    canvas.create_text((x0+x1)//2, (y0+y1)//2, text='Vote', 
                        font='impact 28', fill='white')

def drawPlayerUseButton(app, canvas):
    if app.player.getIsPromptingUse() == True: #draw image, prompting use
        canvas.create_image(app.useButtonCx, app.useButtonCy,
                        image=ImageTk.PhotoImage(app.useButtonImage))
    else: #draw transparent, not prompting use
        canvas.create_image(app.useButtonCx, app.useButtonCy, 
                        image=ImageTk.PhotoImage(app.useButtonImageTrans))

def drawPlayerReportButton(app, canvas):
    #app.reportButtonImage
    if app.player.getIsPromptingReport() == True: #draw image, prompting use
        canvas.create_image(app.reportButtonCx, app.reportButtonCy,
                        image=ImageTk.PhotoImage(app.reportButtonImage))
    else: #draw transparent, not prompting use
        canvas.create_image(app.reportButtonCx, app.reportButtonCy, 
                        image=ImageTk.PhotoImage(app.reportButtonImageTrans))

def drawPlayerKillButton(app, canvas):
    if app.player.getIsPromptingKill() == True: #draw image, prompting use
        canvas.create_image(app.killButtonCx, app.killButtonCy,
                        image=ImageTk.PhotoImage(app.killButtonImage))
    else: #draw transparent, not prompting use
        canvas.create_image(app.killButtonCx, app.killButtonCy, 
                        image=ImageTk.PhotoImage(app.killButtonImageTrans))

#draws left starting wire colored boxes
def drawRandomWirePlacement(app, canvas): 
    currObj = app.currWiresTaskObj #temp currWiresTaskObj for clarity
    
    #draw first left wire
    x0,y0,x1,y1 = currObj.getFirstWireSButtonDims()
    firstColor = currObj.getFirstWireColor()
    canvas.create_rectangle(x0,y0,x1,y1, fill=firstColor)

    #draw second left wire
    x0,y0,x1,y1 = currObj.getSecondWireSButtonDims()
    secondColor = currObj.getSecondWireColor()
    canvas.create_rectangle(x0,y0,x1,y1, fill=secondColor)

    #draw third left wire
    x0,y0,x1,y1 = currObj.getThirdWireSButtonDims()
    thirdColor = currObj.getThirdWireColor()
    canvas.create_rectangle(x0,y0,x1,y1, fill=thirdColor)

    #draw fourth left wire
    x0,y0,x1,y1 = currObj.getFourthWireSButtonDims()
    fourthColor = currObj.getFourthWireColor()
    canvas.create_rectangle(x0,y0,x1,y1, fill=fourthColor)


def drawRightWires(app, canvas): 
    currObj = app.currWiresTaskObj #temp currWiresTaskObj for clarity

    #draw first right wire
    x0,y0,x1,y1 = currObj.getFirstWireEButtonDims()
    canvas.create_rectangle(x0,y0,x1,y1, fill='red')

    #draw second right wire
    x0,y0,x1,y1 = currObj.getSecondWireEButtonDims()
    canvas.create_rectangle(x0,y0,x1,y1, fill='blue')

    #draw third right wire
    x0,y0,x1,y1 = currObj.getThirdWireEButtonDims()
    canvas.create_rectangle(x0,y0,x1,y1, fill='yellow')

    #draw fourth right wire
    x0,y0,x1,y1 = currObj.getFourthWireEButtonDims()
    canvas.create_rectangle(x0,y0,x1,y1, fill='pink')


def drawWiresTask(app, canvas): #need fixed
    currObj = app.currWiresTaskObj #temp currWiresTaskObj for clarity

    #wires task image:
    canvas.create_image(app.width//2, app.height//2,
                        image=ImageTk.PhotoImage(app.wiresTaskImage))
    #wire setup:
    drawRandomWirePlacement(app, canvas)
    drawRightWires(app, canvas)
    #wire player interaction:

    #get wire button start dimensions
    firstSLeftX,firstSLeftY,firstSRightX,firstSRightY = \
                                            currObj.getFirstWireSButtonDims()
    secondSLeftX,secondSLeftY,secondSRightX,secondSRightY = \
                                            currObj.getSecondWireSButtonDims()
    thirdSLeftX,thirdSLeftY,thirdSRightX,thirdSRightY = \
                                            currObj.getThirdWireSButtonDims()
    fourthSLeftX,fourthSLeftY,fourthSRightX,fourthSRightY = \
                                            currObj.getFourthWireSButtonDims()                                        
    #get wire button end dimensions                      
    firstELeftX,firstELeftY,firstERightX,firstERightY = \
                                            currObj.getFirstWireEButtonDims()
    secondELeftX,secondELeftY,secondERightX,secondERightY = \
                                            currObj.getSecondWireEButtonDims()
    thirdELeftX,thirdELeftY,thirdERightX,thirdERightY = \
                                            currObj.getThirdWireEButtonDims()
    fourthELeftX,fourthELeftY,fourthERightX,fourthERightY = \
                                            currObj.getFourthWireEButtonDims()
    

    #first wire
    if currObj.getDrawingFirstWire() and not currObj.getIsFirstWireStuck(): #wire not stuck
        midX0 = (firstSLeftX + firstSRightX) / 2
        midY0 = (firstSLeftY + firstSRightY) / 2
        x0,y0 = midX0 + 20, midY0
        x1, y1 = app.wiresFirstCurrMouseX, app.wiresFirstCurrMouseY #changes
        firstColor = currObj.getFirstWireColor()
        canvas.create_line(x0,y0,x1,y1, fill=firstColor, width=20) 

    elif currObj.getIsFirstWireStuck(): #wire stuck
        midX0 = (firstSLeftX + firstSRightX) / 2
        midY0 = (firstSLeftY + firstSRightY) / 2
        x0,y0 = midX0 + 20, midY0
        #make x1,y1 constant (stuck):
        if currObj.getStickFirstWireInColor('red'): #stick red
            x1, y1 = firstERightX, firstERightY-10
        elif currObj.getStickFirstWireInColor('blue'): #stick blue
            x1, y1 = secondERightX, secondERightY-10
        elif currObj.getStickFirstWireInColor('yellow'): #stick yellow
            x1, y1 = thirdERightX, thirdERightY-10
        elif currObj.getStickFirstWireInColor('pink'): #stick pink
            x1, y1 = fourthERightX, fourthERightY-10
        firstColor = currObj.getFirstWireColor()
        canvas.create_line(x0,y0,x1,y1, fill=firstColor, width=20)
    
    #second wire
    if currObj.getDrawingSecondWire() and not currObj.getIsSecondWireStuck(): #wire not stuck
        midX0 = (secondSLeftX + secondSRightX) / 2
        midY0 = (secondSLeftY + secondSRightY) / 2
        x0,y0 = midX0 + 20, midY0
        x1, y1 = app.wiresSecondCurrMouseX, app.wiresSecondCurrMouseY #changes
        secondColor = currObj.getSecondWireColor()
        canvas.create_line(x0,y0,x1,y1, fill=secondColor, width=20) 

    elif currObj.getIsSecondWireStuck(): #wire stuck
        midX0 = (secondSLeftX + secondSRightX) / 2
        midY0 = (secondSLeftY + secondSRightY) / 2
        x0,y0 = midX0 + 20, midY0
        #make x1,y1 constant (stuck):
        if currObj.getStickSecondWireInColor('red'): #stick red
            x1, y1 = firstERightX, firstERightY-10
        elif currObj.getStickSecondWireInColor('blue'): #stick blue
            x1, y1 = secondERightX, secondERightY-10
        elif currObj.getStickSecondWireInColor('yellow'): #stick yellow
            x1, y1 = thirdERightX, thirdERightY-10
        elif currObj.getStickSecondWireInColor('pink'): #stick pink
            x1, y1 = fourthERightX, fourthERightY-10
        secondColor = currObj.getSecondWireColor()
        canvas.create_line(x0,y0,x1,y1, fill=secondColor, width=20)
    
    #third wire
    if currObj.getDrawingThirdWire() and not currObj.getIsThirdWireStuck(): #wire not stuck
        midX0 = (thirdSLeftX + thirdSRightX) / 2
        midY0 = (thirdSLeftY + thirdSRightY) / 2
        x0,y0 = midX0 + 20, midY0
        x1, y1 = app.wiresThirdCurrMouseX, app.wiresThirdCurrMouseY #changes
        thirdColor = currObj.getThirdWireColor()
        canvas.create_line(x0,y0,x1,y1, fill=thirdColor, width=20) 

    elif currObj.getIsThirdWireStuck(): #wire stuck
        midX0 = (thirdSLeftX + thirdSRightX) / 2
        midY0 = (thirdSLeftY + thirdSRightY) / 2
        x0,y0 = midX0 + 20, midY0
        #make x1,y1 constant (stuck):
        if currObj.getStickThirdWireInColor('red'): #stick red
            x1, y1 = firstERightX, firstERightY-10
        elif currObj.getStickThirdWireInColor('blue'): #stick blue
            x1, y1 = secondERightX, secondERightY-10
        elif currObj.getStickThirdWireInColor('yellow'): #stick yellow
            x1, y1 = thirdERightX, thirdERightY-10
        elif currObj.getStickThirdWireInColor('pink'): #stick pink
            x1, y1 = fourthERightX, fourthERightY-10
        thirdColor = currObj.getThirdWireColor()
        canvas.create_line(x0,y0,x1,y1, fill=thirdColor, width=20)
    
    #fourth wire
    if currObj.getDrawingFourthWire() and not currObj.getIsFourthWireStuck(): #wire not stuck
        midX0 = (fourthSLeftX + fourthSRightX) / 2
        midY0 = (fourthSLeftY + fourthSRightY) / 2
        x0,y0 = midX0 + 20, midY0
        x1, y1 = app.wiresFourthCurrMouseX, app.wiresFourthCurrMouseY #changes
        fourthColor = currObj.getFourthWireColor()
        canvas.create_line(x0,y0,x1,y1, fill=fourthColor, width=20) 

    elif currObj.getIsFourthWireStuck(): #wire stuck
        midX0 = (fourthSLeftX + fourthSRightX) / 2
        midY0 = (fourthSLeftY + fourthSRightY) / 2
        x0,y0 = midX0 + 20, midY0
        #make x1,y1 constant (stuck):
        if currObj.getStickFourthWireInColor('red'): #stick red
            x1, y1 = firstERightX, firstERightY-10
        elif currObj.getStickFourthWireInColor('blue'): #stick blue
            x1, y1 = secondERightX, secondERightY-10
        elif currObj.getStickFourthWireInColor('yellow'): #stick yellow
            x1, y1 = thirdERightX, thirdERightY-10
        elif currObj.getStickFourthWireInColor('pink'): #stick pink
            x1, y1 = fourthERightX, fourthERightY-10
        fourthColor = currObj.getFourthWireColor()
        canvas.create_line(x0,y0,x1,y1, fill=fourthColor, width=20)
    

    #if completed
    if currObj.isAllWiresCompleted():
        canvas.create_text(app.width//2, app.height//5, text='Task Completed',
                            font='impact 36 bold', fill='white')

#draw task bar that fills up
def drawTaskBar(app, canvas):
    
    x0,y0 = app.width/25, app.height/43
    #incrVal = 75
    rectWidth = app.numTaskBarCols*5
    x1 = x0 + rectWidth
    y1 = y0+30
    
    bgX0, bgX1 = x0, (x0+(rectWidth*app.numTaskBarCols))
    canvas.create_rectangle(bgX0,y0,bgX1,y1, fill='gray', width=5,
                                outline='light gray')
    
    for col in range(app.numTaskBarCols):
        if col < app.numTasksCompleted:
            canvas.create_rectangle(x0,y0,x1,y1,fill='dark green', width=0)
        else:
            canvas.create_rectangle(x0,y0,x1,y1,fill='gray', width=0)
        x0 = x1
        x1 = x0+rectWidth
    
    x0,y0 = app.width/25, app.height/43
    x1,y1 = x0+75, y0+30
    x = (x0+x1)/2 + 30
    y = (y0+y1)/2
    canvas.create_text(x, y, text='Total Tasks Completed', 
                        fill='white', font='impact 14')

    #tasks
    tX0, tY0 = x0, y1+10
    tX1, tY1 = x0+115, tY0+100

    if app.player.getImpStatus() == 'crewmate':
        canvas.create_rectangle(tX0,tY0,tX1,tY1,fill='light gray', 
                                    stipple='gray50', width=0)
        canvas.create_text(x-13, tY0+10, text='Tasks:', fill='white smoke', font='impact 14 bold')

        numWCompleted = app.player.getNumWiresTasksCompleted()
        canvas.create_text(x-13, tY0+35, text=f'Fix Wiring ({numWCompleted}/4)', 
                                fill='white smoke', font='14')

    
#draw exclamation marks on map
def drawMapTaskLabels(app, canvas):
    margin = app.mapMargin
    for row in range(app.mapRows):
        for col in range(app.mapCols):
            x0,y0,x1,y1 = getCellBounds(app, row, col, margin)
            x = (x0+x1)/2
            y = (y0+y1)/2
            if app.worldMap[row][col] == 2: #task

                canvas.create_image(x, y,
                        image=ImageTk.PhotoImage(app.taskExclamationImage))

#blue voting screen where they vote
def drawVotingScreen(app, canvas):
    outerMargin = 4
    innerMargin = 10
    innerWidth = 7
    blueMargin = innerMargin+innerWidth
    titleMargin = blueMargin + 30

    canvas.create_rectangle(outerMargin, outerMargin, app.width-outerMargin, 
                                app.height-outerMargin, fill="black")
    canvas.create_rectangle(innerMargin, innerMargin, app.width-innerMargin, 
                                app.height-innerMargin, fill="gray",
                                width=7, outline="dark gray")
    canvas.create_rectangle(blueMargin, blueMargin, app.width-blueMargin, 
                            app.height-blueMargin, fill="light blue",
                              width=7, outline="cyan")
    canvas.create_text(app.width//2, titleMargin, text="Who Is The Imposter?",
                        font = "impact 40 bold", fill="white")
    # canvas.create_text(app.width//2, app.height//2, text="this is where you vote",
    #                     font = "Helvetica 16", fill="black")
    
    totalPeople = app.numAIs+app.numPlayers
    halfPeople = totalPeople//2
    otherHalfPeople = totalPeople-halfPeople
    #print(otherHalfPeople)
    peopleColors = []
    length = 280
    sideLength = 75
    if app.aiReported:
        for ai in app.allAIs:
            peopleColors.append(ai.getColor())
            if ai.getIsReporting(self):
                reportingColor = ai.getColor()
    #peopleColors.append(app.player.getColor())
    #largestVotes

    colorFont = 'helvetica 24'
    tallyFont = 'helvetica 20'
    #player box
    if app.player.getIsAlive():
        fillColor = 'whitesmoke'
        numVotes = app.player.getNumSelfVotes()
    else:
        fillColor = 'gray'
    x0,y0 = app.width*(1/8), app.height*(2/8)
    x1,y1 = x0+length, y0+sideLength
    canvas.create_rectangle(x0+2,y0+1,x1+2,y1+1,fill='dimgray')
    canvas.create_rectangle(x0,y0,x1,y1,fill=fillColor)
    cx,cy = (x0+x1)//2,(y0+y1)//2
    selfColor = app.player.getColor()
    if selfColor == 'yellow':
        selfColor = 'gold'
    canvas.create_text(cx,cy-(sideLength*1/4), text=f'{app.player.getColor()} (you)',
                font=colorFont,fill=selfColor)
    
    # if largestVotes == None or numVotes > largestVotes:
    #     largestVotes = numVotes
    #     mostVotedPerson = app.player
    #if showing votes: player
    
    if app.showingVotes == True:
    #player
        if app.player.getIsAlive():
            #if app.boolVal == True: #to try and prevent repeats
                #print(numVotes)
            #for _ in range(numVotes):
            #print(numVotes)
            canvas.create_text(cx,cy, text=f'{numVotes}',
                        font=colorFont,fill=selfColor)
                    
                    
                    #boolVal = False
        #for ai in app.allAIs:
        


    #ai boxes
    count = 1 #player already went
    for ai in app.allAIs:
        # if ai.getPersonVotingFor() != None:
        #     personVotingFor = ai.getPersonVotingFor()
        #     if personVotingFor == 'player':
        #         personVotingFor = app.player
        #     #print(personVotingFor)
        #     personVotingFor.addOneNumSelfVotes()

        if count > halfPeople: #reset to top right
            x0,y0 = app.width*(4.5/8), app.height*(2/8)
            x1,y1 = x0+length, y0+sideLength
        elif count <= halfPeople:
             #add to y's
            y0 += (sideLength+40)
            y1 = y0+sideLength
        #set alive color
        if ai.getIsAlive(): 
            fillColor = 'whitesmoke'
        else:
            fillColor = 'gray'
        #draw rects
        canvas.create_rectangle(x0+2,y0+1,x1+2,y1+1,fill='dimgray')
        canvas.create_rectangle(x0,y0,x1,y1,fill=fillColor)
        cx,cy = (x0+x1)//2,(y0+y1)//2
        canvas.create_text(cx,cy-(sideLength*1/4), text=f'{ai.getColor()}',
                            font=colorFont,fill=ai.getColor())
        numVotes = ai.getNumSelfVotes()
        #if largestVotes == None or numVotes > largestVotes:
           # largestVotes = numVotes
           # mostVotedPerson = ai
        if app.showingVotes == True:
            for _ in range(numVotes):
                canvas.create_text(cx-(numVotes*3),cy, text='|',
                    font=tallyFont,fill=ai.getColor())
                cx+=3

        count += 1

  
#Tkinter Voting option window
def setUpVotingWindowAtStartAndHide(app):
    app.voteTkWindow = Tk()
   
    app.voteTkWindow.geometry('100x200')
    app.voteTkWindow.configure(bg='light blue')
    app.voteTkWindow.title("Voting")
    #radio vote buttons
    app.titleText = Label(app.voteTkWindow, text="Vote:", 
                        background='light blue', font=('Helvetica', 14, 'bold'))
    app.titleText.grid(row=0, column=0, sticky=W)


    app.voteVar = IntVar(app.voteTkWindow)    

    count = 0
    for ai in app.allAIs:
        if ai.getIsAlive():
            Radiobutton(app.voteTkWindow, 
                    text=f'{ai.getColor()}', variable=app.voteVar,
                    value=count, bg='light blue').grid(row=count+1,column=0,sticky=W)
            count +=1 
    if app.player.getIsAlive():
        Radiobutton(app.voteTkWindow, 
                    text=f'{app.player.getColor()} (you)', variable=app.voteVar,
                    value=count, bg='light blue').grid(row=count+1,column=0,sticky=W)



    #submit button
    Button(app.voteTkWindow, text="Confirm", bg='dark gray', 
        command=lambda:voteConfirmButton(app)).grid(row=app.numAIs+2, column=0, sticky=W)
                                                    
    app.voteTkWindow.withdraw()

#run / show window (loops)
def runVoteWindow(app):
    app.voteTkWindow.deiconify() #show window

#command response for tk button
def voteConfirmButton(app):
    for ai in app.allAIs:
        if ai.getName() == f'ai{app.voteVar.get()}':
            ai.addOneNumSelfVotes()

    app.showingVotes = True 
    app.voteWaitTimer = time.time()

    app.voteTkWindow.withdraw()

#ray casting, draw ais on screen with images
def drawAIs(app, canvas):
    #print(app.sortedAiDistList)
    for (ai,x,y,distToAi) in app.sortedAiDistListPlusExtra:
        #get height:
        aiHeightInPx = int(app.height // distToAi)
        #width is same as height:
        aiWidthInPx = aiHeightInPx

        
        #need to resize image with raycasting aiheight/aiwidth
        aiColor = ai.getColor()
        colorImagesDict = {
                            "blue": (app.blueAliveImage,app.blueDeadImage),
                            "orange": (app.orangeAliveImage,app.orangeDeadImage),
                            "green": (app.greenAliveImage,app.greenDeadImage),
                            "red": (app.redAliveImage,app.redDeadImage),
                            "yellow": (app.yellowAliveImage,app.yellowDeadImage),
        }
        distToWallAtX = app.vertLineDimensions[x][3]
        if distToAi < distToWallAtX: #in front of wall
            aliveImage = colorImagesDict.get(aiColor, 'color not in images dict')[0]
            deadImage = colorImagesDict.get(aiColor, 'color not in images dict')[1]

            if ai.getIsAlive():
                resizedImage = aliveImage.resize((aiWidthInPx,aiHeightInPx))
            else: #dead
                resizedImage = deadImage.resize((aiWidthInPx,aiHeightInPx))

            #draw the image
            canvas.create_image(x, y, image=ImageTk.PhotoImage(resizedImage))


def drawPlayerDiedText(app, canvas):
    canvas.create_text(app.width//2,app.height//4,text='You Have Been Killed!', 
                        fill='red', font='impact 48 bold')


#end screen, states num imposters left
def drawEjectedScreen(app,canvas):
    canvas.create_rectangle(0,0,app.width,app.height, fill='black')
    drawScreenStarEffect(app,canvas)
    font = 'helvetica 36'
    if app.mostVotedPlayer.getImpStatus() == 'imposter':
        text = f'{app.mostVotedPlayer.getColor()} was An Imposter'
        text2 = '0 Imposters remain.'
    if app.mostVotedPlayer.getImpStatus() == 'crewmate':
        text = f'{app.mostVotedPlayer.getColor()} was not An Imposter'
        text2 = '1 Imposter remains.'
    
    canvas.create_text(app.width//2, app.height//2, text=text, 
                        font=font, fill='white')
    canvas.create_text(app.width//2, app.height//2+50, text=text2, 
                        font=font, fill='white')


#called continuously, draws everything
def redrawAll(app, canvas):
    if not app.drawingATitleScreen: #in game
        #raycasting
        drawCeilingAndFloor(app, canvas)
        drawVertLines(app, canvas)
        drawAIs(app,canvas) #raycast ais
  
        #player stuff
        drawTaskBar(app, canvas)
        drawPlayerReportButton(app, canvas)

        if app.player.getImpStatus() == 'crewmate':
            drawPlayerUseButton(app, canvas)
            if app.player.getIsDoingTask(): #if doing task
                taskName = app.player.getCurrTask()
                if taskName == 'wires':
                    drawWiresTask(app, canvas)
            if app.drawingPlayerDiedText:
                drawPlayerDiedText(app, canvas)
        elif app.player.getImpStatus() == 'imposter':
            drawPlayerKillButton(app, canvas)

        # if app.promptVent:
        #     drawVentPrompt(app, canvas)

        #map
        if app.isMapOpen:
            drawMap(app, canvas)
            drawPlayerOnMap(app, canvas)
            if app.playerViewAIsOnMap:
                drawAiOnMap(app, canvas)
            drawMapLabels(app, canvas)
            if app.player.getImpStatus() == 'crewmate': 
                drawMapTaskLabels(app, canvas) 
    else: #drawing a title screen
        
        if app.drawingMainTitleScreen:
            drawTitleScreen(app, canvas)
            drawTitleSinglePlayerButton(app, canvas)
        if app.drawingSinglePlayerScreen:
            drawSinglePlayerScreen(app, canvas)
            drawConfigureSPButton(app, canvas)
            drawSPPlayButton(app, canvas)
        if app.drawingCrewWinScreen or app.drawingImpWinScreen:
            drawPlayAgainScreen(app, canvas)
            drawPlayAgainButton(app, canvas)
        
        if app.drawingVotingScreen:
            drawVotingScreen(app, canvas)
            if app.showingVotes == False:
                drawVoteButton(app, canvas)
        if app.drawingEjectedScreen:
            drawEjectedScreen(app,canvas)


    if app.drawingReportingScreen: 
        canvas.create_rectangle(0,0,app.width,app.height,fill='black')
        canvas.create_image(app.width//2,app.height//2,
            image=ImageTk.PhotoImage(app.bodyReportedScreenImage))
            
#runs the app through cmu_112_graphics, given width/height of window
runApp(width=900, height=600)