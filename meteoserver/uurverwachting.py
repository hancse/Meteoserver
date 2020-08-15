#  Copyright (c) 2020  Marc van der Sluys - marc.vandersluys.nl
#  
#  This file is part of the Meteoserver Python package, containing a Python module to obtain and read Dutch
#  weather data from Meteoserver.nl.  See: https://github.com/MarcvdSluys/Meteoserver
#  
#  This is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#  
#  This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
#  warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License along with this code.  If not, see
#  <http://www.gnu.org/licenses/>.


"""Functions to obtain and read 4-10 day weather-forecast data from Meteoserver.nl.
"""



import pandas as pd
import json
import requests



def read_json_url_uurverwachting(key, location):
    """Get weather-forecast data from the Meteoserver server and return them as a dataframe.
    
    Parameters:
        key (string):       The Meteoserver API key.
        location (string):  The name of the location (in the Netherlands) to obtain data for (e.g. 'De Bilt').
    
    Returns:
        data (df):  Pandas dataframe containing forecast data for the specified location (or region).
    """
    
    # Get online data and return a string containing the json file:
    dataJSON = requests.get('https://data.meteoserver.nl/api/uurverwachting_gfs.php?locatie='+location+'&key='+key).text
    
    # Convert the JSON 'file' to a dictionary with keys 'plaatsnaam' and 'data':
    dataDict = json.loads(dataJSON)  # Note: .loads(), not .load()!
    
    # Get the forecast-data dataframe from the data dictionary:
    data = extract_hourly_forecast_dataframes_from_dict(dataDict)
    
    return data


def read_json_file_uurverwachting(fileJSON):
    """Read a Meteoserver weather-forecast-data JSON file from disc and return the data as a dataframe.
    
    Parameters:
        fileJSNO (string):  The name of the JSON file to read.
    
    Returns:
        data (df):  Pandas dataframe containing forecast data for the specified location (or region).
    """
    
    with open(fileJSON) as dataJSON:
        # Convert the JSON 'file' to a dictionary with keys 'plaatsnaam' and 'data':
        dataDict = json.load(dataJSON)  # Note: .load(), not .loads()!
        
        # Get the forecast-data dataframe from the data dictionary:
        data = extract_hourly_forecast_dataframes_from_dict(dataDict)
        
    return data


def extract_hourly_forecast_dataframes_from_dict(dataDict):
    """Extract the forecast-data Pandas dataframe from a data dictionary.
    
    Parameters:
        dataDict (dict):  The name of the data dictionary to convert.
    
    Returns:
        data (df):  Pandas dataframe containing forecast data for the specified location (or region).
    """
    
    # print(dataDict.keys())  # Dictionary with keys: ['plaatsnaam' and 'data']
    # print(type(dataDict['plaatsnaam']))  # List of 1 dict containing a location name
    # print(type(dataDict['data']), len(dataDict['data']))       # List with (152) forecasts
    
    # Create Pandas dataframes from lists of dictionaries:
    # location = pd.DataFrame.from_dict(dataDict['plaatsnaam']).plaats[0]  # List of dict -> df -> str
    data = pd.DataFrame.from_dict(dataDict['data'])
    
    # print(type(location))
    # print(data)
    
    return data