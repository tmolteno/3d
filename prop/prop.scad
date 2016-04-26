module raw_blade() {
        union() {
            import("blade5x3.stl");
        }
}

blade_inner_r = 18;

module inner_mask() {
    difference() {
        cylinder(r=blade_inner_r + 0.1, h=100, center=true);
        cylinder(r=blade_inner_r,h=100, center=true);
    }
}

module blade_root() {
    hull() {
        intersection() {
            raw_blade();
           inner_mask();
        }
        cylinder(d=center_hole,h=5, center=true);
    }
}

module outer_mask() {
    difference() {
        cylinder(r=500, h=100, center=true);
        cylinder(r=blade_inner_r,h=100, center=true);
    }
}
module blade_outer() {
            intersection() {
            raw_blade();
            outer_mask();
        }
}

module blade() {
    union() {
        blade_root();
        blade_outer();
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
            translate([0,0,-5]) cylinder(d=12, h=10, $fn=51);
            }
       //  cylinder(r=100, h=10, center=true);
        }
       cylinder(d = center_hole, h=55, center=true, $fn=31);
    }
}
prop();
