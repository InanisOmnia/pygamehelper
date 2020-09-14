import sys
import pygame
from pygame.locals import *

resAlphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," "]
extAlphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
";",":",",",".","'",'"',"!","£","$","%","^","&","*","(",")","<",">","?","@","#","~","-","_","[","]","{","}","+","=","|"," ","/","`","¬","0","1","2","3","4","5","6","7","8","9"]

#Special Variables
screenClicked = False
resizeWidth = None
resizeHeight = None
keyPressed = []
keyBeenPressed = False
event = None

#Input Handler#
def conInput(prompt, filter = None, lowerBound = None, upperBound = None):
    output = None
    valid = False
    while not valid:

        ###INTEGER CHECK###
        if filter == "integer":
            try:
                output = int(input(prompt))
            except:
                print("Integer Please")
            else:
                valid = True
            
            if valid == True:
                if lowerBound != None:
                    if output < lowerBound:
                        valid = False
                        print("input out of bounds")
                
                if upperBound != None:
                    if output > upperBound:
                        valid = False
                        print("input out of bounds")

        ###FLOAT CHECK###
        elif filter == "float":
            try:
                output = float(input(prompt))
            except:
                print("Float Please")
            else:
                valid = True

            if valid == True:
                if lowerBound != None:
                    if output < lowerBound:
                        valid = False
                        print("input out of bounds")
                
                if upperBound != None:
                    if output > upperBound:
                        valid = False
                        print("input out of bounds")
        
        ###EXTENDED ALPHABET CHECK###
        elif filter == "strAll":
            try:
                output = str(input(prompt))
            except:
                print("string please")
            else:
                valid = True

            if valid == True:
                for i in output:
                    if i not in extAlphabet:
                        valid = False
                        print("letter",i,"not valid")

        ###RESTRICTED ALPHABET CHECK###
        elif filter == "strRES":
            try:
                output = str(input(prompt))
            except:
                print("string please")
            else:
                valid = True
        
            if valid == True:
                for i in output:
                    if i not in resAlphabet:
                        valid = False
                        print("letter",i,"not valid")

        ###NO FILTER CHECK###
        elif filter == None:
            valid = True
            output = input(prompt)
        
        else:
            print("ERROR, FILTER TYPE INVALID")
            break
    
    return output

#Richardson-Virgenere Encryptor

def Encrypt(original,key):
    origArray = []
    for i in original:
        origArray.append(i)
    new = Richardson(origArray)
    new = Vigenere(new,key)
    new = Richardson(new)
    complete = ""
    for i in new:
        complete += i
    return complete

def Richardson(origArray):
    counter = 1
    new = []

    new.append(origArray[0])
    del origArray[0]

    for i in origArray:
        if counter == 1:
            new.insert(len(new),i)
        elif counter == 2:
            new.insert(0,i)
        elif counter == 3:
            counter = 1
            new.insert(len(new),i)
        else:
            print("Encryption Error, Something Broke")
        counter += 1
    return new
    
def Vigenere(origArray,key):
    keyShift = []
    for i in key:
        keyShift.append(extAlphabet.index(i))
    counter = 0
    newArray = []
    for i in origArray:
        indx = extAlphabet.index(i) + keyShift[counter]

        if indx >= len(extAlphabet):
            indx -= len(extAlphabet)
        
        newArray.append(extAlphabet[indx])
        counter += 1

        if counter == len(keyShift):
            counter = 0
    return newArray

#Richardson-Vigenere Decryptor
def Decrypt(original,key):
    origArray = []
    new = []
    complete = ""

    for i in original:
        origArray.append(i)
    new = DecRichardson(origArray)
    new = DecVigenere(new,key)
    new = DecRichardson(new)
    for i in new:
        complete += i
    return complete
def DecRichardson(origArray):
    new = []
    new2 = []

    while bool(origArray):
        if len(origArray) % 2:
            new.append(origArray[0])
            del(origArray[0])
        else:
            new.append(origArray[len(origArray)-1])
            del(origArray[len(origArray)-1])

    for i in range(len(new)-1,-1,-1):
        new2.append(new[i])

    return new2
def DecVigenere(new,key):
    keyShift = []
    new2 = []

    for i in key:
        keyShift.append(extAlphabet.index(i))
    
    counter = 0
    for i in new:
        #remember % returns the REMAINDER
        #index = original index, - key index with loops taken off, then remove extra loops of alphabet
        indx = (extAlphabet.index(i) - keyShift[counter % len(key)]) % len(extAlphabet)

        counter += 1
        new2.append((extAlphabet[indx]))
    
    return new2







##PYGAME STUFF##

