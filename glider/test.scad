width=10.3;

$fn=100;

//module foo() {
//    intersection() {
//        cube([20,20,20], center=true);
//        sphere(r = 12);
//    }
//}
//
//difference() {
//    foo();
//    cylinder(d=3, h=100, center=true);
//}
//

hull() {
    sphere(r=10);
    translate([10,10,10]) cube([10,10,10]);
}

