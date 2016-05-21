length = 50;
tipWidth = 4;
baseWid = 2;
height = 5;
diameter = 15;
wheelD = 10;
hull() {
	translate([length+diameter+1,-tipWidth/2,0])cube([1,tipWidth,height]);
	translate([diameter/2-1,-baseWid/2,0])cube([1,baseWid,height]);
}
difference() {
	translate([0,0,0])cylinder(d=diameter,h=height);
	translate([0,0,-1])cylinder(d=wheelD,h=height+2);
}
