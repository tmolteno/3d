use <MCAD/boxes.scad>
$fn =51;

module extruder() {
    translate([0,0,15.5]) cylinder(d=25, h=30);
    translate([4,0,10]) cube([16,16,8], center=true);
    cylinder(d1=1, d2=7, h=6);
}


module fan() {
    rotate([0,90,0]) difference() {
        roundedBox([40,40,8], 3, true);
        cylinder(d=38,h=20, center=true);
    }
}

duct_diameter = 38;

module cooler_old() {
    difference() {
        hull() {
            translate([18,0,-4]) fan();
            translate([0,0,0]) cylinder(d=27,h=30, center=true);
        }
        hull() {
           translate([15,0,0]) rotate([0,70,0]) cylinder(d=31,h=20, center=true);
          translate([0,0,-5]) cylinder(d=25,h=28, center=true);
        }
        cylinder(d=24, h=100, center=true);
        translate([-10,0,0]) cube([20,20,100], center=true);
    }
}

duct_x = 26;

module top_duct() {
    hull() {
          translate([duct_x,0,33]) rotate([0,90,0]) 
              roundedBox([15,34,1], 6, true);
        translate([0,0,16]) cylinder(d=23, h=28);
    }
}
module bottom_duct() {
    hull() {
          translate([duct_x,0,16]) rotate([0,90,0]) 
              roundedBox([15,34,1], 6, true);
        translate([0,0,2]) cylinder(d=15, h=1);
    }
}

module keep_out() {
    union() {
        translate([0,0,-0.1]) cylinder(d = 20, h=16);
        translate([-23,0,39]) cube([40,40,80], center=true);
        extruder();
    }
}

module cooler() {
    difference() {
        hull() {
            translate([duct_x-4,0,25]) fan();
            cylinder(d=30,h=45);
        }
        bottom_duct();
        top_duct();
        keep_out();
    }
}

//rotate(180) extruder();
//translate([duct_x+4,0,25]) color("gray") fan();
cooler();
//bottom_duct();
//top_duct();
//keep_out();