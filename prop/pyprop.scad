module blade() {
            import("blade5x3.stl");
}

center_hole = 5; // diameter of the prop shaft.
hub_diameter = 12.0;
hub_height = 6.0;

$fn=121;

module prop() {
    difference() {
        intersection() {
            union() {
            for(angle = [0 : 180 : 360]) {
                rotate(angle) blade();
            }
            translate([0,0,-hub_height]) cylinder(d=hub_diameter+0.1, h=hub_height);
            }
        }
       cylinder(d = center_hole, h=55, center=true);
       //translate([-100,-100,0]) cube([200,200,200]);
    }
}
prop();
