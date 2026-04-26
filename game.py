
import os               # used for file handling , history.csv

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # key value array to hide the useless lineof pygame


import pygame as py    #alias
import sys             # to read command line argument , exit program safely
from datetime import datetime         #to reacord date and time of each game
import matplotlib.pyplot as plt
from collections import Counter          #counter class to count items
import subprocess


player1 = sys.argv[1]
player2 = sys.argv[2]  # get usernames from main.sh , python3 game.py aman ankit , aman = sys.argv index = 1

py.init()  # starts all pygame modules


py.mixer.init()           #starts sound system #mixer

music_on = True   # bool variable
music_file = "materials/2.mp3"   

py.mixer.music.load(music_file)      
py.mixer.music.play(-1)           # -1 is used for forever loop




# creating window
width,height = 600,500
screen = py.display.set_mode((width,height))         #set_mode creates window
py.display.set_caption("MINI GAME HUB")


#image as background

bgimg1 = py.image.load("materials/5.jpg")
bgimg1 = py.transform.scale(bgimg1,(width,height))    # make the image equal to size of window

bgimg2 = py.image.load("materials/4.jpg")
bgimg2 = py.transform.scale(bgimg2,(width,height))


#setting pygame's text(font) Font as font path of size
FONT_PATH = "materials\Jersey10-Regular.ttf"

def get_font(size):
    return py.font.Font(FONT_PATH, size)



textcolor = (255,255,255)

#how to write text inside buttons or to draw text and put it at x,y pos , it converts text to image 
def  draw_text(text,size,x,y,color=textcolor):
    font = get_font(size)
    img = font.render(text,True,color)  #font is the variable having font stored in it and  render converts text to image
    rect = img.get_rect(center=(x,y))     #now as text is converted to image now get_rect makes rectangle around it
    screen.blit(img,rect)     # put that img at x,y position on screen


white = (255,255,255)   # NEED TO DEFINE COLOR BEFORE NO COLOR IS IMPORTED
black = (30,30,30)
hovercolor = (191, 195, 201)
textcolor = (255,255,255)
btncolor = (69, 74, 82)

backtop = (30,30,60)
backbtm = (10,10,30)



def show_charts():

    #if history.csv does not exists
    if not os.path.exists("history.csv"):
        print("No history yet")
        return
    

    games = []      #empty list
    wins = []

    with open("history.csv", "r") as f:       #open this file in read mode and store in varible f
        
        next(f) # skip first line in  history.csv     

        for line in f:
            parts = line.strip().split(",")      # parts is list , strip removes extra spaces and split at ,

            if len(parts) >= 4 and parts[0] != "":
                winner = parts[0]
                game = parts[3]

                #add item to empty list created above 
                wins.append(winner)
                games.append(game)

#???????????????????????????????

    # TOP 5 PLAYERS
    win_count = Counter(wins).most_common(5)
    players = [x[0] for x in win_count]
    counts = [x[1] for x in win_count]

    # counts
    win_count = Counter(wins).most_common(5)
    players = [x[0] for x in win_count]
    counts = [x[1] for x in win_count]

    game_count = Counter(games)


#????????????????????????????????????

    plt.style.use("dark_background")    #set dark background in graph window

# two graphs i n a single window
# fig is figure (whole window) , axs is array of graphs , 1 row 2 columns

    fig,axs = plt.subplots(1, 2, figsize=(12, 5))

# bar graph 
    axs[0].bar(players, counts, color=["cyan", "orange", "lime", "pink", "yellow"])          #players vs counts
    axs[0].set_title("Top 5 Players")
    axs[0].set_xlabel("Players")   #  X axis name
    axs[0].set_ylabel("Wins")      # Y axis name
    axs[0].grid(True, linestyle="--", alpha=0.5)           #to set grid

#text colors for labels and title

    axs[0].title.set_color("white")
    axs[0].xaxis.label.set_color("white")
    axs[0].yaxis.label.set_color("white")


#  PIE CHART
    axs[1].pie(
    game_count.values(),          # pie chart of games
    labels=game_count.keys(),       #?????????????
    autopct="%1.1f%%",
    colors=["gold", "lightcoral", "skyblue", "lightgreen"]
    )

    axs[1].set_title("Game Distribution")
  

    axs[1].title.set_color("white")

    plt.tight_layout()
    plt.show()





#button with hover effect

def drawbutton(rect,text):
    mouseposition = py.mouse.get_pos()            #gets mouse position x,y

    if rect.collidepoint(mouseposition):         # mouse pos collided with rect around image as text
        py.draw.rect(screen,hovercolor,rect,border_radius=15)
    
    else:
        py.draw.rect(screen , btncolor,rect,border_radius=15)

    draw_text(text,40,rect.centerx,rect.centery)           # calls draw text function







# function to save result in history.csv

def save_result(winner, loser, game_name):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   #datetime.now gives cuurent time and strftime is used to format it 

    file_exists = os.path.exists("history.csv")     #check if file exists

    with open("history.csv", "a") as f:          #open in append mode
        if not file_exists:          # write header if new file 
            f.write("Winner,Loser,Date,Game\n")

        f.write(f"{winner},{loser},{date},{game_name}\n")    # write all things 




#////////////////////////////////

