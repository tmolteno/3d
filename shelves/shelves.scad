width = 1560;
height = 2200;
depth = 300;

module plank(length) {
    cube([length, 65, 19]);
}

module vertical(length) {
    rotate([0,-90,0]) plank(length); 
}
module shelf(height) {
    translate([0,0,height])cube([width/2, depth, 20]);
}

translate([0,0,0]) vertical(2200);
translate([0,depth,0]) vertical(2200);
translate([width,0,0]) vertical(2200);
translate([width,depth,0]) vertical(2200);
translate([width/2,0,0]) vertical(2200);
translate([width/2,depth,0]) vertical(2200);
shelf(865); 