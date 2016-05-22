goodKKWid = 51;
holdWid = goodKKWid + 5;
kkWid = 50.5;
motorBoltSpace = 14;
armWid = 25;
armLength = 110-armWid/2;   // Distance to center of motor mount

module kk() {
	cube([goodKKWid,goodKKWid,12]);
}
module kkHold() {
	difference() {
		cube([holdWid,holdWid,12]);
		translate([2.5,2.5,2.5])kk();
	}
}

module attach(width,height) {
	difference() {
		translate([-width,0,0])cube([width,width,height]);
		translate([-(width/4)*3,width/4,-0.5])cube([width/2,width/2,height+1]);
	}
}

module main() {
	kkHold();
	translate([0,holdWid/2-7.5,0])attach(15,5);
	translate([holdWid/2+7.5,-15,0])attach(15,5);
	translate([holdWid+15,55.5/2-7.5,0])attach(15,5);
	translate([holdWid/2+7.5,holdWid,0])attach(15,5);
}

armH = 10;
module arm() {
	difference() {
		translate([-armLength+armWid,0,0])cube([armLength,armWid,armH]);
		translate([armWid/2.5,armWid/5,-1])cube([16,15,6]);
		translate([13.75,35/4,-0.5])cube([15/2,15/2,15+1]);
	}
     translate([-armLength+armWid/2, armWid/2, 0]) motor_mount();
}


/*
    The motor mount. Cylinder with slots for the motor bolts. This 
    is done because the motor mounting holes are not on a square
*/
motorD = 28;
motorR = motorD/2;
holeR = 1.5;

module slot() {
    hull() {
        cylinder(r=holeR, h=100, center=true);
        translate([4,0,0]) cylinder(r=holeR, h=100, center=true);
    }
}

module motor_base() {
   hull() {
       cylinder(r = motorR+1.5, h=armH);
       translate([motorR+1, -armWid/2,0]) cube([1,armWid,armH]);
   }
}

module motor_mount() {
    difference() {
        motor_base();
        translate([0,0,6]) cylinder(r= motorR, h=7);
        for(angle = [0 : (360/4) : 360]) {
            rotate(angle) translate([5.5,0,0]) slot();
        }
    }
}

translate([-25,holdWid/2-12.5,0])arm();
//main();
