#!/usr/bin/env python 
''' Project Metal Box Template for BitX40  http://www.hfsigs.com/

This is a executable python program that generates DXF (2-d CAD Files) that are templates for a project metal box for the BitX40 radio  (http://www.hfsigs.com/ ).  3 DXF files are created - Top pattern, Bottom pattern and Front Panel. 

This program uses the python dxfwrite library ("pip install dxfwrite").  The project box dimensions can be modified by adjusting the paramters below.

version  1.0

''' 

import dxfwrite 
from dxfwrite import  DXFEngine as dxf

''' circle_ch()

draws a circle with a cross-hair.  It adds the circle to the default '0' layer, and a cross-hair in the drill layer. 

'''
def circle_ch(r, x , y , chl=1.0, layer='0', layerch='drill' ):  
    ''' Circle with cross-hair center ''' 
    drawing.add(dxf.circle( r , ( x, y) , layer=layer) ) 
    drawing.add(dxf.line( (x, y - chl ) , ( x , y + chl) , layer=layerch) ) 
    drawing.add(dxf.line( (x + chl , y  ) , ( x - chl  , y ) , layer=layerch) ) 

''' 
Dimensions of Project box - set variables here
''' 
# box dimensions
w = 140.0 # width of box
h = 60.0 # height of box
d = 160.0 # depth of box
t = 10.0 # tab width
ba = 1.790 # bend adjust

# other dimensions
chl = 1.5  # cross hair length
cr = 5 # calibration circle radius = 5mm radius/10mm diameter

# box hole sizes
tr = 1.13 # number 4 screw hole for AL is 0.089 inches, 2.25 mm dia

# lcd cutout dimensions and location
lw = 72.0 # lcd width
lh = 25.0 # lcd height
lx = 0.18 * h  # lcd x 
ly = t + (w * 0.40) + 2.0    # lcd y 
lhr=2.0 # lcd drilling hole radius

lmh1x= lx - ( (31.0 - lh )/2.0) # lcd mnt hole 1 x
lmh1y= ly - ( (75.0 - lw )/2.0) # lcd mnt hole 1 y
lmh1r = 1.56 # lcd mnt hole 1 radius 1/8"

# volume pot size and location
volx=42.0
voly=20.0 + t
volr=3.5

#  tuning  pot size and location
tunx=18.0
tuny=voly
tunr=5.0 # tuning pot hole radius


# jack - mic
micx=50.0
micy=90.0 + t
micr=2.8

# jack - head
headx=50.0
heady=101.5 + t
headr=2.8

# anderson pp opening
ppw=17.5
pph=9.7
ppx= 4.0 + (1.5*h)+d-(pph/2.0) 
ppy= t + (w*3.0/4.0) - (ppw/2.0)   

pphr=2.0 # pp mnt holes - radius
pphd=17.3  # pp mnt holes - distance

# ant hole

antx= 4.0 +  (1.5*h) + d 
anty= t + (1.0*w/4.0) 
antr= 6.35 # ant connector radius


# pcb mounting holes

pcbw = 117.5 #pcb hole width
pcbd = 105.0 #pcb hole width
pcbr = 1.75 # pcb hole radius
pcbx = h + ( (d - pcbw) / 2.0 ) + 7.0
pcby = t + ( (w - pcbd) / 2.0 )

''' main

'''


print "Project box dxf file creator - bitx"
print "version 1.0"
print "box dimensions (mm) height: %6.2f width: %6.2f depth: %6.2f tab: %6.2f" % (h,w,d,t) 
print "box dimensions (mm) bend adjustment: %6.2f " % (ba) 

'''
Top + Sides
'''
# define top drawing
drawing = dxf.drawing('pb_top.dxf')


alen = w + ( 2.0*h ) + ( 2.0*ba)  # adjusted length

# main outline
drawing.add(dxf.rectangle( (0,0), d,  alen ) )  
# create layers
drawing.add_layer('bend',color=2)
drawing.add_layer('calibrate', color=3)
drawing.add_layer('drill', color=4) 
# add bend lines
acen = alen / 2.0 # center of adjusted length
bendlen =   ( w + ba/2.0 ) / 2.0 # bend length from center 
drawing.add(dxf.line( ( 0,  acen + bendlen ) , ( d, acen + bendlen), layer='bend' ) )    
drawing.add(dxf.line( ( 0, acen - bendlen ),( d, acen - bendlen  ), layer='bend' ) )    
# add box screw holes (#4 screws) 
# side 1
circle_ch(tr,t/2,h/2) 
circle_ch(tr,d-(t/2),h/2) 
circle_ch(tr,d/2,t/2) 
# side 1
circle_ch(tr,t/2,alen-(h/2)) 
circle_ch(tr,d-(t/2),alen - (h/2)) 
circle_ch(tr,d/2,alen - (t/2)) 

