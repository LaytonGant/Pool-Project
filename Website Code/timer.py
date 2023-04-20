import cgi
import time

form = cgi.FieldStorage()
minutes_str = form.getvalue("minutes")

# Check if the "minutes" field is present and has a valid value
if minutes_str is None:
    print("Content-type: text/html\n\n")
    print("<p>Error: Missing value for 'minutes' field.</p>")
elif not minutes_str.isdigit():
    print("Content-type: text/html\n\n")
    print("<p>Error: Invalid value for 'minutes' field.</p>")
else:
    minutes = int(minutes_str)

    # Convert minutes to seconds and start the timer
    seconds = minutes * 60
    time.sleep(seconds)

    # Print a message to indicate that the timer has finished
    print("Content-type: text/html\n\n")
    print(f"<p>Timer finished after {minutes} minutes.</p>")
