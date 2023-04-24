'''
Test working with the current date and time. 
'''

import datetime, time

time1 = datetime.datetime.now().time()

min = time1.minute
sec = time1.second
hour = time1.hour

time.localtime()
