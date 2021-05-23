import pandas as pd 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.SQLite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect= True)
# View all of the classes that automap found
Base.classes.keys()

#Save references to each table
Measure = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route('/')
def home_page():
    return(
        f"Available routes:<br/>"
        f"<'/api/v1.0/precipitation'><br/>"
        f"<'/api/v1.0/stations'><br/>"
        f"<'/api/v1.0/tobs'><br/>"
        # f"<'/api/v1.0/<start'>"
        # f"<'/api/v1.0/<start>/<end'>"
    )
@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    # Find the most recent date in the data set.
    recent = session.query(Measure.date).order_by(Measure.date.desc()).first()
    # return jsonify(f"The most recent date in dataset: {recent}")

    
    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days= 365)   
    
    # year_ago

    # Perform a query to retrieve the data and precipitation scores
    data= session.query(Measure.date, Measure.prcp).filter(Measure.date >= year_ago).all()
   
    # Save the query results as a Pandas DataFrame and set the index to the date column
    yrly_prcp = pd.DataFrame(data)
    # print(yrly_prcp)
    # Sort the dataframe by date
    date_df = yrly_prcp.groupby("date").max()
    # print(date_df)
    prcp_dict = date_df.to_dict()
    # Use Pandas Plotting with Matplotlib to plot the data

    # date_df.plot(x= "date", y="prcp", rot= 90)
    # plt.show()
    # session.close()
    # prcp_table = { 
    #     (date:{prcp_data}), (prcp:{yrly_prcp})
    # }
    
    # 
    # return (
    #     f"The most recent date in dataset: {recent}.<br/>"
    #     f"Date one year from last recorded: {year_ago}.<br/>"
    #     f"Listed is the data set used: {prcp_dict}<br/>"                
    # )
    session.close()
    return jsonify(prcp_dict["prcp"])
    
    # return jsonify(f"Date one year from last recorded: {year_ago}")
    # return jsonify(f"the data")

@app.route('/api/v1.0/stations')
def stations():
    active_stations= session.query(Station.station).all()
    active_station_list = list(np.ravel(active_stations))

    session.close()
    return jsonify(active_station_list)
    # Measure.station, func.count(Measure.station)).\
    # group_by(Measure.station).\
    # order_by(func.count(Measure.station).desc()).all()

@app.route('/api/v1.0/tobs')
def tobs():
    
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days= 365)

    max_temp= session.query(Measure.tobs).\
        filter(Measure.station == 'USC00519281').\
        filter(Measure.date >= year_ago).all()
    # print(max_temp)
    max_temp_list = list(np.ravel(max_temp))

    session.close()
    return jsonify(max_temp_list)

if __name__ == '__main__':
    app.run(debug=True)