CREATE TABLE IF NOT EXISTS usage_logs (
    id INTEGER PRIMARY KEY, 
    box_name TEXT, 
    dimensions TEXT, 
    weight_grams REAL, 
    qty INTEGER, 
    timestamp TEXT
);