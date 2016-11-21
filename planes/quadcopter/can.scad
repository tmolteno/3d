canD = 67;
canH = 124;
wall = 3;
UltraWid = 45;
UltraLen = 20;
UltraHole = 1.3;
module can() {
	intersection() {
		difference() {
			cylinder(d = canD+wall,h = canH/2, center = true);
                translate([0,0,-wall])
                cylinder(d = canD, h = canH/2, center=true);
		}
		cube([canD*0.85,canD*0.85,canH], center=true);
	}
    difference() {
        translate([-canD/2+6,0,0])
        cube([15, UltraWid-4, UltraLen], center=true);
            translate([0,0,0])  
            cylinder(d = canD,h = canH/2, center = true); 
        translate([-canD/2,0,-6])
        cube([4,12,10],center=true);
    }
    difference() {
        translate([-canD/2-2,0,0])
        cube([1, UltraWid, UltraLen],center=true);
        //Mounting holes for the ultrasonic sensor
        translate([0,-21,-17/2])
        rotate([0,270,0])
        cylinder(d=UltraHole,h=100);
        translate([0,-21,17/2])
        rotate([0,270,0])
        cylinder(d=UltraHole,h=100);
        translate([0,21,-17/2])
        rotate([0,270,0])
        cylinder(d=UltraHole,h=100);
        translate([0,21,17/2])
        rotate([0,270,0])
        cylinder(d=UltraHole,h=100);
        //RUNS INTO CAN (not anymore)
        translate([-canD/2-1,0,-6])
        cube([4,12,10],center=true);
    }
    //battery mounting
    translate([-1,-20,29.5])difference() {
        cube([36, 40,18]);
        translate([2+32/2,0,1.5+15/2])cube([32,100,15], center = true);
        
    }
    translate([-35,-20,29.5])difference() {
        cube([36, 40,18]);
        translate([2+32/2,0,1.5+15/2])cube([32,100,15], center= true);
        
    }
}
can();
//translate([0,0,-wall])
#cylinder(d = canD-wall, h = canH, center=true);