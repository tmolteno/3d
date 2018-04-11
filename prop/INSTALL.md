# Install Instructions

Note: Development is being done on Debian linux. Any debian derived distribution should be fine, and most other linux distributions
should work just fine too. 

## Prereq

    sudo aptitude install python-pip python-yaml python-matplotlib python-scipy meshlab openscad
    sudo pip install numpy-stl enum enum34


## XFOIL

The package located at [https://github.com/tmolteno/xfoil.git] is much
better and appears to work correctly

The path to the xfoil is contained in the file xfoil.py.


## First Run

To get started there is a makefile that will build a prop called test_prop.json. The propeller description is contained in that file.