def game_over_screen(winner, game_name):
    while True:
        screen.blit(bgimg2,(0,0))

        draw_text("GAME OVER", 75, width//2, 80)

        if winner == "DRAW":
            draw_text("It's a Draw!", 45, width//2, 140)
        elif winner == "QUIT":
            draw_text("Game Aborted", 45, width//2, 140)
        else:
            draw_text(f"Winner: {winner}", 45, width//2, 140)

       # play_btn = py.Rect(200,200,200,50)
       # menu_btn = py.Rect(200,270,200,50)
       # lead_btn = py.Rect(200,340,200,50)
        btn_width = width * 0.4
        btn_height = height * 0.08
        center_x = width * 0.5

        play_btn = py.Rect(center_x - btn_width/2, height*0.40, btn_width, btn_height)
        menu_btn = py.Rect(center_x - btn_width/2, height*0.52, btn_width, btn_height)
        lead_btn = py.Rect(center_x - btn_width/2, height*0.64, btn_width, btn_height)


        drawbutton(play_btn, "PLAY AGAIN")
        drawbutton(menu_btn, "MAIN MENU")
        drawbutton(lead_btn, "LEADERBOARD")

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if event.type == py.MOUSEBUTTONDOWN:
                pos = py.mouse.get_pos()

                if play_btn.collidepoint(pos):
                    return "play"

                if menu_btn.collidepoint(pos):
                    return "menu"

                if lead_btn.collidepoint(pos):
                    return "leaderboard"

        py.display.update()




#////////////////////////////////////
# import subprocess
# function to 
def launchgame(gamefile, game_name):
    global player1, player2

    # 1. Run game and CAPTURE winner from output
    result = subprocess.run(            # subprocess.run is used to run other file you want
        ["python", gamefile, player1, player2],   
        capture_output=True,      # capture print output
        text=True          # output as string
    )

    
    output = result.stdout.strip().split("\n")          # modifies the result by stripping and splitting it

    winner = output[-1].strip() if output else "QUIT"     # last line in output is winner


    if winner == "QUIT" or winner == "":
    # still show menu, but no saving
        choice = game_over_screen("QUIT", game_name)

        if choice == "play":
            launchgame(gamefile, game_name)

        elif choice == "menu":

            return
        elif choice == "leaderboard":

            metric = leaderboard_screen()
            os.system(f"bash leaderboard.sh {metric}")
            show_charts()
        return
    

    # handle draw case
    if winner == "DRAW":
        loser = "NONE"
    else:
        loser = player2 if winner == player1 else player1

    # Save correct result
    save_result(winner, loser, game_name)

    # Show GAME OVER SCREEN 
    choice = game_over_screen(winner, game_name)

    if choice == "play":
        launchgame(gamefile, game_name)

    elif choice == "menu":
        return

    elif choice == "leaderboard":
        
        metric = leaderboard_screen()

        print("\nSHOWING LEADERBOARD......\n")
        os.system(f"bash leaderboard.sh {metric}")

        show_charts()
        return
    




def leaderboard_screen():
    while True:
        screen.blit(bgimg2,(0,0))

        draw_text("SORT LEADERBOARD", 40, width//2, 80)

        #wins_btn = py.Rect(200,180,200,50)
        #loss_btn = py.Rect(200,250,200,50)
        #ratio_btn = py.Rect(200,320,200,50)

        btn_width = width * 0.4
        btn_height = height * 0.08
        center_x = width * 0.5

        wins_btn = py.Rect(center_x - btn_width/2, height*0.35, btn_width, btn_height)
        loss_btn = py.Rect(center_x - btn_width/2, height*0.47, btn_width, btn_height)
        ratio_btn = py.Rect(center_x - btn_width/2, height*0.59, btn_width, btn_height)


        drawbutton(wins_btn, "SORT BY WINS")
        drawbutton(loss_btn, "SORT BY LOSSES")
        drawbutton(ratio_btn, "SORT BY RATIO")

        for event in py.event.get():
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if event.type == py.MOUSEBUTTONDOWN:
                pos = py.mouse.get_pos()

                if wins_btn.collidepoint(pos):
                    return "wins"

                if loss_btn.collidepoint(pos):
                    return "losses"

                if ratio_btn.collidepoint(pos):
                    return "ratio"

        py.display.update()




# main game loop

running = True
while running:
    screen.fill(white)    #everytime in each loop frame make screen white

    screen.blit(bgimg1,(0,0))    #put img at (0,0)


    draw_text("MINI GAME HUB", int(height*0.12), width//2, height*0.12)
    draw_text(f"{player1} Vs {player2}", int(height*0.06), width//2, height*0.24)



    #ttt_btn = py.Rect(200,160,200,50)
    #oth_btn = py.Rect(200,240,200,50)    #x,y and w,h of clickable box
    #c4_btn = py.Rect(200,320,200,50)
   # music_btn = py.Rect(200,400,200,50)
   # 
    btn_width = width * 0.3
    btn_height = height * 0.08
    center_x = width * 0.5

    ttt_btn = py.Rect(center_x - btn_width/2, height*0.30, btn_width, btn_height)
    oth_btn = py.Rect(center_x - btn_width/2, height*0.45, btn_width, btn_height)
    c4_btn = py.Rect(center_x - btn_width/2, height*0.60, btn_width, btn_height)
    music_btn = py.Rect(center_x - btn_width/2, height*0.75, btn_width, btn_height)

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
                launchgame("games/tictactoe.py","TIC TAC TOE")

            
            if oth_btn.collidepoint(mouseposition):
                launchgame("games/othello.py","OTHELLO")
            
            if c4_btn.collidepoint(mouseposition):
                launchgame("games/connect4.py","CONNECT 4")

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



