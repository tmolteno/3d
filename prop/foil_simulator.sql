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

-- ['CM', 'CL', 'Top_Xtr', 'CD', 'CDp', 'alpha', 'Bot_Xtr']

create table polar (
   id integer primary key,
   sim_id integer references simulation(id),
   alpha float,
   cl float,  -- Lift Coefficient
   cd float,  -- Drag Coefficient
   cdp float,
   cm float,
   Top_Xtr float,
   Bot_Xtr float
);

