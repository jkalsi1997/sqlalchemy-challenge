# Import the dependencies.
import numpy as np 
import datetime as dt  # Add this line for datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect=True)

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# Create our session (link) from Python to the DB
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
        f"Check out the available routes for Hawaii weather data<br/>"
        f"precipitation: /api/v1.0/precipitation<br/>"
        f"list of stations: /api/v1.0/stations<br/>"
        f"temperature observations: /api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"
    )

# Convert the query results from the precipitation analysis to a dictionary 
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    """Return a list of precipitation and date data"""
    last_date = session.query(func.max(measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(last_date, '%Y-%m-%d') - dt.timedelta(days=365)
    precipitation_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_year_ago).\
        filter(measurement.date <= last_date).all()

    # Close session
    session.close()

    # Convert to dictionary
    all_precipitation = []
    for date, prcp in precipitation_data:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        all_precipitation.append(prcp_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    """Return a list of all the stations"""
    station_total = session.query(station.station).\
                        order_by(station.station).all()
    
    session.close()

    all_stations = list(np.ravel(station_total))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    """Return the temperature observations from the previous year"""
    most_active_station = (
        session.query(measurement.station, func.count(measurement.station))
        .order_by(func.count(measurement.station).desc())
        .group_by(measurement.station)
        .first()
    )
    
    most_active_station_no = most_active_station[0]
    
    recent_date_query = (
        session.query(measurement.date, measurement.tobs)
        .filter(measurement.station == most_active_station_no)
        .order_by(measurement.date.desc())
        .first()
    )

    yearly_data_query = (
        session.query(measurement.date, measurement.tobs)
        .filter(measurement.station == most_active_station_no)
        .filter(measurement.date > "2016-08-17")
        .all()
    )
    
    session.close()  

    tobsall = []
    for date, tobs in yearly_data_query:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs 
        tobsall.append(tobs_dict)

    return jsonify(tobsall)

@app.route("/api/v1.0/<start>")

def get_temps_start(start):
    session = Session(engine)
    yearly_data_query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
              filter(measurement.date >= start).all()
    session.close()

    temps = []
    for min_temp, avg_temp, max_temp in yearly_data_query:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = min_temp
        temps_dict['Average Temperature'] = avg_temp
        temps_dict['Maximum Temperature'] = max_temp
        temps.append(temps_dict)

    return jsonify(temps)

@app.route("/api/v1.0/<start>/<end>")
def get_temps_start_end(start, end):
    session = Session(engine)
    yearly_data_query = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
              filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()

    temps = []
    for min_temp, avg_temp, max_temp in yearly_data_query:
        temps_dict = {}
        temps_dict['Minimum Temperature'] = min_temp
        temps_dict['Average Temperature'] = avg_temp
        temps_dict['Maximum Temperature'] = max_temp
        temps.append(temps_dict)

    return jsonify(temps)



if __name__ == '__main__':
    app.run(debug=True)
