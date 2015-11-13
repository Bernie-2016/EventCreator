from bsdapi.BsdApi import Factory
import json
import xmltodict

import settings

api = Factory().create(
    id=settings.BSD_ID,
    secret=settings.BSD_SECRET,
    host=settings.BSD_HOST,
    port='80',
    securePort='443'
)


def check_credentials(form):
    resp = api.account_checkCredentials(form['email'], form['pw'])
    return resp.body


def create_account(form):

    if form['password1'] != form['password2']:
        return 'passwords do not match'
    resp = api.account_createAccount(form['email'], form['password1'], form['firstname'], form['lastname'], form['zip'])
    return resp.body


def fetch_constituent(creator_email):
    # resp = api.doRequest('cons/get_constituents_by_email', api.POST, body={"emails": creator_email})

    # resp = api.cons_getConstituents({'email': creator_email})
    resp = api.doRequest('/cons/get_constituents_by_email', None, api.POST, body={"emails": creator_email})

    # Parse the xml response to a dict object
    doc = xmltodict.parse(resp.body)

    if doc['api'] is not None:
        return doc['api']['cons']['@id']
    else:
        params = '<?xml version="1.0" encoding="utf-8"?><api><cons send_password="y"><cons_email><email>' + creator_email + '</email></cons_email></cons></api>'
        resp = api.doRequest('/cons/set_constituent_data', None, api.POST, body=params)
        doc = xmltodict.parse(resp.body)
        return doc['api']['cons']['@id']


def create_events(form):

    # validations
    # Remove special characters from phone number
    contact_phone = ''.join(e for e in form['contact_phone'] if e.isalnum())

    constituent_id = fetch_constituent(form['cons_email'])

    params = {
        'event_type_id': form['event_type_id'],
        'creator_cons_id': constituent_id,
        'name': form['name'],
        'description': form['description'],
        'venue_name': form['venue_name'],
        'venue_zip': form['venue_zip'],
        'venue_city': form['venue_city'],
        'venue_state_cd': form['venue_state_cd'],
        'venue_addr1': form['venue_addr1'],
        'venue_addr2': form['venue_addr2'],
        'venue_country': form['venue_country'],
        'venue_directions': form['venue_directions'],
        'days': [{
            'start_datetime_system': '',  # This will be defined below
            'duration': int(form['duration_num']) * int(form['duration_unit']),
            'capacity': form['capacity']
        }],
        'local_timezone': form['start_tz'],
        'attendee_volunteer_message': form['attendee_volunteer_message'],
        'is_searchable': form['is_searchable'],
        'public_phone': form['public_phone'],
        'contact_phone': contact_phone,
        'host_receive_rsvp_emails': form['host_receive_rsvp_emails'],
        'rsvp_use_reminder_email': form['rsvp_use_reminder_email'],
        'rsvp_reminder_hours': form['rsvp_email_reminder_hours']
    }

    if form['start_time[a]'] == 'pm':
        start_hour = int(form['start_time[h]']) + 12
    else:
        start_hour = int(form['start_time[h]'])

    event_dates = json.loads(form['event_dates'])

    for day in event_dates:
        start_time = day['date'] + ' ' + str(start_hour) + ':' + form['start_time[i]'] + ':00'
        params['days'][0]['start_datetime_system'] = start_time
        response = api.doRequest('/event/create_event', None, api.POST, body={"event_api_version": 2, "values": json.dumps(params)})
    return response.body
