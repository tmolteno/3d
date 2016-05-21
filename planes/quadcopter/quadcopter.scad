goodKKWid = 51;
holdWid = goodKKWid + 5;
kkWid = 50.5;
motorBoltSpace = 14;
armWid = 25;
armLength = 110;
holeR = 2;
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
module arm() {
	difference() {
		translate([-armLength+armWid,0,0])cube([armLength,armWid,10]);
		translate([armWid/2.5,armWid/5,-1])cube([16,15,6]);
		translate([13.75,35/4,-0.5])cube([15/2,15/2,15+1]);
		holes();
	}
}
module holes() {
	translate([-armLength+armWid*1.25,armWid/2,-1])cylinder(r=holeR, h= 100);
	translate([-armLength+armWid*1.25+14,armWid/2,-1])cylinder(r=holeR, h= 100);
	translate([-armLength+armWid*1.25+7,armWid/2+7,-1])cylinder(r=holeR, h= 100);
	translate([-armLength+armWid*1.25+7,armWid/2-7,-1])cylinder(r=holeR, h= 100);
}
translate([-25,holdWid/2-12.5,0])arm();
main();
