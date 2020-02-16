import vUtility
import random

class VValue:
    def __init__(self):
        self.value=0.00
        self.rightNode=None
        self.leftNode=None
        self.what="valuebox"
    def updatePoints(self):
        self.startX = self.centreX - vUtility.valueWidth / 2
        self.startY = self.centreY - vUtility.valueHeight / 2
        self.endX = self.centreX + vUtility.valueWidth / 2
        self.endY = self.centreY + vUtility.valueHeight / 2

        self.leftX = self.startX
        self.leftY = self.centreY
        self.rightX = self.endX
        self.rightY = self.centreY

        self.textX = (self.startX + self.endX) / 2
        self.textY = (self.startY + self.endY) / 2

    def create(self, can, cod, offset):
        self.centreX,self.centreY=cod
        self.centreX+=offset
        self.canvas = can
        self.updatePoints()
        self.rid = self.canvas.create_rectangle(self.startX, self.startY, self.endX, self.endY, tags="valueBox")
        #self.startId = self.canvas.create_rectangle(self.leftX - vUtility.dotHalfSize,
                                                    #self.leftY - vUtility.dotHalfSize,
                                                    #self.leftX + vUtility.dotHalfSize,
                                                    #self.leftY + vUtility.dotHalfSize,
                                                    #fill="gray", tags="valueBox")
        #self.endId = self.canvas.create_rectangle(self.rightX - vUtility.dotHalfSize,
                                                  #self.rightY - vUtility.dotHalfSize,
                                                  #self.rightX + vUtility.dotHalfSize,
                                                  #self.rightY + vUtility.dotHalfSize,
                                                  #fill="gray", tags="valueBox")

        self.tId = self.canvas.create_text(self.textX, self.textY, text=str(self.value), tag="valueBox")
    def setRightNode(self, n):
        self.rightNode=n
    def setLeftNode(self,n):
        self.leftNode=n
    def move(self,x,y):
        self.canvas.move(self.rid, x, y)
        #self.canvas.move(self.endId, x, y)
        #self.canvas.move(self.startId, x, y)
        self.canvas.move(self.tId, x, y)