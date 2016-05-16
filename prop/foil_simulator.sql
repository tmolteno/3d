PRAGMA foreign_keys = ON;

drop table polar;
drop table simulation;
drop table foil;

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
   alpha float,
   cl float,
   cd float 
);