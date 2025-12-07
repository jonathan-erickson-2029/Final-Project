import pygame
import random
import sys

pygame.init()

#screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Street Dice Game")
clock = pygame.time.Clock()

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GOLD = (166, 124, 0)
BLUE = (0, 0, 255)
PURPLE = (177, 156, 217)

#fonts
font = pygame.font.Font(None, 28)
small_font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 50,)

players = {"player1":0, "computer":0}
balance = 20.0

#dice
def roll():
    return random.randint(1,6)

def droll():
    d1 = random.randint(1,6)
    d2 = random.randint(1,6)
    return d1, d2

#drawing
def draw_die(x, y, size, value):
    #actual die
    pygame.draw.rect(screen, WHITE, (x, y, size, size), border_radius=10)
    #black outline of die
    pygame.draw.rect(screen, BLACK, (x, y, size, size), 3, border_radius=10)
    #center of die x, y
    cx = x + size // 2
    cy = y + size // 2
    #how far from center of die
    offset = size // 4
    #how big each dot is
    r = size // 10
    #dictionary for positions of dots depend on what number is rolled
    positions = {
        1: [(cx, cy)],
        2: [(cx - offset, cy - offset), (cx + offset, cy + offset)],
        3: [(cx - offset, cy - offset), (cx, cy), (cx + offset, cy + offset)],
        4: [(cx - offset, cy - offset), (cx + offset, cy - offset), (cx - offset, cy + offset), (cx + offset, cy + offset)],
        5: [(cx - offset, cy - offset), (cx + offset, cy - offset), (cx, cy), (cx - offset, cy + offset), (cx + offset, cy + offset)],
        6: [(cx - offset, cy - offset), (cx + offset, cy - offset), (cx - offset, cy), (cx + offset, cy), (cx - offset, cy + offset), (cx + offset, cy + offset)],
    }
    for (px, py) in positions[value]:
        pygame.draw.circle(screen, BLACK, (px, py), r)

def draw_screen(lines, dice_values=None, highlight=None, extra_bottom=None):
    screen.fill(PURPLE)
    global balance, players
    #title
    title = big_font.render("Jon's Online Street Dice", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))
    #display balance
    balance_text = font.render(f"Balance: {balance:.2f} tokens", True, GOLD)
    screen.blit(balance_text, (30, 80))
    #display who is the Shooter
    shooter_text = "Shooter: You" if players["player1"] == 1 else "Shooter: Player 2"
    shooter_surf = font.render(shooter_text, True, WHITE)
    screen.blit(shooter_surf, (30, 120))
    #red message if incorrect input is put in 
    if highlight:
        hl_surf = small_font.render(highlight, True, RED)
        screen.blit(hl_surf, (30, HEIGHT - 80))
    #text
    y = 170
    for line in lines:
        text_surf = small_font.render(line, True, WHITE)
        screen.blit(text_surf, (30, y))
        y += 28
    #dice drawing
    if dice_values is not None:
        d1, d2 = dice_values
        size = 90
        spacing = 40
        total_width = 2 * size + spacing
        start_x = WIDTH // 2 - total_width // 2
        y_dice = 320
        draw_die(start_x, y_dice, size, d1)
        draw_die(start_x + size + spacing, y_dice, size, d2)
    #tells player to click SPACE to continue at each stage of the game
    if extra_bottom:
        hint_surf = small_font.render(extra_bottom, True, WHITE)
        screen.blit(hint_surf, (30, HEIGHT - 50))
    #update screen
    pygame.display.flip()

#stop program if you close out the window
def quitting():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

#makes it so only if you press SPACE or ENTER or click the game will continue
def continuing(lines, dice_values=None, highlight=None, extra="Press SPACE or click to continue"):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                return
        draw_screen(lines, dice_values=dice_values, highlight=highlight, extra_bottom=extra)
        clock.tick(60)

#the "dice rolling" animation (just goes through multiple faces of the die)
def animate_dice(final_d1, final_d2, lines_before_roll):
    duration_ms = 700
    start = pygame.time.get_ticks()
    while True:
        now = pygame.time.get_ticks()
        if now - start > duration_ms:
            break
        temp_d1 = roll()
        temp_d2 = roll()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_screen(lines_before_roll, dice_values=(temp_d1, temp_d2), extra_bottom="Rolling...")
        clock.tick(60)
    #show final result for a bit
    draw_screen(lines_before_roll + [f"Roll: {final_d1 + final_d2}"], dice_values=(final_d1, final_d2))
    pygame.time.delay(600)

#allows you to enter your bet when asked for
def get_bet():
    global balance
    bet_str = ""
    error_msg = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    bet_str = bet_str[:-1]
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    #convert to float and validate
                    if bet_str.strip() == "":
                        error_msg = "You must enter a number."
                    else:
                        try:
                            bet = float(bet_str)
                            if bet <= 0:
                                error_msg = "Bet must be positive."
                            elif bet > balance:
                                error_msg = "You do not have enough tokens."
                            else:
                                return bet
                        except ValueError:
                            error_msg = "Invalid input."
                else:
                    #only accept digits and decimal point
                    if event.unicode.isdigit() or event.unicode == ".":
                        if len(bet_str) < 10:
                            bet_str += event.unicode
        lines = ["You are the Shooter.", "Enter your bet into the pot and press ENTER.", f"Bet: {bet_str}"]
        draw_screen(lines, highlight=error_msg)
        clock.tick(60)

#for when the player reaches the goal of 200, asks if they want to keep playing or not
def yes_no(question):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                if event.key == pygame.K_n:
                    return False
        lines = [question, "Press Y for Yes, N for No."]
        draw_screen(lines)
        clock.tick(60)

