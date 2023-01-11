class User():
    def __init__(self, name):
        self.name = name
        self.es = 0
        self.ms = 0
        self.hs = 0
    
    def update_high_scores(self, score, level):
        if level == 1 and score > self.es: self.es = score
        elif level == 2 and score > self.ms: self.ms = score
        elif score > self.hs: self.hs = score
    
    def get_highscores(self):
        return f'{self.name};*|{self.es};*|{self.ms};*|{self.hs}'

    def __eq__(self, __o: object) -> bool:
        return self.name == __o.name