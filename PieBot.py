from functions import *
import emoji
import schedule

pre_flight_checks()

if environment == "production":
    print("Production")

else:
    print("Dev")
