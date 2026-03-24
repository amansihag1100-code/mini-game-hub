import sys

player1 = sys.argv[1]
player2 = sys.argv[2]

print("WELCOME TO MINI GAME HUB!")

print(f"Player1 : {player1}")
print(f"player2 : {player2}")

while True:
    print("\n Select a game :")
    print("1. Tic Tac Toe ")
    print("2. Connect Four")
    print("3. Othello")
    print("4. Exit")

    choice = input("Enter choice number: ")

    if choice == "1":
        print("Starting Tic Tac Toe.....")
    
    elif choice =="2":
              print("Starting Connect Four.....")
    elif choice =="3":
              print("Starting Othello.....")
    elif choice =="4":
              print("GoodBye!")
              break
    else:
              print("INVALID CHOICE NUMBER!")


