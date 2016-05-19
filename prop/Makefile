all:	prop scad

prop:
	python prop.py --n 40 --resolution 2.0 --param='prop_design.json'
	meshlabserver -i test_prop_blade.stl -o test_prop_blade.stl -s meshclean.mlx

auto:
	python prop.py --auto --n 40 --resolution 3.0 --param='prop_design.json' --stl-file 'blade_auto.ascii.stl'
	meshlabserver -i blade_auto.ascii.stl -o blade_auto.stl -s meshclean.mlx

scad:
	openscad -m make -d pyprop.deps -o test_prop.ascii.stl test_prop.scad
	meshlabserver -i test_prop.ascii.stl -o test_prop.stl -s meshclean.mlx
	

mesh:
	python prop.py --min-edge 0.35 --n 10 --param='prop_design.json' --mesh --resolution 10
	
sym:
	python naca_sym.py

db:
	sqlite3 foil_simulator.db < foil_simulator.sql

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
