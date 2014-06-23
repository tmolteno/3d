/*
    Openscad HP2GoPro pad.

    Replace the backplate of the HP ac200w case and use GoPro accessories.

    Copyright (C) 2014. Max Scheel, max@max.ac.nz

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

bolt_hole = 5.5 / 2;
holedistance = 18.64;

module GoPro_two_pin()
{
	translate([0,3,0])
	{
		difference()
		{
			union()
			{
				translate([3.3,0,0]){
					cube([3.0,10,10]);
					translate([0,10,5]) rotate([90,0,90]) cylinder(3.0,5,5);
				}
				translate([9.7,0,0]){
					cube([3.0,10,10]);
					translate([0,10,5]) rotate([90,0,90]) cylinder(3.0,5,5);
				}
			}
			translate([-7, 10, 5]) rotate([0,90,0]) cylinder(30, bolt_hole, bolt_hole);
		}
	}
	cube([15.8,3,10]);
}

module fillet(r, h) {
	translate([r / 2, r / 2, 0])
	difference() {
		cube([r + 0.005, r + 0.005, h], center = true);
		translate([r/2, r/2, 0]) cylinder(r = r, h = h + 1, center = true);
	}
}

module hole(){
	union(){
		cylinder(h = 7, r=3.12/2);
		translate([0, 0, 3.36]) cylinder(h = 1.64+0.1, r=5/2);
		translate([0, 0, 0]) cylinder(h = 2.24, r=5/2);
		translate([0, 0, 0]) cylinder(h = 0.5, r1=5.7/2, r2=5/2);
	}
}

module holes(){
		translate([0, 0,-0.05]) hole();
		translate([holedistance, holedistance,-0.05]) hole();
		translate([0, holedistance,-0.05]) hole();
		translate([holedistance,0,-0.05]) hole();
}

module base()
{
	difference(){
		union(){
			rotate([90,0,90]) translate([7.6,4,10.5]) GoPro_two_pin();
			cube([31,31,5]);
		}
		union(){
			translate([ 0, 0,-1]) rotate([0, 0,  0]) fillet(6, 20);
			translate([31,31,-1]) rotate([0, 0,180]) fillet(6, 20);
			translate([31, 0,-1]) rotate([0, 0, 90]) fillet(6, 20);
			translate([ 0,31,-1]) rotate([0, 0,-90]) fillet(6, 20);
		}
	}

}

module hp2gopro(){
	difference(){
		base();
		translate([ 6.18, 6.18 ]) holes();
	}
}


hp2gopro();