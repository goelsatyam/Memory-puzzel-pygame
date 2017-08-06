import random , pygame, sys
from pygame.locals import *

FPS=30
windowwidth = 640
windowheight = 480
revealspeed = 8
boxsize = 40
gapsize = 10
boardwidth = 10
boardheight = 7
assert (boardheight*boardwidth %2 ==0)

xmargin = int((windowwidth - (boardwidth*(boxsize+gapsize)))/2) 
ymargin = int((windowheight-((boardheight)*(boxsize+gapsize)))/2)

gray     = (100,100,100)
navyblue = (60,60,100)
white    = (255,255,255)
red      = (255,0,0)
green    = (0,255,0)
blue     = (0,0,155)
yellow   = (255,255,0)
orange   = (255,128,0)
purple   = (255,0,255)
cyan     = (0,255,255)

bgcolor = navyblue
lightbgcolor = gray
boxcolor = white
highlightcolor = blue

donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'
allcolors = (red,green,blue,yellow,orange,purple,cyan)
allshapes = (donut,square,diamond,lines,oval)

def main():

	global fpsclock, displaysurf
	pygame.init()
	fpsclock = pygame.time.Clock()
	displaysurf = pygame.display.set_mode((windowwidth,windowheight))
	mousex = 0
	mousye = 0
	pygame.display.set_caption('Memory Game')

	mainboard = getRandomizedBoard()
	revealedBoxes = generateRevealedBoxesData(False)

	firstSelection = None
	displaysurf.fill(bgcolor)

	startGameAnimation(mainboard)
	while True:
		mouseClicked = False
		displaysurf.fill(bgcolor)
		drawBoard(mainboard,revealedBoxes)

		for event in pygame.event.get():
			mousex,mousey=0,0
			if event.type==QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex,mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClicked = True

			boxx, boxy = getBoxAtpixet(mousex,mousey)
	
			if boxx!=None and boxy!=None:
				if not revealedBoxes[boxx][boxy]:
					drawHighlightBox(boxx,boxy)

				if not revealedBoxes[boxx][boxy] and mouseClicked:
					revealBoxesAnimation(mainboard,[(boxx,boxy)])
					revealedBoxes[boxx][boxy] = True
					if firstSelection==None:
						firstSelection = (boxx,boxy)
					else:
						icon1shape,icon1color = getShapeAndColor(mainboard,firstSelection[0],firstSelection[1])
						icon2shape,icon2color = getShapeAndColor(mainboard,boxx,boxy)

						if icon1shape!=icon2shape or icon1color!=icon2color:
							pygame.time.wait(1000)
							coverBoxesAnimation(mainboard,[(firstSelection[0],firstSelection[1]),(boxx,boxy)])
							revealedBoxes[firstSelection[0]][firstSelection[1]]=False
							revealedBoxes[boxx][boxy] = False	
						if hasWon(revealedBoxes):
							gameWonAnimation(mainboard)
							pygame.time.wait(1000)

							mainboard= getRandomizedBoard()
							revealedBoxes = generateRevealedBoxesData(False)
							drawBoard(mainboard,revealedBoxes)
							pygame.display.update()
							pygame.time.wait(100)
							startGameAnimation(mainboard)
						firstSelection=None		
		pygame.display.update()		
		fpsclock.tick(FPS)

def drawHighlightBox(boxx,boxy):
	left, top = leftTopCoordsofBox(boxx,boxy)
	pygame.draw.rect(displaysurf,highlightcolor,(left-5,top-5,boxsize+10,boxsize+10),4)

def generateRevealedBoxesData(val):
	revealedBoxes=[[val for i in range(boardheight)] for j in range(boardwidth)]
	return revealedBoxes

def getRandomizedBoard():
	icons=[]
	for color in allcolors:
		for shape in allshapes:
			icons.append((shape,color))

	random.shuffle(icons)
	numIconsUsed = int(boardwidth*boardheight/2.0)
	icons = icons[:numIconsUsed]*2
	random.shuffle(icons) 

	board = []
	for x in range(boardwidth):
		column = []
		for y in range(boardheight):
			column.append(icons[0])
			del icons[0]
		board.append(column)

	return board		

