from os import system
from random import choice
from math import sqrt

#global grid_dim, rows, cols
#global grid_area, grid
rows, cols = 0, 0 # rows, column
grid_dim = (0,0)
grid_area = 0
grid = []

#global players
players = [] # 5 Player Max
class player:
    def __init__(self,name=None, isbot=False):

        if not isbot:
            if name is not None and name != "": # valid custom
                self.__name = name
                self.__symbol = self.__createSymbol()

            else: # dafault
                plr_num = len(players)+1
                self.__name = f"Player {plr_num}"
                self.__symbol = f"P{plr_num}"
        else:
            self.__name = "@Bot"
            self.__symbol = self.__createSymbol()

        self.isbot = isbot
        self.__score = 0

    def __createSymbol(self) -> str:
        name = self.__name
        dupes = 0
        for plr in players:
            if plr.name == name:
                dupes += 1

        name = name[0] + (str(dupes) if dupes != 0 else "")
        return name


    def get_name(self) -> str:
        return self.__name

    def get_symbol(self) -> str:
        return self.__symbol

    def get_score(self) -> int:
        return self.__score

    def add_point(self):
        self.__score += 1

    name = property(get_name)
    symbol = property(get_symbol)
    score = property(get_score)

    def __repr__(self) -> str:
        return f"{self.name} ({self.__symbol})"



# Win identities
winningMoves = None
can_diagonal = True # defualt is true

rounds = 0

def getWinningMoves() -> dict:
    """Calculate winning moves onto a map

        Winning moves include:\n
            'horizontal' (<columns> across)\n
            'vertical' (<rows> up or down)\n
            'diagonal' (<columns> from top corner to bottom corner)\n
    """

    global row,col
    global can_diagonal
    row,col = 0,0   

    _moves = []
    

    # Horizontal
    while row < rows:
        start = (row*cols)
        end = start+cols
        _moves.append(list(range(start,end)))

        row += 1

    # Vertical
    col = 0
    vertices = []
    while col < cols:
        row = 0
        while row < rows:
            vertices.append(col+(cols*row))
            row += 1


        _moves.append(list(vertices)) # copy vertices
        vertices.clear()

        col += 1

    # Diagonal
    if can_diagonal: # Can check for diagonals
        global diags, idiags
        diags, idiags = [], []

        row = 0
        col = 0
        while row < rows:
            diags.append(col+(cols*row))
            inverse = (rows-1)-row
            idiags.append(col+(cols*inverse))
            col += 1
            row += 1

        _moves.append(diags)
        _moves.append(idiags)

    return _moves

def _cls():
    system("cls")

ready = False

max_players = 0 # == math.sqrt(grid_area)/2
def setup():
    global rows, cols, grid_dim, grid_area
    global grid
    global winningMoves, can_diagonal
    global rounds, players, max_players
    global ready

    _cls()
    print("Ultimate Tic-Tac-Toe | SETUP")

    # Simply using returns to refresh setup info in console for each step
    print(f"\nBoard Dimensions: [{rows if rows != 0 else '?'} x {cols if cols != 0 else '?'}]")
    if rows == 0:
        entry = input("\n-> Enter dimension 1 (3..10)\n<- ")
        if entry.isdigit():
            entry = int(entry)
            if entry >= 3 and entry <= 10:
                rows = entry
                return
            else:
                print("Invalid entry! Please try again!")
                return
        else:
            print("Invalid entry! Please try again!")
            return
            
    if cols == 0:
        entry = input("\n-> Enter dimension 2 (3..10)\n<- ")
        if entry.isdigit():
            entry = int(entry)
            if entry >= 3 and entry <= 10:
                cols = entry
                return
            else:
                print("Invalid entry! Please try again!")
                return
        else:
            print("Invalid entry! Please try again!")
            return

    if rows != cols:
        can_diagonal = False

    if max_players == 0: # max_players was not set | Will fail if rows & cols are < 3
        max_players = int(sqrt(rows*cols)) # Should work

    print(f"""
    Game Details:
        Rounds: {rounds if rounds != 0 else '?'}
        Diagonal wins: {'Enabled' if can_diagonal else 'Disabled'}
        Players ({len(players)} out of {max_players}): 
            {', '.join(list(map(str,players)))}
    """)

    if rounds == 0:
        entry = input("\n-> How many rounds to play? (1+)\n<- ")
        if entry.isdigit():
            entry = int(entry)
            if entry >= 1:
                rounds = entry
                return
            else:
                print("Invalid entry! Please try again!")
                return
        else:
            print("Invalid entry! Please try again!")
            return

    def addPlayer():
        name = input(f"\n-> Enter name for Player {len(players)+1} or nothing for default. (Enter 'bot' for AI)\n<- ")
        name = name.strip()
        if name.isalpha() or name == "":
            players.append(player(name, isbot=(name.lower() == "bot")))
            return True

    if players == []:
        if not addPlayer():
            print("Invalid entry! Please try again!")
        
        return

    player_spots_left = len(players) < max_players
    if player_spots_left:
        entry = input(f"\n-> Add another player? [y/n]\n<- ")
        if entry == "y":
            if not addPlayer():
                print("Invalid entry! Please try again!")
            
            return

        elif entry != "n":
            print("Invalid entry! Please try again!")
            return 
        


    grid_area = (rows*cols)
    grid_dim = (rows,cols)
    grid = [None]*grid_area

    winningMoves = getWinningMoves()
    ready = True

