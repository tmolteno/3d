strutWidth = 5;
clipLength = 15;
holeDi = 1;
holeSpacing = (clipLength*0.8) + strutWidth/4 + strutWidth;
holeSpacing2 = (clipLength*0.8) + strutWidth/4;
height = 1;

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
translate([strutWidth/2,-holeSpacing2,height])cylinder(d=holeDi,h=height);
translate([strutWidth/2,-holeSpacing2,2*height])sphere(d=holeDi*1.2,h=height);