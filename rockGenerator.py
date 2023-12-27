import maya.cmds as cmds
import random

#UI
window = cmds.window(title='Rock Generator', menuBar = True, width=250)
container = cmds.columnLayout()
cols = cmds.rowLayout(numberOfColumns=3, p=container)
leftmar = cmds.columnLayout(p=cols)
cmds.text('         ', p =leftmar)
maincol = cmds.columnLayout('Block', p=cols)

cmds.separator(height = 10)
nameparam = cmds.textFieldGrp(label = 'Name ')
cmds.separator(height = 10)
cmds.intSliderGrp("num", label="Number of Mushrooms ", field = True, min = 1, max = 20, v = 4)
cmds.floatSliderGrp("spread", label="Location Scatter ", field = True, min = 1, max = 50, v = 20)
cmds.separator(height = 10)

submitrow = cmds.rowLayout(numberOfColumns=2, p=maincol)
cmds.text(label='                                                                                           ')
cmds.button(label="Create Rock(s)", c="createRock()", p = submitrow)

cmds.separator(height = 10, p = maincol)
rightmar = cmds.columnLayout(p=cols)
cmds.text('         ', p =rightmar)

cmds.showWindow(window)

def appendName(name, textstring):
    textstring = name + textstring
    return textstring
    
def randomfloat():
    return 1
    
#main function    
def createRock():
    inputname = cmds.textFieldGrp(nameparam, query = True, text = True)
   
    num = cmds.intSliderGrp("num", q = True, v=True)
    spread = cmds.floatSliderGrp("spread", q = True, v = True)
    
    for x in range(1, num+1):
        #obj name
        name = inputname + str(x)
        
        #basic rock shape
        cmds.polyCube(w = random.randint(1,3), d = random.randint(1,3), cuv=4, sd = 3, sh = 3, sw = 3, n = name)
        cmds.select(appendName(name, '.f[4]'), appendName(name, '.f[1]'))
        cmds.move(0, 0, random.uniform(0,1), r=True)
        cmds.select(appendName(name, '.f[22]'), appendName(name, '.f[25]'))
        cmds.move(0, 0, -random.uniform(0,1), r=True)
        cmds.select(appendName(name, '.f[37]'), appendName(name, '.f[40]'))
        cmds.move(random.uniform(0,1), 0, 0, r=True)
        cmds.select(appendName(name, '.f[49]'), appendName(name, '.f[46]'))
        cmds.move(-random.uniform(0,1), 0, 0, r=True)
        cmds.select(appendName(name, '.f[13]'))
        cmds.move(0, random.uniform(0,1), 0, r=True)
        """
   
        """