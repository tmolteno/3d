module raw_blade() {
        union() {
            import("test_prop_blade.stl");
        }
}

$fn=31;

center_hole = 5;
center_r = center_hole / 2;
key_r = 3;
hub_h = 8;
hub_r = 5.5;

module blade_inside() {
    hull() {
        intersection() {
            cylinder(r = hub_r+0.25, h=100, center=true);
            raw_blade();
        }
        translate([center_hole/2+1 ,0,-hub_h]) cylinder(d=2, h=hub_h);
    }
}

module key() {
    translate([center_hole/2-key_r*cos(120)+0.5, 0,0]) hull() {
        for(a =  [120:120:350]) {
            rotate(a) translate([key_r,0,-hub_h]) cylinder(d=1, h=hub_h);
        }
       translate([0 ,0,-hub_h]) cylinder(d=2, h=hub_h);
    }
    blade_inside();
}


module blade_root() {
    union() {
           raw_blade();
           key();
   }
}

overlap = 1.0;
module hub() {
    difference() {
        translate([0,0,-hub_h-overlap]) cylinder(r=hub_r,h=hub_h+2*overlap);
         for(angle =  [0:120:360]) {
                 rotate(angle) translate([0,0,0]) key();
        }
        cylinder(d=center_hole,h=100,center=true);
    }
}

module bottom_half() {
    translate([0,0,hub_h + overlap]) difference() {
        hub();
        translate([-50,-50,-hub_h/2]) cube([100,100,20]);
    }
}

module top_half() {
    translate([0,0,overlap]) rotate([180,0,0]) difference() {
        hub();
        translate([-50,-50,-hub_h/2-20]) cube([100,100,20]);
    }
}
for(a=[0:120:360]) rotate(a) translate([hub_r*2,0,-center_r]) rotate([0,270,0]) blade_root();
//blade_inside();
//key();
//hub();
rotate(60) translate([hub_r + 2,0,0]) top_half();
rotate(-60) translate([hub_r +2,0,0]) bottom_half();

