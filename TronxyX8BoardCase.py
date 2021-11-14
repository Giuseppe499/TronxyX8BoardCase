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
hexmask = cq.Workplane("XY").copyWorkplane(case.faces("<Z").workplane());
hexOffset = wall + 1.2;
hexSize = 10;
hexSpacing = 0.6;
x = -length/2 + 2;
zig = True
while (x < length/2):
#for i in range(4):
    y = - width/2
    if (zig):
        y += (hexSpacing + hexSize)/2
    while (y < width/2 + hexSize +hexSpacing):
    #for j in range(4):
    #if True:
        hexmask = hexmask\
            .pushPoints([(x,y)])\
            .polygon(6, hexSize).extrude(- wall - 2);
        y += (hexSize + hexSpacing);
    zig = not zig;
    x += (hexSize + hexSpacing) * 0.9; 

offsetMask = cq.Workplane("XY").box(length - hexOffset*2, width - hexOffset*2, heigth + 10, (True, True, False)).edges("|Z").fillet(fillet)
hexmask = hexmask.intersect(offsetMask)
del offsetMask
case = case.cut(hexmask)
del hexmask


#Screw Posts
case = case.union(basePlane.rect(dX, dY, forConstruction=True).vertices()\
        .circle(pOuterRadius).extrude(-pHeigth))
screwHoles = basePlane.rect(dX, dY, forConstruction=True).vertices()\
        .circle(pInnerRadius).extrude(-pHeigth)
case = case.cut(screwHoles)
del screwHoles
