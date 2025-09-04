# Example script enables all bots 5 minutes before earliest entry time, sets to disable on close 5 minutes after latest entry time
import WhisperDriver
import datetime
from datetime import timedelta
from functools import partial

#############  FILL IN DETAILS HERE ######
WT_USR = ''
WT_PWD = ''
WT_API_TOKEN = ''
NO_TOUCHY_BOTS = ['WFNVC6MY4G', 'etc...'] # bot id "number" from bot url
#########################################


def run_main():   

    # Don't run on weekends
    day = ['m', 't', 'w', 'th', 'f', 'sa', 'su'][datetime.datetime.today().weekday()]
    if day == 'sa' or day == 'su':
        print("Market not open on weekends!")
        return

    # Instantiate WhisperDriver
    WD = WhisperDriver.ApiWrapper(WT_API_TOKEN)
    WD.via_selenium.enable(WT_USR, WT_PWD, is_verbose=True, is_headless=True)   

    # Start Scheduler. Schedule loop will keep process alive until stopped.  Schedule stop time so process dies
    WD.scheduler.start()
    WD.scheduler.stop_scheduler_at_time('4:30 PM', 'America/New_York')

    # Get all bots
    bots = WD.bots.bots_list.all

    # Schedule enable and soft disable for each bot based on its unique entry window
    today = datetime.datetime.now().date()
    for bot in bots:
        bot_num = bot.number
        if bot_num in NO_TOUCHY_BOTS:
            print(f"Skipping bot {bot_num} as it is in the no-touchy list.")
            continue

        # Pull earliest/latest entry times
        earliest = bot.entry_condition.get('earliest_time_of_day')
        latest = bot.entry_condition.get('latest_time_of_day')

        # Error handling for missing entry times
        if not earliest or not latest:
            print(f"{bot_num} has no earliest/latest entry time defined, skipping scheduling.")
            continue
        try:
            earliest_dt = datetime.datetime.strptime(f"{today} {earliest}", "%Y-%m-%d %I:%M %p")
            latest_dt = datetime.datetime.strptime(f"{today} {latest}", "%Y-%m-%d %I:%M %p")
        except Exception as e:
            print(f"Could not parse entry times for bot {bot_num}: {e}")
            continue

        # Calculate enable/disable times
        enable_time = (earliest_dt - timedelta(minutes=5)).strftime("%I:%M %p")
        disable_time = (latest_dt + timedelta(minutes=5)).strftime("%I:%M %p")

        # Use bot methods to schedule enable/disable
        bot.enable_at_time(enable_time, 'America/New_York')
        print(f"Scheduled enable for bot {bot_num} at {enable_time}")
        bot.disable_at_time(disable_time, 'America/New_York')
        print(f"Scheduled soft disable for bot {bot_num} at {disable_time}")

    # Example scheduling of arbitrary function via partial function application
    def print_message(msg):
        print(msg)

    stop_time = datetime.datetime.strptime('16:30', '%H:%M')
    five_min_before = (stop_time - timedelta(minutes=5)).strftime('%I:%M %p')
    message = 'Script will stop in 5 min!'
    WD.scheduler.add_task(five_min_before, 'America/New_York', partial(print_message, message))
    # End partial function example

if __name__ == '__main__':
    run_main()