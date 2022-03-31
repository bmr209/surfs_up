# import dependencies
#from cProfile import run
import datetime as dt
from http.client import REQUEST_URI_TOO_LONG
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# To allow me to query the SQLite database file use create_engine()
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect database into classes
Base = automap_base()

# Reflect the database
Base.prepare(engine, reflect=True)

# Save the references to each table to a variable
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a like from Python to the database
session = Session(engine)


# Create a new Flask instance called app
#app = Flask(__name__)

#@app.route('/')
#def hello_world():
    #return 'Hello world'


# Create a Flask application called "app"
app = Flask(__name__)

# Define the welcome route
@app.route("/")

# Create a function with a return statement with f-strings as a reference to all of the other routes
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Create the precipitation route (aligned all the way to the left)
@app.route("/api/v1.0/precipitation")

# Now create the precipitation() function
def precipitation():
    # Calculate the date one year go from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Write a query to the date and precipitation for the previous year
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()

    # Create a dictionary with the date as the key and the precipitation as the vaulue
    precip = {date: prcp for date, prcp in precipitation}

    # Use josnify() to format our results into a JSON structure file; jsonify() converts the dictionary to a JSON file
    return jsonify(precip)

# Create the stations route
@app.route("/api/v1.0/stations")

# Create a new function called stations
def stations():
    # Get all the stations in the database
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Goal of temperature observations route is to return the temperature observations for the previous year
# Create the temperature observations route
@app.route("/api/v1.0/tobs")

# Create a function called temp_montly()
def temp_monthly():
    # Calculates the date one year ago from the last date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # Query the primary station for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year).all()

    # Unravel the results into a one-dimensional array and convert that array into a list
    temps = list(np.ravel(results))
    
    # Jsonify the list and return the results
    return jsonify(temps=temps)


# Create a route for the summary statistics report
# Report on the minimum, average and maximum temperatures
# Have to provide a starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create a function called stats()
def stats(start=None, end=None):
    # Create a query to select min, avg, and max temps from database
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # Use an if-not statement since we need to determine the starting and ending date
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
    
    results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temps = list(np.ravel(results))
    return jsonify(temps)


