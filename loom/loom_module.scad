/*
    Openscad Rubber-band Loom.

    This is a rubber-band loom for weaving.

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

post_height  = 18.0;  /* Height of the Loom from Bottom to top */
base_height  = 4.0;   /* Height of the base (mm) */

  
module post(h) {
  difference() {
    hull() {
      translate([ 5,0,0]) cylinder(r = 3, h=h, $fn=13);
      translate([-1.5,0,0]) cylinder(r = 3, h=h, $fn=13);
    }
    hull() {
      translate([-0.75,0,-1]) cylinder(r = 2.0, h=h + 2, $fn=13);
      translate([2,0,-1]) cylinder(r = 2.2, h=h + 2, $fn=13);
    }
    translate([2.5,0, base_height+3.75]) hull() {
      rotate([90,0,0]) cylinder(r=2.5, h=10, center=true, $fn=19);
      translate([1,0,5]) rotate([90,0,0]) cylinder(r=3.5, h=10, center=true, $fn=19);
    }
    translate([2.5,-5,-2.5]) cube([10,10,h+5]);
  }
  cylinder(r=4, h=base_height+1);
}


module base(width, center, step_angle) {
  
  for (angle = [0:step_angle:(360 - step_angle)]) {
    rotate(angle)  translate([width/2-1.5,0,0]) post(post_height);
  }
  difference() {
    cylinder(r=width/2, h=base_height,$fn=31);
    translate([0,0,-1]) cylinder(r=center/2, h=12, $fn=31); // Center Hole
  }
}


module loom(n_posts, post_spacing) {

  width = (post_spacing*n_posts) / 3.1415;
  center = width - 12.0;
  step_angle = 360 / n_posts;


  intersection() {
    base(width, center, step_angle);
    cylinder(r=width/2, h=50, $fn=31);
  }
}


loom(8, 12);
//post(18);