#game functions
def position():
    global players
    while True:
        continuing(["To decide who will start as the Shooter", "You and Player 2 will each roll one die."])
        p1 = roll()
        p2 = roll()
        #no ties
        while p1 == p2:
            draw_screen([f"You rolled a {p1}. Player 2 rolled a {p2}.", "It is a tie. Rolling again..."], dice_values=(p1, p2))
            pygame.time.delay(900)
            p1 = roll()
            p2 = roll()
        continuing([f"You rolled a {p1}. Player 2 rolled a {p2}."], dice_values=(p1, p2))
        if p1 > p2:
            players["player1"] = 1
            players["computer"] = 0
            continuing(["You are the Shooter."])
        else:
            players["player1"] = 0
            players["computer"] = 1
            continuing(["Player 2 is the Shooter."])
        return players["player1"]

#game function for when you are the Shooter
def shooter():
    global balance, players
    bet = get_bet()
    balance -= bet
    pot = bet * 2
    continuing([f"You placed {bet:.2f} tokens into the pot.", f"New balance: {balance:.2f}", "Press SPACE to roll two dice for the comeout."])
    d1, d2 = droll()
    comeout = d1 + d2
    animate_dice(d1, d2, ["Shooter comeout roll..."])
    if comeout in (7, 11):
        balance += pot
        continuing([f"You rolled a {comeout}. You win!", f"Balance: +{pot:.2f}", f"New balance: {balance:.2f}"], dice_values=(d1, d2))
    elif comeout in (2, 3, 12):
        continuing([f"You rolled a {comeout}. You lose.", f"Balance: {balance:.2f}"], dice_values=(d1, d2))
        players["player1"] = 0
        players["computer"] = 1
    else:
        point = comeout
        continuing([f"You rolled a {comeout}. The point is {point}.", "Roll this number again before a 7 to win."], dice_values=(d1, d2))
        roll2 = 0
        while roll2 != point and roll2 != 7:
            continuing([f"The Point is {point}.", "Press SPACE to roll again."])
            d1, d2 = droll()
            roll2 = d1 + d2
            animate_dice(d1, d2, [f"Rolling for point {point}..."])
            if roll2 == point:
                balance += pot
                continuing([f"You rolled {roll2}. You hit the point.", f"You win +{pot:.2f} tokens.", f"Balance: {balance:.2f}"], dice_values=(d1, d2))
            elif roll2 == 7:
                continuing([f"You rolled 7 before the point.", "You lose.", f"Balance: {balance:.2f}"], dice_values=(d1, d2))
                players["player1"] = 0
                players["computer"] = 1
            else:
                continuing([f"You rolled {roll2}.", "Roll again..."], dice_values=(d1, d2))

#game function for when the computer is the Shooter
def target():
    global balance, players
    if balance < 2:
        bet = balance
    else:
        bet = random.randint(1, int(balance // 2))
    continuing([f"Player 2 bet {bet:.2f} tokens.", "You must match the bet."])
    balance -= bet
    pot = bet * 2
    continuing([f"You placed {bet:.2f} tokens into the pot.", f"New balance: {balance:.2f}", "Player 2 rolls two dice for the comeout."])
    d1, d2 = droll()
    comeout = d1 + d2
    animate_dice(d1, d2, ["Player 2 comeout roll..."])
    continuing([f"Player 2 rolled a {comeout}.", f"The comeout is {comeout}."], dice_values=(d1, d2))
    if comeout in (7, 11):
        continuing(["You lose this round.", f"Balance: {balance:.2f}"], dice_values=(d1, d2))
    elif comeout in (2, 3, 12):
        balance += pot
        continuing(["You win this round.", f"Balance: +{pot:.2f}", f"New balance: {balance:.2f}"],dice_values=(d1, d2))
        players["player1"] = 1
        players["computer"] = 0
    else:
        point = comeout
        continuing([f"The Point is {point}.", "Player 2 must roll this again before a 7 to win."], dice_values=(d1, d2))
        roll2 = 0
        while roll2 != point and roll2 != 7:
            continuing([f"The Point is {point}.", "Press SPACE to let Player 2 roll again."])
            d1, d2 = droll()
            roll2 = d1 + d2
            animate_dice(d1, d2, [f"Player 2 rolling for point {point}..."])
            if roll2 == point:
                continuing([f"Player 2 rolled {roll2}. They hit the point.", "You lose this round.", f"Balance: {balance:.2f}"], dice_values=(d1, d2))
            elif roll2 == 7:
                balance += pot
                continuing(["Player 2 rolled 7 before the point.", "You win this round.", f"Balance: +{pot:.2f}", f"New balance: {balance:.2f}"], dice_values=(d1, d2))
                players["player1"] = 1
                players["computer"] = 0
            else:
                continuing([f"Player 2 rolled {roll2}.", "Rolling again..."], dice_values=(d1, d2))

#this function runs the game with all above integrated in here
def game():
    global balance, players
    #intro screen
    continuing(["You are Player 1.", "You are competing against Player 2.", "Your starting balance is 20.0 tokens.", "Your goal is to reach 200 tokens."])
    position()
    #main game loop
    running = True
    while running and balance > 0:
        if players["player1"] == 1:
            shooter()
        else:
            target()

        if balance > 200:
            choice = yes_no(f"You have reached {balance:.2f} tokens. Do you want to keep playing?")
            if not choice:
                running = False
    #game over screen
    continuing([f"The game is over.", f"Your final balance is {balance:.2f} tokens.", "Thank you for playing."])
    pygame.quit()
    sys.exit()

game()



