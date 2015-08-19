/*
	 Guitar Pick No. 2.

    This pick is twisted to emulate a gypsy pick.

    Copyright 2014, Peter and Tim Molteno. tim@molteno.net

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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