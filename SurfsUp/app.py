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

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/start_date'>/api/v1.0/start_date</a><br/>"
        f"<a href='/api/v1.0/start_date/end_date'>/api/v1.0/start_date/end_date</a>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    # Perform a query to retrieve the data and precipitation scores
    precipitation_data = session.query(Measurement.date, Measurement.prcp)\
    .filter(Measurement.date >= one_year_ago)\
    .order_by(Measurement.date).all()
    
    session.close()
    # Convert the query results to a dictionary
    precipitation_dict = precipitation_df.set_index('date').to_dict()['precipitation']

    # Return the JSON representation of the dictionary
    return jsonify(precipitation_dict)

  



@app.route("/api/v1.0/stations")
def stations():

    # Perform a query to retrieve the stations
    station_data = session.query(Station.station).all()
    
    session.close()
    
    # Convert the query results to a list
    stations_list = [station for station, in station_data]

    # Return the JSON representation of the list
    return jsonify(stations_list)

    



@app.route("/api/v1.0/tobs")
def tobs():
    # Query the temperature observations for the most-active station for the previous year
    Waihee_station = 'USC00519281'  

    Waihee_station_data = session.query(func.min(Measurement.tobs),
                                    func.max(Measurement.tobs),
                                    func.avg(Measurement.tobs))\
                                    .filter(Measurement.station == Waihee_station)\
                                    .all()
    session.close()

    # Convert the query results to a list
    Waihee_station_list=[]
    for station, date, prcp, tobs in Waihee_station_data:
        tobs_dict={}
        tobs_dict=["station"] = station_id
        tobs_dict=["date"] = date
        tobs_dict=["prcp"] = precipitation
        tobs_dict=["tobs"] = temperature
        Waihee_tobs.append(tobs_dict)

     # Return the JSON representation of the list
    return jsonify(Waihee_tobs)

@app.route("/api/v1.0/startdate")
def startdate():
     
    # Perform a query to retrieve the temp. stats
    temp_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
                                .filter(Measurement.date >= start)\
                                .all()
    session.close()
    
    TMIN, TAVG, TMAX = temp_results[0]
    
    
    # Return the JSON
    return jsonify({"TMIN": TMIN, "TAVG": TAVG, "TMAX": TMAX})




@app.route("/api/v1.0/start_date/end_date")
def enddate():
     
    # Perform a query to retrieve the temp. stats for the dates from the start date to the end date, inclusive.

    temp_range_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
                                        .filter(Measurement.date >= start)\
                                        .filter(Measurement.date <= end)\
                                        .all()
    session.close()

    TMIN, TAVG, TMAX = temp_range_results[0]
      
    # Return the JSON
    return jsonify({"TMIN": TMIN, "TAVG": TAVG, "TMAX": TMAX})

if __name__ == '__main__':
    app.run(debug=True)
