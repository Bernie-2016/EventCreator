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
        'venue_addr1' : form['venue_addr1'],
        'venue_addr2' : form['venue_addr2'],
        'venue_country' : form['venue_country'],
        'venue_directions' : form['venue_directions'],
        'days' : [{
            'start_datetime_system': '', # This will be defined below
            'duration': int(form['duration_num']) * int(form['duration_unit']),
            'capacity' : form['capacity']
        }],
        'local_timezone' : form['start_tz'],
        'attendee_volunteer_message' : form['attendee_volunteer_message'],
        'is_searchable' : form['is_searchable'],
        'public_phone' : form['public_phone'],
        'contact_phone' : form['contact_phone'],
        'host_receive_rsvp_emails' : form['host_receive_rsvp_emails'],
        'rsvp_use_reminder_email' : form['rsvp_use_reminder_email'],
        'rsvp_reminder_hours' : form['rsvp_email_reminder_hours']
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