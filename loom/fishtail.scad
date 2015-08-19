/*
    Openscad Rubber-band Loom.

    This is a fishtail rubber-band loom for weaving.

    Copyright (C) 2014. Linus Molteno, linus@molteno.net
  
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

module fishtail_post(h) {
  difference() {
    cube([5,5,h]);
    translate([1,-1,-1])cube([3,4,h+5]);
    translate([1,-1,1.5])cube([3,4,h-3]);
    translate([-2,-2, 1]) cube([10,4,h-2]);
    translate([-1,-1,-1])cube([10,3,3]);
    hull() {
    translate([-1,1,0.25])rotate([90,90,90])cylinder(r=2, h=10);
    translate([-1,0,3])rotate([90,90,90])cylinder(r=2, h=10);
    }
  }
}

module base() {
  difference() {
    cylinder(h=20, r=5);
    translate([0,0,-1])cylinder(h=23,r=3);
    translate([-13,2,10])cube(20,5,5);
  }
}
module full() {
  translate([-7,2,20])rotate([0,0,270])fishtail_post(h=10);
  translate([7.5,-3,20])rotate([0,0,90])fishtail_post(h=10);
  base();
}

full();