from hnzView import View
from hnzController import Controller
from tkinter import *
from pubsub import pub
import vUtility


if __name__ == "__main__":
    mainwin = Tk()
    WIDTH = vUtility.windowWidth
    HEIGHT = vUtility.windowHeight
    mainwin.geometry("%sx%s" % (WIDTH, HEIGHT))
    #mainwin.resizable(0, 0)
    mainwin.title("Graphic Neural Network")
    #create view and controller
    controller=Controller()
    view=View(mainwin)
    #cross lin view and controller
    controller.setView(view)
    view.setController(controller)
    #setup and complete view
    view.setup()
    mainwin.mainloop()
