from fastapi import FastAPI, HTTPException, Query
import requests
import json
from datetime import datetime, timedelta

app = FastAPI()

NEO_WS_URL = 'https://api.nasa.gov/neo/rest/v1/feed'
API_KEY = 'TVxKLbnTpEDZU6s5tetg3UkhQc4Sbg5ocXCBkHJ0'

@app.get('/objects')
def get_neo_objects(start_date: str = Query(..., description='Start date (YYYY-MM-DD)', example='2022-01-01'),
                    end_date: str = Query(..., description='End date (YYYY-MM-DD)',   example='2022-01-07')):
   
    #check the input dates format
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        raise HTTPException(status_code=400, detail='Invalid date format, should be YYYY-MM-DD')

    #check if start date is before end date
    if start_date > end_date:
        raise HTTPException(status_code=400, detail='End date must be after start date')
    
    #set the delta variable for nasa api limit
    delta = timedelta(days=7)
    results = []

    #keep requesting data until the enddate is reached
    while start_date < end_date:
        query_start_date = start_date.strftime("%Y-%m-%d")
        query_end_date = (start_date + delta).strftime("%Y-%m-%d")
        
        #request the data from api and append it to the results list
        url = f'{NEO_WS_URL}?start_date={query_start_date}&end_date={query_end_date}&api_key={API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            data = json.loads(response.text)
            for date in data['near_earth_objects']:
                if datetime.strptime(date, '%Y-%m-%d') > end_date:
                    continue

                for near_earth_object in data['near_earth_objects'][date]:
                    neo_object = {
                        'name': near_earth_object['name'],
                        'size': near_earth_object['estimated_diameter']['meters']['estimated_diameter_max'],
                        'closest_approach_date': near_earth_object['close_approach_data'][0]['close_approach_date'],
                        'closest_approach_distance': near_earth_object['close_approach_data'][0]['miss_distance']['kilometers']
                    }
                    results.append(neo_object)
                    
        start_date += delta
    if not results:
        raise HTTPException(status_code=404, detail='No near-earth objects found in date range')
    #sort the list
    return sorted(results, key=lambda k: k['closest_approach_distance'])
