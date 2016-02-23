width = 1560;
height = 2200;
depth = 300;

module plank(length) {
    cube([length, 100, 20]);
}


module vertical(length) {
    rotate([0,-90,0]) plank(length); 
}



translate([0,0,0]) vertical(2200);
translate([0,depth,0]) vertical(2200);
translate([width,0,0]) vertical(2200);
translate([width,depth,0]) vertical(2200);
