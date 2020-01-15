class Name:
    def __init__(self):
        self.name = self.get_name()
    
    def get_name(self):
        return "bab"


bob = Name()
print(bob.name)