import creds as personal
import WhisperDriver
import time
import datetime
from functools import partial
from WhisperDriver.Obj.throttle import WhisperTradesThrottle

# Global WD instance and enable via_selenium
WD = WhisperDriver.ApiWrapper(personal.WT_API_TOKEN)
WD.via_selenium.enable(personal.USER, personal.PWD, is_verbose=True, is_headless=True)
active_bots = ['bot_num', 'bot_num_2']



def test_throttle_demo():
    """
    Demonstrate WhisperTradesThrottle usage: enable/disable, set delay, and wrap a function call.
       Default is 2 seconds, enabled.
    """
    throttle = WhisperTradesThrottle()
    print(f"Initial throttle state: is_on={throttle.is_on}, delay_sec={throttle.delay_sec}")
    throttle.set_delay_sec(1)
    print("Set delay to 1 second.")
    throttle.disable()
    print(f"Throttle disabled: is_on={throttle.is_on}")
    throttle.enable()
    print(f"Throttle enabled: is_on={throttle.is_on}")
    def sample_fxn():
        print(f"Function called at {time.time()}")
    print("Calling sample_fxn with throttle...")
    print("Done with throttle demo.")

def test_update_methods_demo():
    """
    Demonstrate all update methods: bots, variables, entry/exit settings, and report update.
    """
    print("Calling WD.bots.update_all_bots()...")
    WD.bots.update_all_bots()
    print("Updated all bots.")
    print("Calling WD.variables.update_all_variables()...")
    WD.variables.update_all_variables()
    print("Updated all variables.")
    WD.update_all_bots_list()
    bot_num = WD.bot_number_list[0] if WD.bot_number_list else None
    if bot_num:
        print(f"Calling WD.via_selenium.update_entry_settings for bot {bot_num}...")
        entry_settings = WD.via_selenium.get_entry_settings(bot_num)
        WD.via_selenium.update_entry_settings(bot_num, entry_settings)
        print("Updated entry settings.")
        print(f"Calling WD.via_selenium.update_exit_settings for bot {bot_num}...")
        exit_settings = WD.via_selenium.get_exit_settings(bot_num)
        WD.via_selenium.update_exit_settings(bot_num, exit_settings)
        print("Updated exit settings.")
    else:
        print("No bots found for entry/exit update demo.")
    WD.update_all_reports_list()
    report_num = WD.report_number_list[0] if WD.report_number_list else None
    if report_num:
        print(f"Calling WD.endpts.reports.update_bot_report for report {report_num}...")
        WD.endpts.reports.update_bot_report(report_num)
        print("Updated bot report.")
    else:
        print("No reports found for update_bot_report demo.")

def test_apiwrapper_info_methods():
    """
    Test all ApiWrapper methods that retrieve information and do not alter state.
    """
    # Test update_all_bots_list
    WD.update_all_bots_list()
    print('Bot number list:', WD.bot_number_list)
    assert isinstance(WD.bot_number_list, list)

    # Test update_all_reports_list
    WD.update_all_reports_list()
    print('Report number list:', WD.report_number_list)
    assert isinstance(WD.report_number_list, list)

    # Test update_all_variables_list
    WD.update_all_variables_list()
    print('Variable number list:', WD.variable_number_list)
    assert isinstance(WD.variable_number_list, list)

    # Test bots.get_all_bot_variables (returns json)
    all_bot_vars = WD.bots.get_all_bot_variables()
    print('All bot variables:', all_bot_vars)
    assert isinstance(all_bot_vars, list)

    # Test bots.bots_list.all (list of bot objects)
    all_bots = WD.bots.bots_list.all
    print('All bots:', all_bots)
    assert isinstance(all_bots, list)

    # Test variables.variables_list.all (list of variable objects)
    all_vars = WD.variables.variables_list.all
    print('All variables:', all_vars)
    assert isinstance(all_vars, list)

    # Test endpts.bots.get_all_bots (returns json)
    all_bots_json = WD.endpts.bots.get_all_bots()
    print('All bots (json):', all_bots_json)
    assert isinstance(all_bots_json, list)

    # Test endpts.reports.get_all_bot_reports (returns json)
    all_reports_json = WD.endpts.reports.get_all_bot_reports()
    print('All reports (json):', all_reports_json)
    assert isinstance(all_reports_json, list)

    # Test endpts.variables.get_all_bot_variables (returns json)
    all_vars_json = WD.endpts.variables.get_all_bot_variables()
    print('All variables (json):', all_vars_json)
    assert isinstance(all_vars_json, list)

    # Test endpts.brokers.get_all_broker_connections (returns json)
    all_brokers_json = WD.endpts.brokers.get_all_broker_connections()
    print('All broker connections (json):', all_brokers_json)
    assert isinstance(all_brokers_json, list)

    # Demonstrate via_selenium get_entry_settings and get_exit_settings for one bot
    example_bot = WD.bot_number_list[0] if WD.bot_number_list else None
    if example_bot:
        entry_settings = WD.via_selenium.get_entry_settings(example_bot)
        print(f"Entry settings for bot {example_bot}:", entry_settings)
        exit_settings = WD.via_selenium.get_exit_settings(example_bot)
        print(f"Exit settings for bot {example_bot}:", exit_settings)
    else:
        print("No bots found in bot_number_list.")

