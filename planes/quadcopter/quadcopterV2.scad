canD = 67;
canH = 124;
wall = 3;
module can() {
	intersection() {
		difference() {
			cylinder(d = canD,h = canH/2, center = true);
			translate([0,0,-wall])cylinder(d = canD-wall, h = canH/2, center=true);
		}
		cube([canD*0.85,canD*0.85,canH], center=true);
	}
}
can();
//translate([0,0,-wall])cylinder(d = canD-wall, h = canH, center=true);