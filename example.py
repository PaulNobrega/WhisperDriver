# Example script enables all bots 5 minutes before earliest entry time, sets to disable on close 5 minutes after latest entry time
import WhisperDriver
import datetime
from datetime import timedelta
import creds as personal
from functools import partial


def run_main():   
    day = ['m', 't', 'w', 'th', 'f', 'sa', 'su'][datetime.datetime.today().weekday()]

    if day == 'sa' or day == 'su':
        print("Market not open on weekends!")
        return

    WD = WhisperDriver.ApiWrapper(personal.WT_API_TOKEN)
    WD.via_selenium.enable(personal.USER, personal.PWD, is_verbose=True, is_headless=True)   

    WD.scheduler.start()
    WD.scheduler.stop_scheduler_at_time('4:30 PM', 'America/New_York')

    # Get all bots
    bots = WD.bots.get_all_bots()

    # Schedule enable and soft disable for each bot based on its unique entry window
    today = datetime.datetime.now().date()
    for bot in bots:
        bot_num = bot.get('number')
        entry_cond = bot.get('entry_condition', {})
        earliest = entry_cond.get('earliest_time_of_day')
        latest = entry_cond.get('latest_time_of_day')
        if not earliest or not latest or not bot_num:
            print(f"{bot_num} has no earliest/latest entry time defined, skipping scheduling.  {bot}")
            continue
        try:
            earliest_dt = datetime.datetime.strptime(f"{today} {earliest}", "%Y-%m-%d %I:%M %p")
            latest_dt = datetime.datetime.strptime(f"{today} {latest}", "%Y-%m-%d %I:%M %p")
        except Exception as e:
            print(f"Could not parse entry times for bot {bot_num}: {e}")
            continue
        enable_time = (earliest_dt - timedelta(minutes=5)).strftime("%I:%M %p")
        disable_time = (latest_dt + timedelta(minutes=5)).strftime("%I:%M %p")
        # Schedule enable for this bot
        WD.scheduler.add_task(enable_time, 'America/New_York', fxn=partial(WD.bots.enable_bot, bot_num))
        print(f"Scheduled enable for bot {bot_num} at {enable_time}")
        # Schedule soft disable for this bot using partial
        soft_disable_fn = partial(WD.via_selenium.enabled_to_soft_disabled_by_list, [bot_num])
        WD.scheduler.add_task(disable_time, 'America/New_York', fxn=soft_disable_fn)
        print(f"Scheduled soft disable for bot {bot_num} at {disable_time} via selenium")
    


if __name__ == '__main__':
    run_main()
