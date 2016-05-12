module blade() {
     import("blade5x3.stl");
}

center_hole = 5; // diameter of the prop shaft.
hub_diameter = 13.0;
blade_radius = 100;
hub_height = 6.0;
n_blades = 3;

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
       //translate([-blade_radius,-blade_radius,0]) cube([2*blade_radius,2*blade_radius,2*blade_radius]);
    }
}
prop();
