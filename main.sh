#!/bin/bash

echo "WELCOME TO MINI GAME HUB"
echo""
echo " WANT THE CODE FOR THIS GAME , THEN SCAN THIS QR CODE OR GO TO MY REPO GIVEN BELOW AND MAKE YOUR OWN "
# BUT SORRY MY REPO IS PRIVATE 
qrencode -t ANSIUTF8 "https://github.com/amansihag1100-code/mini-game-hub"
echo""
echo "OR"
echo ""
echo "REPO ADDRESS :  https://github.com/amansihag1100-code/mini-game-hub "


function_to_login_user(){

	while true
	do
		echo " ENTER USERNAME: "
		read username
		echo ""

		echo " ENTER PASSWORD: "
		read password
		echo ""

		hashed_password=$( echo -n "$password" | sha256sum | cut -d ' ' -f1)

		user_found=0

		while read u p 
		do
			if [ "$u" = "$username" ]
			then 
				user_found=1

				if [ "$p" = "$hashed_password" ]
				then
					echo " LOGIN SUCCESSFUL "
				
					return
				else
					echo " WRONG PASSWORD ,TRY AGAIN "
					break
				fi
			fi
		done < users.tsv

		if [ "$user_found" = "0" ]
		then
			echo " USER NOT FOUND. WANT TO REGISTER ? ( TYPE (Yes/No))"
			read ans
			echo""


			if [ "$ans" = "Yes" ]
			then
				echo "$username $hashed_password">> users.tsv
				echo "REGISTRATION SUCCESSFUL "
				
				return
			fi
		fi
	done
}

echo""
echo " LOGIN PLAYER 1"
function_to_login_user
user1=$username

echo""
echo " LOGIN PLAYER 2"
function_to_login_user
user2=$username


if [ "$user1" = "$user2" ]
then
	echo""
	echo " USERNAMES SHOULD BE DIFFERENT"
	exit
fi

echo " STARTING GAME .... "

python3 game.py "$user1" "$user2"



						
