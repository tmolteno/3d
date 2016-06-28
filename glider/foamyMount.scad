use <motor.scad>;

width = 72;
radius = 17;
length = 65;

mount_offset = 17;

translateY = width-2*radius;
translateX = length-2*radius;
 module pillar() {
     difference() {
         cylinder(h=35, r=4, $fn=31);
     }
 } 
  module motorMount() {
     cylinder(r=20, h= 35);
  }

  module holes() {
     for (angle = [0,90,180,270]) {
      rotate(angle) translate([mount_offset,0,0]) cylinder(r=1.5, h = 100,center=true);
     }
     translate([0,0,-1])cylinder(d=30,h=100);
     translate([0,0,12.5])rotate([90,0,45])cylinder(d=15,h=100);
     translate([0,0,12.5])rotate([0,270,45])cylinder(d=15,h=100);
     translate([0,0,12.5])rotate([0,90,45])cylinder(d=15,h=100);
//     translate([0,0,12.5])rotate([270,0,45])cylinder(d=10,h=100);
     translate([0,0,35])rotate([270,0,45])cylinder(d=10,h=100);
 }
    
difference() {
    union() {
    hull() {
        cube([55,30,5]);
    }
    translate([translateX/2+10,translateY/2-4,0])rotate([0,0,45])motorMount();
    }
    translate([translateX/2+10,translateY/2-4])rotate([0,0,45])holes();
}