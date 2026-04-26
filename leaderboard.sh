#!/bin/bash     #run script using bash shell

FILE="history.csv"

#check if file exista or not , if not exist echo and exit with return code 1
if [ ! -f "$FILE" ]; then
    echo "No history found"
    exit 1
fi

metric=$1   #first argument stored in metric variable

echo -e "\e[31m                                                        LEADERBOARD                     \e[0m" # print  leaderboard in red 

#used -F to set comma as separator
awk -F"," '    
NR>1 {     #process each row skip header as nr>1

    game = $4
    winner = $1        #extract columns in these variables
    loser = $2

    win[game,winner]++     #increase win and lose count for winner and loser respectively
    loss[game,loser]++       

    players[winner]=1      #created a set which will contain unique players only by assigning some key(1) which makes it different from arrays
    players[loser]=1
    games[game]=1
}

END {
    for (g in games) {     # g variable used to iterate over all unique games in games array
        
        print "\n"

        printf "\n\033[33m                %s \033[0m\n", g     #prints game name in yellow
        print "\n"


        printf "\033[31m%-15s %-10s %-10s %-10s\033[0m\n", "Player", "Wins", "Losses", "Ratio"      # print columns %-15s leftlaigned width15
        for (p in players) {                        #to iterate over all players in players named array
            
            w = win[g,p] + 0
            l = loss[g,p] + 0                #get wins/losses for player p in game g , store in w,l , added plus zero to make it numeric also to avoid null

            if (w==0 && l==0) continue

            r = (l==0)? w : w/l            # calculating ratio atio equals to wins if loses =0 else ratio is win by lose

            printf "\033[32m%-15s %-10d %-10d %-10.2f\033[0m\n", p, w, l, r            #%[alignment][width][type] like - used for left align (default is right aligned) 15 is take 15 spaces and s is string d is integer   %-10.2f is two decimal floating number 
        }
    }
}
' "$FILE"