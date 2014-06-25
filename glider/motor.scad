module motor_mount() {
  difference() {
    union() {
      cylinder(r=6.5, h=10);
      translate([0,0,0.75]) cube([26,7 ,1.5], center=true);
      translate([0,0,0.75]) cube([7, 26,1.5], center=true);
    }
    cylinder(r=4, h=12, center=true);
    for (angle = [0,90,180,270]) {
      rotate(angle) translate([10,0,0]) cylinder(r=1.5, h=5, center=true);
    }
  }
}

/* Turnigy 2730-1500 */
module motor() {
  rotate([0,90,0]) {
    motor_mount();
    cylinder(r=1.5, h=42); // shaft
    translate([0,0,3]) cylinder(r=4, h=15); // housing
    translate([0,0,18]) cylinder(r=13.5, h=10); // outrunner
    translate([0,0,28]) cylinder(r=4, h=4.5); // forward housing
  }
}
