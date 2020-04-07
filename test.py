from cmu_112_graphics import *
import math
from tkinter import *


def loadImages(app):
    tiles = {}
    tiles['1'] = PhotoImage(file="s01.png")
    tiles['2'] = PhotoImage(file="s02.png")
    app.tiles = tiles


def appStarted(app): # init everything
    app.width = 800
    app.height = 600
    app.baseLine = 50
    app.startOfAimingLine = app.width/2, app.height - app.baseLine
    app.aimingAngle = math.pi/4 # 45 degrees
    app.ballPos = app.startOfAimingLine
    app.ballAngle = app.aimingAngle
    app.ballColor = 'blue'
    app.ballSize = 15
    app.timerDelay = 25
    app.ballMoving = False
    app.ballSpeed = 10
    app.bubbleColors = {'1':'red', '2':'green', '3':'yellow', '4':'blue'}
    
    app.bubbleSize = 20
    
    app.topMargin = app.bubbleSize * 2
    app.leftMargin = app.bubbleSize + 5
    readBubbles(app)
    loadImages(app)
    
    
def readBubbles(app):
    bubbles = "1112222111\n222000222\n1112222111\n222000222\n"
    app.bubbleRows = bubbles.splitlines()
    
    
    
def nextPlay(app):
    appStarted(app)

def moveBall(app):
    if app.ballMoving:
        x, y = app.ballPos
        v  = app.ballSpeed
        a = app.ballAngle
        xu = x + v * math.cos(a)
        yu =  y + v *  math.sin(-a)
        app.ballPos = xu, yu
        wall = ballBounced(app)
        if wall != None:
            if wall == "L" or wall == "R":
                app.ballAngle = (math.pi - a) % (math.pi * 2)
            elif wall == "T":
                app.ballAngle = (2*math.pi - a) % (math.pi * 2)
            else: # Wall == "B"
                nextPlay(app)
        
def timerFired(app):
    moveBall(app)
    
    
    
def ballBounced(app):
    x0, y0 = app.ballPos
    r = app.ballSize
    if x0 + r >= app.width: # right wall
        return "R"
    if x0 - r <= 0: # left wall
        return "L"
    if y0 - r <= 0: #top wall
        return "T"
    elif y0 + r >= app.height:
        return "B"
    return None
    
def keyPressed(app, event):
    if event.key == "Left":
        app.aimingAngle = (0.02 + app.aimingAngle) % (math.pi * 2)
        app.ballAngle = app.aimingAngle
    elif event.key == "Right":
        app.aimingAngle = (app.aimingAngle - 0.02)  % (math.pi * 2)
        app.ballAngle = app.aimingAngle
        
    elif event.key == "Space":
        app.ballMoving = not app.ballMoving
    
    

### drawing funcs:
        
def drawBubbleRows(app, canvas):
    numRows = len(app.bubbleRows)
    for i in range(numRows):
        row = app.bubbleRows[i]
        for j in range(len(row)):
            bubble = row[j] # '0', '1', '2', etc.
            if bubble in app.bubbleColors: # '0' (empty space) isn't in this dict, so the if condition is false nothing is drawn
                
                #color = app.bubbleColors[bubble]
                img = app.tiles[bubble]
                y = app.topMargin + i * app.bubbleSize * 2 # bubbleSize is radius, not diameter
                if i % 2 == 0:
                    x = app.leftMargin + app.bubbleSize * 2 * j
                else:
                    x = app.leftMargin + app.bubbleSize * 2 * j + app.bubbleSize
                """
                top = y - app.bubbleSize
                left = x - app.bubbleSize
                right = x +  app.bubbleSize
                bottom = y + app.bubbleSize
                canvas.create_oval(left, top, right, bottom, fill=color, outline=color, width=2)
                """
                canvas.create_image(x, y, image = img)
    
def drawAimingLine(app, canvas):
    if not app.ballMoving:
        x0, y0 = app.startOfAimingLine
        a = app.aimingAngle
        #r = 600
        #fx, fy = sx + r * math.cos(a), sy + r * math.sin(-a)
        #canvas.create_line(sx, sy, fx, fy, fill='red')
        # line has 25 segments
        # each segment length is 20
        
        for i in range(50): # half are red, half are blank
            if i % 2 == 0:
                p1 = (x0 + 20 * i * math.cos(a),  y0 + 20 * i * math.sin(-a))
                p2 =  (p1[0] + 20 * math.cos(a), p1[1] + 20 * math.sin(-a))
            
            canvas.create_line(p1, p2,  fill='red')
        
    
        
def drawBall(app, canvas):
    bx, by = app.ballPos
    r = app.ballSize
    top = by - r
    left = bx - r
    bottom = by + r
    right = bx + r
    canvas.create_oval((left, top), (right, bottom), fill=app.ballColor)
    
    
    
    
def redrawAll(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill='black')
    drawAimingLine(app, canvas)
    drawBall(app, canvas)
    drawBubbleRows(app, canvas)
    
runApp(width=800, height=600)