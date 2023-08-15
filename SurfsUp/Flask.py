from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///../Starter_Code/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    """List all available api routes"""
    return (
        f"Available routes for Hawaii Climate Temperatures:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )
    
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session link from Python to the db
    session = Session(engine)
    # Find the endpoint for the last year of data
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query date and precipitation from the last year
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).order_by(Measurement.date).all()
    
    session.close()
    
    # Create a dictionary from the row data and append to a list of dates
    all_dates = []
    for date in results:
        date_dict = {}
        date_dict["date"] = date[0]
        date_dict["prcp"] = date[1]
        all_dates.append(date_dict)
        
    return jsonify(all_dates)


@app.route("/api/v1.0/stations")
def stations():
    # Create session link from Python to the db
    session = Session(engine)
    # Query the station and the name of each station
    station = session.query(Station.station, Station.name).all()
    
    session.close()
    # Create a dictionary with the station and name data and then put it into a list
    # in order to jsonify it
    station_s = []
    
    for result in station:
        station_dict = {}
        station_dict['station'] = result[0]
        station_dict['name'] = result[1]
        station_s.append(station_dict)
    
    return jsonify(station_s)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session link from Python to the db
    session = Session(engine)
    # Find the endpoint for the last year of data
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Query the date and temp for the most-active station and filter it for the last year
    tobs = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').filter(Measurement.date >= year_ago).all()
     
    session.close()
    # Create a dictionary for the date and temp and then put it into a list
    # in order to jsonify it
    temperature_totals = []
    for temp in tobs:
        temp_dict = {}
        temp_dict["date"] = temp[0]
        temp_dict["temp"] = temp[1]
        temperature_totals.append(temp_dict)
        
    return jsonify(temperature_totals)

@app.route("/api/v1.0/<start>")
def temp1(start):
    # Create session link from Python to the db
    session = Session(engine)
    # Find the start date for the last year of data
    start = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Find the max, min and avg temp for the last year
    averages = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    session.close()
    # Convert the tuple to a list in order to jsonify it
    trip = list(np.ravel(averages))
    return jsonify(trip)

@app.route("/api/v1.0/<start>/<end>")
def temp2(start,end):
    # Create session link from Python to the db
    session = Session(engine)
    # Find the start date from 2 years ago 
    start = dt.date(2017, 8, 23) - dt.timedelta(days=730)
    # Find the end date from a year ago 
    end = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Find the max, min and avg temp from in between 1-2 years ago 
    averages = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        
    session.close()
    # Convert the tuple to a list in order to jsonify it
    trip = list(np.ravel(averages))
    return jsonify(trip)
    
    
if __name__ == '__main__':
    app.run(debug=True)