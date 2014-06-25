/*
    Openscad Bikelight2gopro

    Replace standard mount of the bike light use GoPro accessories.

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

module GoPro_two_pin()
{
	translate([0,3,0])
	{
		difference()
		{
			union()
			{
				translate([0,0,0]){
					cube([3.0,10,10]);
					translate([0,10,5]) rotate([90,0,90]) cylinder(3.0, 5, 5);
				}
				translate([6.4,0,0]){
					cube([3.0,10,10]);
					translate([0,10,5]) rotate([90,0,90]) cylinder(3.0, 5, 5);
				}
			}
			translate([-7, 10, 5]) rotate([0,90,0]) cylinder(30, bolt_hole, bolt_hole);
		}
	}
}

module hole(){
	cylinder(h=15,r=4.2/2, center=true);
	translate([0,0,1.3+0.05]) cylinder(h=2.6+0.01,r=6.5/2, center=true);
}

module base()
{
	union(){
		translate([-9.4/2,5,-1]) rotate([90,0,0]) GoPro_two_pin();
		cube([20.4,30,5], center=true);
		//translate([0,0,-3.8]) cube([1.9,30,3], center=true);
		//translate([-3.9,0,-3.2]) cube([1.9,30,1.6], center=true);
		//translate([3.9,0,-3.2]) cube([1.9,30,1.6], center=true);
	}
}

module light2gopro(){
	difference(){
	base();
	translate([0,15-4-4.2/2,0]) hole();
	}
}

light2gopro();