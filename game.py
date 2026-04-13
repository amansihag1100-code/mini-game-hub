import pygame as py    #alias
import sys             # to read command line argument , exit program safely
import os                # used for file handling , history.csv
from datetime import datetime         #to reacord date and time of each game


player1 = sys.argv[1]
player2 = sys.argv[2]  # get usernames from main.sh , python3 game.py aman ankit , aman = sys.argv index = 1

py.init()  # starts all pygame modules


# creating window
width,height = 600,500
screen = py.display.set_mode((width,height))         #set_mode creates window
py.display.set_caption("MINI GAME HUB")

font = py.font.SysFont(None,40) #to set font of none type and size 40

#how to write text inside buttons or to draw text and put it at x,y pos
def  draw_text(text,x,y):
    img = font.render(text,True,black)  #font render converts text to image
    screen.blit(img,(x,y))     # put that img at x,y position on screen


white = (255,255,255)   # NEED TO DEFINE COLOR BEFORE NO COLOR IS IMPORTED
black = (0,0,0)
blue = (50 , 150 ,255)

# function to run game

def launchgame(gamefile):
    py.quit()    #close the pygame window so that it does not freeze

    os.system(f"python {gamefile} {player1} {player2}")

    #restart game.py after game ends
    os.system(f"python game.py {player1} {player2}")

    sys.exit()





# main game loop

running = True
while running:
    screen.fill(white)    #everytime in each loop frame make screen white

    for event in py.event.get():      #takes event mouse clicks , keyboard , window close etc.
        if event.type == py.QUIT:          #user clicks cross
            running = False

        if event.type == py.MOUSEBUTTONDOWN:
            mouseposition = py.mouse.get_pos()

            if ttt_btn.collidepoint(mouseposition):
                launchgame("games/tictactoe.py")

            
            if oth_btn.collidepoint(mouseposition):
                launchgame("games/othello.py")
            
            if c4_btn.collidepoint(mouseposition):
                launchgame("games/connect4.py")


    
    draw_text("MINI GAME HUB",185,50)

    ttt_btn = py.Rect(200,150,200,50)
    oth_btn = py.Rect(200,230,200,50)    #x,y and w,h of clickable box
    c4_btn = py.Rect(200,310,200,50)

    py.draw.rect(screen,blue,ttt_btn)
    py.draw.rect(screen,blue,oth_btn)
    py.draw.rect(screen,blue,c4_btn)


    # text to be written inside buttons
    draw_text("TIC TAC TOE",218,162)
    draw_text("OTHELLO",235,242)
    draw_text("CONNECT 4",225,322)


    py.display.update()          #refresh screen 




py.quit()   #close pygame
sys.exit()        #exit program

