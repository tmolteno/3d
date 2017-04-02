# TODO list

* [DONE] Create an interpolated ARA foil class that can have any aspect ratio.
* Improve interpolation to make ARA foils smooth as thickness varies.
* [DONE] Allow trailiing edge specification in ARA foil class
* [DONE] Modify trailing edge specification in JSON to be in mm.


* Allow units in the JSON spec. trailing_edge = '0.5 mm' (units are m, mm, cm, m/s, kph, mph)


## Performance

* Use multiprocessing for polars
* Reduce polling CPU time.
