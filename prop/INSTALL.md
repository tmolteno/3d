# Install Instructions

Note: Development is being done on Debian linux. Any debian derived distribution should be fine, and most other linux distributions
should work just fine too. 

## Prereq

    sudo aptitude install python-pip
    sudo pip install numpy-stl enum enum34


## XFOIL

The package located at [https://github.com/RobotLocomotion/xfoil.git] is much
better and appears to work correctly (the debian install doesn't and I'm figuring out
why at the moment. Any help appreciated)

The path to the xfoil is contained in the file xfoil_2.py.


## First Run

The results from xfoil are stored in a database (sqlite). The distribution contains a database file (foil_simulator.db)
If this is missing, or you believe the results stored there are corrupted, you can delete this file and recreate it using

    make db

This avoids recalculation of polars for airfoils already calculated.
