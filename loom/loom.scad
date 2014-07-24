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
$fn=31;

n_posts      = 8;     /* Number of posts */
post_spacing = 10.0;  /* Spacing between posts around perimeter */
post_height  = 18.0;  /* Height of the Loom from Bottom to top */

width = (post_spacing*n_posts) / 3.1415;
center = width - 12.0;
step_angle = 360 / n_posts;


module post(h) {
  difference() {
    cylinder(r = 3, h=h);
    translate([0,0,-1]) cylinder(r = 2, h=h + 2);
  }
}


module base() {
  
  for (angle = [0:step_angle:(360 - step_angle)]) {
    rotate(angle)  translate([width/2-1,0,0]) post(post_height);
  }
  difference() {
    cylinder(r=width/2, h=6);
    translate([0,0,-1]) cylinder(r=center/2, h=12);
  }
}


intersection() {
  difference() {
    base();
    translate([0,0,7]) difference() {
      cylinder(r=width, h=8.5);
      cylinder(r=width/2-1, h=8.5);
    }
  }
  cylinder(r=width/2, h=50);
}