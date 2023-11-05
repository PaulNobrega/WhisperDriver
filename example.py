import WhisperDriver

if __name__ == '__main__':
    WT_API_TOKEN = 'WT_API_TOKEN' # Token provided by Whisper Trades 
    
    # Instnatiate WhisperTrades API Wrapper
    WD = WhisperDriver.ApiWrapper(WT_API_TOKEN)

    # Upon instantiatioin, data is pulled form the API to build WhisperDriver objects.
    # For instance: We now have a complete list of bot numbers and their associated data 
    print(WD.bot_number_list) # print all bot_numbers
    first_bot = WD.bot_number_list[0]
    print(WD.bots(first_bot).status) # print first bot in list's status

    # By default, endpoint requests are throttled with a 2 second delay prior to the request.
    # This ensures that the API rate limit will not be exceeded.  It is toggleable
    WD.throttle.disable()
    WD.throttle.set_delay_sec(2)
    WD.throttle.enable()

    # We can use the endpoints object directly to do a number of things
    first_bot_data = WD.endpts.bots.get_bot(first_bot) # get bot data for first bot via API query
    print(first_bot_data['status'])
    WD.endpts.bots.enable_bot(first_bot)
    WD.endpts.bots.disable_bot(first_bot)

    # We can accomplish the same using the abstracted bot object
    WD.bots(first_bot).update()
    print(WD.bots(first_bot).status)
    WD.bots(first_bot).enable()
    WD.bots(first_bot).disable()

    # The bot object makes use of WhisperDriver's scheduler object so you can also schedule non-blocking actions.
    # The scheduler uses the local system time and accepts meredian time or military time as a string
    WD.scheduler.start() # This is optional as adding tasks will automatically start the scheduler
    WD.scheduler.stop_scheduler_at_time('4:30 PM', 'America/New_York') # This will automatically stop the scheduler at a defined time so the thread will close and your code will not hang on the background thread
    WD.bots(first_bot).enable.at_time('9:00 PM', 'America/New_York') # example using defined meredian time and timezone
    WD.bots(first_bot).disable.at_time('16:21') # example using defined military time and default timezone = 'America/New_York'
    WD.scheduler.stop() # If you don't schedule a stop, you will want to explicitly stop the schedule thread.  This will cancel all pending tasks

    # Useful Code Examples:
    WD.bots.update_all_bots() # pull all bot data via API request
    disabled_bots = WD.bots.bots_list.is_disabled() # get list of all disabled bots
    _ = [WD.bots(bot.number).enable() for bot in disabled_bots] # enable all disabled bots
    WD.bots.update_all_bots() # pull all bot data via API request
    enabled_bots = WD.bots.bots_list.is_enabled() # get list of all enabled bots
    _ = [WD.bots(bot.number).disable() for bot in enabled_bots] # disable all enabled bots
    _ = [WD.bots(first_bot).enable.at_time(WD.bots(bot).entry_condition['earliest_time_of_day'], 'America/New_York') for bot in WD.bot_number_list] # Schedule bot enable at earliest time of day
    _ = [WD.bots(first_bot).disable.at_time(WD.bots(bot).entry_condition['latest_time_of_day'], 'America/New_York') for bot in WD.bot_number_list] # Schedule bot disable on close  at latest time of day

    # WhisperDriver can hit all WhisperTrades endpoints documented as of 11/05/2023 via the endpoints object
    report_number = 'report_number'
    report = WD.endpts.reports.get_bot_report(report_number)
    all_reports = WD.endpts.reports.get_all_bot_reports()
    api_reponse = WD.endpts.reports.run_bot_report(report_number)
    api_response = WD.endpts.reports.update_bot_report(report_number, new_name='rename_report', new_start_date='YYYY-MM-DD', new_end_date='YYYY-MM-DD', run_until_latest_date=True)

    unassociated_variable_number = 'var_num' #Variables associated with bots will be within the bot object. Variables not associated with a bot's state are contained in the variables object
    WD.variables.update_all_variables()
    print(WD.variables.unassociated_variable_numbers)
    print(WD.variables.variables_list.all())
    print(WD.variables(unassociated_variable_number).number)
    print(WD.variables(unassociated_variable_number).name)
    print(WD.variables(unassociated_variable_number).bot)
    print(WD.variables(unassociated_variable_number).value)
    print(WD.variables(unassociated_variable_number).free_text_value)
    print(WD.variables(unassociated_variable_number).last_updated_at)
    print(WD.variables(unassociated_variable_number).conditions)
    WD.variables(unassociated_variable_number).set('free_text_value')
    WD.variables(unassociated_variable_number).update()

    # There are other functions that are not documented here.  Please see docstrings in code for other functionalities 