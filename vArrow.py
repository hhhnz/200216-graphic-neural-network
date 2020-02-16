import vUtility
import random
class VArrow:
    def __init__(self):
        self.weight=0#round(random.uniform(0.00,1.00),2)
        self.leftNode=None
        self.rightNode=None
        self.what="arrow"
        self.startId=None
        self.endId=None
        #self.startX=50 #left side
        #self.startY=25
        #self.endX=150 #right side
        #self.endY=75
        #self.updatePoints()

    def updateWeight(self,w):
        #update arrow weight
        self.weight=w
        self.canvas.itemconfig(self.tid,text="W: "+str(self.weight))
        if (0 >= float(w)):
            self.canvas.itemconfig(self.tid,fill="green")
        else:
            self.canvas.itemconfig(self.tid,fill="red")

    def updatePoints(self):
        self.textX=(self.startX+self.endX)/2
        self.textY=(self.startY+self.endY)/2
    def create(self, can, s, e):
        self.startX, self.startY=s
        self.endX, self.endY=e
        self.updatePoints()
        #creat arrow and 2 end handle points
        self.canvas=can
        self.aid = self.canvas.create_line(self.startX, self.startY, self.endX, self.endY, arrow="last", tags="arrow")
        #self.startId = self.canvas.create_rectangle(self.startX - vUtility.dotHalfSize, self.startY - vUtility.dotHalfSize,
                                                    #self.startX + vUtility.dotHalfSize, self.startY + vUtility.dotHalfSize,
                                                    #fill="gray", tags = "arrow")
        #self.endId = self.canvas.create_rectangle(self.endX - vUtility.dotHalfSize, self.endY - vUtility.dotHalfSize,
                                                  #self.endX + vUtility.dotHalfSize, self.endY + vUtility.dotHalfSize,
                                                  #fill="gray", tags = "arrow")
        self.tid = self.canvas.create_text(self.textX,self.textY,text="W: "+str(self.weight),tag="arrow",font=vUtility.numberFont)
    def containArrowText(self, id):
        #  check if contains the id for arrow or points
        if id == self.aid:
            return True
        elif id == self.tid:
            return True
        else: return False
    def containPtStart(self,id):
        if id == self.startId:
            return True
        else:
            return False
    def containPtEnd(self,id):
        if id == self.endId:
            return True
        else:
            return False
    def moveArrowText(self, x, y):
        self.canvas.move(self.aid, x, y)
        #self.canvas.move(self.endId, x, y)
        #self.canvas.move(self.startId, x, y)
        self.canvas.move(self.tid, x, y)
        self.startX += x; self.startY += y; self.endX += x; self.endY += y;
        self.updatePoints()
        #self.canvas.itemconfig(self.aid, fill = "black")
    def movePtLeft(self, x, y):
        #self.canvas.move(self.startId, x - self.startX, y-self.startY)
        self.startX,self.startY = x, y
        self.canvas.coords(self.aid, self.startX, self.startY, self.endX, self.endY)
        self.updatePoints()
        self.canvas.coords(self.tid, self.textX, self.textY)
        #self.canvas.itemconfig(self.startId, fill="gray")
    def movePtRight(self, x, y):
        #self.canvas.move(self.endId, x-self.endX, y-self.endY)
        self.endX, self.endY = x, y
        self.canvas.coords(self.aid, self.startX, self.startY, self.endX, self.endY)
        self.updatePoints()
        self.canvas.coords(self.tid, self.textX, self.textY)
        #self.canvas.itemconfig(self.endId, fill="gray")
    def changeDefaulColor(self):
        self.canvas.itemconfig(self.endId, fill="gray")
        self.canvas.itemconfig(self.startId, fill="gray")
        self.canvas.itemconfig(self.aid, fill="black")
