'''
Test adding/removing events in a scheduler in a different thread. 
'''

import sched, time, threading

# Create schedule manager
schedManager = sched.scheduler(time.time, time.sleep)

def print_time(a='default'):
    print("From print_time", time.time(), a)

def add_some_times():
    print(time.time())
    schedManager.enter(10, 1, print_time)
    schedManager.enter(5, 2, print_time, argument=('positional',))
    # despite having higher priority, 'keyword' runs after 'positional' as enter() is relative
    schedManager.enter(5, 1, print_time, kwargs={'a': 'keyword'})
    schedManager.enterabs(1_650_000_000, 10, print_time, argument=("first enterabs",))
    schedManager.enterabs(1_650_000_000, 5, print_time, argument=("second enterabs",))
    # schedManager.run()
    # print(time.time())

def add_more_times():
    schedManager.enter(4, 1, print_time, argument=("Extra event 1",))
    schedManager.enter(8, 1, print_time, argument=("Extra event 2",))

# Start scheduler
add_some_times()
schedThread = threading.Thread(target=schedManager.run)
schedThread.start()

# Delay and then try adding another event
time.sleep(3)
add_more_times()

# End 
print("End main thread.")
