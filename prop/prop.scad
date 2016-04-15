module blade() {
    difference() {
        import("prop2.stl");
  }
}

module prop() {
    intersection() {
        union() {
        rotate(0) blade();
        rotate(120) blade();
        rotate(240) blade();
        translate([0,0,-5]) cylinder(d=17, h=10, $fn=51);
        }
     cylinder(r=100, h=10, center=true);
    }
}
union() {
    difference() {
        prop();
       cylinder(r=2, h=55, center=true, $fn=31);
    }
}
