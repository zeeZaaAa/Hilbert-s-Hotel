class Guest:
    def __init__(self, chanel, order):
        self.chanel = chanel
        self.order = order
    
    def __str__(self):
        return "Chanel:"+str(self.chanel) + "," + "Order:"+str(self.order)