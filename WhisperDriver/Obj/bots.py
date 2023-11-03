########################################################################################################################
########################################################################################################################
###   Bot Objects for WhisperTrades.com API                                                                          ###
###                                                                                                                  ###
###   Authored by Paul Nobrega   Contact: Paul@PaulNobrega.net                                                       ###
###   Python Version 3.10                                                                                            ###
########################################################################################################################
########################################################################################################################
import json
import warnings
import schedule
from datetime import datetime
import time
from threading import Thread

class WhisperTradesBots(object):

    def __init__(self, endpts):
        self._endpts = endpts
        self.bots_list = self.__bot_list(self._endpts)
        self.scheduler_is_on = True
        self.__scheduler = Thread(target=self.__schedule_loop)
        self.__scheduler.start()

    def __call__(self, bot_number):
        for bot in self.bots_list.all:
            if bot.number == bot_number:
                return bot
        warnings.warn(f"Bot Number: {bot_number} not found!")
        return
    
    def __del__(self):
        self.stop_scheduler()
        return

    def __schedule_loop(self):
        while self.scheduler_is_on:
            schedule.run_pending()
            time.sleep(1)
        return
    
    def start_scheduler(self):
        """
        Start Scheduler loop in unique thread.  Thread automatically started at instantiation
        """
        if self.scheduler_is_on == False:
            self.scheduler_is_on = True
            self.__scheduler.start()
        return 
    
    def stop_scheduler(self):
        """
        Stop Scheduler loop thread.
        """
        if self.scheduler_is_on == True:
            schedule.clear()
            self.scheduler_is_on = False
        return
    
    def stop_scheduler_at_time(self, time_str: str=None, tz_str: str='America/New_York'):
        """
        Stop Scheduler thread at predefined time.
        
        :param time_str: string representation of military time (example: '22:30'). If 12-hr format, PM or AM must be included in string.
        :type time_str: String
        :param tz_str: human readable TimeZone. Default is 'America/New_York'
        :type tz_str: String
        """
        if not time_str:
            raise ValueError('Time input string is required!')
        if 'pm' in time_str.lower() or 'am' in time_str.lower():
            time_str = datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M')
        schedule.every().day.at(time_str, tz_str).do(self.stop_scheduler)

    def get_all_bot_variables(self) -> json:
        """
        Query WhisperTrades.com for all bot variables and associate data with related bot object
       
        :return: json data from response recieved from WhisperTrades API
        :type return: json
        """
        all_variables = self._endpts.variables.get_all_bot_variables()
        for var in all_variables:
            for bot in self.bots_list.all:
                for i, bot_var in enumerate(bot.variables):
                    if bot_var['number'] == var['number']:
                        bot.variables[i] = var
        return all_variables
    
    def update_all_bots(self):
        """
        Update bots_list with data retrieved from WHisperTrades.com API
        """
        self.bots_list.all = []
        _ = [self.bots_list.add_bot_to_list(bot) for bot in self._endpts.bots.get_all_bots()]
        return

    class __bot_list(object):
        def __init__(self, endpts):
            self.all = []
            self._endpts = endpts
        
        def all(self) -> list:
            """
            Return list of all bot numbers
            """
            return self.all
        
        def is_enabled(self) -> list:
            """
            Return list of all bot numbers that have status = 'enabled'
            """
            return [bot for bot in self.all if bot.status.lower() == 'enabled']
        
        def is_disabled(self) -> list:
            """
            Return list of all bot numbers that have status = 'disabled'
            """
            return [bot for bot in self.all if bot.status.lower() == 'disabled']
        
        def is_disabled_on_close(self) -> list:
            """
            Return list of all bot numbers that have status = 'disabled on close'
            """
            return [bot for bot in self.all if bot.status.lower() == 'disabled on close']
        
        def add_bot_to_list(self, bot_dict:dict={}):
            """
            Add dictionary representation of a WT bot to bot_list.all

            Note: if bot_number exists in bot_list.all, it is removed and replaced with the new information
            """
            if bot_dict=={}:
                warnings.warn(f'bot_dict is empty!')
                return
            bot_json = json.loads(json.dumps(bot_dict))
            self.remove_bot_from_list(bot_json['number'])
            self.all.append(self.bot_obj(bot_json, self._endpts))
            return
        
        def remove_bot_from_list(self, bot_number:str):
            """
            Removes bot from bots.all list by given bot number
            """
            for i in range(len(self.all)):
                if self.all[i].number == bot_number:
                    del self.all[i]
                    return
            return


        class bot_obj(object):
            
            def __init__(self, bot_dict, endpts):
                self.number = ''
                self.name = ''
                self.broker_connection = {}
                self.is_paper= False
                self.status = ''
                self.can_enable = True
                self.can_disable = True
                self.symbol = ''
                self.type = ''
                self.notes = ''
                self.last_active_at = ''
                self.disabled_at = ''
                self.entry_condition = {}
                self.exit_condition = {}
                self.adjustments = []
                self.notifications = []
                self.variables = []
                self._endpts = endpts
                self.__bot_dict_to_attr(bot_dict)
                self.enable = self._change_status('enable', self.number, self._endpts)
                self.disable = self._change_status('disable', self.number, self._endpts)
           
            def __str__(self):
                attrs = vars(self)
                test = [f'{item[0]}: {str(item[1])}' for item in attrs.items()]
                return "\n".join(test)
            
            def __repr__(self):
                return self.__str__()
            
            def __bot_dict_to_attr(self, bot_dict):
                for key in bot_dict: 
                    setattr(self, key, bot_dict[key])
            
            def update(self):
                """
                Query WhisperTrades.com for bot information and update object with new information 
                """
                bot_dict = self._endpts.bots.get_bot(bot_number=self.number)
                self.__bot_dict_to_attr(json.loads(json.dumps(bot_dict)))
                return
            
            def get_bot_variables(self):
                """
                Query WhisperTrades.com for variables associated with bot and update object with new information 
                """
                all_var = [v['number'] for v in self.variables]
                self.variables = []
                self.variables = [self._endpts.variables.get_bot_variables(v) for v in all_var]
                return self.variables
            
            class _change_status(object):

                def __init__(self, target_status, bot_number, endpts):
                    self._endpts = endpts
                    self._target_status = target_status
                    self._bot_number = bot_number

                def __call__(self):
                    return self._toggle_status()
                
                def _toggle_status(self):
                    if self._target_status == 'enable':
                        return self._endpts.bots.enable_bot(self._bot_number)
                    elif self._target_status == 'disable':
                        return self._endpts.bots.disable_bot(self._bot_number)
                    return
                
                def _meridian_time_to_military_time(self, time_str):
                    return datetime.strptime(time_str, '%I:%M %p').strftime('%H:%M')

                def at_time(self, time_str=None, tz_str='America/New_York'):
                    """
                    Schedule bot status change.
                    
                    :param time_str: string representation of military time (example: '22:30'). If 12-hr format, PM or AM must be included in string.
                    :type time_str: String
                    :param tz_str: human readable TimeZone. Default is 'America/New_York'
                    :type tz_str: String
                    """
                    if not time_str:
                        raise ValueError('Time input string is required!')
                    if 'pm' in time_str.lower() or 'am' in time_str.lower():
                        time_str = self._meridian_time_to_military_time(time_str)
                    schedule.every().day.at(time_str, tz_str).do(self._toggle_status)
                    



    