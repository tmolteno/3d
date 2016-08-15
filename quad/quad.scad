motor_dia = 23.0;
motor_height = 18.5;
controller_width = 40;

use <prop/multistar_1704_1900kv.scad>;

module motor_mount() {
    translate([0,0,-5]) cylinder(d=motor_dia, h=5);
}


module prop_disk() {
    prop();
    translate([0,0,-10]) difference() {
        cylinder(d=120, h=10);
        cylinder(d=120-5, h=30, center=true);
    }
}


// DYS BE 1806
module motor() {
    cylinder(d = motor_dia, h=motor_height);
    cylinder(d = 5, h = motor_height+13);
    translate([0,0,motor_height+13]) rotate(90) prop_disk(); // cylinder(d=prop_diameter, h=10);
}

prop_diameter = 120;
motor_offset = (prop_diameter - 15)/2;

module arm_base(height) {
    hull() {
        translate([motor_offset, 0, height]) motor_mount();
        translate([0, -25/2, 0]) cube([25, 25, 10]);
    }
    // Show motor and prop disk
    # translate([motor_offset, 0, height]) motor();

}

module motor_mount_hole() {
    union() {
        cylinder(h=70, d=3, center=true);
        translate([0,0,-105]) cylinder(h=100, d=6);
    }
}

module arm(height) {
    difference() {
        arm_base(height);
        
        // Motor Holes
        translate([motor_offset, 0, height]) {
            for (a =[0, 180]) {
                rotate(a) translate([6,0,0]) motor_mount_hole();  // 12.0 mm dia
                rotate(a + 90) translate([8,0,0]) motor_mount_hole(); // 16 mm dia
            }
        }
    }
}


module base() {
    cylinder(d=70, h=10);
    
    // Arms
    for (a =[0, 180]) {
        rotate(a) translate([20,0,0]) arm(65);
        rotate(a + 90) translate([20,0,0]) arm(50);
    }
    
    // KK Mini
}

base();

//#difference() {
//    cylinder(d=270,h=100);
//    cylinder(d=265, h=500, center=true);
//}