difference() {
    cube([25,30,2]);
    translate([12.5,5,-1])cylinder(r=3,h=4);
    translate([12.5,5+20,-1])cylinder(r=3,h=4);
}