def aiMove(bot) -> int:
    wins_for_bot = []

    def hasNone(lst: list) -> bool:
        return any(elem is None for elem in lst)

    def hasWin(lst: list) -> bool:
        oneleft = len(lst)-1
        global non_null
        non_null = None
        for elem in lst:
            if elem is not None:
                non_null = elem
                break

        return (lst.count(non_null) == oneleft)

    for scan in winningMoves:
        read = list(map(lambda i: grid[i], scan))
        if hasNone(read) and hasWin(read):
            readi = read.index(None)
            return scan[readi]
        
        if all((elem is None or elem is bot.symbol for elem in read)):
            wins_for_bot.append(scan)

    if wins_for_bot != []:
        best_chance = wins_for_bot[0]
        for win in wins_for_bot:
            if len(win) > len(best_chance):
                best_chance = win
        
        if best_chance != []:
            filtered_bc = list(filter(lambda i: grid[i] is None, best_chance))
            return choice(filtered_bc)

    # random choice for bot
    available = list(filter(lambda i: grid[i] is None, range(grid_area)))
    return choice(available)


def drawGame(round: int, plr: player = None) -> str:
    """Clears console, and outputs the board in string format"""

    _cls()

    print(f"[Round {round} of {rounds}]")
    print("\n")
    if plr is not None:
        print(f"{plr.name} has {plr.score} points\n")
    build = str()

    Xlen = len(str(len(grid))) # length of biggest number
    box_spacing = Xlen + 2 # add spacing on both sides
    h_line = '-' #

    for i,move in enumerate(grid):
        move = str(i+1) if move == None else move
        if i != 0 and i % grid_dim[0] == 0:
            print(f"{build}")
            print(h_line*len(build))
            build = ""

        if len(build) > 0:
            build += f"|{move:^{box_spacing}}"
        else:     
            build += f"{move:^{box_spacing}}"

        


    if build != "": 
        print(build)
        build = str()

    print("\n")


def checkWinner() -> player:
    """Checks winning move from a player"""

    for plr in players:
        for scan in winningMoves:
            read = list(map(lambda i: grid[i], scan)) 
            if all(symbol is plr.symbol for symbol in read): # p1 wins
                return plr

def checkDraw() -> bool:
    """Checks if no moves are left"""
    # Check tie
    moves_left = list(filter(lambda move: move == None, grid))
    if not moves_left: # if moves_left not empty
        return True
    
    return False # necessary?


def validateMove(move : int = None) -> bool:
    """Checks if a move is on the board and unique"""

    if move and move >= 1 and move <= grid_area: # in grid
        if not grid[move-1]:    # if gridspace is None
            return True
        else:
            print(f"{move} is taken.")
    else:
        print(f"{move} is not in range (1-{grid_area}).")
        
    return False
            

def play():
    """Play specified rounds of tic-tac-toe!"""

    global grid
    global rounds
    round = 1
    while round <= rounds:
        for plr in players:
            drawGame(round, plr)
            if(plr.isbot): # bot turns
                move = aiMove(plr)
                grid[move] = plr.symbol
            else:
                while True:
                    move = input(f"{plr.name}'s Turn\n-> To make your move, enter a number on the board.\n<- ")
                    if move.isdigit():
                        move = int(move)
                        if validateMove(move):
                            grid[move-1] = plr.symbol
                            break
                    else:
                        print(f"'{move}' is not a number.")
                        drawGame(round, plr)

            if plr == checkWinner():
                plr.add_point()
                drawGame(round, plr)
                print(f"{plr} won!")
                input("Press 'enter' to continue...")

                grid = [None]*grid_area
                round += 1
                break
            elif(checkDraw()):
                drawGame(round, plr)
                print(f"It's a draw!")
                input("Press 'enter' to continue...")

                grid = [None]*grid_area
                round += 1
                break


print("Welcome to Ultimate Tic-Tac-Toe!")
input("Press 'enter' to continue...")

while not ready:
    setup()

input("\nSetup Complete!\nPress 'enter' to start...")
_cls()
play()

            

