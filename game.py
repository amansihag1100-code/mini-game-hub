import os               # used for file handling , history.csv

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # key value array to hide the useless lineof pygame
# hides pygame welcome message in terminal


import pygame as py    #alias
import sys             # to read command line argument , exit program safely
from datetime import datetime         #to reacord date and time of each game
import matplotlib.pyplot as plt
from collections import Counter          #counter class to count items for top5 players
import subprocess


player1 = sys.argv[1]     # which was passed in main.sh as python game.py user1 user2
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
py.display.set_caption("MINI GAME HUB")     # title of window


#image as background

bgimg1 = py.image.load("materials/5.jpg")
bgimg1 = py.transform.scale(bgimg1,(width,height))    # make the image equal to size of window

bgimg2 = py.image.load("materials/4.jpg")
bgimg2 = py.transform.scale(bgimg2,(width,height))


#setting pygame's text(font) Font as "FONT_PATH" of size
FONT_PATH = "materials/Jersey10-Regular.ttf"

def get_font(size):
    return py.font.Font(FONT_PATH, size)



textcolor = (255,255,255)

#how to write text inside buttons or to draw text and put it at x,y pos , it converts text to image 
def  draw_text(text,size,x,y,color=textcolor):
    font = get_font(size)     # get font of given size by calling get fotn function
    img = font.render(text,True,color)  #font is the variable having font or text  stored in it and  render converts text to image
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
# function to show charts of top 5 players and distribution of games played in different games using matplotlib

    #if history.csv does not exists
    if not os.path.exists("history.csv"):
        print("No history yet")
        return
#
    games = []      #empty list
    wins = []
# read history.csv and fill games and wins list
    with open("history.csv", "r") as f:       #open this file in read mode and store in varible f

        next(f) # skip first line in  history.csv

        for line in f:
            parts = line.strip().split(",")      # parts is list , strip removes extra spaces and split at ,

            if len(parts) >= 4 and parts[0] != "":   # check if line has at least 4 parts and winner is not empty
                winner = parts[0]          #winner is the first part of line which is before first comma in history.csv
                game = parts[3]

                # add item to empty list created above 
                wins.append(winner)  # winner is added to wins list and game is added to games list
                games.append(game)

                #so at end we have list of all winners and games played 

#/////////////////////////////////////////////

    # counts for top 5 players
# win_count is a list of tuples where each tuple is (winner, count) and it is sorted in descending order of count and only top 5 are taken

    win_count = Counter(wins).most_common(5)     # Counter(wins) counts the occurrences of each winner in wins list and 
                                                  # most_common(5) gives top 5 most common winners as list of tuples (winner, count)
    players = [x[0] for x in win_count] #x[0] is winner and x[1] is count in each tuple of win_count list so we create players list with winners (top 5)
    counts = [x[1] for x in win_count] # similarly we create counts list with counts of wins for top 5 players

    
    game_count = Counter(games) 
# game_count is a dictionary where key is game name and value is count of how many times that game was played 
# which is calculated by Counter class on games list which has all games played as read from history.csv



    plt.style.use("dark_background")    #set dark background in graph window 

# two graphs i n a single window
# fig is figure (whole window) , axs is array of graphs , 1 row 2 columns
#fig, axs = plt.subplots(1, 2) # this creates a figure with 1 row and 2 columns of subplots and 
# axs is an array of those subplots (graphs) which we can access by axs[0] and axs[1]

    fig,axs = plt.subplots(1, 2, figsize=(12, 5)) # figsize is size of whole window of graphs in inches (width,height)

# bar graph 

    axs[0].bar(players, counts, color=["cyan", "orange", "lime", "pink", "yellow"])  # bar graph of top 5 players and their win counts with different colors for each bar
    axs[0].set_title("Top 5 Players")
    axs[0].set_xlabel("Players")   #  X axis name
    axs[0].set_ylabel("Wins")      # Y axis name
    axs[0].grid(True, linestyle="--", alpha=0.5)           #to set grid

