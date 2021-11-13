import cadquery as cq

#Box Variables
length = 120
width = 100
heigth = 50
fillet = 5
wall = 1.8

#Screw Holes Variables
pHeigth = 10;
pOuterRadius = 6/2;
pInnerRadius = 3/2;
dX = 102
dY = 82

case = cq.Workplane("XY").box(length, width, heigth, (True, True, False)).edges("|Z").fillet(fillet)
case = case.faces("+Z").shell(-wall)

basePlane = cq.Workplane("XY").copyWorkplane(case.faces("<Z").workplane());

#Hexagonal lattice
hexOffset = 5;
hexSize = 10;
hexSpacing = 1;
a = int((length - 2 * hexOffset) / (hexSize + hexSpacing) * 0.9 * 0.5) + 1
b = int((width - 2 * hexOffset) / (hexSize + hexSpacing) * 0.5)
x = - a * (hexSize + hexSpacing) * 0.9;
zig = True
while (x < a * (hexSize + hexSpacing)* 0.9):
#for i in range(4):
    y = - b * (hexSize + hexSpacing)
    if (zig):
        y += (hexSpacing + hexSize)/2
    while (y < b * (hexSize + hexSpacing)):
    #for j in range(4):
        case = case.faces("<Z").workplane()\
            .pushPoints([(x,y)])\
            .polygon(6, hexSize).cutBlind(- wall - 2);
        y += (hexSize + hexSpacing);
    zig = not zig;
    x += (hexSize + hexSpacing) * 0.9;


#Screw Posts
case = case.union(basePlane.rect(dX, dY, forConstruction=True).vertices()\
        .circle(pOuterRadius).extrude(-pHeigth))
screwHoles = basePlane.rect(dX, dY, forConstruction=True).vertices()\
        .circle(pInnerRadius).extrude(-pHeigth)
case = case.cut(screwHoles)
del screwHoles
