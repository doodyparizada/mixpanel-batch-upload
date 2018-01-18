"""Example of uploading a csv file using the batching API of mixpanel.

ip and time fields are treated specially by mixpanel and are set as `meta` fields.
user_id is set as the distinct_id.
all other fields are set as properties.
"""
import os
import sys

from mixpanel import Mixpanel, BufferedConsumer
import pandas


TOKEN = os.getenv('MIXPANEL_API_TOKEN')
SECRET = os.getenv('MIXPANEL_API_SECRET') 
API = os.getenv('MIXPANEL_API_KEY')


FIELDS = ['os_name',
          'language',
          'os_version',
          'session_id',
          'platform',
          'app_version']

mp = Mixpanel(TOKEN, BufferedConsumer())


def main():
    try:
        start = int(sys.argv[1])
        index = 0
        df = pandas.read_csv('input.csv')

        for index, row in df.iterrows():
            if index < start:
                continue
            fields = {k: v for k, v in row.items() if k in FIELDS}
            print row['user_id'], row['event_type'], fields
            mp.import_data(api_key=API,
                           distinct_id=row['user_id'],
                           event_name=row['event_type'],
                           timestamp=int(row['time']/1000),
                           properties=fields,
                           meta={'ip': row['ip']})
    except (KeyboardInterrupt, Exception) as e:
        print '='*100
        print 'finished at', index
        print '='*100
        print e
        print '='*100

    mp._consumer.flush()


if __name__ == '__main__':
    main()
