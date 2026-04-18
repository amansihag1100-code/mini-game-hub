
import pygame as py    #alias
import sys             # to read command line argument , exit program safely
import os                # used for file handling , history.csv
from datetime import datetime         #to reacord date and time of each game


player1 = sys.argv[1]
player2 = sys.argv[2]  # get usernames from main.sh , python3 game.py aman ankit , aman = sys.argv index = 1

py.init()  # starts all pygame modules


py.mixer.init()

music_on = True
music_file = "materials/2.mp3"

py.mixer.music.load(music_file)
py.mixer.music.play(-1)




# creating window
width,height = 600,500
screen = py.display.set_mode((width,height))         #set_mode creates window
py.display.set_caption("MINI GAME HUB")

#image as background

bgimg = py.image.load("materials/1.jpg")
bgimg = py.transform.scale(bgimg,(width,height))


font = py.font.SysFont(None,40) #to set font of none type and size 40

textcolor = (255,255,255)

#how to write text inside buttons or to draw text and put it at x,y pos
def  draw_text(text,size,x,y,color=textcolor):
    font = py.font.SysFont("arial",size,bold=True)
    img = font.render(text,True,color)  #font render converts text to image
    rect = img.get_rect(center=(x,y))
    screen.blit(img,rect)     # put that img at x,y position on screen


white = (255,255,255)   # NEED TO DEFINE COLOR BEFORE NO COLOR IS IMPORTED
black = (30,30,30)
hovercolor = (100 , 170 ,255)
textcolor = (255,255,255)
btncolor = (70,130,255)

backtop = (30,30,60)
backbtm = (10,10,30)


#button with hover effect
def drawbutton(rect,text):
    mouseposition = py.mouse.get_pos()

    if rect.collidepoint(mouseposition):
        py.draw.rect(screen,hovercolor,rect,border_radius=15)
    
    else:
        py.draw.rect(screen , btncolor,rect,border_radius=15)

    draw_text(text,25,rect.centerx,rect.centery)


#function for background with gradient color
def gradient():
    for y in range(height):
        color = ( backtop[0] + (backbtm[0] - backtop[0]) * y//height ,
                  backtop[1] + (backbtm[1] - backtop[1]) * y // height,
                  backtop[2] +(backbtm[2] - backtop[2]) * y//height)

        py.draw.line(screen,color,(0,y),(width,y))




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

    screen.blit(bgimg,(0,0))    #put img at (0,0)


    draw_text("MINI GAME HUB",45,width//2,80)

    draw_text(f"{player1} Vs {player2}" , 25 , width//2 ,130)



    ttt_btn = py.Rect(200,150,200,50)
    oth_btn = py.Rect(200,230,200,50)    #x,y and w,h of clickable box
    c4_btn = py.Rect(200,310,200,50)
    music_btn = py.Rect(200,390,200,50)

    drawbutton(ttt_btn,"TIC TAC TOE")
    drawbutton(oth_btn,"OTHELLO")
    drawbutton(c4_btn,"CONNECT 4")
    drawbutton(music_btn,"MUSIC OFF" if music_on else "MUSIC ON")


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

            if music_btn.collidepoint(mouseposition):
                if music_on:
                    py.mixer.music.pause()
                    music_on = False
                else:
                    py.mixer.music.unpause()
                    music_on = True




    #gradient()

    
    
    '''
     py.draw.rect(screen,blue,ttt_btn)
    py.draw.rect(screen,blue,oth_btn)
    py.draw.rect(screen,blue,c4_btn)


    # text to be written inside buttons
    draw_text("TIC TAC TOE",218,162)
    draw_text("OTHELLO",235,242)
    draw_text("CONNECT 4",225,322)'''

    

    py.display.update()          #refresh screen 




py.quit()   #close pygame
sys.exit()        #exit program



