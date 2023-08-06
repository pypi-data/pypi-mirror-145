# habitat-fydp-package

### Purpose of the Package

Democratize access to HAB related data in Lake Erie to be used for scientific research. 

### Getting Started

Getting started is easy! Just pip install our package as below: 

```
pip install habitat-fydp-package
```

To test if the package downloaded try this! 

```python
from habitat_fydp_package import list_station_measurment_types
list_station_measurment_types('Toledo Pump Station')
``` 

### Usage 

Call help on any of the functions listed in the table to return docstring and information on inputs / oupus for a particular function!

### Features

Listed API function currently available are listed below: 

##### List Available Stations 

This function lists all the stations available in the GLOS dataset. Preforms an API call to return (for each station available), its name, id, latitude and longitude coordinates, and platform id. Returns these details as a dictionary object, indexed by station name.

```python
from habitat_fydp_package import list_stations
list_stations()

# {'Sandusky Water Intake': [{'dataset_id': 20},
#   {'latitude': 41.464403},
#   {'longitude': -82.647768},
#   {'platform_id': 14},
#   {'org_platform_id': 'LEBIWW'}],
#  'Ottawa County': [{'dataset_id': 22},
#   {'latitude': 41.514315},
#   {'longitude': -82.9386},
#   {'platform_id': 16},
#   {'org_platform_id': 'LEOC'}], ...
```


##### List Measurment Types Available at a Station 

Given a station name from GLOS (input), return all time series measurement types available at this station. Returns a list of these names.

```python
from habitat_fydp_package import list_station_measurment_types
station_name = 'Sandusky Water Intake'
list_station_measurment_types(station_name) 

# {'body_of_water': 'lake-erie',
#  'obs_dataset_id': 20,
#  'org_platform_id': 'LEBIWW',
#  'parameters': [{'name_vocabulary': 'cf',
#    'standard_name': 'mass_concentration_of_oxygen_in_sea_water'},
#   {'name_vocabulary': 'cf',
#    'standard_name': 'fractional_saturation_of_oxygen_in_sea_water'},
#   {'name_vocabulary': 'cf', 'standard_name': 'sea_water_turbidity'},
#   {'name_vocabulary': 'cf',
#    'standard_name': 'sea_water_electrical_conductivity'},
#   {'name_vocabulary': 'cf',
#    'standard_name': 'sea_water_ph_reported_on_total_scale'},
#   {'name_vocabulary': 'ioos', 'standard_name': 'chlorophyll_fluorescence'},
#   {'name_vocabulary': 'glos',
#    'standard_name': 'mass_concentration_of_blue_green_algae_in_sea_water_rfu'},
#   {'name_vocabulary': 'cf', 'standard_name': 'sea_surface_temperature'}],
#  'platform_event': 'activated',
#  'platform_name': 'Sandusky Water Intake',
#  'platform_type': 'fixed'}
```

##### Return Measurement Definition

Given a measurment type from one of the available GLOS stations return its defintion ie. what is it? to the user.

 ```python
 from habitat_fydp_package import list_measurement_defintion
 measurement_type = 'Chlorophyll Fluorescence'
 list_measurement_defintion(measurement_type) 

#  {'alerts': {'threshold_max': 70, 'threshold_min': -2},
#  'canonical_unit_id': 'rfu',
#  'display_description': {'en': 'Chlorophyll is the green pigment found in most plants, algae, and cyanobacteria. Chlorophyll fluorescence is a relative measure of the abundance of phytoplankton in a water sample.'},
#  'display_name': {'en': 'Chlorophyll Fluorescence'},
#  'name_vocabulary': 'ioos',
#  'preferred_imperial_unit_id': 'rfu',
#  'preferred_metric_unit_id': 'rfu',
#  'standard_name': 'chlorophyll_fluorescence',
#  'units': [{'id': 'rfu',
#    'js_qty_unit': 'RFU',
#    'symbol': 'RFU',
#    'udunit': 'RFU'}]}
 ``` 

##### Get the Most Recent Station Measurement

Given a GLOS station name, and a measurement type available at the station, return the most recent value of that measurement. ie. surface temperature at toledo site is 10 degree Celcius right now

```python
from habitat_fydp_package import get_most_recent_measurement
station_name = 'Toledo Pump Station' 
measurement_type = 'Chlorophyll Fluorescence'
get_most_recent_measurement(station_name, measurement_type)

# [{'latitude': 41.67496,
#   'longitude': -83.3079,
#   'timestamp': '2022-03-08T18:20:00+00:00',
#   'value': 0.64}]

``` 

##### Get Historical Station Measurements 

Given a GLOS station, a measurement available at that station, a start_date, and end_date, return the measurement values over that window. Returns timeseries as a pandas dataframe object.

```python
from habitat_fydp_package import get_historical_measurements
get_historical_measurements(station_name, measurement, start_date, end_date)
```

##### Return Lake Depth 

Given a path to the stored contour depth file of lake erie (this is available from the sdk), plot it. Shows that different depth levels in Lake Erie 

```python
from habitat_fydp_package import plot_lake_depth
plot_lake_depth()
```

##### Return Historical Weather Data

Function to retrieve the weather data available. Returns weather from the location of the station through satilite.

start_date: first data point from this date
end_date: last data point from this date
station_name: station of interest
freq: frequency of the observations ie. 1 min, 1 hr, 1 day, e.t.c
api_key: api_key to access open weather api
returns: pandas df with the weather data

```python
from habitat_fydp_package import get_weather_variables
get_weather_variables(start_date, end_date, station_name, freq)
``` 

##### Aggregate Data Soucres 

Function to aggregate all available data into one frame.

measurement: measurement of interest that is available at the station
start_date: first data point from this date
end_date: last data point from this date
station_name: station of interest
freq: frequency of the observations ie. 1 min, 1 hr, 1 day, e.t.c
path_to_contour_file: path to the bathemetry shap file.
returns: pandas df indexed by timestamp with all the data

```python
from habitat_fydp_package import aggregate_data

aggregate_habnet_data(station_name, measurement, start_date, end_date,freq,path_)
``` 

##### Filter Time Series Noise

Given a time series "smooth" the data to reduce noise given a specfic window size to preform the averaging over. This function uses basic stats to additonally show anomolous points by setting plot_anomalies to True. This function can also provide a confidence interval over the average

given plot_interval = True. A point is considered an anomaly if outside this range.
series - dataframe with timeseries
window - rolling window size
plot_intervals - show confidence intervals
plot_anomalies - show anomalies

```python
from habitat_fydp_package import plotMovingAverage
plotMovingAverage(series, window, plot_intervals=False, scale=1.96, plot_anomalies=False
``` 

##### Time Series Decomposition

Decomposes the time series for a specific measurement and station

```python
from habitat_fydp_package import decomposition_timeseries_measurment

decomposition_timeseries_measurment()
``` 

##### Univariate Time Series Forecasting

Forecasts a specific measurement for a given station based on its historical data
Using a simple ARIMA model provide a forecast for one time series variable

series: time series to forecast
horizon: units in advance to forecast
frequency_of_obvs: days, months, seconds, e.t.c
returns: predictions, lower bound, upper bound confidence interval

```python 
from habitat_fydp_package import univariate_forecast_arima
univariate_forecast_arima(series, horizon, frequency_of_obvs)                        
```