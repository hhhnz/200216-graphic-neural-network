import vUtility
import random
import vArrow
class VNode:
    def __init__(self):
        #self.weight = 0.00
        #self.startX = 100
        #self.startY = 200
        #self.endX = self.startX+vUtility.nodeWidth
        #self.endY = self.startY+vUtility.nodeHeight
        #self.updatePoints()
        self.bias = 0#round(random.uniform(0.00,1.00),2)
        self.leftArrow = []
        self.rightArrow = []
        self.what=None
        self.layer=None
        self.value=0
    def updatePoints(self):
        self.endX = self.startX + vUtility.nodeWidth
        self.endY = self.startY + vUtility.nodeHeight
        self.centerX, self.centerY = (self.startX + self.endX) / 2, (self.startY + self.endY) / 2
        self.leftX, self.leftY = self.startX, self.centerY
        self.rightX, self.rightY = self.endX, self.centerY
        self.textX = (self.startX + self.endX) / 2
        self.textY = (self.startY + self.endY) / 2- vUtility.textOffsetY #bias on top
        self.textVX = (self.startX + self.endX) / 2
        self.textVY = (self.startY + self.endY) / 2 + vUtility.textOffsetY  #value to bottom

    def updateBias(self, b):
        self.bias=b
        self.canvas.itemconfig(self.tidbias, text="B: "+str(self.bias))
        if (0 >= float(b)):
            self.canvas.itemconfig(self.tidbias,fill="green")
        else:
            self.canvas.itemconfig(self.tidbias,fill="red")
    #update Value
    def updateValue(self,v):
        self.value=v
        self.canvas.itemconfig(self.tidValue, text="V: "+str(self.value))

    def create(self, can,x,y):
        self.startX=x
        self.startY=y
        self.updatePoints()
        self.canvas = can
        self.cid = self.canvas.create_oval(self.startX, self.startY, self.endX, self.endY, fill = "orange",tags = "drag")
        self.startId = self.canvas.create_rectangle(self.leftX - vUtility.dotHalfSize,
                                                    self.leftY - vUtility.dotHalfSize,
                                                    self.leftX + vUtility.dotHalfSize,
                                                    self.leftY + vUtility.dotHalfSize,
                                                    fill="gray", tags="drag")
        self.endId = self.canvas.create_rectangle(self.rightX - vUtility.dotHalfSize, self.rightY - vUtility.dotHalfSize,
                                                  self.rightX + vUtility.dotHalfSize, self.rightY + vUtility.dotHalfSize,
                                                  fill="gray", tags="drag")
        self.tidbias = self.canvas.create_text(self.textX, self.textY, text=str("B: "+str(self.bias)), fill="red", tag="drag")
        self.tidValue= self.canvas.create_text(self.textVX, self.textVY, text=str("V: "+str(self.value)), fill="blue", tag="drag")
    def containAny(self,id):
        if id == self.startId:
            return True
        elif id==self.endId:
            return True
        elif id==self.cid:
            return True
        elif id==self.tidbias:
            return True
        elif id== self.tidValue:
            return True
        else:
            return False
    def move(self,x ,y):
        self.canvas.move(self.cid, x, y)
        self.canvas.move(self.endId, x, y)
        self.canvas.move(self.startId, x, y)
        self.canvas.move(self.tidbias, x, y)
        self.canvas.move(self.tidValue, x, y)
        self.startX += x;
        self.startY += y;
        self.endX += x;
        self.endY += y;
        self.updatePoints()
        self.canvas.tag_raise(self.cid)
        self.canvas.tag_raise(self.startId)
        self.canvas.tag_raise(self.endId)
        self.canvas.tag_raise(self.tidbias)
        self.canvas.tag_raise(self.tidValue)
        #move left and right element
        for la in self.leftArrow:
            if la.what=="arrow":
                la.movePtRight(self.leftX,self.leftY)
            elif la.what=="valuebox":
                la.move(x,y)


        for ra in self.rightArrow:
            if ra.what=="arrow":
                ra.movePtLeft(self.rightX,self.rightY)
            elif ra.what=="valuebox":
                ra.move(x,y)

    def getLeftCod(self):
        return (self.leftX, self.leftY)
    def getRightCod(self):
        return (self.rightX, self.rightY)
    def addLeftArrow(self, la):
        self.leftArrow.append(la)
    def addRightArrow(self, ra):
        self.rightArrow.append(ra)