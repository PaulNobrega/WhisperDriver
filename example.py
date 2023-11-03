import WhisperDriver
import time

if __name__ == '__main__':
    WT_API_TOKEN = ''

    # WD = WhisperDriver.ApiWrapper(WT_API_TOKEN)
    
    #print(WD.bot_number_list) # print all bot_numbers

    #first_bot = WD.endpts.bots.get_bot(WD.bot_number_list[0]) # get bot data for first bot in list ------------THIS IS RETURNING THE WRONG DATA

    # first_bot = WD.bot_number_list[0]

    # print(WD.bots(first_bot).status) # print first bot in list's status

    #first_bot_variables = WD.bots(first_bot).get_bot_variables() # get all variables associated with first_bot

    #WD.bots(first_bot).update() # update bot info via API call

    #all_vars = WD.bots.get_all_bot_variables() # get all variables
    
    # paper_bot = 'JB8RBJIAR8'
    # unassociated_variable_number = 'UVZVCZD6J6'

    # print(WD.bots(paper_bot).variables)
    # WD.bots(paper_bot).get_bot_variables()
    # print(WD.bots(paper_bot).variables)

    # print(WD.variables.unassociated_variable_numbers)
    # print(WD.bots.bots_list.all)
    # print(WD.variables.variables_list.all)

    # x = WD.variables(unassociated_variable_number).set('test')

    # disabled_bots = WD.bots.bots_list.is_disabled() # get list of bot numbers of all disabled bots

    # _ = [WD.endpts.bots.enable_bot(bot.number) for bot in disabled_bots] # enable all disabled bots

    # for i in range(len(WD.bots.bots_list.all)):
    #     WD.endpts.bots.disable_bot(WD.bots.bots_list.all[i].number)
    #     print(f'Disabling {WD.bots.bots_list.all[i].number}')
    #     time.sleep(10)
    
    WD = WhisperDriver.ApiWrapper(WT_API_TOKEN)
    bot_number='NZN493HYLC'
    WD.bots(bot_number).enable()
    print('now')
    WD.bots.stop_scheduler_at_time('6:29 PM', 'America/New_York')
    WD.bots(bot_number).disable.at_time('5:31 PM')