## Author Tim Molteno tim@elec.ac.nz
##
## Copyright 2016-2017.
##
## To build another prop, just type make TARGET=multistar_1704_1900kv
##
TARGET=test_prop

.PHONY: bem blade scad push pull

all:	bem scad

# Build using the Blade Element Momentum method
bem:
	python prop.py --arad --bem  --n 40 --resolution 2.0 --param='${TARGET}.json'
	meshlabserver -i ${TARGET}_blade.stl -o ${TARGET}_blade.stl -s meshclean.mlx

scad:	${TARGET}.stl
	
blade:  ${TARGET}_removable.stl

sym:
	python naca_sym.py

# Erases the database, so don't do this by mistake.
db:
	rm foil_simulator.db

pull:
	rsync -zv tim@electron.otago.ac.nz:/freenas/temp/foil_simulator.db .

push:
	rsync -zv foil_simulator.db tim@electron.otago.ac.nz:/freenas/temp/foil_simulator.db

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

	
#  TARGETS THAT ARE NOT WORKING YET
prop:
	python prop.py --n 40 --resolution .5 --param='${TARGET}.json'
	meshlabserver -i ${TARGET}_blade.stl -o ${TARGET}_blade.stl -s meshclean.mlx

auto:
	python prop.py --naca --auto --n 40 --resolution 2.0 --param='${TARGET}.json'
	meshlabserver -i ${TARGET}_blade.stl -o ${TARGET}_blade.stl -s meshclean.mlx

mesh:
	python prop.py --min-edge 0.35 --n 10 --param='prop_design.json' --mesh --resolution 10

