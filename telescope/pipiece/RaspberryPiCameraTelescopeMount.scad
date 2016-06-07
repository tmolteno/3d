// This mount connects your RaspberryPi Camera to your 1.25 inch eyepiece focuser of your telescope.
// Needs the RaspberryPiCamera.scad: http://www.thingiverse.com/thing:123218

// Remove the lens if you want to see stars
// Leave the lens on if you want to use the camera for collimation of your telescope
// You can try to mount it on top of this housing: http://www.thingiverse.com/thing:89745 

// Changelog: The lower M2 screws hit the cylinder. I opened the cylinder, in order to fit a regurla DIN 912 M2 screw. The inner ractangle was enlarged, to avoid problems with the front cable.

// Designed by René Bohne

$fn = 100;

include <RaspberryPiCamera.scad>

module eyepiece()
{
	difference()
	{
		cylinder(r=31.75/2, h=20, center=true);
		cylinder(r=31.75/2-1, h=21, center=true);
	}
}


module eyepieceMount_base()
{
	difference()
	{
		translate([lens_housing_x,lens_housing_y,0])		cube([31.75,31.75,board_thickness], center=true);

		translate([screw1_x,screw1_y,0]) cylinder(r=2/2, h=10, center=true);
		translate([screw2_x,screw2_y,0]) cylinder(r=2/2, h=10, center=true);
		translate([screw3_x,screw3_y,0]) cylinder(r=2/2, h=10, center=true);
		translate([screw4_x,screw4_y,0]) cylinder(r=2/2, h=10, center=true);
		
	}
}


module eyepieceMount()
{
	difference()
	{
		translate([0,0,board_thickness+0.1])
		{
			translate([lens_housing_x,lens_housing_y,20/2+board_thickness/2]) eyepiece();
			eyepieceMount_base();
		}


		translate([screw2_x,screw2_y,26]) cylinder(r=3.8/2, h=50, center=true);
		translate([screw4_x,screw4_y,26]) cylinder(r=3.8/2, h=50, center=true);
	
		raspberryPiCamera();
	}
}

eyepieceMount();