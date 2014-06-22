/*
	Guitar Pick 2.

   This pick is twisted to emulate a gypsy pick.

   Copyright 2014, Peter and Tim Molteno. tim@molteno.net

   Licensed under GPLv3
*/
$fn = 37;
pick_length = 15;
tip_radius = 1;
hold_radius = 11;

module pick2d() {
  hull() {
    translate([-pick_length,0,0]) circle(r=tip_radius);
    circle(r=hold_radius);
  }
}

module pick() {
  // For a right-handed pick, change the twist to +10
  linear_extrude(height=3, twist=-10, center=true) 
    pick2d();
}

n = 7; 
difference() {
  pick();

  // Now decorate the pick with some features.
  translate([0,0,17]) sphere(r=18, center=true, $fn=61);

  cylinder(r=4, h=10, center=true, $fn=7);
  
  for (angle = [(360/n):(360/n):360+(360/n)]) {
    rotate(angle) translate([5.95,0,0]) cylinder(r=1, h=5, center=true);
  }
}