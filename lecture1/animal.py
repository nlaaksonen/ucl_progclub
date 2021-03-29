class Animal():
    def __init__(self, age=0):
        self.age = age
        self.legs = 0
        self.hasTail = False

    def speak(self):
        pass

class Cat(Animal):
    """docstring for Cat"""
    def __init__(self, *args, **kwargs):
        Animal.__init__(self, *args, **kwargs)
        self.legs = 4
        self.hasTail = True

    def speak(self):
        print("Meow!")

class Bird(Animal):
    """docstring for Bird"""
    def __init__(self, *args, **kwargs):
        Animal.__init__(self, *args, **kwargs)
        self.legs = 2
        self.hasTail = False

    def speak(self):
        print("Chirp!")
