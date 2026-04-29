#!/bin/bash     #run script using bash shell

FILE="history.csv" #file which contains game history data

#check if file exista or not , if not exist echo and exit with return code 1
if [ ! -f "$FILE" ]; then
    echo "No history found"
    exit 1
fi

metric=$1   #first argument stored in metric variable which will be used to decide sorting metric in leaderboard (wins, losses or ratio)

echo -e "\e[31m                                                        LEADERBOARD                     \e[0m" # print  leaderboard in red 

#used -F to set comma as separator
awk -F"," -v metric="$metric" ' #awk script starts here , -v is used to pass shell variable metric to awk variable metric
NR>1 {     #process each row skip header as nr>1

    game = $4
    winner = $1        #extract columns in these variables
    loser = $2

    win[game,winner]++     #increase win and lose count for winner and loser respectively
    loss[game,loser]++       # win and loss are 2D arrays where first dimension is game and second dimension is player name , value is count of wins or losses for that player in that game

    players[winner]=1      #created a set which will contain unique players only by assigning some key(1) which makes it different from arrays
    players[loser]=1 
    games[game]=1   # similarly created a set for unique games played
}

#after processing all lines of file we will have win and loss counts for each player in each game and also sets of unique players and games

END { 
    for (g in games) {     # g variable used to iterate over all unique games in games array
        
        print "\n"

        printf "\n\033[33m                %s \033[0m\n", g     #prints game name in yellow
        print "\n"

        printf "\033[31m%-15s %-10s %-10s %-10s\033[0m\n", "Player", "Wins", "Losses", "Ratio"      # print columns %-15s leftlaigned width15

        # decide sorting column based on metric selected from pygame menu
        if (metric == "wins") {
        
         # if metric is wins sort by wins column which is 2nd column in temp data
        
            sort_cmd = "sort -t, -k2 -nr"        # sort command to sort by 2nd column (wins) in numeric reverse order (highest wins first)
        }                                       #-t sets comma as delimiter for sort command, -k2 specifies sorting by 2nd column, -n for numeric sort, -r for reverse order
        
        else if (metric == "losses") {
            sort_cmd = "sort -t, -k3 -nr"
        } 
        
        
        else {
            sort_cmd = "sort -t, -k4 -nr"
        }



        # temp string to store all players data before sorting


        temp = ""  # we will collect all player data for this game in temp variable as comma separated values (player,wins,losses,ratio) which will be passed to sort command for sorting based on selected metric

        for (p in players) {                        #to iterate over all players in players named array
            
            w = win[g,p] + 0     
            l = loss[g,p] + 0                #get wins/losses for player p in game g , store in w,l , added plus zero to make it numeric also to avoid null

            if (w==0 && l==0) continue

            r = (l==0)? w : w/l            # calculating ratio atio equals to wins if loses =0 else ratio is win by lose

            # store clean comma separated data (important for sorting)
            temp = temp sprintf("%s,%d,%d,%.2f\n", p, w, l, r)   
        }  #sprintf is used to format the string with player name, wins, losses and ratio in comma separated format which will be stored in temp variable for sorting

        # run sorting command on collected data
        cmd = "echo \"" temp "\" | " sort_cmd      # pipe the temp data to sort command for sorting based on selected metric and store the command in cmd variable

        # read sorted output line by line
        while ((cmd | getline line) > 0) {   #getline reads output of cmd line by line into variable line until no more lines are left (cmd | getline line) > 0 means while there are lines to read from cmd output

            if (line == "") continue           

            split(line, parts, ",")     # split the sorted line into parts array using comma as delimiter so parts[1] is player name, parts[2] is wins, parts[3] is losses and parts[4] is ratio

            # print nicely formatted + colored output AFTER sorting
            printf "\033[32m%-15s %-10d %-10d %-10.2f\033[0m\n", parts[1], parts[2], parts[3], parts[4]
        }

        close(cmd) 
    }
}
' "$FILE"