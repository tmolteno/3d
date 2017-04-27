/*
 * The parameters for the prop are written into the file 'prop_parameters.scad' by the design programme.
 * This file should contain the following definitions.
 * 
*/

middle = (y_max + y_min) / 2;

module raw_blade() {
        translate([0,0,-middle]) {
            import(blade_name);
        }
}

$fn=31;

center_r = center_hole / 2;
key_r = hub_diameter / 3.5;
hub_h = hub_height + 2;
hub_r = hub_diameter / 2 + 1;

module blade_inside() {
    intersection() {
        cylinder(r = hub_r+0.25, h=100, center=true);
        raw_blade();
    }
}

module key() {
    rotate([40,0,0]) translate([center_hole/2-key_r*cos(120)+1, 0,0]) hull() {
        for(a =  [120:120:350]) {
            rotate(a) translate([key_r,0,-hub_h/2]) sphere(d=1);
            rotate(a) translate([key_r,0,hub_h/2]) sphere(d=1);
        }
       translate([0 ,0,-hub_h/2]) sphere(d=1);
       translate([0 ,0, hub_h/2]) sphere(d=1);
    }
    hull() {
        blade_inside();
        translate([-key_r/3,0,0]) blade_inside();
    }
}


module blade_root() {
    union() {
           raw_blade();
           key();
   }
}

overlap = 1.0;
z_move = -(hub_h+2*overlap)/2;
module hub() {
    difference() {
        translate([0,0,z_move]) cylinder(r=hub_r,h=hub_h+2*overlap);
         for(angle = [0 : (360/n_blades) : 360]) {
                 rotate(angle) translate([0,0,0]) key();
        }
        cylinder(d=center_hole,h=100,center=true);
    }
}

module bottom_half() {
    translate([0,0,-z_move]) difference() {
        hub();
        translate([-50,-50,0]) cube([100,100,20]);
    }
}

module top_half() {
    translate([0,0,-z_move]) rotate([180,0,0]) difference() {
        hub();
        translate([-50,-50,-20]) cube([100,100,20]);
    }
}
for(a = [0 : (360/n_blades) : 360])  rotate(a) translate([hub_r*2,0,-(center_r+0.5)]) rotate([0,270,0]) blade_root();
//blade_root();
//key();
//hub();
rotate(60) translate([hub_r + 2,0,0]) top_half();
rotate(-60) translate([hub_r +2,0,0]) bottom_half();
