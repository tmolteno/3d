/*
    Openscad Birdfeeder.

    Copyright (C) 2014. Tim Molteno, tim@molteno.net
  
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
$fn=12;

hopper_height = 120;
wall_thickness = 3; 
base_diameter = 150;

module base() {
  difference() {
   cylinder(r=base_diameter/2, h=15);
   translate([0,0,5]) cylinder(r=base_diameter/2 - wall_thickness, h=15);
   
   for (angle = [0:60:300]) {
     rotate(angle) translate([60,0,0]) cylinder(r=5, h=25);
   }
  }
}


module hopper() {
  union() { 
  difference() {
    cylinder(r=25, h=hopper_height);
    translate([0,0,0]) cylinder(r=25-wall_thickness, h=hopper_height+5);
    translate([0,0,5]) rotate([90,0,0]) cylinder(r=12, h=100, center=true);
    translate([0,0,5]) rotate([0,90,0]) cylinder(r=12, h=100, center=true);
    translate([0,0,hopper_height-15]) rotate([90,0,0]) cylinder(r=12, h=100);
  }
  cylinder(r=25, h=5); // base plate
}
}

module cap() {
  translate([0,0,hopper_height]) {
    difference() {
      translate([0,0,4]) cylinder(r1=25, r2=5, h=30);
      cylinder(r1=25-wall_thickness, r2=1, h=30);
    }
    translate([0,0,33]) {
      difference() {
        cylinder(r=5, h=15);
        translate([0,0,10]) rotate([90,0,0]) cylinder(r=3, h=30, center=true); 
      }
    }
  }
}

union() {
  base();
  translate([0,0,4]) hopper();
  cap();
}