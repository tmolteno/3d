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
$fn = 37;
pick_length = 16;
tip_radius = 2;
hold_radius = 11;

module b18650() {
    cylinder(d=18, h=65);
    translate([0,0,65]) cylinder(d=6, h=2);
}

module m8(len) {
    cylinder(d=8, h=len);
    translate([0,0,len]) cylinder(d=12, h=5, $fn=6);
}

b18650();
translate([0,0,67]) m8(20);