# add calibration marks
circle_ch(cr,d/2.0,acen,chl,'calibrate','calibrate') 
drawing.save() 

'''
Box Bottom (Front/Back+tabs) 

'''

drawing = dxf.drawing('pb_bottom.dxf')

# add layers
drawing.add_layer('bend',color=2)
drawing.add_layer('calibrate', color=3)
drawing.add_layer('drill', color=4) 

# bottom outline
drawing.add(dxf.rectangle( (0,0), d  + (2.0*h) , ( 2.0 * t ) + w  ) ) 
# lcd hole
drawing.add(dxf.rectangle( (lx,ly), lh, lw ) ) 
# lcd corner holes
circle_ch(lhr, lx+lhr, ly+lhr)  
circle_ch(lhr, lx+lh-lhr, ly+lw-lhr)  
circle_ch(lhr, lx+lhr, ly+lw-lhr)  
circle_ch(lhr, lx+lh-lhr, ly+lhr )  

# lcd mnt holes
circle_ch(lmh1r, lmh1x, lmh1y)  
circle_ch(lmh1r, lmh1x + 31.0, lmh1y)  
circle_ch(lmh1r, lmh1x + 31.0, lmh1y + 75.0)  
circle_ch(lmh1r, lmh1x , lmh1y + 75.0)  

# pot holes
circle_ch(volr,volx,voly) 
circle_ch(tunr,tunx,tuny) 

# Kenwood-style  2 pin jack holes
circle_ch(micr,micx,micy) 
circle_ch(headr,headx,heady) 

# Anderson Powerpole  opening
drawing.add(dxf.rectangle( (ppx,ppy),pph, ppw ) ) 

# antenna  opening
circle_ch(antr,antx,anty) 

# 4 PCB  mounting holes 
circle_ch(pcbr,pcbx,pcby) 
circle_ch(pcbr,pcbx+pcbw,pcby) 
circle_ch(pcbr,pcbx,pcby+pcbd) 
circle_ch(pcbr,pcbx+pcbw,pcby+pcbd) 

# calibration hole
circle_ch(cr, (d +(2.0*h))/2.0  , ((2.0*t)+w)/2.0,chl,'calibrate','calibrate') 

# front bends
drawing.add(dxf.line( ( h, 0 ) , (  h,  (2.0*t) + w ), layer='bend' ) )    
drawing.add(dxf.line( ( d + h , 0  ),( d+h,  (2.0*t) + w )  , layer='bend' ) )    

# tab bends 
drawing.add(dxf.line( ( 0, t + w ) , ( d+(h*2.0) ,  t + w ), layer='bend' ) )    
drawing.add(dxf.line( ( 0, t  ),( d+(h*2.0) ,  t  )  , layer='bend' ) )    

drawing.save() 

'''
Front panel template
'''
drawing = dxf.drawing('pb_front.dxf')

drawing.add_layer('bend',color=2)
drawing.add_layer('calibrate', color=3)
drawing.add_layer('drill', color=4) 

# rounded rectangle radius 
rrr=2.0

# full panel outline
drawing.add(dxf.line( (rrr, 0.0) , ( h-rrr, 0.0) ) )   
drawing.add(dxf.line( (rrr, w)   , ( h-rrr, w)   ) )   
drawing.add(dxf.line( (0.0, rrr) , ( 0.0, w-rrr) ) )   
drawing.add(dxf.line( (h, rrr)   , ( h, w-rrr)   ) )   


# edge corners rounded
drawing.add(dxf.arc(rrr,center=(rrr,rrr),startangle=180.0,endangle=270.0))
drawing.add(dxf.arc(rrr,center=(rrr,w-rrr),startangle=90.0,endangle=180.0))
drawing.add(dxf.arc(rrr,center=(h-rrr,rrr),startangle=270.0,endangle=0.0))
drawing.add(dxf.arc(rrr,center=(h-rrr,w-rrr),startangle=0.0,endangle=90.0))

# lcd hole
drawing.add(dxf.rectangle( (lx,ly-t), lh, lw ) ) 

# pot holes
circle_ch(volr,volx,voly-t) 
circle_ch(tunr,tunx,tuny-t) 

# Kenwood-style 2 pin jack holes
circle_ch(micr,micx,micy-t) 
circle_ch(headr,headx,heady-t) 

drawing.save() 

