class Pokemon:

    # serve a contare le tipologie ed i teratipi più usati.
    set_types = {
        "Normal",
        "Fire",
        "Water",
        "Grass",
        "Electric",
        "Ice",
        "Fighting",
        "Poison",
        "Ground",
        "Flying",
        "Psychic",
        "Bug",
        "Rock",
        "Ghost",
        "Dragon",
        "Dark",
        "Steel",
        "Fairy"
    }

    def __init__(self, name="default", typo="default", ability='default', tera="default", moves="default", item_held='default'):
        self.name = name
        self.typo = typo
        self.ability = ability 
        self.tera = tera
        self.moves = moves
        self.item_held = item_held

    def __str__(self):
        return "Pokèmon: %s, tera: %s, teratype: %s, moveset: %s" %(self.name, self.typo, self.tera, self.moves)

    def set_name(self, name):
        self.name = name

    def set_typo(self, typo):
        self.typo = typo
    
    def set_tera(self, tera):
        self.tera = tera
    
    def set_moves(self, moves):
        self.moves = moves

    def get_name(self):
        return self.name
    
    def get_typo(self):
        return self.typo
    
    def get_tera(self):
        return self.tera
    
    def get_moves(self):
        return self.moves