-- SQL for foil database
-- Author Tim Molteno (c) 2016 tim@molteno.net
--
PRAGMA foreign_keys = ON;

drop table if exists polar;
drop table if exists simulation;
drop table if exists foil;

create table foil (
   id integer primary key,
   hash varchar(255)
);

create table simulation (
   id integer primary key,
   foil_id integer references foil(id),
   reynolds float,
   mach float
);


create table polar (
   id integer primary key,
   sim_id integer references simulation(id),
   alpha float,     -- Angle of Attack
   cl float,        -- Lift Coefficient
   cd float,        -- Drag Coefficient
   cdp float,       -- Pressure Drag portion of cd
   cm float,        -- Pitching Moment Coefficient about the quarter chord point (measured back from leading edge)
   Top_Xtr float,   -- Top Transistion (Detachment of top flow from foil) x coordinate'
   Bot_Xtr float
);

