##Climate Analysis and Flask API - README
#Introduction
Congratulations on planning your long holiday vacation to Honolulu, Hawaii! To enhance your trip planning, you've chosen to conduct a climate analysis of the area. This README will guide you through the necessary steps to perform the analysis and create a Flask API for easy access to the climate data.

#Part 1: Analyze and Explore the Climate Data
Jupyter Notebook Database Connection
Database Connection:

Connect to the SQLite database using SQLAlchemy.
Table Reflection:

Reflect tables into classes using automap_base().
Session Link:

Link Python to the database by creating a SQLAlchemy session.
Session Closure:

Close the session at the end of the notebook.
Precipitation Analysis
Most Recent Date Query:

Find the most recent date in the dataset.
Precipitation Data Query:

Collect date and precipitation for the last year without passing the date as a variable.
DataFrame Creation:

Save query results to a Pandas DataFrame.
DataFrame Sorting:

Sort DataFrame by date.
Plotting:

Plot results using DataFrame plot method.
Summary Statistics:

Use Pandas to print summary statistics for precipitation data.
Station Analysis
Number of Stations Query:

Find the number of stations in the dataset.
Most-Active Stations Query:

List stations and observation counts, find the most active station.
Temperature Statistics Query:

Find min, max, and average temperatures for the most active station.
TOBS Query:

Get the previous 12 months of TOBS data for the most active station.
TOBS DataFrame:

Save TOBS query results to a Pandas DataFrame.
Histogram Plotting:

Plot a histogram with bins=12 for the last year of data using TOBS.
#Part 2: Design Your Climate App
API SQLite Connection & Landing Page
Engine Generation:

Generate the engine for the correct SQLite file.
Schema Reflection:

Reflect the database schema using automap_base().
Table References:

Save references to tables in the SQLite file (measurement and station).
Session Binding:

Create and bind the session between the Python app and the database.
Route Display:

Display available routes on the landing page.
API Static Routes
Precipitation Route:

Return JSON with date as the key and precipitation as the value, limited to the last year.
Stations Route:

Return JSONified data of all stations.
TOBS Route:

Return JSONified data for the most active station, limited to the last year.
API Dynamic Route
Start Route:

Accept the start date parameter, return min, max, and average temperatures from start to the end of the dataset.
Start/End Route:

Accept start and end date parameters, return min, max, and average temperatures from start to end.
