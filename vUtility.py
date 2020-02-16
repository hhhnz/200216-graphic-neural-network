dotHalfSize=4
canvasWidth=1000
canvasHeight=770
nodeWidth=50
nodeHeight=50
valueWidth=100
valueHeight=20
windowWidth=1400
windowHeight=800
networkOffset=-180
numberFont="Helvetica 7"
#statusFont="Helvetica 10 red"
textOffsetY=16

inputNColor="gray"
layer1Color="red"
layer2Color="yellow"
layer3Color="blue"
outputNColor="cyan"
screenPrint=True
def tprint(x):
    if screenPrint:
        print(x)

def getNodePosition(totalcolumn,thisTotalrow, layerno):
    columnDis = (canvasWidth+100)/(totalcolumn)
    x=layerno*columnDis+networkOffset
    #tr=(int(thisTotalrow)+2)
    yGap=canvasHeight/(thisTotalrow+2)
    listCoord=[]
    for i in range(0,thisTotalrow):
        y=(i+1)*yGap
        listCoord.append([x-nodeWidth/2,y-nodeHeight/2])
    #print (listCoord)
    return listCoord



