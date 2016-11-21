use <can.scad>;
servoWid = 26;
goodKKWid = 37;
holdWid = goodKKWid + 5 + servoWid;
rPiLen = 66;
rPiWid = 31;
servoLen = 63;
holdLen = rPiLen +5;
kkWid = 36;
motorBoltSpace = 14;
armWid = rPiWid;
armLength = 110-armWid/2;   // Distance to center of motor mount
height = 15;
batH = 30;
batL = 54;
batW = 18;
module pi() {
	cube([rPiLen, rPiWid, 1], center=true);
}
module servo() {
	cube([servoLen, servoWid, 254],center=true);
}
module kk() {
	cube([goodKKWid,goodKKWid,12]);
}
module kkHold() {
	difference() {
		translate([0,0,-(height - 12)])cube([holdWid,holdLen,height]);
		translate([-2.5+(goodKKWid*1.5),-1+(goodKKWid/2),2])rotate([0,0,90])kk();
        
	}
}

module attach(width,height) {
	difference() {
		translate([-width,0,0])cube([width,width,height]);
		translate([-(width/4)*3,width/4,-0.5])cube([width/2,width/2,height+1]);
	}
}
module PiServo() {
    difference() {
        translate([0,0,100])cube([75,75,5],center=true);
        translate([-15,0,103])cube([rPiWid,rPiLen,5], center=true);
        translate([15,0,103])cube([servoWid,servoLen,5], center=true);
        translate([34,34,50])cylinder(d=2.8,h=100);
        rotate([0,0,90])translate([34,34,50])cylinder(d=2.8,h=100);
        rotate([0,0,180])translate([34,34,50])cylinder(d=2.8,h=100);
       rotate([0,0,-90])translate([34,34,50])cylinder(d=2.8,h=100);
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

module slot(radius) {
    hull() {
        cylinder(r=radius, h=100, center=true);
        translate([4,0,0]) cylinder(r=radius, h=100, center=true);
    }
}

module motor_base() {
   hull() {
       cylinder(r = motorR+1.5, h=armH);
      translate([motorR+1, -armWid/2,0])cube([1,armWid,armH]);
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
	 //#translate([0,0,10])cylinder(r=127/2, h=10);
}
module motor_clear() {
    union() {
        translate([0,0,6]) cylinder(r= motorR, h=7);
        for(a = [0 : (90) : 360]) {
            rotate(a) translate([5.5,0,0]) slot(1.5);
            rotate(a) translate([5.5,0,-50])slot(3);
        }
     }
}


//translate([-25,holdLen/2-12.5,0])arm();
//main();
module newMain() {
    difference() {
        cube([130,130,height], center=true);
        //corners that are cut
        rotate([0,0,45])translate([-110,0,-1])cube([100,100,20],center = true);
        rotate([0,0,45])translate([110,0,-1])cube([100,100,20],center=true);
        rotate([0,0,90])union() {
            rotate([0,0,45])translate([-110,0,-1])cube([100,100,20],center = true);
            rotate([0,0,45])translate([110,0,-1])cube([100,100,20],center=true);
         }
        //KK mini holder
       rotate([0,0,45])translate([-holdWid/2,-holdLen/2,0])kkHold();
//         Holes for 2.75mm bolts
       rotate([0,0,45])translate([34,34,-50])cylinder(d=2.8,h=100);
        rotate([0,0,135])translate([34,34,-50])cylinder(d=2.8,h=100);
        rotate([0,0,225])translate([34,34,-50])cylinder(d=2.8,h=100);
        rotate([0,0,-45])translate([34,34,-50])cylinder(d=2.8,h=100);
         translate([0,0,6]) cylinder(r= motorR, h=7);
        translate([0,0,6]) cylinder(r= motorR, h=7);
        translate([0,0,6]) cylinder(r= motorR, h=7);
         // Extra motor holes
        rotate([0,0,-45])translate([0,69.5,-1.5]) cylinder(r= motorR, h=10);
         rotate([0,0,45])translate([0,69.5,-1.5]) cylinder(r= motorR, h=10);
         rotate([0,0,135])translate([0,69.5,-1.5]) cylinder(r= motorR, h=10);
         rotate([0,0,225])translate([0,69.5,-1.5]) cylinder(r= motorR, h=10);
          ultraBottom();
         //Difference ending
     }
     //motor mounts
    rotate([0,0,45])translate([-70,0,-7.5])motor_mount();
        rotate([0,0,225,])translate([-70,0,-7.5])motor_mount();
        rotate([0,0,90])union() {
            rotate([0,0,45])translate([-70,0,-7.5])motor_mount();
            rotate([0,0,225])translate([-70,0,-7.5])motor_mount();
         }
         //Can pick up thing
//         difference() {
//            translate([0,0,-50])cylinder(d=57,h=50);
//             translate([0,0,-51])cylinder(d=54,h=50);
//         }
}
module KKMiniHold() {
	difference() {
		cube([goodKKWid + 5, goodKKWid+5,10], center = true);
		translate([0,0,3])cube([goodKKWid,goodKKWid,10], center=true);
	}
}

module motor_arm(height) {
   		 difference() {
                hull() {
                    difference() {
                        translate([20,-armWid/2,-14])rotate([0,-65,0])cube([120,armWid,10]);
                        translate([20,-50,height+10])cube(100,100,100);
                    }
                    translate([70,0,height])rotate([0,0,180])motor_mount();
                }
                    //Arm Cutouts
				translate([-goodKKWid/2,-goodKKWid/2,-2])kk();
				translate([-50,-50,-17])cube([100,100,12]);
            translate([70,0,height]) motor_clear();
				translate([0,0,150])servo();
		}
}

module body() {
	//Motor Mounts
	for(angle = [0, 180]) {
		//Forward and back
        difference() {
            hull() {
                rotate(angle)translate([70,0,50])rotate([0,0,180])motor_mount();
                rotate(angle)translate([52,-armWid/2,-5])cube([5,armWid,56]);
            }
            rotate(angle)translate([70,0,50])motor_clear();
        }
        rotate(angle)translate([37/2,-armWid/2,-5])cube([52-(37/2),armWid,5]);
		difference() {
		 	rotate(angle)translate([20,-armWid/2,-14])rotate([0,-60,0])cube([90,armWid,10]);
            rotate(angle)translate([20,-50,50+10])cube(100,100,100);
			//Arm Cutouts
			translate([-goodKKWid/2,-goodKKWid/2,-2])kk();
			translate([-30,-30,-17])cube([60,60,12]);
			rotate(angle)translate([70,0,50])rotate([0,0,180])motor_clear();
		}
   }
	for(angle = [90, 270]) {
   		 rotate(angle) motor_arm(30);
	}
	//KK Mini Holder
	KKMiniHold();
    /*translate([0,0,20]) difference() {
        cylinder(d=85,h=10);
        cylinder(d=60,h=30, center=true);
    }*/
	//Cross between arms
	
}

module prop() {
    cylinder(d=127.5, h=10);
}
module mounting_holes() {
		difference() {
			union() {
				translate([0,0,32.5])cube([80,armWid,15], center=true);
			}
			translate([0,0,-1])sphere(d=100);
			translate([(rPiLen/2)-(1.4+3.5),(rPiWid/2)-(1.4+3.5),30])cylinder(d=2.8, h=100);
			translate([(-rPiLen/2)+(1.4+3.5),(-rPiWid/2)+(1.4+3.5),30])cylinder(d=2.8, h=100);
			translate([(rPiLen/2)-(1.4+3.5),(-rPiWid/2)+(1.4+3.5),30])cylinder(d=2.8, h=100);
			translate([(-rPiLen/2)+(1.4+3.5),(rPiWid/2)-(1.4+3.5),30])cylinder(d=2.8, h=100);
		}
    	difference() {
			union() {
        		body();
		  	}
        	translate([45,-21/2,-7]) cylinder(r=1, h=10);
        	translate([45, 21/2, -7]) cylinder(r=1,h=10);
        	translate([32.5,21/2, -7]) cylinder(r=1, h=10);
        	translate([32.5,-21/2,-7]) cylinder(r=1, h=10);
            translate([-32.5,0,0])hull() {
                    translate([0,5,0])cylinder(r=1.5, h=10, center=true);
                    translate([0,-5,0])cylinder(r=1.5, h=10,center = true);
            }
            translate([-47.5,0,0])hull() {
                    translate([0,5,0])cylinder(r=1.5, h=10, center=true);
                    translate([0,-5,0])cylinder(r=1.5, h=10,center = true);
            }
    	}
}

//motor_arm(70);

mounting_holes();
//newMain();
//translate([0,0,-60])PiServo();
//prop size
/*#rotate([0,0,0])translate([70,0,70]) prop();
#rotate([0,0,90])translate([70,0,50]) prop();
#rotate([0,0,180])translate([70,0,70]) prop();
#rotate([0,0,270])translate([70,0,50]) prop();
*/
rotate([0,0,0])translate([0,0,-124/4-5])can();
//Boundry cylinder
//#cylinder(r=135,h=270);