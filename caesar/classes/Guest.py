class Guest:
    def __init__(self, chanel, order):
        self.chanel = chanel
        self.order = order
    
    def __str__(self):
        return "Ch:"+str(self.chanel) + "," + "Num:"+str(self.order)