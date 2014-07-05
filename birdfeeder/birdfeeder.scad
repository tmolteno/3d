/*
    Openscad Birdfeeder.

    This birdfeeder can be hung in a tree, and filled with seeds.

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
$fn=32;

hopper_height = 120;
wall_thickness = 3; 
base_diameter = 135;
cap_height = 20;

module base() {
  difference() {
   cylinder(r=base_diameter/2, h=15);
   translate([0,0,5]) cylinder(r=base_diameter/2 - wall_thickness, h=15);
   
   for (angle = [0:40:320]) {
     rotate(angle) translate([60,0,-5]) cylinder(r=2, h=25);
   }
  }
  for (angle = [20:40:340]) {
    rotate(angle) hull() {
      translate([base_diameter/2-3,0,0]) cylinder(r=2, h=15);
      translate([20,0,0]) cylinder(r=2, h=7);
    }
  }
}

hopper_radius = 25;

module bayonet() {
  rotate([0,90,0]) cylinder(h=hopper_radius + 2, r=3);
}

module bayonet_fitting() {

 hull() {
    bayonet();
    rotate(20) bayonet();
 }
 hull() {
    rotate(20) bayonet();
    translate([0,0,15]) rotate(20) bayonet();
 }
 hull() {
    bayonet();
    translate([0,0,3]) bayonet();
 }
}

module hopper() {
  union() { 
    difference() {
      cylinder(r=hopper_radius, h=hopper_height);
      translate([0,0,0]) cylinder(r=hopper_radius-wall_thickness, h=hopper_height+5);
      translate([0,0,5]) rotate([90,0,0]) cylinder(r=10, h=100, center=true);
      translate([0,0,5]) rotate([0,90,0]) cylinder(r=10, h=100, center=true);
      translate([0,0,hopper_height-14]) bayonet_fitting();
      translate([0,0,hopper_height-14]) rotate(180) bayonet_fitting();
    }
    cylinder(r1=base_diameter/2-3, r2=25.5, h=5); // base plate
  }
}

module cap() {
   {
    translate([0,0,18]) cylinder(r1=hopper_radius+5, r2=5, h=cap_height+7);
    cylinder(r=hopper_radius-wall_thickness-0.5,h=19);
    translate([0,0,3]) bayonet();
    translate([0,0,3]) rotate(180) bayonet();
    translate([0,0,cap_height+20]) {
      difference() {
        hull () {
          translate([0,0,15]) sphere(r=5);
          cylinder(r=5, h=5);
        }
        translate([0,0,10]) rotate([90,0,0]) cylinder(r=3, h=cap_height, center=true); 
      }
    }
  }
}

/* There are two parts to print separately. The base+hopper, and the cap
*/
module feeder() {
  union() {
    base();
    translate([0,0,4]) hopper();
  }
}

  
feeder();
translate([0,0,hopper_height - 13]) cap();

