goodKKWid = 37;
holdWid = goodKKWid + 5;
rPiLen = 66;
rPiWid = 31;
holdLen = rPiLen +5;
kkWid = 36;
motorBoltSpace = 14;
armWid = 25;
armLength = 110-armWid/2;   // Distance to center of motor mount
height = 15;
module kk() {
	cube([goodKKWid,goodKKWid,12]);
}
module kkHold() {
	difference() {
		translate([0,0,-(height - 12)])cube([holdWid,holdLen,height]);
		translate([2.5,2.5,2.5])kk();
        translate([rPiWid/2+(rPiWid+holdWid)/13,rPiLen/2+2.5,-3])cube([rPiWid,rPiLen,5], center=true);
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
	translate([0,holdLen/2-7.5,0])attach(15,5);
	translate([holdWid/2+7.5,-15,0])attach(15,5);
	translate([holdWid+15,holdLen/2-7.5,0])attach(15,5);
	translate([holdWid/2+7.5,holdLen,0])attach(15,5);
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

translate([-25,holdLen/2-12.5,0])arm();
main();