class Window():
    def __init__(self,width,height,name):
        self.width = width
        self.height = height
        self.name = name
    
        self.resizable = False

    def initScreen(self):
        pygame.init()
        if self.resizable:
            self.windowSurface = pygame.display.set_mode((self.width,self.height),pygame.RESIZABLE,32)
        else:
            self.windowSurface = pygame.display.set_mode((self.width,self.height),0,32)
        pygame.display.set_caption(self.name)

    def screenSizeUpdate(self):
        global resizeWidth
        global resizeHeight
        if resizeWidth != None:
            self.width = resizeWidth
            self.height = resizeHeight
            self.windowSurface = pygame.display.set_mode((self.width,self.height),pygame.RESIZABLE,32)

    def screenFill(self,fill,image = False, xOffset = 0, yOffset = 0, imageSizeX = 0, imageSizeY = 0):
        if image == False:
            self.windowSurface.fill(fill)
        else:
            self.windowSurface.blit(fill(xOffset,yOffset,imageSizeX,imageSizeY))

#Button#
class Button():
    def __init__(self,width,height,x,y,toggleable = False):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.clickDuration = 10
        self.toggleable = toggleable
        self.clicked = False
        self.rect = None
        self.clickTimer = loopTimer(0)
        self.active = True

        self.startColour = (0,0,0)
        self.endColour = (50,50,50)

        #can be edited manually by user to be a Text() object
        self.label = None

    def checkClicked(self):
        if self.active:
            if screenClicked:
                x, y = pygame.mouse.get_pos()
                if self.rect != None:
                    if self.rect.collidepoint((x, y)):
                        if self.toggleable == True:
                            if self.clicked == True:
                                self.clicked = False
                            else:
                                self.clicked = True
                        else:
                            self.clicked = True
                            self.clickTimer = loopTimer(self.clickDuration)
                            self.clickTimer.start()
            else:
                if self.toggleable == False:
                    self.clickTimer.increment()
                    if self.clickTimer.done:
                        self.clicked = False


    def drawButton(self,window):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if self.clicked:
            pygame.draw.rect(window.windowSurface,self.endColour,self.rect)
        else:
            pygame.draw.rect(window.windowSurface,self.startColour,self.rect)
        
        if self.label != None:
            self.label.createSquare(0,0)
            self.label.textRect.center = ((self.width/2) + self.x) , ((self.height/2) + self.y)
            self.label.showText(window)
            

        

class Text():
    def __init__(self, font,fontsize, words, colour = (0,0,0)):
        self.font = str(font)
        self.words = str(words)
        self.colour = colour
        self.fontsize = fontsize

        self.font = pygame.font.SysFont(self.font, self.fontsize)
        self.text = self.font.render(self.words,True,self.colour)
        self.textRect = None
    
    def createSquare(self,left,top):
        self.textRect = self.text.get_rect()
        self.textRect.left = left
        self.textRect.top = top
    
    def showText(self,window):
        window.windowSurface.blit(self.text,self.textRect)



class TextBox():
    def __init__(self,width,height,x,y,prompt,fontSize = 25,colour = (255,255,255)):
        self.prompt = prompt
        self.complete = False
        self.active = False
        self.text = ""
        self.fontSize = fontSize
        self.font = "ariel"
        self.colour = colour
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

    def checkActive(self):
        global screenClicked
        if screenClicked:
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint((x, y)):
                self.active = True
            else:
                self.active = False

    def keypressed(self):
        global keyPressed
        global keyBeenPressed
        if self.active:
            if keyBeenPressed:
                if keyPressed[1] == pygame.K_RETURN:
                    self.complete = True
                elif keyPressed[1] == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += keyPressed[0]
    
    def showTextBox(self,window):
        if self.text == "":
            screenText = Text(self.font, self.fontSize, self.prompt)
        else:
            screenText = Text(self.font, self.fontSize, self.text)
        screenText.createSquare(self.x+5, self.y+5)

        pygame.draw.rect(window.windowSurface,self.colour,self.rect)
        if self.text == "" and self.active != True:
            screenText.showText(window)
        elif self.text != "":
            screenText.showText(window)

    def reset(self):
        self.text = ""
        self.complete = False



class loopTimer():
    def __init__(self,loops):
        self.loops = loops
        self.counting = False
        self.count = 0
        self.done = False
    
    def start(self):
        self.counting = True
        self.count = 0
        self.done = False
    
    def increment(self):
        self.count += 1
        if self.count >= self.loops:
            self.counting = False
            self.done = True







def eventGet():

    global screenClicked
    screenClicked = False
    global resizeWidth
    global resizeHeight
    resizeWidth = None
    resizeHeight = None
    global keyPressed
    global keyBeenPressed
    keyBeenPressed = False

    for event in pygame.event.get():

        #detect screen close
        if event.type == QUIT:
            pygame.quit()
            quit()

        #detect screen click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            screenClicked = True
        
        #Get new size of window after resizing
        elif event.type == pygame.VIDEORESIZE:
            resizeWidth = event.w
            resizeHeight = event.h

        elif event.type == pygame.KEYDOWN:
            keyBeenPressed = True
            keyPressed = []
            keyPressed.append(event.unicode)
            keyPressed.append(event.key)

def pygameKill():
    pygame.quit()
    quit()
