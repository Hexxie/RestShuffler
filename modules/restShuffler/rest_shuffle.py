import datetime
import sqlite_db
from dateutil import parser
from random import shuffle

class Event():

    def __init__(self, user_id = 1):
        self.user_id = user_id
        self._cur = sqlite_db.db.get_cursor()
        self._con = sqlite_db.db.get_connection()

    def add(self, event):
        res = self._cur.execute(f"SELECT user_id from USER WHERE user_id = {self.user_id}")
        if not res.fetchall():
            print("User not found")
        else:
            print(f"""INSERT INTO REST_EVENT 
                        (name, counter, last_date, user_id )
                        VALUES ('{event}', '0', NULL, '{self.user_id}')""")
            self._cur.execute(f"""INSERT INTO REST_EVENT 
                        (name, counter, last_date, user_id )
                        VALUES ('{event}', '0', NULL, '{self.user_id}')""")
            self._con.commit()

    def update(self, event_id, counter, date):
        self._cur.execute(f"""UPDATE REST_EVENT 
                SET counter = '{counter}', last_date = '{date}'
                WHERE event_id = '{event_id}' AND user_id = '{self.user_id}'""")
        self._con.commit()

    def remove(self, event_id):
        self._cur.execute(f"""DELETE FROM REST_EVENT WHERE event_id = '{event_id}' AND user_id = '{self.user_id}'""")
        self._con.commit()

    def find_all(self):
        res = self._cur.execute(f"""
                                SELECT USER.name, REST_EVENT.name, REST_EVENT.counter, REST_EVENT.event_id, REST_EVENT.last_date
                                FROM USER 
                                INNER JOIN REST_EVENT ON USER.user_id = REST_EVENT.user_id
                                WHERE USER.user_id = '{self.user_id}'""")
        return res.fetchall()
    
    def find_today(self):
        events = self.find_all()
        #Remove events with today's date from the list to exclude them from shuffling
        for item in events.copy():
            try:
                date_str = item[4]
                event_date = parser.parse(date_str)
                if(event_date.date() == datetime.date.today()):
                    events.remove(item)
            except TypeError:
                continue
        return events


def get_shuffled_event(user_id):
    events = Event(user_id)
    all_events = events.find_today()
    if not all_events:
        return "I run out of the events. You can choose whatever you want!"
    shuffle(all_events)
    chosen_event = all_events[0]
    print(chosen_event)

    #This is how to update an event with date and counter (I want to know how often I get particular events)
    count = chosen_event[2] + 1
    event_id = chosen_event[3]
    event_name = chosen_event[1]
    events.update(event_id, count, datetime.datetime.now())
    return event_name

def add_events_from_file(file, user_id):
    events = Event(user_id)
    with open(file) as f:
        [events.add(line) for line in f.readlines()]

if __name__ == '__main__':
    #to run from the shortcut
    print()
    print(get_shuffled_event(1))
    x = input()