#text colors for labels and title

    axs[0].title.set_color("white") # to set title color
    axs[0].xaxis.label.set_color("white")
    axs[0].yaxis.label.set_color("white")


#  PIE CHART
    axs[1].pie(
    game_count.values(),          # pie chart of games
    labels=game_count.keys(),       # labels are game names which are keys of game_count dictionary and values are counts of how many times each game was played
    autopct="%1.1f%%",  # to show percentage on pie chart with 1 decimal place
    colors=["gold", "lightcoral", "skyblue", "lightgreen"]
    )

    axs[1].set_title("Game Distribution")
  

    axs[1].title.set_color("white")

    plt.tight_layout()  # to adjust spacing between graphs so that they don't overlap
    plt.show()




#the function that is called to draw buttons //////////////////
#button with hover effect as becomes big on hovering over it

def drawbutton(boxes,text):
    mouseposition = py.mouse.get_pos()            #gets mouse position x,y

    if boxes.collidepoint(mouseposition):         # mouse pos collided with rect
        py.draw.rect(screen,hovercolor,boxes,border_radius=15)        #also draw the btns boxes on screen now   #then show hover color

    else:
        py.draw.rect(screen , btncolor,boxes,border_radius=15)         #else show btn color

    draw_text(text,40,boxes.centerx,boxes.centery)           # calls draw text function to dissplay text on the boxes ke centre x,y







# function to save result in history.csv //////////

def save_result(winner, loser, game_name): # this function is called at the end of game with winner and loser as arguments which is printed by game file at the end of game and game name is used to save in history.csv
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")   #datetime.now gives cuurent time and strftime is used to format it 

    file_exists = os.path.exists("history.csv")     #check if file exists

    with open("history.csv", "a") as f:          #open in append mode
        if not file_exists:          # write header if new file 
            f.write("Winner,Loser,Date,Game\n")

        f.write(f"{winner},{loser},{date},{game_name}\n")    # write all things 
            # these all winner , loser ,game_name varibles come from launchgame function



#////////////////////////////////

