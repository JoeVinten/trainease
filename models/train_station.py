class TrainStation:
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return f"TrainStation(name='{self.name}', code='{self.code}')"
