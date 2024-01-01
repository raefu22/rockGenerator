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
    print(level)
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
        width = random.randint(1,3)
        depth = random.randint(1,3)
        cmds.polyCube(w = width, d = depth, cuv=4, sd = 3, sh = 3, sw = 3, n = name)
        
        cmds.select(appendName(name, '.f[4]'), appendName(name, '.f[1]'))
        cmds.move(0, 0, random.uniform(0,1), r=True)
        cmds.select(appendName(name, '.f[22]'), appendName(name, '.f[25]'))
        cmds.move(0, 0, -random.uniform(0,1), r=True)
        
        cmds.select(appendName(name, '.f[37]'), appendName(name, '.f[40]'))
        if (width == 1 and depth == 1):
            cmds.move(random.uniform(0,0.04), 0, 0, r=True)
            cmds.select(appendName(name, '.f[49]'), appendName(name, '.f[46]'))
            cmds.move(-random.uniform(0,0.03), 0, 0, r=True)
            cmds.select(appendName(name, '.f[13]'))
            cmds.move(random.uniform(-0.2,0.2), random.uniform(0,0.03), random.uniform(-0.2,.2), r=True)
        else:
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
        position = locations(curvename, (x-0.0)/num)
        cmds.move(position[0], position[1], position[2], relative = True)
        
        #UVs
        cmds.polyProjection(name+".f[0:53]", md = 'y')
        
        edgenums = ['.e[0:2]', '.e[27:29]', '.e[72]', '.e[75:76]', '.e[79:80]', '.e[83]', '.e[37]', '.e[41]', '.e[45]']   
        edges = []
        for edge in edgenums:
            edges.append(appendName(name,edge))
        
        cmds.polyMapCut(edges)
        cmds.select(name + '.f[0:53]')
        cmds.u3dUnfold(name + '.f[0:53]', ite=1, p=0, bi=1, tf=1, ms=1024, rs=0)
        cmds.u3dLayout(name+'.f[0:53]', res=256, scl=1, box=[0, 1, 0, 1])
        
        #material
        shader = cmds.shadingNode('aiStandardSurface', asShader = True, n=name + 'shader')
        
        cmds.sets(renderable=True, noSurfaceShader= True, empty=True, n= 'aiSurfaceShader' + name + 'SG')
        cmds.select(name)
        cmds.hyperShade(assign = 'aiSurfaceShader' + name + 'SG')
        cmds.connectAttr(name + 'shader.outColor', 'aiSurfaceShader' + name +'SG.surfaceShader', f=True)
        
        #initial noise
        cmds.shadingNode('noise', asTexture=True, n = name + 'noise1')
        
        cmds.shadingNode('place2dTexture', asUtility = True, n = name + 'place2dTexture1')
        cmds.connectAttr (name + 'place2dTexture1.outUV', name + 'noise1.uv')
        cmds.connectAttr(name + 'place2dTexture1.outUvFilterSize', name + 'noise1.uvFilterSize')
        
        #cmds.defaultNavigation(createNew= True, destination= name + 'noise1.colorOffset')
        #cmds.createRenderNode -allWithTexturesUp 
        #cmds.defaultNavigation(force=True, connectToExisting=True, source=%node, destination= name + 'noise1.colorOffset')
        #cmds.defaultNavigation(defaultTraversal=True, destination= name + 'noise1.colorOffset')
        cmds.shadingNode('simplexNoise', asTexture=True, n = name + 'simplexNoise1')
        cmds.shadingNode('place2dTexture', asUtility=True, n = name + 'place2dTexture2')
        cmds.connectAttr(name + 'place2dTexture2.outUV', name + 'simplexNoise1.uv')
        cmds.connectAttr(name +'place2dTexture2.outUvFilterSize', name + 'simplexNoise1.uvFilterSize')
        #cmds.defaultNavigation(force=True, connectToExisting=True, source=name + 'simplexNoise1', destination=name + 'noise1.colorOffset')
        #cmds.window -e -vis false createRenderNodeWindow;
        cmds.connectAttr(name + 'simplexNoise1.outColor', name + 'noise1.colorOffset', force=True)
        
        cmds.shadingNode('aiMultiply', asUtility=True, n = name + 'aiMultiply1')
        cmds.connectAttr(name + 'noise1.outColor', name + 'aiMultiply1.input1', force = True)
        
        cmds.shadingNode('noise', asTexture=True, n = name + 'noiseColor')
        cmds.shadingNode('place2dTexture', asUtility = True, n = name + 'place2dTexture3')
        cmds.connectAttr (name + 'place2dTexture3.outUV', name + 'noiseColor.uv')
        cmds.connectAttr(name + 'place2dTexture3.outUvFilterSize', name + 'noiseColor.uvFilterSize')
        cmds.connectAttr(name + 'noiseColor.outColor', name + 'aiMultiply1.input2', force = True)
        #mountain texture
        cmds.shadingNode('mountain', asTexture=True, n = name + 'mountain1')
        cmds.shadingNode('place2dTexture', asUtility=True, n = name + 'place2dTexture4')
        cmds.connectAttr(name + 'place2dTexture4.outUV', name + 'mountain1.uv')
        cmds.connectAttr(name + 'place2dTexture4.outUvFilterSize', name + 'mountain1.uvFilterSize')
        
        cmds.shadingNode('fractal', asTexture=True, n = name + 'fractal1') 
        cmds.shadingNode('place2dTexture', asUtility=True, n=name + 'place2dTexture5')
        cmds.connectAttr(name + 'place2dTexture5.outUV', name + 'fractal1.uv')
        cmds.connectAttr(name + 'place2dTexture5.outUvFilterSize', name + 'fractal1.uvFilterSize')
        cmds.shadingNode('aiAdd', asUtility=True, n = name + 'aiAdd1')
        cmds.connectAttr(name + 'mountain1.outColor', name + 'aiAdd1.input1', force = True)
        cmds.connectAttr(name + 'fractal1.outColor', name + 'aiAdd1.input2', force = True)
        
        cmds.shadingNode('aiMultiply', asUtility=True, n = name + 'aiMultiply2')
        cmds.connectAttr(name + 'aiMultiply1.outColor', name + 'aiMultiply2.input1', force = True)
        cmds.connectAttr(name + 'aiAdd1.outColor', name + 'aiMultiply2.input2', force = True)
        cmds.connectAttr(name + 'aiMultiply2.outColor', name + 'shader.baseColor', force = True)
        
        #adjustments
        cmds.setAttr(name + 'noise1.amplitude', 0.42)
        cmds.setAttr(name + 'noise1.ratio', 1.0)
        cmds.setAttr(name + 'noise1.frequencyRatio', 29.636)
        cmds.setAttr(name + 'noise1.frequency', 95.804)
        cmds.setAttr(name + 'noise1.density', 1.0)
        cmds.setAttr(name + 'noise1.spottyness', 0)
        cmds.setAttr(name + 'noise1.sizeRand', 0)
        cmds.setAttr(name + 'noise1.randomness', 1.0)
        cmds.setAttr(name + 'noise1.colorGain',  0.804, 0.771, 0.763, type='double3')
        cmds.setAttr(name + 'noise1.alphaGain', 0.392)
        
        cmds.setAttr(name + 'simplexNoise1.scale', 4.476)
        cmds.setAttr(name + 'simplexNoise1.amplitude', 0.399)
        cmds.setAttr(name + 'simplexNoise1.threshold', 0.0)
        cmds.setAttr(name + 'simplexNoise1.ratio', 0.707)
        cmds.setAttr(name + 'simplexNoise1.frequency', 6.853)
        cmds.setAttr(name + 'simplexNoise1.frequencyRatio', 1.0)
        cmds.setAttr(name + 'simplexNoise1.gamma', .455)
        
        cmds.setAttr(name + 'noiseColor.amplitude', 0.182)
        cmds.setAttr(name + 'noiseColor.ratio', 0.643)
        cmds.setAttr(name + 'noiseColor.frequencyRatio', 1.566)
        cmds.setAttr(name + 'noiseColor.frequency', 9.091)
        cmds.setAttr(name + 'noiseColor.noiseType', 4)
        cmds.setAttr(name + 'noiseColor.colorGain', 1, 0.712, 0.712, type='double3')
        cmds.setAttr(name + 'noiseColor.colorOffset', 0.224, 0.171, 0.171, type='double3')
        cmds.setAttr(name + 'noiseColor.alphaGain', 1.0)
        
        cmds.setAttr(name + 'mountain1.snowColor', 1, 1, 1, type='double3')
        cmds.setAttr(name + 'mountain1.rockColor', 0.503, 0.503, 0.503, type='double3')
        cmds.setAttr(name + 'mountain1.amplitude', 1.0)
        cmds.setAttr(name + 'mountain1.snowRoughness', 0.4)
        cmds.setAttr(name + 'mountain1.rockRoughness', 0.707)
        cmds.setAttr(name + 'mountain1.boundary', 0.874)
        cmds.setAttr(name + 'mountain1.snowAltitude', 0.5)
        cmds.setAttr(name + 'mountain1.snowDropoff', 2.0)
        cmds.setAttr(name + 'mountain1.snowSlope', 3.0)
        
        
        cmds.setAttr(name + 'fractal1.amplitude', 1.0)
        cmds.setAttr(name + 'fractal1.threshold', 0.0)
        cmds.setAttr(name + 'fractal1.ratio', 0.972)
        cmds.setAttr(name + 'fractal1.frequencyRatio', 2.0)
        cmds.setAttr(name + 'fractal1.bias', 0.636)
        
        #for normal map
        cmds.shadingNode('layeredTexture', asTexture=True, n = name + 'layeredTexture1') 
        cmds.setAttr(name + 'layeredTexture1.inputs[0].color', 0.523, 0.523, 0.523, type="double3")
        cmds.setAttr(name + 'layeredTexture1.inputs[0].alpha', 1)
        cmds.setAttr(name + 'layeredTexture1.inputs[0].blendMode', 6)
        cmds.connectAttr(name + 'mountain1.outAlpha', name + 'layeredTexture1.inputs[0].alpha', force = True)
        cmds.setAttr(name + 'mountain1.alphaIsLuminance', 1)
        cmds.setAttr(name + 'layeredTexture1.alphaIsLuminance', 1)
        cmds.setAttr(name + 'layeredTexture1.inputs[1].color', 0.242, 0.242, 0.242, type="double3")
        cmds.setAttr(name + 'layeredTexture1.inputs[1].alpha', 1)
        cmds.setAttr(name + 'layeredTexture1.inputs[1].blendMode', 4)
        cmds.connectAttr(name + 'fractal1.outAlpha', name + 'layeredTexture1.inputs[1].alpha', force = True)
        cmds.setAttr(name + 'fractal1.alphaIsLuminance', 1)
       
        cmds.shadingNode('bump2d', asUtility=True, n = name + 'bump2d1')
        cmds.connectAttr(name + 'layeredTexture1.outAlpha', name + 'bump2d1.bumpValue', f = True)
        cmds.connectAttr(name + 'bump2d1.outNormal', name + 'shader.normalCamera')
        
        
        
        '''
        cmds.shadingNode('rock', asTexture = True, n = name + 'rock')
        cmds.shadingNode('place3dTexture', asUtility = True, n = name + 'place3dTexture')
        cmds.connectAttr (name + 'place3dTexture.wim[0]', name + 'rock.pm')
        cmds.connectAttr(name + 'rock.outColor', name + 'shader.baseColor')
        '''
        #smooth
        #cmds.polySmooth(mth=0, sdt=2, ovb=1, ofb=3, ofc=0, ost=0, ocr=0, dv=2, bnr=1, c=1, kb=1, ksb=1, khe=0, kt=1, kmb=1, suv=1, peh=0, sl=1, dpe=1, ps=0.1, ro=1, ch=1)