import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import asksaveasfile, asksaveasfilename

from pubsub import pub
from random import sample

from vArrow import VArrow
from vNode import VNode
from vValue import VValue
from hnzController import *
import webbrowser
import vUtility as vu
import pickle


class View:

    def __init__(self, parent):
        # initialize variables
        self.container = parent
        self.flagNetworkCreated = False
        self.flagNetworkTrained = False
        self.flagLoadTrainFeature = False
        self.flagLoadTrainLabel = False
        self.lastx = 0
        self.lasty = 0
        self.listVArrow = []
        self.listVNode = []
        self.listComboBox = []
        self.listInputNode=[]
        self.listOutputNode=[]
        self.controller = None
        self.listFlatVNode=[]
        self.trainLabelPath=""
        self.trainFeaturePath=""
        self.testFeaturePath = ""
        #The 'subscriber' here
        #pub.subscribe(self.updateLossTxt,"update loss function txt")

    def updateLossTxt(self,data):
        self.text31ErrorTxtbox.insert(INSERT, data)


    def setup(self): # run first
        """Calls methods to setup the user interface."""
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        """Create various widgets in the tkinter main window."""
        #self.var = tk.IntVar()
        #self.background_label = tk.Label(self.container)
        self.leftFrame = Frame(self.container,width=100, height=vu.windowHeight)
        self.midFrame = Frame(self.container,width=vu.canvasWidth, height=vu.canvasHeight)
        self.rightFrame = Frame(self.container,width=100, height=vu.windowHeight)
        self.rightFrame1=Frame(self.rightFrame)
        self.rightFrame2=Frame(self.rightFrame)

        self.statusbar=tk.Label(self.midFrame,text="On the way…", bd=1, relief=tk.SUNKEN, anchor=tk.W,fg="red")
        #button
        #self.b1Arrow = tk.Button(self.leftFrame, text = "Create Arrow", command = self.createArrows, width=20, height = 1)
        self.lab1input = tk.Label(self.leftFrame,text="input layer")
        self.combo1input = ttk.Combobox(self.leftFrame,values=[1,2,3,4])

        self.lab2layer1 = tk.Label(self.leftFrame, text="mid layer 1")
        self.combo2layer1 = ttk.Combobox(self.leftFrame, values=[ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.lab3layer2 = tk.Label(self.leftFrame, text="mid layer 2")
        self.combo3layer2 = ttk.Combobox(self.leftFrame, values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.lab4layer3 = tk.Label(self.leftFrame, text="mid layer 3")
        self.combo4layer3 = ttk.Combobox(self.leftFrame, values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.lab5output = tk.Label(self.leftFrame, text="output layer")
        self.combo5output = ttk.Combobox(self.leftFrame, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.b2Circle = tk.Button(self.leftFrame, text = "Create Network", command = self.createNodes, width =20, height =1)
        self.lab6TrainDiv = tk.Label(self.leftFrame, text="===Train===")
        #self.b7randomNum = tk.Button(self.leftFrame, text="Random Number", command=self.randomNum, width=20, height=1)
        self.c = Canvas(self.midFrame, bg='white', width=vu.canvasWidth, height=vu.canvasHeight)
        self.c.tag_bind("drag", "<Button-1>", self.clicked)
        self.c.tag_bind("drag", "<B1-Motion>", self.drag)
        #training inputs
        self.lab7LearningRate=tk.Label(self.leftFrame,text="learning Rate")
        self.combo6learningRate=ttk.Combobox(self.leftFrame,values=[0.0001,0.0005,0.001,0.005,0.01,0.05,0.1,0.5])
        self.lab8epoch=tk.Label(self.leftFrame,text="number of epochs")
        self.combo7epoch = ttk.Combobox(self.leftFrame,
                                               values=[10,5000,10000,50000,100000,200000,500000,1000000,2000000,5000000,
                                                       10000000,20000000,50000000])
        self.lab9refreshRate=tk.Label(self.leftFrame,text="Refresh rate (epochs)")
        self.combo8refreshRate = ttk.Combobox(self.leftFrame,
                                        values=[2,100,200,300,500,1000,2000,3000])
        self.b8LoadFeature=tk.Button(self.leftFrame, text="Load Features", command=self.loadTrainFeature, width=20, height=1)
        self.b9LoadLabel = tk.Button(self.leftFrame, text="Load Labels", command=self.loadTrainLabel, width=20,
                                     height=1)
        self.b10StartTrain=tk.Button(self.leftFrame, text="Start Training", command=self.startTrain,

                                                        width=20, height=1)
        self.lab9aSaveLoadFile = tk.Label(self.leftFrame, text="===Save/Load NN===")
        self.b10aSaveNN = tk.Button(self.leftFrame, text="Save Network", command=self.saveNN,

                                                        width=20, height=1)
        self.b10bLoadNN = tk.Button(self.leftFrame, text="Load Network", command=self.loadNN,

                                    width=20, height=1)
        #prediction inputs
        self.lab10DivPredection=tk.Label(self.leftFrame,text="===Prediction===")
        self.b11LoadPreFeature = tk.Button(self.leftFrame, text="Load Predict Features", command=self.loadPreFeature, width=20,
                                       height=1)
        self.b12StartPredict = tk.Button(self.leftFrame, text="Start Prediction", command=self.startPredict,
                                         width=20, height=1)
        self.lab11PreRounding=tk.Label(self.leftFrame,text="Rounding")
        self.combo9PreRounding = ttk.Combobox(self.leftFrame,
                                               values=[1, 0.1, 0.01, 0.001, 0.0001, 0.00001])
        # hyper link
        self.hyp1youtube = tk.Label(self.leftFrame, text="youtube.com/user/hhhnzw", fg="blue", cursor="hand2")
        self.hyp1youtube.bind("<Button-1>", lambda e: self.callback("https://www.youtube.com/user/hhhnzw"))
        #error rate and prediction text boxes to right hand frame
        self.lab31ErrorRate=tk.Label(self.rightFrame,text="===Loss Function Value===")

        self.text31ErrorTxtbox=tk.Text(self.rightFrame1,width=30)
        self.scl31vbar = tk.Scrollbar(self.rightFrame1, orient=VERTICAL)
        self.text31ErrorTxtbox.config(yscrollcommand=self.scl31vbar.set)
        self.scl31vbar.config(command=self.text31ErrorTxtbox.yview)
        #self.scl31vbar.config(command=self.text31ErrorTxtbox.xview)
        self.lab32PredictionResult=tk.Label(self.rightFrame,text="===Prediction Result===")
        self.text32PredictTxtbox = tk.Text(self.rightFrame2,width=30)
        self.scl32vbarPre = tk.Scrollbar(self.rightFrame2, orient=VERTICAL)
        self.text32PredictTxtbox.config(yscrollcommand=self.scl32vbarPre.set)
        self.scl32vbarPre.config(command=self.text32PredictTxtbox.yview)


        #TODO add file save and load status to menubar


        self.listComboBox.append(self.combo1input)
        self.listComboBox.append(self.combo2layer1)
        self.listComboBox.append(self.combo3layer2)
        self.listComboBox.append(self.combo4layer3)
        self.listComboBox.append(self.combo5output)


    def setup_layout(self):
        self.leftFrame.pack(side = LEFT)
        self.midFrame.pack (side=LEFT)
        self.rightFrame.pack (side = RIGHT)



        #self.b1Arrow.pack( side=TOP)
        self.lab1input.pack(side=TOP)
        self.combo1input.pack(side=TOP)
        self.lab2layer1.pack(side=TOP)
        self.combo2layer1.pack(side=TOP)
        self.lab3layer2.pack(side=TOP)

        self.combo3layer2.pack(side=TOP)
        self.lab4layer3.pack(side=TOP)
        self.combo4layer3.pack(side=TOP)
        self.lab5output.pack(side=TOP)
        self.combo5output.pack(side=TOP)
        self.b2Circle.pack(side = TOP)
        # training divider
        self.lab6TrainDiv.pack(side=TOP)
        #self.b7randomNum.pack(side=TOP)
        self.lab7LearningRate.pack(side=TOP)
        self.combo6learningRate.pack(side=TOP)
        self.lab8epoch.pack(side=TOP)
        self.combo7epoch.pack(side=TOP)
        self.lab9refreshRate.pack(side=TOP)
        self.combo8refreshRate.pack(side=TOP)
        self.b8LoadFeature.pack(side=TOP)
        self.b9LoadLabel.pack(side=TOP)
        self.b10StartTrain.pack(side=TOP)

        #canvas
        self.c.pack(side=TOP)
        #save load nn
        self.lab9aSaveLoadFile.pack(side=TOP)
        self.b10aSaveNN.pack(side=TOP)
        self.b10bLoadNN.pack(side=TOP)
        #prediction buttons
        self.lab10DivPredection.pack(side=TOP)
        self.b11LoadPreFeature.pack(side=TOP)
        self.b12StartPredict.pack(side=TOP)
        self.lab11PreRounding.pack(side=TOP)
        self.combo9PreRounding.pack(side=TOP)
        #hyper link
        self.hyp1youtube.pack(side=TOP)
        #pack rightFrame
        self.lab31ErrorRate.pack(side=TOP)
        self.rightFrame1.pack(side=TOP, fill=BOTH)
        self.text31ErrorTxtbox.pack(side=LEFT)
        self.scl31vbar.pack(side=LEFT,fill=Y)

        self.lab32PredictionResult.pack(side=TOP)
        self.rightFrame2.pack(side=BOTTOM, fill=BOTH)
        self.text32PredictTxtbox.pack(side=LEFT)
        self.scl32vbarPre.pack(side=LEFT,fill=Y)

        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        #set default combobox default value
        self.combo1input.current(1)
        self.combo2layer1.current(3)
        self.combo3layer2.current(0)
        #self.combo3layer2["state"]=DISABLED
        self.combo4layer3.current(0)
        #self.combo4layer3["state"] = DISABLED
        self.combo5output.current(2)
        #set train combobox
        self.combo6learningRate.current(2)
        self.combo7epoch.current(1)#1, #0 for testing
        self.combo8refreshRate.current(2)#2, #0 for testing
        self.combo9PreRounding.current(1)#2 round to 0.1
        self.statusbar["text"] = "Ready."

    def callback(self, url):
        webbrowser.open_new(url)
    def saveNN(self): #TODO save and load NN
        if self.flagNetworkTrained == False:
            tk.messagebox.showinfo(title="Error", message="Please create and train network first")

        else:
            p = asksaveasfilename(initialdir="./", defaultextension=".nn",
                                                    title="Save a network",
                                                    filetypes=[("Network File", "*.nn")],
                                                    )
            if p is None:
                self.statusbar["text"]="Network file saving failed."
                return
            else:
                saveObjs =[]
                saveObjs.append(self.combo1input.current())#0
                saveObjs.append(self.combo2layer1.current())#1
                saveObjs.append(self.combo3layer2.current())#2
                saveObjs.append(self.combo4layer3.current())#3
                saveObjs.append(self.combo5output.current())#4
                saveObjs.append(self.combo6learningRate.current())#5
                saveObjs.append(self.combo7epoch.current())#6
                saveObjs.append(self.combo8refreshRate.current())#7
                saveObjs.append(self.combo9PreRounding.current())#8
                saveObjs.append(self.controller.listBias)#9
                saveObjs.append(self.controller.listWeight)#10
                layerLen=[]
                for l in self.listVNode:
                    layerLen.append(l.__len__())
                saveObjs.append(layerLen)#11
                with open(p,'wb') as saveFile:
                    pickle.dump(saveObjs,saveFile)

                self.statusbar["text"] = "Network file saved."


    def loadNN(self):
        p = askopenfilename(initialdir="./",
                              title="Load a network",
                              filetypes=[("Network File", "*.nn")],
                              )
        if p is None:
            self.statusbar["text"] = "Network file saving failed."
            return
        else:
            with open (p,'rb') as f:

                loadObjs=pickle.load(f)

                layerLen = loadObjs[11]
                # TODO reinstate network and weights
                self.combo1input.current(0)
                self.combo2layer1.current(0)
                self.combo3layer2.current(0)
                self.combo4layer3.current(0)
                self.combo5output.current(0)
                for i in range (layerLen.__len__()):
                    if i == layerLen.__len__()-1:
                        self.combo5output.current(layerLen[i]-1)
                    elif i == 2 or i == 3:
                        self.listComboBox[i].current(layerLen[i])
                    else:
                        self.listComboBox[i].current(layerLen[i]-1)
                self.clear()
                self.createNodes()
                self.controller.listBias = loadObjs[9]
                self.controller.listWeight = loadObjs[10]
                # update weighs in view
                self.controller.flattenListWeight(self.controller.listWeight)
                self.updateWeight(self.controller.listFlatWeight)
                # update Biases in view
                self.controller.flattenListBias(self.controller.listBias)
                self.updateBias(self.controller.listFlatBias)
                #update combo box as per saved, which may different from nn
                self.combo1input.current(loadObjs[0])
                self.combo2layer1.current(loadObjs[1])
                self.combo3layer2.current(loadObjs[2])
                self.combo4layer3.current(loadObjs[3])
                self.combo5output.current(loadObjs[4])
                self.combo6learningRate.current(loadObjs[5])
                self.combo7epoch.current(loadObjs[6])
                self.combo8refreshRate.current(loadObjs[7])
                self.combo9PreRounding.current(loadObjs[8])
            self.flagNetworkTrained=True
            self.statusbar["text"] = "Network file loaded."
    def loadPreFeature(self):
        if self.flagNetworkTrained == False:
            tk.messagebox.showinfo(title="Error", message="Please create and train network first")

        else:
            self.testFeaturePath = ""
            self.testFeaturePath = askopenfilename(initialdir="./",
                                                    filetypes=[("Text File", "*.txt"), ("All Files", "*.*")],
                                                    title="Choose a file."
                                                    )
            self.controller.loadTestFeature(self.testFeaturePath)

    def loadTrainFeature(self):
        if self.flagNetworkCreated==False:
            tk.messagebox.showinfo(title="Error", message="Please create network first")
        else:
            self.trainFeaturePath=""
            self.trainFeaturePath = askopenfilename(initialdir="./",
                                   filetypes=[("Text File", "*.txt"), ("All Files", "*.*")],
                                   title="Choose a file."
                                   )
            self.controller.loadTrainFeature(self.trainFeaturePath)

            #self.flagLoadTrainFeature=True

    def loadTrainLabel(self):
        if self.controller.flagTrainFeatureLoad==False:
            tk.messagebox.showinfo(title="Error", message="Please create network, and load training feature set first")
        else:
            self.trainLabelPath=""
            self.trainLabelPath = askopenfilename(initialdir="./",
                                   filetypes=[("Text File", "*.txt"), ("All Files", "*.*")],
                                   title="Choose a file."
                                   )
            self.controller.loadTrainLabel(self.trainLabelPath)

            #self.flagLoadTrainLabel=True
    def startTrain(self):
        if self.controller.flagTrainLabelLoad == False:
            tk.messagebox.showinfo(title="Error", message="Please create network, and load training feature and label first.")
        else:
            self.b10StartTrain["state"] = DISABLED
            self.statusbar["text"] = "Training....."
            #complete start train
            self.controller.startTrain()
            self.b10StartTrain["state"] = NORMAL
            self.flagNetworkTrained=True
    def startPredict(self):
        if self.controller.flagTestFeatureLoad == False:
            tk.messagebox.showinfo(title="Error", message="Please load data for prediction")
        # TODO complete start Predict
        else:
            self.b12StartPredict["state"] = DISABLED
            self.statusbar["text"] = "Predicting....."
            self.controller.startPredict()
            self.b12StartPredict["state"] = NORMAL
    def updateBias(self,controlFlatBiasList):
        for i in range (0, controlFlatBiasList.__len__()):
            self.listFlatVNode[i].updateBias(controlFlatBiasList[i])
        pass
    def flattenListVNode(self): #no input layer
        self.listFlatVNode.clear()
        for layer in range(1,self.listVNode.__len__()):
            for n in self.listVNode[layer]:
                self.listFlatVNode.append(n)

    def updateWeight(self,controlFlatWeightList):
        for i in range (0, controlFlatWeightList.__len__()):
            self.listVArrow[i].updateWeight(controlFlatWeightList[i])

    def createArrows(self):
        for i in range (0, len(self.listVNode) ):
            #get column into J
            for j in self.listVNode[i]:
                arrowStart = j.getRightCod()


                if i<len(self.listVNode)-1:
                    #get rows in column
                    listArrowCol = []
                    for q in self.listVNode[i+1]:
                        arrowEnd = q.getLeftCod()
                        vArrow = VArrow()
                        vArrow.create(self.c, arrowStart,arrowEnd)
                        q.addLeftArrow(vArrow) #link from node
                        j.addRightArrow(vArrow)
                        #link node in arrow
                        vArrow.leftNode=j
                        vArrow.rightNode=q
                        self.listVArrow.append(vArrow)





        #vArrow = VArrow()
        #aid = self.c.create_line(50, 25, 150, 75, arrow="last",tags = "drag")
        #vArrow.setArrowId(aid)
        #vArrow.create(self.c,)
        #self.listVArrow.append(vArrow)
        #self.c.pack()
        #vu.tprint(aid)
        #vu.tprint ("list varrow length= "+str(len(self.listVArrow)))
    def clearInputValue(self):
        for n in self.listInputNode:
            n.updateValue(0.0)

    def clearOutputValue(self):
        for n in self.listOutputNode:
            n.updateValue(0.0)
    def clear(self):
        #remove all from canvas
        self.c.delete("all")
        self.lastx = 0
        self.lasty = 0
        self.listVArrow.clear()
        self.listVNode.clear()
        #self.listComboBox.clear()
        self.listInputNode.clear()
        self.listOutputNode.clear()
        self.listFlatVNode.clear()
        self.controller.clear()


    def createNodes(self):
        #network exists clear first
        if self.flagNetworkCreated:
            self.clear()

        listComboGet=[]
        #put combobox number into listComboGet
        for cb in self.listComboBox:
            if cb.get() != '0':
                listComboGet.append(cb.get())
        vu.tprint("listComboGet")
        vu.tprint(listComboGet)

        #vu.tprint (listComboGet)
        totalColumn=len(listComboGet)
        j=0
        #listNodeCoord=[]
        index=0
        for i in listComboGet:
            j=j+1
            #node coord by column
            listNodeCoord=vu.getNodePosition(totalColumn,int(i),j)
            #vu.tprint (listNodeCoord)
            listLayer=[]
            index+=1


            #create nodes based on coordination
            for c1 in listNodeCoord:
                vNode = VNode()
                vNode.create(self.c, c1[0], c1[1])
                # append value box if in first or last column
                if index == 1:#node with input
                    #vValue = VValue()
                    #vValue.create(self.c,vNode.getLeftCod(),-vu.valueWidth/2)
                    #setup input node
                    vNode.what="input"
                    #vNode.bias=1
                    #vNode.updateBiasView()
                    #vNode.addLeftArrow(vValue)
                    self.listInputNode.append(vNode)
                    #vValue.setRightNode(vNode)
                elif index == listComboGet.__len__():#node with output
                    #vValue = VValue()
                    #vValue.create(self.c, vNode.getRightCod(), vu.valueWidth / 2)
                    # setup output node
                    vNode.what = "output"
                    #vNode.addRightArrow(vValue)
                    self.listOutputNode.append(vNode)
                    #vValue.setLeftNode(vNode)
                listLayer.append(vNode)
            self.listVNode.append(listLayer)


        #pub.sendMessage("Button_createNode_Clicked")
        #self.b2Circle["state"]=DISABLED
        #create arrows
        self.createArrows()
        self.flattenListVNode()
        #setup controller network
        self.setupControlNetwork()
        # generate random weight and bias
        self.randomNum()
        # set flag as true
        self.flagNetworkCreated = True
        self.flagNetworkTrained = False
        #reload train feature and label if they have been loaded before
        if self.controller.flagTrainFeatureLoad:
            self.controller.loadTrainFeature(self.trainFeaturePath)
        if self.controller.flagTrainLabelLoad:
            self.controller.loadTrainLabel(self.trainLabelPath)
        #vu.tprint (self.listVNode)
    def randomColor(self):# not in use
        listColor = ["red","blue","yellow","green","orange","purple"]
        return sample (listColor,1)

    def clicked (self,event):
        self.clickedid= event.widget.find_withtag('current')[0]
        self.lastx, self.lasty = event.x, event.y
        #self.c.tag_raise(self.clickedid)
        #self.c.itemconfig(self.clickedid,fill="red")
        #vu.tprint ("clicked id: "+str(self.clickedid))

    def drag(self,event):
        #search id to see if the item is in an arrow
        #for column in self.listVArrow:
            #for a in column:
                #if a.containArrowText(self.clickedid):
                    #vu.tprint("arrow found: "+str(self.clickedid))
                    #a.moveArrowText(event.x-self.lastx, event.y-self.lasty)
                    #self.lastx = event.x
                    #self.lasty = event.y
                    #return
                #if a.containPtStart(self.clickedid):
                    #vu.tprint("point found: " + str(self.clickedid))
                    #a.movePtLeft(event.x, event.y)
                    #self.lastx = event.x
                    #self.lasty = event.y
                    #return
                #if a.containPtEnd(self.clickedid):
                    #a.movePtRight(event.x, event.y)
                    #self.lastx = event.x
                    #self.lasty = event.y
                    #return
        # search id to see if the item is in a node
        for column in self.listVNode:
            for n in column:
            #another loop to get node element
                if n.containAny(self.clickedid):
                    #vu.tprint("arrow found: "+str(self.clickedid))
                    n.move(event.x-self.lastx, event.y-self.lasty)
                    self.lastx = event.x
                    self.lasty = event.y
                    return
        self.c.move(self.clickedid,event.x-self.lastx, event.y-self.lasty)
        self.lastx=event.x
        self.lasty=event.y
    def randomNum(self):
        self.controller.randomWeights(self.listVNode)
        self.controller.randomBias(self.listVNode)
        #self.b7randomNum["state"] = DISABLED

        #self.lab6TrainDiv.pack(side=TOP)
    def setController(self,con): #set link to controller
        self.controller=con
    def setupControlNetwork(self):#pass number to controller
        self.controller.numInput=len(self.listInputNode)
        self.controller.numOutput=len(self.listOutputNode)
        vu.tprint(len(self.listComboBox))
        for i in range (len(self.listComboBox)):
            vu.tprint ("i=")
            vu.tprint (i)
            if (i >0) and i<len(self.listComboBox)-1:
                # setup total hidden layer in controller
                j=int(self.listComboBox[i].get())
                if j!=0:
                    self.controller.numOfHLayers.append(j)
        vu.tprint("number of hidden layer")
        vu.tprint(self.controller.numOfHLayers)
#test view
if __name__ == "__main__":
    mainwin = Tk()
    WIDTH = vu.windowWidth
    HEIGHT = vu.windowHeight
    mainwin.geometry("%sx%s" % (WIDTH, HEIGHT))
    #mainwin.resizable(0, 0)
    mainwin.title("view testing")

    view=View(mainwin)
    view.setup()
    mainwin.mainloop()