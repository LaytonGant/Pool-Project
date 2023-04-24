import schedule, time, datetime, threading

# Controls whether to run the schedule thread or not
runThread = True

# Simple function to be run as an event
def timeFunc(msg="world"):
    print("Hello {}!".format(msg))

# Function to continuously run pending events. Runs based on the state of runThread
def updateSchedule():
    while runThread:
        schedule.run_pending()  # If any events take a significant amount of time, it may be good to run this in a separate thread
        time.sleep(1)
    print("Update schedule ended.")

# Add scheduling event(s)
schedule.every().minute.at(":00").do(timeFunc)

# Start scheduler thread
schedThread = threading.Thread(target=updateSchedule)
schedThread.start()
print("Thread started")

# Continue program until a certain minute value is reached
while not datetime.datetime.now().time().minute == 31:
    time.sleep(1)

# Stop scheduler thread
runThread = False
schedThread.join()

# End
print("Main loop ended")
