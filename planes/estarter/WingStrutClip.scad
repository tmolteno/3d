/* Wing Strut for the GWS E-Starter 

    Author: Linus Molteno <linus@molteno.net>
    Copyright 2016.
    License GPLv3
*/

inbetweenLength = 1;
strutWidth = 4.5;
clipLength = 35;
holeDi = 1.7;
holeSpacing = 30+inbetweenLength+strutWidth;
holeSpacing2 = 30+inbetweenLength   ;
height = 1.5;
pillarHeight = 4.3;
ballDiameter = 1.7;
$fn=31;

module inbetween() {
    translate([0,0,height/3])cube([strutWidth,inbetweenLength,height/5]);
}
cube([strutWidth,strutWidth,height]);
translate([0,strutWidth,0])inbetween();
translate([strutWidth,0,0])rotate([0,0,180])inbetween();
difference() {
	translate([0,strutWidth+(inbetweenLength),0])cube([strutWidth,clipLength,height]);
	#translate([strutWidth/2,holeSpacing,-1])cylinder(d=holeDi,h=height+2);
}
translate([strutWidth,-inbetweenLength,0])rotate([0,0,180])cube([strutWidth,clipLength,height]);
#translate([strutWidth/2,-holeSpacing2,height])cylinder(d=holeDi,h=pillarHeight);
translate([strutWidth/2,-holeSpacing2,pillarHeight+ballDiameter])sphere(d=ballDiameter);
difference() {
    translate([strutWidth/2,strutWidth/2,height])cylinder(d=4.2,h=6.4);
    translate([strutWidth/2,strutWidth/2,height])cylinder(d=3,h=7);
}