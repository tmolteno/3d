CREATE TABLE  polar (
    sim_id int, 
    alpha float, 
    cl float, 
    cd, 
    cdp, 
    cm, 
    Top_Xtr, 
    Bot_Xtr);
    
CREATE TABLE foil(
    id integer PRIMARY KEY AUTOINCREMENT,
    hash varchar);
    
CREATE TABLE simulation(
    id integer PRIMARY KEY AUTOINCREMENT,
    foil_id int, 
    reynolds float, 
    mach float);
