import pygame, sys
from pygame.locals import *

resAlphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"," "]
extAlphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
";",":",",",".","'",'"',"!","£","$","%","^","&","*","(",")","<",">","?","@","#","~","-","_","[","]","{","}","+","=","|"," ","/","`","¬","0","1","2","3","4","5","6","7","8","9"]

##Special Variables
resizeWidth = None
resizeHeight = None
screenClicked = False


##EVENT HANDLER##
def eventGet():

    global resizeWidth
    global resizeHeight
    global screenClicked
    screenClicked = False

    for event in pygame.event.get():

        #detect screen close
        if event.type == QUIT:
            pygame.quit()
            quit()
        
        
        #detect screen resizing and places new dimensions 
        #into resizeWidth/Height that is used in Window class
        
        if event.type == pygame.VIDEORESIZE:
            resizeWidth = event.w
            resizeHeight = event.h

        #detecting screen clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            screenClicked = True

        #detecting keyboard presses
            #figure this out