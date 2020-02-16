from hnzView import *
from tkinter import *
from pubsub import pub
import numpy as np
import matplotlib.pyplot as plt
from tkinter.filedialog import askopenfilename
import csv
import vUtility as vu

from datetime import datetime
class Controller:

    def __init__(self):
        self.view = None
        self.numInput=0
        self.numOutput=0
        self.numOfHLayers=[]
        self.listWeight=[]
        self.listFlatWeight=[]
        self.listBias=[]
        self.listFlatBias=[]
        self.trainFeatureSet=[]
        self.testFeatureSet = []
        self.trainLabelSet=[]
        self.flagTrainFeatureLoad=False
        self.flagTestFeatureLoad = False
        self.flagTrainLabelLoad=False
        #self.listNodeValue=[]
        self.listAhiddenLayer=[] #node value after sigmoid function
        self.listZhiddenLayer=[] #node sum value before sigmoid function
        self.error_cost=[]
        self.ao=None
        self.inputTrainFilePath=""
        self.outputTrainFilePath=""
        np.random.seed(42)
    #set link to view
    def setView(self,vie):
        self.view=vie
    def randomBias(self,listvn):
        for i in range (1,listvn.__len__()):
            currentNodeQty=listvn[i].__len__()
            npBias=np.random.rand(currentNodeQty)
            self.listBias.append(npBias)
        self.flattenListBias(self.listBias)
        self.view.updateBias(self.listFlatBias)

    def randomWeights(self,listvn):
        for i in range (0,listvn.__len__()-1):
            currentNodeQty=listvn[i].__len__()
            nextNodeQty=listvn[i+1].__len__()
            #create weight matrix
            npMatrixWeight=np.random.rand(currentNodeQty,nextNodeQty)
            self.listWeight.append(npMatrixWeight)
        #append to flat list
        self.flattenListWeight(self.listWeight)
            #update arrow weight in view object
        self.view.updateWeight(self.listFlatWeight)
        #vu.tprint ("listWeight =")
        #vu.tprint(self.listWeight)
        #vu.tprint("flattened list weight=")
        #vu.tprint (self.listFlatWeight)

    def flattenListBias(self,lb):
        self.listFlatBias=[]
        for layer in lb:
            for i in layer:
                self.listFlatBias.append(i)

    def flattenListWeight(self, lw):
        self.listFlatWeight.clear()
        for layer in lw:
            for i in layer:
                for j in i:
                    self.listFlatWeight.append(j)
        vu.tprint (len(self.listFlatWeight))
