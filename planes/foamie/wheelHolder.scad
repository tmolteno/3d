width = 50;
length = 80;
height=35;

heightOfWheels = 15;
walls = (width - 32)/2;
screwR = 1.25;

$fn=31;
use <MCAD/boxes.scad> 


difference() {
	translate([width/2, length/2, height/2]) roundedBox([width, length, height], radius=5);
	translate([walls, -1,heightOfWheels+10])cube([32,100,100]);
	translate([walls-5,length/2-2,-1])cube([width-walls /1,2.5,heightOfWheels -2]);
	translate([width-walls * 1.25,length/2-4,-1])cylinder(r=screwR, h=5);
	translate([width-walls * 4.5,length/2+2.5,-1])cylinder(r=screwR, h=5);
    translate([walls,-1,2])cube([32,30,100]);
    
    
    translate([width/2, length/4,0]) cylinder(d= width/2, h=100, center=true);
    translate([width/2, length*0.75,0]) cylinder(d= width/2, h=100, center=true);
    translate([width/2,length/4,height/2])rotate([0,90,0])cylinder(d=width/2,h=1000, center=true);
     translate([width/2,length*0.75,height/2])rotate([0,90,0])cylinder(d=width/2,h=1000, center=true);
}