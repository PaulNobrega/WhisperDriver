import WhisperDriver

if __name__ == '__main__':
    WT_API_TOKEN = 'token_string'

    WD = WhisperDriver.ApiWrapper(WT_API_TOKEN)
    
    print(WD.bot_number_list) # print all bot_numbers

    first_bot = WD.endpts.bots.get_bot(WD.bot_number_list[0]) # get bot data for first bot in list

    print(WD.bots(first_bot).status) # print first bot in list's status

    first_bot_variables = WD.bots(first_bot).get_bot_variables() # get all variables associated with first_bot

    WD.bots(first_bot).update() # update bot info via API call

    all_vars = WD.bots.get_all_bot_variables() # get all variables
    
    WD.bots(WD.bot_number_list[0]).set_bot_variables(variable_number = 'VARIABLE_NUMBER', variable_name='realized_profit_paper', new_value='10') # set bot variable

    disabled_bots = WD.bots.bots_list.is_disabled() # get list of bot numbers of all disabled bots

    _ = [WD.endpts.bots.enable_bot(bot.number) for bot in disabled_bots] # enable all disabled bots
