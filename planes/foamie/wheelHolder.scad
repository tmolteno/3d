width = 36;
length = 20;
heightOfWheels = 10;
walls = (width - 32)/2;
screwR = 1;
difference() {
	cube([width, length, 20]);
	translate([walls, -1,heightOfWheels])cube([32,100,100]);
	translate([walls,length/2-2,-1])cube([width-walls * 2,2,heightOfWheels -2]);
	translate([width-walls * 2,length/2-4,-1])cylinder(r=screwR, h=5);
	translate([width-walls * 16,length/2+2,-1])cylinder(r=screwR, h=5);
}