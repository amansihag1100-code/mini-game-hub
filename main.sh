#!/bin/bash

echo " MINI GAME HUB "

# PLAYER 1

read -p "Enter Player 1 Username : " user1

read -s -p "Enter Password : " password1

echo ""

# PLAYER 2

read -p "Enter Player 2 Username: " user2 

read -s -p "Enter password : " password2
echo ""

# PREVENT SAME USER REGISTRATION

if [ "$user1" == "$user2" ]; then
	echo "Players must be different!"
	exit 1
fi

echo "LOGGING IN ....."

#let user1 and user2 enter in game.py

python3 game.py "$user1" "$user2"


