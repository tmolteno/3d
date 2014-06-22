/*
	Guitar Pick.

   Copyright 2014, Peter and Tim Molteno. tim@molteno.net

   Licensed under GPLv3
*/
$fn = 37;
pick_length = 16;
tip_radius = 2;
hold_radius = 11;

module pick() {
  hull() {
    translate([0,0,0.0]) cylinder(r=tip_radius,h=1);
    translate([pick_length,0,0]) cylinder(r=hold_radius,h=3);
  }
}

difference() {
  pick();

  // Now decorate the pick with some features.
  translate([pick_length,0,17]) sphere(r=17, center=true, $fn=101);
  translate([pick_length,0,]) cylinder(r=4, h=10, center=true, $fn=25);
  translate([pick_length,0,]) {
    for (angle = [0:60:300]) {
      rotate(angle) translate([5.95,0,0]) cylinder(r=1, h=5, center=true);
    }
  }
}