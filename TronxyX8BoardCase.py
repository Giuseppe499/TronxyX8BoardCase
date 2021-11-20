'''
Procedural motherboard/electronics case for cxy-v2-0508 (Tronxy X8 board)
Copyright (C) 2021  Giuseppe Scarlato

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import cadquery as cq
from cadquery import exporters

#Box Variables
length = 140
width = 110
heigth = 60
fillet = 5
wall = 2.4

#Screw Holes Variables
pHeigth = 10;
pOuterRadius = 8/2;
pInnerRadius = 4/2;
dX = 101
dY = 81

#Lid Variables
lidHeigth = max(wall, fillet)

case = cq.Workplane("XY").box(length, width, heigth, (True, True, False)).edges("|Z").fillet(fillet).edges(">Z").fillet(fillet)
insideMask = case
case = case.shell(-wall)
shellMask = case

basePlane = cq.Workplane("XY").copyWorkplane(case.faces("<Z").workplane());

#Hexagonal lattice
hexOffset = max(wall, fillet);
hexSize = 15;
hexSpacing = 1.2;

def hexMask(workplane, startX, endX, startY, endY):
    hexmask = workplane;
    x = startX;
    zig = True
    while (x < endX):
    #for i in range(4):
        y = startY
        if (zig):
            y += (hexSpacing + hexSize)/2
        while (y < endY):
        #for j in range(4):
        #if True:
            hexmask = hexmask\
                .pushPoints([(x,y)])\
                .polygon(6, hexSize).extrude(- wall - fillet);
            y += (hexSize + hexSpacing);
        zig = not zig;
        x += (hexSize + hexSpacing) * 0.9; 
        
    return hexmask

# Z hex cut
workplane = cq.Workplane("XY").copyWorkplane(case.faces("<Z").workplane());
hexmask = hexMask(workplane, -length/2 - 3, length/2, - width/2, width/2 + hexSize +hexSpacing);
offsetMask = cq.Workplane("XY").box(length - hexOffset*2, width - hexOffset*2, heigth + 10, (True, True, False)).edges("|Z").fillet(fillet)
hexmask = hexmask.intersect(offsetMask)
case = case.cut(hexmask)
del hexmask

workplane = cq.Workplane("XY").copyWorkplane(case.faces(">Z").workplane());
hexmask = hexMask(workplane, -length/2 - 3, length/2, - width/2, width/2 + hexSize +hexSpacing);
hexmask = hexmask.intersect(offsetMask)
case = case.cut(hexmask)
del offsetMask
del hexmask

#Y hex cut
workplane = cq.Workplane("XY").copyWorkplane(case.faces("<Y").workplane());
hexmask = hexMask(workplane, -length/2, length/2, 0, heigth + hexSize + hexSpacing);
offsetMask = cq.Workplane("XY").workplane(offset=hexOffset)  .box(length - hexOffset*2, width + 10, heigth - hexOffset*2, (True, True, False))
hexmask = hexmask.intersect(offsetMask)
case = case.cut(hexmask)

del hexmask


workplane = cq.Workplane("XY").copyWorkplane(case.faces(">Y").workplane());
hexmask = hexMask(workplane, -length/2, length/2, 0, heigth + hexSize + hexSpacing);
hexmask = hexmask.intersect(offsetMask)
case = case.cut(hexmask)
del offsetMask
del hexmask

#X hex cut
workplane = cq.Workplane("XY").copyWorkplane(case.faces("<X").workplane());
hexmask = hexMask(workplane, -width/2 - 3.2 , width/2, -5, heigth + hexSize + hexSpacing);
offsetMask = cq.Workplane("XY").workplane(offset=hexOffset).box(length + 10, width - hexOffset*2, heigth - hexOffset*2, (True, True, False))
hexmask = hexmask.intersect(offsetMask)
case = case.cut(hexmask)

del hexmask

workplane = cq.Workplane("XY").copyWorkplane(case.faces(">X").workplane());
hexmask = hexMask(workplane, -width/2 - 3.2, width/2, -5, heigth + hexSize + hexSpacing);
hexmask = hexmask.intersect(offsetMask)
case = case.cut(hexmask)
del offsetMask
del hexmask

(lid,case) = case.faces(">Z").workplane(-lidHeigth).split(keepTop=True,keepBottom=True).all()

#Lid Inset
iHeigth = 5
iWall = 1.8
iClearance =0.6

# iMargin = cq.Workplane("XY").box(length, width, heigth, (True, True, False)).edges("|Z").fillet(fillet)
# iMargin = iMargin.faces(">Z").shell(-wall -iClearance -iWall)
# iMargin = iMargin.faces(">Z").workplane(-lidHeigth).split(keepTop=True)
# iMargin = iMargin.intersect(insideMask)
# lid = lid.union(iMargin)
# del iMargin

inset = cq.Workplane("XY").box(length, width, heigth, (True, True, False)).edges("|Z").fillet(fillet)
inset = inset.cut(inset.faces(">Z").shell(-wall -iClearance)).faces(">Z").shell(-iWall)
inset = inset.faces(">Z").workplane(-lidHeigth -iHeigth).split(keepTop=True)
inset = inset.intersect(insideMask)
lid = lid.union(inset)
del inset

#Lid-Case Connectors
cThickness = 3
cHeigth = 5
cWidth = 15
cClearance = 1.2
cOverhangCompensation = 0.3
cPocket = wall
cCutHeigth = 10
cCutMargin = wall

workplane = cq.Workplane("XY").copyWorkplane(lid.faces(">Z").workplane());

connector1 = workplane.center(length/2 - (wall + cThickness)/2, 0).workplane(offset=0).rect(cThickness + wall, cWidth - cClearance).workplane(offset=-lidHeigth).rect(cThickness + wall, cWidth - cClearance).loft()
connector1 = connector1.intersect(insideMask)
connector1 = connector1.center(- wall/2, 0).rect(cThickness, cWidth - cClearance)\
    .workplane(offset = -cHeigth - cCutMargin - cClearance/2 - cOverhangCompensation).rect(cThickness, cWidth - cClearance).loft()\
    .center(cPocket/2 , 0).rect(cThickness + cPocket, cWidth - cClearance)\
    .workplane(offset = -cCutHeigth + cClearance + cOverhangCompensation).center( - cPocket/2 - cClearance/2, 0).rect(cThickness - cClearance, cWidth - cClearance).loft()

connector2 = workplane.center(-length/2 + (wall + cThickness)/2, 0).workplane(offset=0).rect(cThickness + wall, cWidth - cClearance).workplane(offset=-lidHeigth).rect(cThickness + wall, cWidth - cClearance).loft()
connector2 = connector2.cut(connector2.cut(insideMask))
connector2 = connector2.center( wall/2, 0).rect(cThickness, cWidth - cClearance)\
    .workplane(offset = -cHeigth - cCutMargin - cClearance/2 - cOverhangCompensation).rect(-cThickness, cWidth - cClearance).loft()\
    .center(-cPocket/2, 0).rect(cThickness + cPocket, cWidth - cClearance)\
    .workplane(offset = -cCutHeigth + cClearance + cOverhangCompensation).center(cPocket/2 + cClearance/2, 0).rect(cThickness - cClearance, cWidth - cClearance).loft()

lid = lid.union(connector1, clean = False).union(connector2, clean = False)
del connector1, connector2


#Case Connectors cut
caseShellMask = shellMask.faces(">Z").workplane(-lidHeigth).split(keepBottom=True)
workplane = cq.Workplane("YZ").workplane(offset = length/2 - wall).center(0, heigth - lidHeigth)
boxToCut = workplane.center(0, -cHeigth -cCutMargin - cCutHeigth/2).box(cWidth ,cCutHeigth, wall + fillet)
marginBox = workplane.center(0, -cHeigth -cCutMargin - cCutHeigth/2).box(cWidth + 2 * cCutMargin,cCutHeigth + 2 * cCutMargin, wall + fillet)
marginBox = marginBox.intersect(caseShellMask)
case = case.union(marginBox).cut(boxToCut)

workplane = cq.Workplane("YZ").workplane(offset = -length/2 + wall).center(0, heigth - lidHeigth)
boxToCut = workplane.center(0, -cHeigth -cCutMargin - cCutHeigth/2).box(cWidth ,cCutHeigth, wall + fillet)
marginBox = workplane.center(0, -cHeigth -cCutMargin - cCutHeigth/2).box(cWidth + 2 * cCutMargin,cCutHeigth + 2 * cCutMargin, wall + fillet)
marginBox = marginBox.intersect(caseShellMask)
case = case.union(marginBox).cut(boxToCut)

#Case USB and SD cut
cutBottomMargin = 5
cutSideMargin = 45
cutWidth = 25
cutLength = 50
workplane = cq.Workplane("XZ").workplane(offset = width/2 - wall).center(-length/2 + cutSideMargin + cutLength/2, cutBottomMargin)
boxToCut = workplane.center(0, cutWidth/2).box(cutLength, cutWidth, wall + fillet)
marginBox = workplane.center(0, cutWidth/2).box(cutLength + 2 * cCutMargin, cutWidth + 2 * cCutMargin, wall + fillet)
marginBox = marginBox.intersect(caseShellMask)
case = case.union(marginBox).cut(boxToCut)

#Case LCD Cables cut
cutUpperMargin = 15
cutSideMargin = 15
cutWidth = 25
cutLength = 15
workplane = cq.Workplane("YZ").workplane(offset = -length/2 + wall).center(width/2 - cutSideMargin - cutLength/2, heigth - cutUpperMargin)
boxToCut = workplane.center(0, -cutWidth/2).box(cutLength, cutWidth, wall + fillet)
marginBox = workplane.center(0, -cutWidth/2).box(cutLength + 2 * cCutMargin,cutWidth + 2 * cCutMargin, wall + fillet)
marginBox = marginBox.intersect(caseShellMask)
case = case.union(marginBox).cut(boxToCut)

del boxToCut


#case upper margin
marginBox = cq.Workplane("XY").workplane(offset = heigth - lidHeigth -cCutMargin/2).box(length, width, cCutMargin)
marginBox = marginBox.intersect(caseShellMask)
case = case.union(marginBox)
del marginBox

#Rotate and translate lid
lid = lid.rotateAboutCenter((1, 0, 0), 180).translate((0, width + 10,-heigth + lidHeigth/2))

#Screw Posts
case = case.union(basePlane.rect(dX, dY, forConstruction=True).vertices()\
        .circle(pOuterRadius).extrude(-pHeigth))
screwHoles = basePlane.rect(dX, dY, forConstruction=True).vertices()\
        .circle(pInnerRadius).extrude(-pHeigth)
case = case.cut(screwHoles)
del screwHoles

del caseShellMask
del insideMask
del shellMask
exporters.export(case, 'case_last.stl')
exporters.export(lid, 'lid_last.stl')
