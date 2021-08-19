import pandas as pd 
import datetime as dt
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.SQLite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect= True)
# View all of the classes that automap found
# Base.classes.keys()

#Save references to each table
Measure = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route('/')
def home_page():
    return(
        f"Welcome to the Hawaii Climate Analysis APT!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
        
    )
@app.route('/api/v1.0/precipitation')
def precipitation():
    '''Return the precipitation for the last year'''

    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days= 365)

    data= session.query(Measure.date, Measure.prcp).filter(Measure.date >= year_ago).all()

    precip = {date: prcp for date, prcp in data}
    return jsonify(precip)

@app.route('/api/v1.0/stations')
def stations():
    '''Return a list of stations.'''
    active_stations= session.query(Station.station).all()
    active_station_list = list(np.ravel(active_stations))

    
    return jsonify(active_station_list=active_station_list)
    

@app.route('/api/v1.0/tobs')
def monthly_temp():
    
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days= 365)

    max_temp= session.query(Measure.tobs).\
        filter(Measure.station == 'USC00519281').\
        filter(Measure.date >= year_ago).all()
    # print(max_temp)
    max_temp_list = list(np.ravel(max_temp))

    
    return jsonify(max_temp_list=max_temp_list)

@app.route('/api/v1.0/temp/start')
@app.route('api/v1.0/temp/<start>/<end>')
def stats(start=None, end=None):
    """Return TMIN, TAVG, TMAX."""

    sel = [func.min(Measure.tobs), func.max(Measure.tobs), func.avg(Measure.tobs)]

    if not end:

        results = session.query(*sel).\
            filter(Measure.date >= start).all()
        
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*sel).\
        filter(Measure.date >= start).\
        filter(Measure.date <= end).all()
    
    temps = list(np.ravel(results))
    return jsonify(temps=temps)
        


if __name__ == '__main__':
    app.run(debug=True)