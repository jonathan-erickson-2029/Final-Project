#FinalProject
import random

def roll():
    return random.randint(1,6)

def droll():
    return (random.randint(1,6)) + (random.randint(1,6))

print("You are Player 1.")
print("You are competing against Player 2.")
players = {"player1":0, "computer":0}
#1 = the shooter
#0 = not the shooter
print("Your starting balance is 20.0 tokens, your goal is to get to 200 tokens.")
balance = 20.0
bet = 0.0

def position():
    input("Press enter to roll a dice.")
    p1 = roll()
    p2 = roll()
    if p1 == p2:
        while p1 == p2:
            print("You rolled a", p1, " Player 2 rolled a", p2)
            print("Rolling again...")
            p1 = roll()
            p2 = roll()
            print("You rolled a", p1, " Player 2 rolled a", p2)
    else:
        print("You rolled a", p1, " Player 2 rolled a", p2)
    if p1 > p2:
        print("You are the Shooter.")
        players["player1"] = 1
        players["computer"] = 0
    else:
        print("Player 2 is the Shooter.")
        players["player1"] = 0
        players["computer"] = 1
    return players["player1"]

def shooter():
    global balance
    while True:
        bet_str = input("Place your bet into the pot: ")
        if bet_str.strip() == "":
            print("You must enter a number.")
            continue
        if not bet_str.replace(".", "", 1).isdigit():
            print("Invalid input. Enter a number.")
            continue
        bet = float(bet_str)
        if bet <= 0:
            print("Bet must be positive.")
            continue
        if bet > balance:
            print("You do not have enough tokens.")
            continue
        break
    balance -= bet
    print("-",bet,"New balance:", balance)
    pot = bet*2
    input("Roll two dice, press enter.")
    comeout = droll()
    print("You rolled a", comeout)
    print("The comeout is", comeout)
    if comeout == 7 or comeout == 11:
        print("You win! Balance: +", pot)
        balance = balance + pot
        print("Balance:", balance)
        players["player1"] = 1
        players["computer"] = 0
    elif comeout == 2 or comeout == 3 or comeout == 12:
        print("You lose! Balance:", balance)
        players["player1"] = 0
        players["computer"] = 1
    else:
        point = comeout
        print("The point is", point, "roll this number before a 7 to win.")
        roll2 = 0
        while roll2 != point and roll2 != 7:
            input("Roll two dice, press enter.")
            roll2 = droll()
            print("You rolled a", roll2,)
            if roll2 == point:
                print("You win! Balance: +", pot)
                balance = balance + pot
                print("Balance:", balance)
                players["player1"] = 1
                players["computer"] = 0
            elif roll2 == 7:
                print("You lose! Balance:", balance)
                players["player1"] = 0
                players["computer"] = 1
            else:
                print("Roll again...")

def target():
    global balance
    if balance < 2:
        bet = balance
    else:
        bet = random.randint(1,int(balance//2))
    print("Player 2 bet", bet, "tokens.")
    input("Press enter to place your tokens into the pot.")
    balance -= bet
    print("-", bet,"Balance:", balance)
    pot = bet*2
    print("Player 2 is rolling two dice...")
    comeout = droll()
    print("Player 2 rolled a", comeout)
    input("Press enter to continue.")
    print("The comeout is", comeout)
    if comeout == 7 or comeout == 11:
        print("You lose! Balance:", balance)
        players["player1"] = 0
        players["computer"] = 1
    elif comeout == 2 or comeout == 3 or comeout == 12:
        print("You win! Balance: +", pot)
        balance = balance + pot
        print("Balance:", balance)
        players["player1"] = 1
        players["computer"] = 0
    else:
        point = comeout
        print("The point is", point, "Player 2 has to roll this number before a 7 to win.")
        input("Press enter to continue.")
        roll2 = 0
        while roll2 != point and roll2 != 7:
            roll2 = droll()
            print("Player 2 rolled a", roll2, "!")
            if roll2 == point:
                print("You lose! Balance:", balance)
                players["player1"] = 0
                players["computer"] = 1
            elif roll2 == 7:
                print("You win! Balance: +", pot)
                balance = balance + pot
                print("Balance:", balance)
                players["player1"] = 1
                players["computer"] = 0
            else:
                print("Player 2 is rolling again...")
                input("Press enter to continue")

position()
while balance > 0:
    if players["player1"] == 1:
        shooter()
    else:
        target()
    if balance > 200:
        print("You have reached", balance, "tokens!!!")
        path = input("Do you wish to continue? (Y/N)")
        if path == "N":
            break
        else:
            print("Ok, play again.")
print("The game is over. You final balance is", balance)
            




