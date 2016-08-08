use <quadNoArms.scad>;
canR = 52;
canH = 124;
wall = 3;
intersection() {
	difference() {
		cylinder(r = canR,h = canH/2, center = true);
		translate([0,0,-wall])cylinder(r = canR-wall, h = canH/2, center=true);
	}
	cube([1.76*canR,1.76*canR,canH], center=true);
}