/*
    Openscad Aeroplane.

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

/* NACA 5412 Airfoil M=5.0% P=40.0% T=12.0% */

module airfoil(s) {
rotate([0,0,2]) scale([s,s,s]) mirror([1,0])  polygon(points=[
 [1.000000,-0.000000], [0.998459, 0.000480], [0.993844, 0.001912], [0.986185, 0.004266],
 [0.975528, 0.007497], [0.961940, 0.011541], [0.945503, 0.016321], [0.926320, 0.021747],
 [0.904508, 0.027720], [0.880203, 0.034131], [0.853553, 0.040868], [0.824724, 0.047815],
 [0.793893, 0.054856], [0.761249, 0.061875], [0.726995, 0.068760], [0.691342, 0.075399],
 [0.654508, 0.081690], [0.616723, 0.087531], [0.578217, 0.092831], [0.539230, 0.097504],
 [0.500000, 0.101473], [0.460770, 0.104671], [0.421783, 0.107042], [0.383277, 0.108495],
 [0.345492, 0.108628], [0.308658, 0.107381], [0.273005, 0.104801], [0.238751, 0.100962],
 [0.206107, 0.095964], [0.175276, 0.089926], [0.146447, 0.082992], [0.119797, 0.075318],
 [0.095492, 0.067072], [0.073680, 0.058429], [0.054497, 0.049563], [0.038060, 0.040642],
 [0.024472, 0.031824], [0.013815, 0.023248], [0.006156, 0.015030], [0.001541, 0.007261],
 [0.000000, 0.000000], [0.001541,-0.006492], [0.006156,-0.011976], [0.013815,-0.016460],
 [0.024472,-0.019963], [0.038060,-0.022517], [0.054497,-0.024170], [0.073680,-0.024982],
 [0.095492,-0.025026], [0.119797,-0.024389], [0.146447,-0.023173], [0.175276,-0.021490],
 [0.206107,-0.019460], [0.238751,-0.017213], [0.273005,-0.014881], [0.308658,-0.012596],
 [0.345492,-0.010485], [0.383277,-0.008670], [0.421783,-0.007174], [0.460770,-0.005697],
 [0.500000,-0.004250], [0.539230,-0.002888], [0.578217,-0.001653], [0.616723,-0.000578],
 [0.654508, 0.000317], [0.691342, 0.001023], [0.726995, 0.001539], [0.761249, 0.001875],
 [0.793893, 0.002047], [0.824724, 0.002077], [0.853553, 0.001991], [0.880203, 0.001815],
 [0.904508, 0.001578], [0.926320, 0.001305], [0.945503, 0.001019], [0.961940, 0.000743],
 [0.975528, 0.000494], [0.986185, 0.000286], [0.993844, 0.000130], [0.998459, 0.000033],
 [1.000000, 0.000000]]);
}

/* This is a foil with a flat bottom for easy printing */
module flat_foil(s) {
  difference() {
    translate([0,0.02*s, 0]) linear_extrude(height=0.1) airfoil(s);
    translate([-s, -s-5, -1]) cube([s+5,s+5,2]);
  }
}
	
wingspan = 135;
tail_length = 90;
nose_length = 40;

wing_x = 25;
wing_chord = 55;
wing_z = 2;

module wing_left() {
  rotate([90,0,0]) hull() {
     translate([-55,0,0.85*wingspan]) flat_foil(20);
     flat_foil(wing_chord);
    }
}

module wing_center() {
  rotate([90,0,0]) hull() {
     translate([0,0,wingspan/2]) flat_foil(wing_chord);
     translate([0,0,-wingspan/2]) flat_foil(wing_chord);
    }
}


module wing_right() {
  mirror([0,1,0]) wing_left();
}

module wings() {
    translate([wing_x,0,wing_z]) {
      wing_center();
      translate([0, wingspan/2,0]) rotate([10,0,0]) wing_right();
      translate([0, -wingspan/2,0]) rotate([-10,0,0])  wing_left();
    }
}




/** FUSELAGE **/

use <motor.scad>;

module firewall() {
   rotate([0,90,0]) difference() {
	cylinder(r=13.5, h=5, $fn=21);
    for (angle = [0,90,180,270]) {
      rotate(angle) translate([10,0,0]) cylinder(r=1.5, h=12, center=true);
    }
  }
}

module fuselage_plain() {
    %translate([nose_length+5,0,0]) motor();
    translate([nose_length,0,0]) firewall();
    hull() {
      translate([nose_length-5,0,0]) firewall();
      sphere(r=15, $fn=21);
      translate([-tail_length-20,0,2]) sphere(r=3, $fn=21);
    }
}

module fuselage() {
  difference() {
    fuselage_plain();
    wings();
    translate([-tail_length,0,0]) stabilizer_vert();
  }
  %translate([0,0,30]) battery();
  %translate([0,30,30]) servo();
  %translate([0,-30,30]) servo();
}



/** STABILIZERS **/

module stabilizer_right() {
  hull() {
    translate([-20,0,0]) cube([20,2,1.5]);
    translate([-12, 40, 0]) cylinder(r=6, h=0.6);
  }
}

module stabilizer_left() {
  mirror([0,1,0]) stabilizer_right();
}

module stabilizer_vert() {
  translate([-20,0,0])
  hull() {
    translate([0, -1, 1]) cube([20,2,1]);
    translate([4, 0, 40]) rotate([90,0,0]) cylinder(r=4, h=0.8);
  }
}


/* This is the whole plane, as assembled. To print, you
   must generate a separate .stl for each of these parts
*/
module plane() {
  union() {
    fuselage();
    wings();
    translate([-tail_length,0,0]) stabilizer_right();
    translate([-tail_length,0,0]) stabilizer_left();
    translate([-tail_length,0,0]) stabilizer_vert();
  }
}

plane();