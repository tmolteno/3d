/*
    Motor mounts for the OpenSCAD aeroplane

    Copyright (C) Tim Molteno, tim@molteno.net

    
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
    color("silver") cylinder(r=1.5, h=42); // shaft
    color("gold") translate([0,0,3]) cylinder(r=4, h=15); // housing
    color("red") translate([0,0,18]) cylinder(r=13.5, h=10); // outrunner
    translate([0,0,28]) cylinder(r=4, h=4.5); // forward housing
  }
}


/* Turnigy nano-tech 300mAH 2S 35-70C */
module battery() {
  cube([46, 18,12.5], center=true);
}


/* Servo. Turnigy TG9e */

module servo() {
  rotate([0,0,90]) {
    translate([-6, -11.5,0]) cube([12, 23, 23]);
    translate([-6,-16.25,16.5]) cube([12, 32.5, 2]);
    translate([0,0,23]) cylinder(r=6, h=4);
    translate([0,0,27]) cylinder(r=2.5, h=2.5);
  }
}

module servo_arm() {
  cylinder(r=3.5, h=4);
  translate([0,0,2.5]) hull() {
    cylinder(r=3.5, h=1.5);
    translate([14,0,0]) cylinder(r=2, h=1.5);
  }
}

motor();
