import json
import pandas as pd
import numpy as np
import ast

import requests
import pickle
import argparse

def gcApiResponse(latitude,longitude,Google_Cloud_Geocoder_API_Key):
    r = requests.get(f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={Google_Cloud_Geocoder_API_Key}")
    return r

def processArgs(args):
    Google_Cloud_Geocoder_API_Key = args.apiKey
    with open(f'./{args.fileName}', 'rb') as fp:
        data = pickle.load(fp)

    for val in data.values():
        print("Processing : " + str(val['pickup_latitude']) + "," + str(val['pickup_longitude']))
        tempPickupDict = dict()
        if val['pickup_latitude'] != 0 and val['pickup_longitude'] != 0:
            responseDict = gcApiResponse(val['pickup_latitude'],val['pickup_longitude'],Google_Cloud_Geocoder_API_Key).json()['results']
            #print(responseDict)
            # Checking if the google API response is empty or not
            if len(responseDict) > 0:
                for featureDict in responseDict[0]['address_components']:
                    if 'route' in featureDict['types']:
                        tempPickupDict['Pickup_Street'] = featureDict['long_name']
                    
                    if 'sublocality' in featureDict['types']:
                        tempPickupDict['Pickup_Neighborhood'] = featureDict['long_name']
                    
                    if 'postal_code' in featureDict['types']:
                        tempPickupDict['Pickup_Zipcode'] = featureDict['long_name']
                    
                    if 'locality' in featureDict['types']:
                        tempPickupDict['Pickup_Locality'] = featureDict['long_name']
                    
                    if 'administrative_area_level_1' in featureDict['types']:
                        tempPickupDict['Pickup_City'] = featureDict['long_name']
                    
                    if 'administrative_area_level_2' in featureDict['types']:
                        tempPickupDict['Pickup_County'] = featureDict['long_name']
                val.update(tempPickupDict)
                del responseDict,tempPickupDict,featureDict
        print("Processing : " + str(val['dropoff_latitude']) + "," + str(val['dropoff_longitude']))
        tempDropoffDict = dict()
        if val['dropoff_latitude'] != 0 and val['dropoff_longitude'] != 0:
            responseDropoffDict = gcApiResponse(val['dropoff_latitude'],val['dropoff_longitude'],Google_Cloud_Geocoder_API_Key).json()['results']
            #print(responseDict)
            if len(responseDropoffDict) > 0:
                for featureDict in responseDropoffDict[0]['address_components']:
                    if 'route' in featureDict['types']:
                        tempDropoffDict['Dropoff_Street'] = featureDict['long_name']
                    
                    if 'sublocality' in featureDict['types']:
                        tempDropoffDict['Dropoff_Neighborhood'] = featureDict['long_name']
                    
                    if 'postal_code' in featureDict['types']:
                        tempDropoffDict['Dropoff_Zipcode'] = featureDict['long_name']
                    
                    if 'locality' in featureDict['types']:
                        tempDropoffDict['Dropoff_Locality'] = featureDict['long_name']
                    
                    if 'administrative_area_level_1' in featureDict['types']:
                        tempDropoffDict['Dropoff_City'] = featureDict['long_name']
                    
                    if 'administrative_area_level_2' in featureDict['types']:
                        tempDropoffDict['Dropoff_County'] = featureDict['long_name']
                val.update(tempDropoffDict)
                del tempDropoffDict,responseDropoffDict,featureDict


    with open(f'./{args.fileName}', 'wb') as fp:
            pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-fn','--fileName',  type=str, required=True,
                    help='input file name')
    parser.add_argument('-ak','--apiKey',  type=str, required=True,
                    help='google API key')               
    args = parser.parse_args()

    processArgs(args)
