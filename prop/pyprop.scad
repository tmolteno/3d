/*
 * The parameters for the prop are written into the file 'prop_parameters.scad' by the design programme.
 * This file should contain the following definitions.
 * 
center_hole = 5; // diameter of the prop shaft.
hub_diameter = 13.0;
blade_radius = 100;
hub_height = 6.0;
n_blades = 2;
blade_name = "blade5x3.stl";
*/
include <prop_parameters.scad>;

module blade() {
     import(blade_name);
}

$fn=121;

module prop() {
    difference() {
        intersection() {
            union() {
            for(angle = [0 : (360/n_blades) : 360]) {
                rotate(angle) blade();
            }
            translate([0,0,-hub_height]) cylinder(d=hub_diameter+0.1, h=hub_height);
            }
        }
       cylinder(d = center_hole, h=55, center=true);
    }
}
prop();
