import maya.cmds as cmds
import random

#UI
window = cmds.window(title='Rock Generator', menuBar = True, width=250)
container = cmds.columnLayout()
cols = cmds.rowLayout(numberOfColumns=3, p=container)

leftmar = cmds.columnLayout(p=cols)
cmds.text('         ', p =leftmar)

maincol = cmds.columnLayout('Block', p=cols)
cmds.text('            ')
cmds.text('   Select an EP Curve or Bezier Curve to place the rocks along')
cmds.separator(height = 10)
nameparam = cmds.textFieldGrp(label = 'Name ')
cmds.separator(height = 10)
cmds.intSliderGrp("num", label="Number of Rocks ", field = True, min = 1, max = 40, v = 15)

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
    
def locations(curvename, level):
    position = cmds.pointOnCurve(curvename, pr = level, turnOnPercentage = True)
    return position
    
#main function    
def createRock():
    inputname = cmds.textFieldGrp(nameparam, query = True, text = True)
   
    num = cmds.intSliderGrp("num", q = True, v=True)
    
    curvename = cmds.ls(selection = True)
    
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
        cmds.move(random.uniform(0,0.5), 0, 0, r=True)
        cmds.select(appendName(name, '.f[49]'), appendName(name, '.f[46]'))
        cmds.move(-random.uniform(0,1), 0, 0, r=True)
        cmds.select(appendName(name, '.f[13]'))
        cmds.move(random.uniform(-0.2,0.2), random.uniform(0,1), random.uniform(-0.2,.2), r=True)
        #tweaks
        cmds.select(appendName(name, '.vtx[15]'))
        cmds.move(random.uniform(-.2,-0.01), 0, random.uniform(-0.2,-0.01), r=True)
        cmds.select(appendName(name, '.vtx[12]'))
        cmds.move(random.uniform(0.01, 0.2), 0, random.uniform(-0.2,-0.01), r=True)
        cmds.select(appendName(name, '.vtx[27]'))
        cmds.move(random.uniform(-0.2, -0.01), 0, random.uniform(0.01,0.2), r=True)
        cmds.select(appendName(name, '.vtx[24]'))
        cmds.move(random.uniform(0.01, 0.2), 0, random.uniform(0.01,0.2), r=True)
        
        """
   
        """
        #rotate
        cmds.select(name)
        degrees = str(random.uniform(0, 360)) + 'deg'
        cmds.rotate(0, degrees, 0, r=True)
        
        #location
        cmds.select(name)
        position = locations(curvename, (x-1.0)/num)
        cmds.move(position[0], position[1], position[2], relative = True)
        
        #smooth
        cmds.polySmooth(mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=2, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)