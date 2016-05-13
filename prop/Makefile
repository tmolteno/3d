all:	prop scad

prop:
	python prop.py --min-edge 0.5 --n 40 --resolution 5.0 --param='prop_design.json' --stl-file 'blade5x3.ascii.stl'
	meshlabserver -i blade5x3.ascii.stl -o blade5x3.stl -s meshclean.mlx

scad:
	openscad -m make -d pyprop.deps -o pyprop.ascii.stl pyprop.scad
	meshlabserver -i pyprop.ascii.stl -o pyprop.stl -s meshclean.mlx
	

mesh:
	python prop.py --min-edge 0.35 --n 10 --param='prop_design.json' --mesh --resolution 10
	
sym:
	python naca_sym.py

.SECONDARY:

# Explicit wildcard expansion suppresses errors when no files are found.
include $(wildcard *.deps)

%.stl: %.ascii.stl
	meshlabserver -i $< -o $@ -s meshclean.mlx

%.ascii.stl: %.scad
	openscad -m make -d $*.deps -o $@ $<

%.gcode: %.stl
	slic3r -o $@ $<

# Replace tabs with spaces.
%.tab: %.scad
	cp $< $@
	expand $@ > $<
