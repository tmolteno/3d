/*
    OpenSCAD Rubber-band Loom.

    This is a dragon scale rubber-band loom for weaving.

    Copyright (C) 2014. Linus Molteno, linus@molteno.net
  
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

use<loom_module.scad>;

post(h=20);
w=12;
n_posts=6;
//Base
hull() {
  translate([0,0,0])cylinder(r=3, h=4.5);
  translate([0,(n_posts-1)*w,0])cylinder(r=3, h=4.5);
}
//Posts
for (i = [0:n_posts-1]) {
  translate([0,w*i,0])post(h=20);
}


