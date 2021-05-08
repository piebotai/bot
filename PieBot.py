from functions import *
import schedule

pre_flight_checks()


def piebot(pairs):
    print("Bot working")
    for pair in pairs:
        print(pair[0])


if ENVIRONMENT == "production":
    schedule.every().hour.at(":00").do(piebot, pairs=pair_list)

    while True:
        schedule.run_pending()
        time.sleep(1)

else:
    piebot(pairs=pair_list)
