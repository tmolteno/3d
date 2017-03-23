# Prereq
    sudo aptitude install python-pip
    sudo pip install numpy-stl enum enum34


# XFOIL

The package located at [https://github.com/RobotLocomotion/xfoil.git] is much
better and appears to work correctly (the debian install doesn't and I'm figuring out
why at the moment. Any help appreciated)

The path to the xfoil is contained in the file xfoil_2.py.


## First Run

The results from xfoil are stored in a database (sqlite). Before running this program for the first time,
create a database file using 

    make db

This avoids recalculation of polars for airfoils already calculated.
