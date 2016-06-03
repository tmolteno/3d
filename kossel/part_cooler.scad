use <MCAD/boxes.scad>
$fn =51;
step = 2;

module extruder() {
    translate([0,0,15.5]) cylinder(d=25, h=32);
    translate([4,0,10]) cube([16,16,8], center=true);
    cylinder(d1=1, d2=7, h=6);
}


module fan(d=9) {
    rotate([0,90,0]) difference() {
        roundedBox([40,40,d], 3, true);
        cylinder(d=38,h=20, center=true);
    }
}

duct_diameter = 38;
duct_x = 24;
fan_z = 6;

module top_duct() {
    hull() {
          translate([duct_x+0.1,0,fan_z + 20]) rotate([0,90,0]) 
              difference() {
                  cylinder(d=35, h=1,center=true);
                  translate([-2,-50,-50]) cube([100,100,100]);
              }
        translate([0,0,16]) cylinder(d=23, h=28);
    }
}


h = 20;
r = 14;
module cooling_zone() {
   for(angle = [20 : step : 160]) {
      hull() {
         translate([duct_x+0.1, 0,fan_z + h]) 
            rotate([0,90,0]) rotate(angle - 90) 
                translate([r,0,0]) 
                    cylinder(d=9, h=0.1,center=true);
          rotate(angle - 90) translate([9.75,0,0]) 
            cylinder(d=5,h=1,center=true);
    }
  }
}
module cooling_shroud() {
   for(angle = [20 : step : 160]) {
      hull() {
         translate([duct_x-0.1, 0,fan_z + h])  
            rotate([0,90,0]) rotate(angle - 90) 
                translate([r,0,0]) 
                    cylinder(d=12, h=0.1,center=true);
          rotate(angle - 90) translate([10,0,0]) 
            cylinder(d=8,h=1);
    }
  }
}


module keep_out() {
    union() {
        translate([0,0,10]) cylinder(d=15,h=100);
        translate([0,0,9]) cylinder(d1 = 22, d2=23, h=16);
        translate([-25,0,39]) cube([40,40,80], center=true);
        rotate(180) extruder();
    }
}

module cooler() {
   difference() {
        union() {
            hull() {
                translate([duct_x-0.5,0,20+fan_z]) fan(d=1);
                translate([0,0,17]) cylinder(d=30,h=30);
            }
            cooling_shroud();
        }
        top_duct();
        cooling_zone();
        keep_out();
        
        h = 14;
        translate([duct_x-0.5,0,20+fan_z]) rotate([0,90,0]) 
            for(angle = [0 : 90 : 360]) {
                rotate(angle+45) translate([0,22.75,-2.1])
                    cylinder(d=4,h=12);
                rotate(angle+45) translate([0,26.0,-2-h])
                    cylinder(d1=1,d2=11,h=h);
            }
    }
}

//rotate(180) extruder();
//translate([duct_x+4,0,25]) color("gray") fan();
cooler();
//bottom_duct();
//top_duct();
//keep_out();
