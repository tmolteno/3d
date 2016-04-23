/* Wing Strut for the GWS E-Starter 

    Author: Linus Molteno <linus@molteno.net>
    Copyright 2016.
    License GPLv3
*/

strutWidth = 5;
clipLength = 25;
holeDi = 2;
holeSpacing = (clipLength*0.8) + strutWidth/4 + strutWidth;
holeSpacing2 = (clipLength*0.8) + strutWidth/4;
height = 1.5;
pillarHeight = 4.0;
ballDiameter = holeDi * 1.2;
$fn=31;

module inbetween() {
	translate([0,0,height/3])cube([strutWidth,strutWidth/4,height/3]);
}
cube([strutWidth,strutWidth,height]);
translate([0,strutWidth,0])inbetween();
translate([0,-strutWidth/4,0])inbetween();
difference() {
	translate([0,strutWidth+(strutWidth/4),0])cube([strutWidth,clipLength,height]);
	translate([strutWidth/2,holeSpacing,-1])cylinder(d=holeDi,h=height+2);
}
translate([strutWidth,-strutWidth/4,0])rotate([0,0,180])cube([strutWidth,clipLength,height]);
translate([strutWidth/2,-holeSpacing2,height])cylinder(d=holeDi,h=pillarHeight);
translate([strutWidth/2,-holeSpacing2,pillarHeight+ballDiameter/2])sphere(d=ballDiameter);