def test_schedule_enable_disable_for_active_bots():
    """
    For all active bots, schedule enable 5 minutes before earliest entry time and soft disable 5 minutes after latest entry time via Selenium, if bot is valid.
    """
    WD.update_all_bots_list()
    scheduled = []
    for bot_num in active_bots:
        if bot_num not in WD.bot_number_list:
            print(f"Skipping invalid bot: {bot_num}")
            continue
        try:
            entry_settings = WD.via_selenium.get_entry_settings(bot_num)
            # Parse entry times
            entry_time_start = entry_settings.get('entry_time_start')
            entry_time_end = entry_settings.get('entry_time_end')
            if not entry_time_start or not entry_time_end:
                print(f"{bot_num} has no earliest/latest entry time defined, skipping scheduling.")
                continue
            # Parse times (assume format 'HH:MM' or 'HH:MM AM/PM')
            def parse_time(tstr):
                try:
                    return datetime.datetime.strptime(tstr, '%I:%M %p').time()
                except Exception:
                    try:
                        return datetime.datetime.strptime(tstr, '%H:%M').time()
                    except Exception:
                        return None
            start_time = parse_time(entry_time_start)
            end_time = parse_time(entry_time_end)
            if start_time is None or end_time is None:
                print(f"Bot {bot_num} has invalid entry time format ('{entry_time_start}', '{entry_time_end}'), skipping.")
                continue
            # Schedule enable/disable (here, just print the intended schedule)
            try:
                enable_time = (datetime.datetime.combine(datetime.date.today(), start_time) - datetime.timedelta(minutes=5)).time()
                disable_time = (datetime.datetime.combine(datetime.date.today(), end_time) + datetime.timedelta(minutes=5)).time()
            except Exception as e:
                print(f"Bot {bot_num} time math error: {e}, skipping.")
                continue
            print(f"Scheduling bot {bot_num}: enable at {enable_time}, soft disable at {disable_time}")
            # Actually enable/disable via Selenium
            WD.via_selenium.enable_by_bot_num(bot_num)
            # In real scheduling, you'd use a scheduler like APScheduler or cron; here, just call directly for demo
            WD.via_selenium.disable_on_close_by_bot_num(bot_num)
            scheduled.append(bot_num)
        except Exception as e:
            print(f"Error scheduling bot {bot_num}: {e}")
    print(f"Scheduled {len(scheduled)} bots for enable/disable.")

def test_schedule_enable_disable_for_active_bots_v2():
    """
    For all active bots, schedule enable 5 minutes before earliest entry time and soft disable 5 minutes after latest entry time via WD.bots(b).enable/disable.at_time(...), if bot is valid.
    """
    WD.update_all_bots_list()
    scheduled = []
    for bot_num in active_bots:
        if bot_num not in WD.bot_number_list:
            print(f"Skipping invalid bot: {bot_num}")
            continue
        try:
            entry_settings = WD.via_selenium.get_entry_settings(bot_num)
            entry_time_start = entry_settings.get('entry_time_start')
            entry_time_end = entry_settings.get('entry_time_end')
            if not entry_time_start or not entry_time_end:
                print(f"{bot_num} has no earliest/latest entry time defined, skipping scheduling.")
                continue
            def parse_time(tstr):
                try:
                    return datetime.datetime.strptime(tstr, '%I:%M %p').time()
                except Exception:
                    try:
                        return datetime.datetime.strptime(tstr, '%H:%M').time()
                    except Exception:
                        return None
            start_time = parse_time(entry_time_start)
            end_time = parse_time(entry_time_end)
            if start_time is None or end_time is None:
                print(f"Bot {bot_num} has invalid entry time format ('{entry_time_start}', '{entry_time_end}'), skipping.")
                continue
            try:
                enable_time = (datetime.datetime.combine(datetime.date.today(), start_time) - datetime.timedelta(minutes=5)).strftime('%I:%M %p')
                disable_time = (datetime.datetime.combine(datetime.date.today(), end_time) + datetime.timedelta(minutes=5)).strftime('%I:%M %p')
            except Exception as e:
                print(f"Bot {bot_num} time math error: {e}, skipping.")
                continue
            # Schedule using the same syntax as in WT_auto_on_off_bot.py
            _ = WD.bots(bot_num).enable.at_time(enable_time, 'America/New_York')
            _ = WD.bots(bot_num).disable.at_time(disable_time, 'America/New_York')
            print(f"Scheduled bot {bot_num}: enable at {enable_time}, soft disable at {disable_time}")
            scheduled.append(bot_num)
        except Exception as e:
            print(f"Error scheduling bot {bot_num}: {e}")
    print(f"Scheduled {len(scheduled)} bots for enable/disable.")

def test_scheduler_add_task_with_partial_fxn():
    """
    Demonstrate WD.scheduler.add_task using partial to print at 9:30 AM and 4:00 PM EST.
    """
    WD.scheduler.start()
    WD.scheduler.stop_scheduler_at_time('4:30 PM', 'America/New_York')

    # Method to pass into scheduler
    def print_status(msg):
        print(msg)

    # Schedule tasks, pass method and method arguments
    WD.scheduler.add_task('9:30 AM', 'America/New_York', fxn=partial(print_status, 'Market is open'))
    WD.scheduler.add_task('4:00 PM', 'America/New_York', fxn=partial(print_status, 'Market is closed'))
    print("Scheduled print tasks for market open/close.")

# Test Schwab connection renewal
def test_renew_schwab_connection():
    """
    Test renewing Schwab broker connection using credentials from creds.py.
    """
    WD.via_selenium.enable(personal.USER, personal.PWD, is_verbose=True, is_headless=True)
    print("Attempting to renew Schwab connection...")
    result = WD.via_selenium.renew_schwab_connection(personal.Schwab_USER, personal.Schwab_PWD)
    print(f"Renew Schwab connection result: {result}")

# Entry Point
if __name__ == "__main__":
    test_apiwrapper_info_methods()
    test_schedule_enable_disable_for_active_bots_v2()
    test_scheduler_add_task_with_partial_fxn()
    test_renew_schwab_connection()