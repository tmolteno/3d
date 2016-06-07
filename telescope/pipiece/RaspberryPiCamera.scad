// raspberryPiCamera shows the most important mounting elements of the RaspberryPi Camera PCB.
// I took all dimension from here: http://www.raspberrypi.org/phpBB3/viewtopic.php?f=43&t=44466
// Gert van Loo uploaded the mechanical data on scribd: http://www.scribd.com/doc/142718448/Raspberry-Pi-Camera-Mechanical-Data

// Changelog: in this version, I added camera_front_cable. A small cable is located there and should not be touched...
$fn = 100;


board_width = 25;
board_height = 23.9;
board_thickness = 0.95;

lens_housing_size = 8;
lens_housing_thickness = 5.2;

lens_housing_x = 0;
lens_housing_y = (board_height-lens_housing_size)/2-5.1;


screw1_x = -board_width/2+2;
screw1_y = board_height/2-9.35;

screw2_x = -board_width/2+2;
screw2_y = board_height/2-21.85;

screw3_x = -board_width/2+23;
screw3_y = board_height/2-9.35;

screw4_x = -board_width/2+23;
screw4_y = board_height/2-21.85;


back_connector_width = 20;
back_connector_height = 5.6;
back_connector_thickness = 2.8;
back_connector_x = 0 ;
back_connector_y = (board_height-back_connector_height) /2 ;

module camera_pcb()
{
	difference()
	{
		cube([board_width,board_height,board_thickness], center=true);

		translate([screw1_x,screw1_y,0]) cylinder(r=2/2, h=10, center=true);
		translate([screw2_x,screw2_y,0]) cylinder(r=2/2, h=10, center=true);
		translate([screw3_x,screw3_y,0]) cylinder(r=2/2, h=10, center=true);
		translate([screw4_x,screw4_y,0]) cylinder(r=2/2, h=10, center=true);
	}
}

module camera_lens_housing()
{
translate([lens_housing_x,lens_housing_y,(board_thickness+lens_housing_thickness)/2]) cube([lens_housing_size,lens_housing_size, lens_housing_thickness], center=true);
}

module camera_back_connector()
{
	translate([back_connector_x,back_connector_y,-(back_connector_thickness+board_thickness)/2]) cube([back_connector_width, back_connector_height, back_connector_thickness], center=true);
}

module camera_front_cable()
{
	translate([0,lens_housing_y-4-10/2+0.1,3/2+board_thickness/2]) cube([8,10,3], center=true);
}

//center of the board
//#	cylinder(r=2/2, h=100, center=true);

module raspberryPiCamera()
{
	camera_pcb();
	camera_lens_housing();
	camera_back_connector();
	camera_front_cable();
}

//raspberryPiCamera();
