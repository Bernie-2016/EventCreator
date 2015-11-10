from bsdapi.URL import URL
from bsdapi.BsdApi import Factory
import json

import settings

api = Factory().create(
    id=settings.BSD_ID, secret=settings.BSD_SECRET,
    host=settings.BSD_HOST, port='80',
    securePort='443')

def create_events(form, *args, **kwargs):
    params = {
        'event_type_id': form['event_type_id'],
        'creator_cons_id': '1', # hardcoded for now
        'name' : form['name'],
        'description': form['description'],
        'venue_name': form['venue_name'],
        'venue_zip': form['venue_zip'],
        'venue_city': form['venue_city'],
        'venue_state_cd': form['venue_state_cd'],
        'days' : [{
            'start_datetime_system': '', # This will be defined below
            'duration': int(form['duration_num']) * int(form['duration'])
        }]
    }

    if form['start_time[a]'] == 'pm':
        start_hour = int(form['start_time[h]']) + 12
    else:
        start_hour = int(form['start_time[h]'])

    event_dates = json.loads(form['event_dates'])

    for day in event_dates:
        start_time = day['date'] + ' ' + str(start_hour) + ':' + form['start_time[i]'] + ':00'
        params['days'][0]['start_datetime_system'] = start_time
        resp = api.doRequest('/event/create_event', None, api.POST, body={"event_api_version": 2, "values": json.dumps(params)})

    # return start_time
    return resp.body

# called like this:  bsd.create_event(1, 6, "name", "description", "venue_name", "11217", "venue_city", "venue_state_cd")