def game_over_screen(winner, game_name): # this function is called at the end of game with winner as argument which is printed by game file at the end of game and game name is used to show in game over screen and save in history.csv
    while True: # game over screen loop
        screen.blit(bgimg2,(0,0))

        draw_text("GAME OVER", 75, width//2, 80) # draw text function called to show heading of game over screen (text,size,x,y)

        if winner == "DRAW":     # if winner is draw then show it's a draw
            draw_text("It's a Draw!", 45, width//2, 140)
        elif winner == "QUIT":
            draw_text("Game Aborted", 45, width//2, 140)
        else:
            draw_text(f"Winner: {winner}", 45, width//2, 140)         # else show winner's name

     
    
        btn_width = width * 0.4
        btn_height = height * 0.08
        center_x = width * 0.5

        play_btn = py.Rect(center_x - btn_width/2, height*0.40, btn_width, btn_height)
        menu_btn = py.Rect(center_x - btn_width/2, height*0.52, btn_width, btn_height)  # these are the rectangular boxes but not drawn or placed yet on screen which will be done by py.draw.rect which is called in drawbutton function
        lead_btn = py.Rect(center_x - btn_width/2, height*0.64, btn_width, btn_height)


        drawbutton(play_btn, "PLAY AGAIN")
        drawbutton(menu_btn, "MAIN MENU")           # drawbutton function called to draw rect and hover too and to place the text above the rectangle
        drawbutton(lead_btn, "LEADERBOARD")

        for event in py.event.get(): # event handling for mouse clicks and window close
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if event.type == py.MOUSEBUTTONDOWN: 
                pos = py.mouse.get_pos()

                if play_btn.collidepoint(pos):     # if play again button is clicked then return play which is stored in choice variable in launchgame function and then launchgame function is called again to start the game again with same players
                    return "play"

                if menu_btn.collidepoint(pos): # if main menu button is clicked then return menu which is stored in choice variable in launchgame function and then menu_screen function is called to show main menu
                    return "menu"

                if lead_btn.collidepoint(pos): # if leaderboard button is clicked then return leaderboard which is stored in choice variable in launchgame function and then leaderboard_screen function is called to show sorting options
                    return "leaderboard"

        py.display.update()




#/////////////////////////////////////////////////////////////////////////////////////////////////////
# import subprocess
# function the most important
def launchgame(gamefile, game_name):  #this function is called with arguments as game file and game name which is used to save result in history.csv 
    global player1, player2  # use global usernames


#//////////////////////////////////////////////////////


    # run the game file as a subprocess and capture its output
    result = subprocess.run(            # subprocess.run is used to run other file you want to run and capture its output
        ["python", gamefile, player1, player2],   # run this command in terminal to run game file with player1 and player2 as arguments
        capture_output=True,   #does not show in terminal   # capture print output but true is used to capture output as bytes and false is used to show output in terminal but we want to capture it so true
        text=True          # convert output to string 
    )    # in result variable we have output of game file which is the winner printed by game file at the end of game and we will use that to save in history.csv and show in game over screen

    # this is how winner is get
    output = result.stdout.strip().split("\n")           # modifies the result by stripping and splitting it into lines
    winner = output[-1].strip() if output else "QUIT"     # last line in output is winner 
#/////////////////////////////////


#///////////////////////////////////////////////// handeling the case if winner has quit the game in between 
    if winner == "QUIT" or winner == "":
    # still show menu, but no saving    , now game_over screen function caled with input arguments as quit,which will show game aborted screen
        choice = game_over_screen("QUIT", game_name)     #gameover _creen function called and it returns play or menu or leaderboard that is stored in choice varianle

        if choice == "play":
            launchgame(gamefile, game_name)

        elif choice == "menu":

            return
        elif choice == "leaderboard":

            metric = leaderboard_screen()                 # the output of leaderboard screen function is stored in metric 
            #it contains the sorting option user chose
            os.system(f"bash leaderboard.sh {metric}")        #then bash leaderbaord.sh 
            show_charts()          # now this function is called which displays charts
        return
    

 #//////////////////////////

    # handle draw case and loser calculated logically ////////
    if winner == "DRAW":
        loser = "NONE"
    else:
        loser = player2 if winner == player1 else player1
# this is the loser sent as varible to save_result function

    #////////////////////////

    # Save correct result
    save_result(winner, loser, game_name)

    #////////////////////


#////////////////////////////// handliing normal winner case
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
    
#?////////////////////////////////////////////////////////////////////////////



def leaderboard_screen(): 
   # this function is called when user clicks on leaderboard in game over screen and it returns the sorting option user chose which is stored in metric variable in launchgame function and then passed to bash leaderboard.sh to show sorted leaderboard
    while True:
        screen.blit(bgimg2,(0,0)) #background image 2 for leaderboard screen

        draw_text("SORT LEADERBOARD", 40, width//2, 80) #draw text function called to show heading of leaderboard screen (text,size,x,y)

     

        btn_width = width * 0.4 #
        btn_height = height * 0.08
        center_x = width * 0.5

        wins_btn = py.Rect(center_x - btn_width/2, height*0.35, btn_width, btn_height) # these are not drawn yet just the rectangle objects created with x,y and width and height
        loss_btn = py.Rect(center_x - btn_width/2, height*0.47, btn_width, btn_height)
        ratio_btn = py.Rect(center_x - btn_width/2, height*0.59, btn_width, btn_height)


        drawbutton(wins_btn, "SORT BY WINS")
        drawbutton(loss_btn, "SORT BY LOSSES") # drawbutton function called to draw these buttons and place text on it
        drawbutton(ratio_btn, "SORT BY RATIO")

        for event in py.event.get(): # event handling for mouse clicks and window close
            if event.type == py.QUIT:
                py.quit()
                sys.exit()

            if event.type == py.MOUSEBUTTONDOWN:   # when mouse button is clicked get mouse position and check which button is clicked and return the sorting option accordingly to launchgame function
                pos = py.mouse.get_pos()              

                if wins_btn.collidepoint(pos):
                    return "wins"

                if loss_btn.collidepoint(pos):
                    return "losses"

                if ratio_btn.collidepoint(pos):
                    return "ratio"

        py.display.update()




# main game loop /////////////////////////////////////////////////////////////////////

running = True
while running:
    #screen.fill(white)    #everytime in each loop frame make screen white

    screen.blit(bgimg1,(0,0))    #put bgimg1 at (0,0)  every time for ech loop


    draw_text("MINI GAME HUB", int(height*0.12), width//2, height*0.12)
    draw_text(f"{player1} Vs {player2}", int(height*0.06), width//2, height*0.24)                 #draw text function called which needs text,size of text,x,y are positions where to place 
         #player1 and player2 are recieved up in code as sys.argv[1] and 2 resp.
         #so the top text is placed now


  
    btn_width = width * 0.3
    btn_height = height * 0.08
    center_x = width * 0.5


#these are the rectangular boxes but not drawn or placed yet on screen which will be done by py.draw.rect which is called in drawbutton function
#also drawbutton function places text too on it after drawing rectangles or btns
    ttt_btn = py.Rect(center_x - btn_width/2, height*0.30, btn_width, btn_height)        # py.rect(left, top, width, height) creates a rectangle object with given dimensions and position
    oth_btn = py.Rect(center_x - btn_width/2, height*0.45, btn_width, btn_height)        # x,y and width and height of boxes
    c4_btn = py.Rect(center_x - btn_width/2, height*0.60, btn_width, btn_height)
    music_btn = py.Rect(center_x - btn_width/2, height*0.75, btn_width, btn_height)


#draw button function called to draw rect and hover too and to place the text above the rectangle
    drawbutton(ttt_btn,"TIC TAC TOE")         # first argument is the rectangle object and second is the text to be placed on it
    drawbutton(oth_btn,"OTHELLO")
    drawbutton(c4_btn,"CONNECT 4")
    drawbutton(music_btn,"MUSIC OFF" if music_on else "MUSIC ON")



#handling mouse events///////////////////////////////////////////////////////


    for event in py.event.get():      #takes event mouse clicks , keyboard , window close etc.
        if event.type == py.QUIT:          #user clicks cross
            running = False

        if event.type == py.MOUSEBUTTONDOWN:
            mouseposition = py.mouse.get_pos()           #gets mouse position where it is clicked and stored in mouseposition variable as tuple of x,y

            if ttt_btn.collidepoint(mouseposition):           #mouse collides with ttt btn then lunchgame function called with arguments as game file and game name which is used to save result in history.csv
                launchgame("games/tictactoe.py","TIC TAC TOE")
#so game_name comes from here as argument in launchgame function and then it is passed to save_result function which saves it in history.csv and then it is used in show_charts function to show distribution of games played in pie chart
            
            if oth_btn.collidepoint(mouseposition):
                launchgame("games/othello.py","OTHELLO")
            
            if c4_btn.collidepoint(mouseposition):
                launchgame("games/connect4.py","CONNECT 4")

            if music_btn.collidepoint(mouseposition):
                if music_on:
                    py.mixer.music.pause()          #turns off music if it is on and vice versa
                    music_on = False
                else:
                    py.mixer.music.unpause()
                    music_on = True



    py.display.update()          #refresh screen after every loop to show changes like button hover and music on off etc. 

#//////////////////////////////////////////////////////////////////////////////////


py.quit()   #close pygame window
sys.exit()        #exit program 


#/////////////////////////////////////////////////////////////////////////////////
