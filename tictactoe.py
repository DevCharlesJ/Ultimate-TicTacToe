from os import system
from random import uniform,choice
from math import sqrt
from player import Player

class tttConfig():
    def __init__(self):
        self.grid_dim = (self.rows, self.cols) = 0, 0 # rows, column
        self.grid_area = self.rows*self.cols
        self._can_diagonal = False # defualt is true

        self.rounds = 0

        
        self._max_players = 0 # f(grid_area) = math.sqrt(grid_area)/2

    

class Instance():
    def __init__(self, config=None):
        self.config = config if config and isinstance(config, tttConfig) else tttConfig()

        self.grid = []
        self.players = []

        # Calculated wins
        self.winningMoves = None

        # Instance is ready after complete setup
        self.__ready = False

    def isReady(self):
        return self.__ready




    def getWinningMoves(self) -> dict:
        """Get winning moves calculated from the grid

            Winning moves include:\n
                'horizontal' (<columns> across)\n
                'vertical' (<rows> up or down)\n
                'diagonal' (<columns> from top corner to bottom corner)\n
        """

        moves = []
        
        row, col = 0, 0
        
        # Horizontal
        while row < self.config.rows:
            start = (row*self.config.cols)
            end = start+self.config.cols
            moves.append(list(range(start,end)))

            row += 1

        # Vertical
        col = 0
        vertices = []
        while col < self.config.cols:
            row = 0
            while row < self.config.rows:
                vertices.append(col+(self.config.cols*row))
                row += 1


            moves.append(list(vertices)) # copy vertices
            vertices.clear()

            col += 1

        # Diagonal
        if self.config._can_diagonal: # Can check for diagonals
            diags, idiags = [], []

            row = 0
            col = 0
            while row < self.config.rows:
                diags.append(col+(self.config.cols*row))
                inverse = (self.config.rows-1)-row
                idiags.append(col+(self.config.cols*inverse))
                col += 1
                row += 1

            moves.append(diags)
            moves.append(idiags)

        return moves

    def _cls(self):
        system("cls")

    def _out(self, output):
        print(output)

    def _roundinfo_out(self, output):
        print(output)

    def _board_out(self, output):
        print(output)

    def _in(self, prompt):
        return input(prompt)

    def addPlayer(self):
        name = self._in(f"\n-> Enter name for Player {len(self.players)+1} or nothing for default. (Enter 'bot' for AI)\n<- ")
        name = name.strip()

        if name.isalpha() or name == "":
            isBot = name.lower() == "bot"
            if isBot:
                difficulty = self._in(f"\n-> Enter difficulty level (1..3)\n<- ")
                if difficulty.isdigit():
                    difficulty = int(difficulty)
                    if difficulty >= 1 and difficulty <= 3:
                        plr = Player(self,name, isbot=isBot)
                        plr.bot_difficulty = difficulty
                        self.players.append(plr)
                        return True
                
                return

            self.players.append(Player(self,name, isbot=isBot))
            return True

    def setup(self):
        self._cls()
        self._out("Ultimate Tic-Tac-Toe | SETUP")

        # Simply using returns to refresh setup info in console for each step
        self._out(f"\nBoard Dimensions: [{self.config.rows if self.config.rows != 0 else '?'} x {self.config.cols if self.config.cols != 0 else '?'}]")
        if self.config.rows == 0:
            entry = self._in("\n-> Enter the number of rows (3..10)\n<- ")
            if entry.isdigit():
                entry = int(entry)
                if entry >= 3 and entry <= 10:
                    self.config.rows = entry
                    return

            self._out("Invalid entry! Please try again!")
            return
                
        if self.config.cols == 0:
            entry = self._in("\n-> Enter the number of columns (3..10)\n<- ")
            if entry.isdigit():
                entry = int(entry)
                if entry >= 3 and entry <= 10:
                    self.config.cols = entry
                    return

            self._out("Invalid entry! Please try again!")
            return

        if self.config.rows != self.config.cols: # redundant logic for now
            self.config._can_diagonal = False

        if self.config._max_players == 0: # max_players was not set | May fail if rows & cols are < 3
            self.config._max_players = int(sqrt(self.config.rows*self.config.cols))

        self._out(f"""
        Game Details:
            Rounds: {self.config.rounds if self.config.rounds != 0 else '?'}
            Diagonal wins: {'Enabled' if self.config._can_diagonal else 'Disabled'}
            Players ({len(self.players)} out of {self.config._max_players}): 
                {', '.join(list(map(str,self.players)))}
        """)

        if self.config.rounds == 0:
            entry = self._in("\n-> How many rounds to play? (1+)\n<- ")
            if entry.isdigit():
                entry = int(entry)
                if entry >= 1:
                    self.config.rounds = entry
                    return

            self._out("Invalid entry! Please try again!")
            return

        if self.players == []:
            if not self.addPlayer():
                self._out("Invalid entry! Please try again!")
            
            return

        player_spots_left = len(self.players) < self.config._max_players
        if player_spots_left:
            entry = self._in(f"\n-> Add another player? [y/n]\n<- ")
            if entry == "y":
                if not self.addPlayer():
                    self._out("Invalid entry! Please try again!")
                
                return

            elif entry != "n":
                self._out("Invalid entry! Please try again!")
                return 
            


        self.config.grid_area = (self.config.rows*self.config.cols)
        self.config.grid_dim = (self.config.rows, self.config.cols)
        self.grid = [None]*self.config.grid_area

        self.winningMoves = self.getWinningMoves()
        self.__ready = True

    def aiMove(self,bot) -> int:
        wins_for_bot = []

        def hasNone(lst: list) -> bool:
            return any(elem is None for elem in lst)

        def hasWin(lst: list) -> bool:
            oneleft = len(lst)-1

            non_null = None
            for elem in lst:
                if elem is not None:
                    non_null = elem
                    break

            return (lst.count(non_null) == oneleft)


        if bot.bot_difficulty > 1:
            for scan in self.winningMoves:
                read = list(map(lambda i: self.grid[i], scan))
                if bot.bot_difficulty == 3 and hasNone(read) and hasWin(read):
                    readi = read.index(None)
                    return scan[readi]
                
                # Check if all items is either None or bot.symbol
                if bot.bot_difficulty >= 2 and all((elem is None or elem is bot.symbol for elem in read)):
                    wins_for_bot.append(scan)

            if wins_for_bot != []:
                best_chance = wins_for_bot[0]
                if bot.bot_difficulty == 3:
                    for win in wins_for_bot:
                        if len(win) > len(best_chance):
                            best_chance = win
                
                if best_chance != []:
                    filtered_bc = list(filter(lambda i: self.grid[i] is None, best_chance))
                    return choice(filtered_bc)

        # random choice for bot
        available = list(filter(lambda i: self.grid[i] is None, range(self.config.grid_area)))
        return choice(available)


    def renderGame(self, round: int, plr: Player = None):
        """Clears console, and outputs the board in string format"""

        self._cls()

        roundinfo_build, board_build = "", ""

        # Each concat to board_output acts as a print (new line)

        roundinfo_build += f"[Round {round} of {self.config.rounds}]"

        if plr is not None: # idk if this would happen but :/
            roundinfo_build += f"\n{plr.name} has {plr.score} points"

        

        build = ""

        Xlen = len(str(len(self.grid))) # length of biggest number
        box_spacing = Xlen + 2 # add spacing on both sides
        h_line = '-' #

        for i,move in enumerate(self.grid):
            move = str(i+1) if move == None else move
            if i != 0 and i % self.config.grid_dim[1] == 0:
                board_build += f"\n{build}\n{h_line*len(build)}"
                build = ""

            if len(build) > 0:
                build += f"|{move:^{box_spacing}}"
            else:     
                build += f"{move:^{box_spacing}}"

            


        if build != "": 
            board_build += f"\n{build}"
            build = ""

        board_build += "\n"

        self._roundinfo_out(roundinfo_build)
        self._board_out(board_build)


    def checkWinner(self) -> Player:
        """Checks winning move from a player"""

        for plr in self.players:
            for scan in self.winningMoves:
                read = list(map(lambda i: self.grid[i], scan)) 
                if all(symbol is plr.symbol for symbol in read): # p1 wins
                    return plr

    def checkDraw(self) -> bool:
        """Checks if no moves are left"""
        # Check tie
        moves_left = list(filter(lambda move: move == None, self.grid))
        if not moves_left: # if moves_left not empty
            return True
        
        return False # necessary?


    def validateMove(self, move : int = None) -> bool:
        """Checks if a move is on the board and unique"""

        if move and move >= 1 and move <= self.config.grid_area: # in grid
            if not self.grid[move-1]:    # if gridspace is None
                return True
            else:
                self._out(f"{move} is taken.")
        else:
            self._out(f"{move} is not in range (1-{self.config.grid_area}).")
            
        return False
                

    def play(self):
        """Play specified rounds of tic-tac-toe!"""

        if not self.isReady():
            raise "Game Instance is not ready [Missing Setup]"
        
        round = 1
        while round <= self.config.rounds:
            for plr in self.players:
                self.renderGame(round, plr)
                if(plr.isbot): # bot's turn
                    move = self.aiMove(plr)
                    self.grid[move] = plr.symbol
                else:
                    while True:
                        move = self._in(f"{plr.name}'s Turn\n-> To make your move, enter a number on the board.\n<- ")
                        if move.isdigit():
                            move = int(move)
                            if self.validateMove(move):
                                self.grid[move-1] = plr.symbol
                                break
                        else:
                            self._out(f"'{move}' is not a number.")
                            self.renderGame(round, plr)

                if plr == self.checkWinner():
                    plr.add_point()
                    self.renderGame(round, plr)
                    self._out(f"{plr} won!")
                    self._in("Press 'enter' to continue...")

                    self.grid = [None]*self.config.grid_area
                    round += 1
                    
                    if round > self.config.rounds:
                        break
                    #else rotation can keep going
                elif(self.checkDraw()):
                    self.renderGame(round, plr)
                    self._out(f"It's a draw!")
                    self._in("Press 'enter' to continue...")

                    self.grid = [None]*self.config.grid_area
                    round += 1

                    if round > self.config.rounds:
                        break
                    #else rotation can keep going


if __name__ == "__main__":
    game_instance = Instance()

    print("Welcome to Ultimate Tic-Tac-Toe!")
    input("Press 'enter' to continue...")

    while not game_instance.isReady():
        game_instance.setup()

    input("\nSetup Complete!\nPress 'enter' to start...")
    game_instance._cls()
    game_instance.play()

            

