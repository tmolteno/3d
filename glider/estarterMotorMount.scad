use <motor.scad>;

width = 72;
radius = 17;
length = 65;

mount_offset = 17;

translateY = width-2*radius;
translateX = length-2*radius;
 module pillar() {
     difference() {
         cylinder(h=4, r=4, $fn=31);
     }
 } 
  module motorMount() {
     for (angle = [0,90,180,270]) {
      rotate(angle) translate([mount_offset,0,0]) pillar();
     }
  }

  module holes() {
     for (angle = [0,90,180,270]) {
      rotate(angle+45) translate([22,0,0]) cylinder(d=15, h = 40, center=true);
     }
     for (angle = [0,90,180,270]) {
      rotate(angle) translate([mount_offset,0,0]) cylinder(r=1.5, h = 20,center=true);
     }
     cylinder(r=5,h=20, center=true);
  }
    
difference() {
    union() {
    hull() {
        cylinder(h=3, r = radius);
        translate([0,translateY,0])cylinder(h=3, r = radius);
        translate([translateX,0,0])cylinder(h=3, r = radius);
        translate([translateX,translateY,0])cylinder(h=3, r = radius);
    }
    translate([translateX/2,translateY/2,2])rotate([0,0,0])motorMount();
    }
    translate([translateX/2,translateY/2])holes();
}