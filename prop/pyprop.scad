module raw_blade() {
        union() {
            import("blade5x3.stl");
        }
}

module blade() {
    union() {
        raw_blade();
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
            translate([0,0,-10]) cylinder(d=12, h=10, $fn=51);
            }
       //  cylinder(r=100, h=10, center=true);
        }
       cylinder(d = center_hole, h=55, center=true, $fn=31);
    }
}
prop();
