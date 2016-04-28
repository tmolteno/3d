module blade() {
            import("blade5x3.stl");
}

center_hole = 5;
hub_diameter = 12.0;
hub_height = 6.0;

$fn=121;

module prop() {
    difference() {
        intersection() {
            union() {
            rotate(0) blade();
            rotate(120) blade();
            rotate(240) blade();
            translate([0,0,-hub_height]) cylinder(d=hub_diameter, h=hub_height+0.5);
            }
        }
       cylinder(d = center_hole, h=55, center=true);
    }
}
prop();
