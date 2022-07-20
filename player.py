class Player:
    def __init__(self,game_instance, name=None, isbot=False):

        self.game_instance = game_instance # game instance is required

        if not isbot:
            if name is not None and name != "": # valid custom
                self.__name = name
                self.__symbol = self.__createSymbol()
            else: # default
                plr_num = len(self.game_instance.players)+1
                self.__name = f"Player {plr_num}"
                self.__symbol = f"P{plr_num}"
        else:
            self.__name = "@Bot"
            self.__symbol = self.__createSymbol()

        self.isbot = isbot

        # acceptable difficulties will range from 1-3
        self.bot_difficulty = 0 # a difficulty of 0 will be ignored

        self.__score = 0

    def __createSymbol(self) -> str:
        name = self.name
        dupes = 0
        for plr in self.game_instance.players:
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