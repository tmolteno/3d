# Prop


![alt text][prop5x3]




# Creating Props using JavaProp, FreeCAD and OpenSCAD.

## Step 1. Design your prop in JavaProp.

## Step 2. Export your design in IGES format

## Step 3. Create and STL fvrom IGES

This is done using FreeCAD.

* Open FreeCAD and Select Part Mode
* Import your IGES file
* Choose Part -> Shape Builder
* Choose "Face From Edges" and select the boundary of one end of the prop blade. Click "Create"
* Do the same for the other end of the prop blade.
* Choose "Shell from Faces" and select (holding down CTRL) the two ends, and the surface of the prop blade. Click "Create"

You will now have a design with several parts. One of them is called "Shell". Select this, and choose Part -> Convert to solid.

now delete all the other bits of your design (right click and delect the original import, as well as the other parts.

Then export this as an .stl file.


# Step 4. Use OpenSCAD

Import the .stl file inside openscad. The file prop5x3.scad shows how this is done.


[prop5x3]: https://github.com/tmolteno/3d/raw/master/3d/prop/images/prop5x3.png "Three Bladed Prop"