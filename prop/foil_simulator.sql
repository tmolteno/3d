CREATE TABLE foil(
    id integer PRIMARY KEY AUTOINCREMENT,
    hash varchar);

CREATE TABLE simulation(
    id integer PRIMARY KEY AUTOINCREMENT,
    foil_id int REFERENCES foil ON DELETE CASCADE, 
    reynolds float, 
    mach float);

CREATE TABLE  polar (
    sim_id int REFERENCES simulation ON DELETE CASCADE, 
    alpha float, 
    cl float, 
    cd, 
    cdp, 
    cm, 
    Top_Xtr, 
    Bot_Xtr);
    
    
