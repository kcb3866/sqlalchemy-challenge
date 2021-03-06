import pandas as pd 
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import numpy as np

from matplotlib import style
# style.use('fivethirtyeight')
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
        f"Available routes: <`/api/v1.0/precipitation`>"
        f"`/api/v1.0/stations"
        f"`/api/v1.0/tobs`"
        f"/api/v1.0/<start>`"
        f"`/api/v1.0/<start>/<end>`"
    )
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Find the most recent date in the data set.
    recent = session.query(Measure.date).order_by(Measure.date.desc()).first()
    recent
    # Calculate the date one year from the last date in data set.
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days= 365)
    year_ago

    # Perform a query to retrieve the data and precipitation scores
    data= session.query(Measure.date, Measure.prcp).filter(Measure.date >= year_ago).all()
    data
    # Save the query results as a Pandas DataFrame and set the index to the date column
    yrly_prcp = pd.DataFrame(data)
    yrly_prcp
    # Sort the dataframe by date
    date_df = yrly_prcp.sort_values("date")
    date_df
    # Use Pandas Plotting with Matplotlib to plot the data

    date_df.plot(x= "date", y="prcp", rot= 90)
    plt.show()
@app


if __name__ == '__main__':
    app.run(debug=True)