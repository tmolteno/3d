prop:
	python prop.py --diameter 120 --pitch 50 --stl 'blade5x3.ascii.stl'
	meshlabserver -i blade5x3.ascii.stl -o blade5x3.stl -s meshclean.mlx
	openscad -m make -d pyprop.deps -o pyprop.ascii.stl pyprop.scad
	meshlabserver -i pyprop.ascii.stl -o pyprop.stl -s meshclean.mlx
	

sym:
	python naca_sym.py

all: base.stl cap.stl

.SECONDARY:

# Explicit wildcard expansion suppresses errors when no files are found.
include $(wildcard *.deps)

%.stl: %.ascii.stl
	meshlabserver -i $< -o $@ -s ../meshclean.mlx

%.ascii.stl: %.scad
	openscad -m make -d $*.deps -o $@ $<

%.gcode: %.stl
	slic3r -o $@ $<

# Replace tabs with spaces.
%.tab: %.scad
	cp $< $@
	expand $@ > $<
