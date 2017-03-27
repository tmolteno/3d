## Author Tim Molteno tim@elec.ac.nz
##
## Copyright 2016-2017.
##
## To build another prop, just type make TARGET=multistar_1704_1900kv
##
TARGET=test_prop
THRUST=2.0
# 400 g of thrust (4 Newtons)

.PHONY: bem

all:	bem scad

# Build using the Blade Element Momentum method
bem:
	python prop.py --naca --bem  --n 40 --resolution 2.0 --thrust ${THRUST} --param='${TARGET}.json'
	meshlabserver -i ${TARGET}_blade.stl -o ${TARGET}_blade.stl -s meshclean.mlx

scad:	${TARGET}.stl
	

sym:
	python naca_sym.py

# Erases the database, so don't do this by mistake.
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

	
#  TARGETS THAT ARE NOT WORKING YET
prop:
	python prop.py --n 40 --resolution .5 --param='${TARGET}.json'
	meshlabserver -i ${TARGET}_blade.stl -o ${TARGET}_blade.stl -s meshclean.mlx

auto:
	python prop.py --naca --auto --n 40 --resolution 2.0 --param='${TARGET}.json'
	meshlabserver -i ${TARGET}_blade.stl -o ${TARGET}_blade.stl -s meshclean.mlx

mesh:
	python prop.py --min-edge 0.35 --n 10 --param='prop_design.json' --mesh --resolution 10

