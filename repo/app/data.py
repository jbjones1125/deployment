class Data:
    email = ""
    def __init__(self):
        pass

    def setEmail(self, inputEmail: str):
        Data.email = inputEmail

    def getEmail(self):
        return Data.email