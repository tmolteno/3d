module blade() {
        union() {
            import("prop2.stl");
        }
}

center_hole = 5;
module prop() {
    difference() {
        intersection() {
            union() {
            rotate(0) blade();
            rotate(120) blade();
            rotate(240) blade();
            translate([0,0,-5]) cylinder(d=17, h=10, $fn=51);
            }
         cylinder(r=100, h=10, center=true);
        }
       cylinder(d = center_hole, h=55, center=true, $fn=31);
    }
}
prop();
