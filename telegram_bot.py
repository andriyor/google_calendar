from __future__ import print_function

import telebot
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime, time

bot = telebot.TeleBot("191146520:AAGfPgE2Ztq8NAyTs4_3XX7rFn30_1fcSVw")

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    d = datetime.datetime.now()
    mind = d.replace(hour=7)
    mind = mind.isoformat() + "+02:00"
    maxx = d.replace(hour=20)
    maxx = maxx.isoformat() + "+02:00"

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId='pauf8ve9eco0pptvebol371ed4@group.calendar.google.com',
        timeMin=mind, singleEvents=True,
        orderBy='startTime', timeMax=maxx).execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    i = 1
    list_e = ''
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))

        end = event['end'].get('dateTime', event['end'].get('date'))
        start_f = time.strptime(start[0:19], '%Y-%m-%dT%H:%M:%S')
        end_f = time.strptime(end[0:19], '%Y-%m-%dT%H:%M:%S')
        sh, sm = '%02d' % start_f.tm_hour, '%02d' % start_f.tm_min
        eh, em = '%02d' % end_f.tm_hour, '%02d' % end_f.tm_min

        description = event.get('description')
        location = event.get('location')
        all_p = [i, 'Пара', '%s:%s' % (sh, sm,), ':', '%s:%s' % (eh, em,), event['summary'], description, location]
        str_eve = ('  '.join(map(str, all_p)))
        list_e = list_e + str_eve + '\n'
        i += 1
    return list_e


@bot.message_handler(content_types=['text'])
def handle_text(message):
    now = datetime.datetime.now().strftime('%H:%M')
    if "07:30" == now:
        bot.send_message(message.chat.id, main())


bot.polling(none_stop=True, interval=0)
