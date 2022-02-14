/*
    SDC2300 Battery Pack.

    Copyright 2022, Tim Molteno. tim@molteno.net
  
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
$fn = 101;

c_cell_diameter = 25.5;
c_cell_length = 50.0;

clearance_d = 0.75;

total_length = 2*c_cell_length;

module b18650() {
    cylinder(d=18+clearance_d, h=65);
    translate([0,0,65]) cylinder(d=6, h=2);
}


m8_head = 5.3 - 1;
module m8(len) {
    cylinder(d=14.38 + 1, h=m8_head, $fn=6);
    translate([0,0,m8_head]) cylinder(d=8+clearance_d, h=len);
}


module sdc2300_battery() {
    difference() {
        cylinder(d=c_cell_diameter, h=total_length);
        union () {
            cylinder(d=18+clearance_d, h=30, center=true);
        }
    }
}

module hollow() {
    union () {
        b18650();
        translate([0,0,65]) m8(30);
    }
}

module sdc_2300_holder() {
    difference() {
        sdc2300_battery();

        hollow();
    }
}

rotate([180,0,0]) sdc_2300_holder();