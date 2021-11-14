import cadquery as cq
from cadquery import exporters

#Box Variables
length = 140
width = 110
heigth = 55
fillet = 5
wall = 2.4

#Screw Holes Variables
pHeigth = 10;
pOuterRadius = 8/2;
pInnerRadius = 4/2;
dX = 102
dY = 82

case = cq.Workplane("XY").box(length, width, heigth, (True, True, False)).edges("|Z").fillet(fillet)

case = case.shell(-wall)

basePlane = cq.Workplane("XY").copyWorkplane(case.faces("<Z").workplane());

#Hexagonal lattice
hexOffset = max(wall, fillet);
hexSize = 10;
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
hexmask = hexMask(workplane, -length/2 + 2, length/2, - width/2, width/2 + hexSize +hexSpacing);
offsetMask = cq.Workplane("XY").box(length - hexOffset*2, width - hexOffset*2, heigth + 10, (True, True, False)).edges("|Z").fillet(fillet)
hexmask = hexmask.intersect(offsetMask)
case = case.cut(hexmask)
del hexmask

workplane = cq.Workplane("XY").copyWorkplane(case.faces(">Z").workplane());
hexmask = hexMask(workplane, -length/2 + 2, length/2, - width/2, width/2 + hexSize +hexSpacing);
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
hexmask = hexMask(workplane, -width/2 , width/2, 0, heigth + hexSize + hexSpacing);
offsetMask = cq.Workplane("XY").workplane(offset=hexOffset).box(length + 10, width - hexOffset*2, heigth - hexOffset*2, (True, True, False))
hexmask = hexmask.intersect(offsetMask)
case = case.cut(hexmask)

del hexmask

workplane = cq.Workplane("XY").copyWorkplane(case.faces(">X").workplane());
hexmask = hexMask(workplane, -length/2, length/2, 0, heigth + hexSize + hexSpacing);
hexmask = hexmask.intersect(offsetMask)
case = case.cut(hexmask)
del offsetMask
del hexmask


#Screw Posts
case = case.union(basePlane.rect(dX, dY, forConstruction=True).vertices()\
        .circle(pOuterRadius).extrude(-pHeigth))
screwHoles = basePlane.rect(dX, dY, forConstruction=True).vertices()\
        .circle(pInnerRadius).extrude(-pHeigth)
case = case.cut(screwHoles)
del screwHoles

exporters.export(case, 'case_last.stl')
