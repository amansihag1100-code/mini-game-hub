
#!/bin/bash    # tells system to run this script using bash shell

touch users.tsv     #create file if not exist

echo -e "\e[31m            			  	WELCOME TO MINI GAME HUB                \e[0m"   # welcome message echo # -e enables escape sequences, \e[31m sets red color, \e[0m resets color
echo""      #space for next line




function_to_login_user() {          #function defined 

        while true          #infinite loop until thwo players sucessfully logins or register
        do
                echo -n -e " \n \U1F539 ENTER USERNAME: "  # -n prevents input taking from new line
                read username                #read means take input from user(notfile) and store it in a username variable
                echo ""

                echo -n -e " \n \U1F539 ENTER PASSWORD: " 
				read -s password   # -s hides input , -p helps to take input on same line , -e , -n
                echo ""

                hashed_password=$( echo -n "$password" | sha256sum | cut -d ' ' -f1)      # echo -n - prints password without newline
                # sha256sum , hashes password
                # cut , removes extra text, keeps only hash value


# to check if user exist or new registration required

                user_found=0

                while IFS=$'\t' read  u p         #read users.tsv by using tab as delimiter
                # IFS sets delimiter as TAB
                # reads users.tsv line by line into variables u(username) and p(password hash)

                do
                        if [[ $u == $username ]] #spaces mmandatory username match
                        then
                                user_found=1  # user exists
                                echo ""

                                if [[ $p == $hashed_password ]]     #now password also matches
                                then
                                        
                                        echo -e "\e[32m LOGIN SUCCESSFUL \e[0m"

                                        return         #exit
                                else
                                        echo -e "\e[31m WRONG PASSWORD ,TRY AGAIN \e[0m"
                                        echo ""
                                        break   # break inner loop, retry login
                                fi
                        fi
                done < users.tsv #take inputs u and p from this file

                if [ $user_found -eq 0 ]       #user not found so register
                then
						echo ""
                        echo -n -e "\e[31m USER NOT FOUND. WANT TO REGISTER ?  TYPE (Yes/No) : \e[0m"
                        read ans
                        echo""


                        if [[ $ans == "Yes" || $ans == "y" || $ans == "Y" || $ans == "yes" || $ans == "YES" ]]
                        then
                                echo -e "$username\t$hashed_password">> users.tsv         #store both with tab space separated  # append new user to file with tab separator
                                echo -e "\e[32m REGISTRATION SUCCESSFUL \e[0m"

                                return
                        fi
                fi
        done
}




while true     # loop until valid different users
do

        echo""
        echo -e "\e[33m LOGIN PLAYER 1 \e[0m"
        function_to_login_user        # call function for player 1 login
        user1=$username          #save username of player1

        echo""
        echo -e "\e[33m LOGIN PLAYER 2 \e[0m"
        function_to_login_user    # call function again for player 2
        user2=$username     #player2 save


        if [ "$user1" = "$user2" ]
        then
                echo""
                echo -e "\e[31m USERNAMES SHOULD BE DIFFERENT, TRY AGAIN \e[0m"
                continue   # restart loop instead of exiting
        fi

        break  # valid users so exit loop

done

echo ""

echo -e "\e[32m STARTING GAME .... \e[0m"

python game.py "$user1" "$user2" # pass usernames and game.py as arguments to python program



