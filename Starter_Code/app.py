# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date/yyyy-mm-dd<br/>"
        f"/api/v1.0/start_date/end_date/yyyy-mm-dd yyyy-mm-dd"
    )
#for Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the precipitation data"""
    # Query all precipitation
    #prev_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    #Please note the prev year is hard codeded, okey by Anish
    prev_year = '2016-08-23'
    results=session.query(Measurement.date,Measurement.prcp).\
            filter(Measurement.date>=prev_year).all()
    session.close()

    # Create a dictionary from the row data and append to a list of precipitation list
    precip_list = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip_list.append(precip_dict)
    return jsonify(precip_list)
#for Stations
@app.route("/api/v1.0/stations")
def stations():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query statoins
    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#for tobs
@app.route("/api/v1.0/tobs")
def tobs():
        # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all tobs
    #Please note the prev year and active is hard codeded, okey by Anish
    prev_year = prev_year = '2016-08-23' #dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
                filter(Measurement.station == 'USC00519281').\
                filter(Measurement.date>=prev_year).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    temp_list = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["tobs"] = tobs
        temp_list.append(temp_dict)

    return jsonify(temp_list)
#for min,max and avg temparatures for the start date given
@app.route("/api/v1.0/start_date/<start_date>")
def min_max_avg_start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query 
    results = session.query(func.min(Measurement.tobs).label("min_tobs"), \
                            func.max(Measurement.tobs).label("max_tobs"), \
                            func.avg(Measurement.tobs).label("avg_tobs")).\
                            filter(Measurement.date >= start_date).first()
    session.close()

    return (
        f"Min, Max and Avg temparatures for the date >= {start_date}<br/>"
        f"<br/>"
        f"Minimun temparature : {results.min_tobs}<br/>"
        f"Maximum temparature : {results.max_tobs}<br/>"
        f"Average temparature : {results.avg_tobs}"
    )
    


#for min,max and avg temparatures for the given start date and end date
@app.route("/api/v1.0/start_date/end_date/<start_date>/<end_date>")
def min_max_avg_start_end_date(start_date,end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query 
    results = session.query(func.min(Measurement.tobs).label("min_tobs"), \
                             func.max(Measurement.tobs).label("max_tobs"), \
                             func.avg(Measurement.tobs).label("avg_tobs")).\
                             filter(Measurement.date >= start_date).\
                             filter(Measurement.date <= end_date).first()
    session.close()
    
    return (
        f"Min, Max and Avg temparatures for the start date {start_date} and end date, {end_date}<br/>"
        f"<br/>"
        f"Minimun temparature : {results.min_tobs}<br/>"
        f"Maximum temparature : {results.max_tobs}<br/>"
        f"Average temparature : {results.avg_tobs}"
    )

if __name__ == '__main__':
    app.run(debug=True)