def getBoxAtpixet(x, y):
	for boxx in range(boardwidth):
		for boxy in range(boardheight):
			left,top = leftTopCoordsofBox(boxx,boxy)
			boxRect= pygame.Rect(left,top,boxsize,boxsize)
			if boxRect.collidepoint(x,y):
				return (boxx,boxy)
	return (None,None)			

def drawBoxCovers(board, boxes, coverage):
	for box in boxes:
		left,top=leftTopCoordsofBox(box[0],box[1])
		pygame.draw.rect(displaysurf,bgcolor,(left,top,boxsize,boxsize))
		shape,color = getShapeAndColor(board,box[0],box[1])
		drawIcon(shape,color,box[0],box[1])
		if coverage > 0:
			pygame.draw.rect(displaysurf,boxcolor,(left,top,coverage,boxsize))
			pygame.display.update()
			fpsclock.tick(FPS/2)

def splitIntoGroupsOf(groupsize,thelist):
	result = []
	for i in range(0,len(thelist),groupsize):
		result.append(thelist[i:groupsize])
	return result	


def leftTopCoordsofBox(boxx,boxy):
	left = boxx * (boxsize + gapsize) + xmargin
	top = boxy * (boxsize + gapsize)+ ymargin
	return (left,top)

def revealBoxesAnimation(board,boxesToReveal):
	for coverage in range(boxsize,(-revealspeed)-1,revealspeed):
		drawBoxCovers(board,boxesToReveal,coverage)

def coverBoxesAnimation(board,boxesToCover):
	for coverage in range(0,boxsize+revealspeed,revealspeed):
		drawBoxCovers(board,boxesToCover,coverage)		


def getShapeAndColor(board,boxx,boxy):
	return board[boxx][boxy][0],board[boxx][boxy][1]

def drawIcon(shape,color,boxx,boxy):
	quater = int(boxsize * 0.25)
	half = int(boxsize * 0.5)

	left, top = leftTopCoordsofBox(boxx,boxy)

	if shape == donut:
		pygame.draw.circle(displaysurf, color,(left+half,top+half),half-5)
		pygame.draw.circle(displaysurf,bgcolor,(left+half,top + half),quater-5)
	elif shape == square:
		pygame.draw.rect(displaysurf,color,(left+quater,top+quater,boxsize-half,boxsize-half))	
	elif shape == diamond:
		pygame.draw.polygon(displaysurf,color,((left+half,top),(left+boxsize-1,top+half),(left+half,top+boxsize-1),(left,top+half)))

	elif shape == lines:
		for i in range(0,boxsize,4):
			pygame.draw.line(displaysurf,color,(left,top+i),(left+i,top))	
			pygame.draw.line(displaysurf,color,(left+i,top+boxsize-1),(left+boxsize-1,top+i))
	elif shape == oval:
		pygame.draw.ellipse(displaysurf,color,(left,top+quater,boxsize,half))		

def drawBoard(board, revealed):

	for boxx in range(boardwidth):
		for boxy in range(boardheight):
			left, top= leftTopCoordsofBox(boxx,boxy)
			if not revealed[boxx][boxy]:
				pygame.draw.rect(displaysurf,boxcolor,(left,top,boxsize,boxsize))
			else:
				shape,color = getShapeAndColor(board,boxx,boxy)
				drawIcon(shape,color,boxx,boxy)	

def startGameAnimation(board):
	coveredBoxes = generateRevealedBoxesData(False)
	boxes = []
	for x in range(boardwidth):
		for y in range(boardheight):
			boxes.append((x,y))
	random.shuffle(boxes)
	boxgroups = splitIntoGroupsOf(8,boxes)
	drawBoard(board, coveredBoxes)


def gameWonAnimation(board):
	coveredBoxes = generateRevealedBoxesData(True)
	color1 = lightbgcolor
	color2 = bgcolor

	for i in range(13):
		color1,color2 = color2, color1
		displaysurf.fill(color1)
		drawBoard(board, coveredBoxes)
		pygame.display.update()
		pygame.time.wait(300)

def hasWon(revealedBoxes):
	for i in revealedBoxes:
		if False in i:
			return False
	return True		

if __name__ == '__main__':
	main()			