# neural next work functions
    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def sigmoid_der(self, x):
        return self.sigmoid(x) *(1-self.sigmoid (x))

    def softmax(self, A):
        expA = np.exp(A)
        return expA / expA.sum(axis=1, keepdims=True)

    def strToNp(self,list):
        newList=[]
        for i in list:
            vu.tprint ("np i=")
            vu.tprint (np.float64(i))
            newList.append(np.float64(i))
        return newList

    def clear(self):
        self.numInput = 0
        self.numOutput = 0
        self.numOfHLayers.clear()
        self.listWeight.clear()
        self.listFlatWeight.clear()
        self.listBias.clear()
        self.listFlatBias.clear()
        #self.trainFeatureSet.clear()
        #self.trainLabelSet.clear()
    def sigmoid(self,x):
        return 1 / (1 + np.exp(-x))
    def sigmoid_der(self,x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))
    def softmax(self,A):
        expA = np.exp(A)
        return expA / expA.sum(axis=1, keepdims=True)

    def startPredict(self):
        startTime = datetime.now()
        self.view.text32PredictTxtbox.delete('1.0', END)
        result = self.predictLoop()
        vu.tprint("result = ")
        vu.tprint (result)
        for row in result:
            rounding=self.view.combo9PreRounding.current()
            for i in range (row.__len__()):
                line=""
                prefix="%."+str(rounding)+"f"
                f = prefix % round(row[i], rounding)
                if i != row.__len__()-1:
                    line += str(f)+","
                else:
                    line += str(f)+"\n"
                self.view.text32PredictTxtbox.insert(INSERT, line)

        #duration time
        runTime = datetime.now() - startTime
        self.view.statusbar["text"] = "Predicting Completed. Duration: " + str(runTime)
    def startTrain(self):
        startTime = datetime.now()
        self.view.text31ErrorTxtbox.delete('1.0', END)
        totalCheck=int(self.view.combo7epoch.get())/(int(self.view.combo8refreshRate.get()))
        i=1
        for epoch in range(int(self.view.combo7epoch.get())):
            self.trainLoop()
            if epoch % (int(self.view.combo8refreshRate.get())) == 0:
                loss = np.sum(-np.array(self.trainLabelSet) * np.log(self.ao))
                #vu.tprint('Loss function value: ', loss)
                lossTxt=str(loss)+"\n"
                self.view.text31ErrorTxtbox.insert(INSERT, lossTxt)
                self.view.text31ErrorTxtbox.update()
                # show progress percentage
                p=i/totalCheck*100
                runTime = datetime.now() - startTime
                self.view.statusbar["text"]=("Training in progress: "+str(int(p))+"%" + "     Duration:  "+ str(runTime))
                i+=1
                #update weighs in view
                self.flattenListWeight(self.listWeight)
                self.view.updateWeight(self.listFlatWeight)
                #update Biases in view
                self.flattenListBias(self.listBias)
                self.view.updateBias(self.listFlatBias)
        runTime=datetime.now() - startTime
        self.view.statusbar["text"] ="Training Completed. Duration: " + str(runTime)
    def predictLoop(self):
        previous_set = self.testFeatureSet  # initial previouse set
        for i in range(self.listWeight.__len__()):

            if i!=self.listWeight.__len__()-1:
                # get node value
                zh=np.dot(previous_set,self.listWeight[i])+self.listBias[i]#sum
                ah=self.sigmoid(zh)#node value after sigmoid function
                #TODO put in to list
                previous_set=ah
            else:
                zo=np.dot(previous_set,self.listWeight[i])+self.listBias[i]
                ao=self.softmax(zo)#value after softmax

        return ao

    def trainLoop(self):

        #TODO feed forward
        previous_set = self.trainFeatureSet #initial previouse set
        self.listAhiddenLayer.clear()
        self.listZhiddenLayer.clear()
        for i in range (self.listWeight.__len__()):
            if i!=self.listWeight.__len__()-1:
                # get node value
                zh=np.dot(previous_set,self.listWeight[i])+self.listBias[i]#sum
                ah=self.sigmoid(zh)#node value after sigmoid function
                #TODO put in to list
                self.listAhiddenLayer.append(ah)
                self.listZhiddenLayer.append(zh)
                previous_set=ah
            else:
                zo=np.dot(previous_set,self.listWeight[i])+self.listBias[i]
                self.ao=self.softmax(zo)#value after softmax
                self.listAhiddenLayer.append(self.ao)
                self.listZhiddenLayer.append(zo)
        #vu.tprint("self.ao length= "+str(self.ao.__len__()))
        #vu.tprint(self.ao)
        #TODO back propagation
        targetValue_set = self.trainLabelSet
        value_set = self.ao
        lr = float(self.view.combo6learningRate.get())
        #vu.tprint("lr = "+str(lr))
        for i in range (self.listWeight.__len__()-1,-1,-1):
            #phase 1
            if i == self.listWeight.__len__()-1: #for output nodes
            #if True:
                dcost_dzo = value_set - targetValue_set #deviation, node value - target value
                dzo_dwo = self.listAhiddenLayer[i-1]
                dcost_wo = np.dot(dzo_dwo.T,dcost_dzo)#weight adjust
                dcost_bo = dcost_dzo#bias adjust
                #adjusted weight and bias
                unchangedWeight=self.listWeight[i].copy() #keep unchanged for phase 2
                unchangedBias=self.listBias[i].copy()
                self.listWeight[i] -= lr * dcost_wo
                self.listBias[i] -= lr * dcost_bo.sum(axis=0)
                #vu.tprint ("dcost-wo=")
                #vu.tprint(dcost_wo)
            else:
                #phase 2
                dzo_dah = unchangedWeight
                #dzo_dah=self.listWeight[i+1]
                dcost_dah = np.dot(dcost_dzo,dzo_dah.T)#TODO problem how to calculate
                dah_dzh = self.sigmoid_der(self.listZhiddenLayer[i])
                if i==0:
                    # previouse input set
                    previouseInput_set=self.trainFeatureSet
                else:
                    previouseInput_set=self.listAhiddenLayer[i-1]
                dzh_dwh = np.array(previouseInput_set)
                dcost_wh = np.dot(dzh_dwh.T, dah_dzh*dcost_dah)
                dcost_bh = dcost_dah*dah_dzh

                #unchangedWeight = self.listWeight[i].copy()  # keep new weight for next round
                #TODO check to see if works right
                # update dcost_dzo( value_set targetValue_set),

                dcost_dzo=dcost_bh #IMPORTANT
                #updaet to new weights and new bias
                unchangedWeight = self.listWeight[i].copy()  # keep unchanged for next round
                #unchangedBias = self.listBias[i].copy() #keep unchanged bias
                self.listWeight[i] -= lr * dcost_wh
                self.listBias[i] -= lr * dcost_bh.sum(axis=0)
    def loadTestFeature(self,path):#TODO load test feature set
        if len(path) > 0:
            self.view.statusbar["text"] = "Loading..... please wait for numbers shown in input nodes"
            list=[]
            f=open(path,"r")
            lines=f.read().split('\n')
            f.close()
            #load into list
            for l in lines:
                #vu.tprint(l)
                if l !="":
                    self.inputTrainFilePath=l
                    row=self.strToNp(l.split(","))
                    list.append(row)
            self.testFeatureSet.clear()
            self.testFeatureSet=list
            #check input node length
            if self.testFeatureSet[0].__len__()!=self.view.listInputNode.__len__():
                tk.messagebox.showinfo(title="Error", message="DataSet not compatible with Network")
                self.view.statusbar["text"] = "Test Feature set loading failed"
                return
            self.setInputValue(self.testFeatureSet)

            self.flagTestFeatureLoad=True
            self.view.statusbar["text"] = "Test Feature set loaded"
        # test dot option->both work in same way
        #vu.tprint(np.dot(self.trainFeatureSet,self.listWeight[0]))
        #vu.tprint(np.dot(np.array(self.trainFeatureSet), np.array(self.listWeight[0])))
        else:
            #load failed clean input
            self.flagTestFeatureLoad=False
            self.trainFeatureSet.clear()
            self.view.clearInputValue()
            self.view.statusbar["text"] = "Test Feature set loading failed"
    def loadTrainFeature(self,path):


        if len(path) > 0:
            self.view.statusbar["text"] = "Loading..... please wait for numbers shown in input nodes"
            list=[]
            f=open(path,"r")
            lines=f.read().split('\n')
            f.close()
            #load into list
            for l in lines:
                #vu.tprint(l)
                if l !="":
                    self.inputTrainFilePath=l
                    row=self.strToNp(l.split(","))
                    list.append(row)
            self.trainFeatureSet.clear()
            self.trainFeatureSet=list
            #check input node length
            if self.trainFeatureSet[0].__len__()!=self.view.listInputNode.__len__():
                self.view.combo1input.set(self.trainFeatureSet[0].__len__())
                self.view.createNodes()
            self.setInputValue(self.trainFeatureSet)

            self.flagTrainFeatureLoad=True
            self.view.statusbar["text"] = "Training Feature set loaded"
        # test dot option->both work in same way
        #vu.tprint(np.dot(self.trainFeatureSet,self.listWeight[0]))
        #vu.tprint(np.dot(np.array(self.trainFeatureSet), np.array(self.listWeight[0])))
        else:
            #load failed clean input
            self.flagTrainFeatureLoad=False
            self.trainFeatureSet.clear()
            self.view.clearInputValue()
            self.view.statusbar["text"] = "Training Feature set loading failed"
    def setInputValue(self,set):
        # set input node value
        for i in range(set[0].__len__()):
            self.view.listInputNode[i].updateValue(set[0][i])
    def loadTrainLabel(self,path):

        if len(path) > 0:
            self.outputTrainFilePath=path
            self.view.statusbar["text"] = "Loading..... please wait for numbers shown in output nodes"
            list=[]
            f=open(path,"r")
            lines=f.read().split('\n')
            f.close()
            for l in lines:
                if l != "":
                    vu.tprint(l)
                    row=self.strToNp(l.split(","))
                    list.append(row)
            self.trainLabelSet.clear()
            self.trainLabelSet = list
            #vu.tprint("control train label set= ")
            vu.tprint(self.trainLabelSet)
            # check output node length

            if self.trainLabelSet[0].__len__() != self.view.listOutputNode.__len__():
                self.view.combo5output.set(self.trainLabelSet[0].__len__())
                self.view.createNodes()
                # re-set input node value
                for i in range(self.trainFeatureSet[0].__len__()):
                    self.view.listInputNode[i].updateValue(self.trainFeatureSet[0][i])

            # set output node value
            for i in range(self.trainLabelSet[0].__len__()):
                self.view.listOutputNode[i].updateValue(self.trainLabelSet[0][i])
            self.flagTrainLabelLoad=True
            self.view.statusbar["text"] = "Training label set loaded"
        else:
            # load failed clean output
            self.flagTrainLabelLoad=False
            self.trainLabelSet.clear()
            self.view.clearOutputValue()
            self.view.statusbar["text"] = "Training Load set loading failed"

if __name__ == "__main__":
    vu.tprint("controller")