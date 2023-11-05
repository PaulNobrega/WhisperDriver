########################################################################################################################
########################################################################################################################
###   Python Wrapper for WhisperTrades.com API                                                                       ###
###                                                                                                                  ###
###   Authored by Paul Nobrgea   Contact: Paul@PaulNobrega.net                                                       ###
###   Python Version 3.10                                                                                            ###
########################################################################################################################
########################################################################################################################
from . import Obj
import time

class ApiWrapper(object):

    def __init__(self, token):
        self.throttle = Obj.WhisperTradesThrottle()
        self.throttle.disable()
        self.endpts = Obj.WhisperTradesEndpoints(token, self.throttle)
        self.scheduler= Obj.WhisperTradesScheduler(self.endpts)
        self.bots = Obj.WhisperTradesBots(self.scheduler)
        self.variables = Obj.WhisperTradesVariables(self.endpts)
        self.bot_number_list = []
        self.report_number_list = []
        self.variable_number_list = []
        self.__populate()
        self.throttle.enable()

    def __del__(self):
        '''
        Do not destroy object until scheduler thread completes
        '''
        while self.scheduler.scheduler_is_on:
            time.sleep(1)
        return

    def __populate(self):
        self.update_all_bots_list()
        self.update_all_reports_list()
        self.update_all_variables_list()
        return
    
    def update_all_bots_list(self):
        """
        Update list of bot numbers via call to WhisperTrades API
        """
        self.bots.update_all_bots()
        self.bot_number_list = [i.number for i in self.bots.bots_list.all]
        return

    def update_all_reports_list(self):
        """
        Update list of report numbers via call to WhisperTrades API
        """
        self.report_number_list = [i['number'] for i in self.endpts.reports.get_all_bot_reports()]
        return
    
    def update_all_variables_list(self):
        """
        Update list of variable numbers via call to WhisperTrades API
        """
        self.variable_number_list = [i['number'] for i in self.endpts.variables.get_all_bot_variables()]
    
    def start_scheduler(self):
        """
        Start Scheduler loop in unique thread.  Thread automatically started at instantiation
        """
        self.scheduler.start()
        return 
    
    def stop_scheduler(self):
        """
        Stop Scheduler loop thread.
        """
        self.scheduler.stop()
        return
    
    def stop_scheduler_at_time(self, time_str: str=None, tz_str: str='America/New_York'):
        """
        Stop Scheduler thread at predefined time.
        
        :param time_str: string representation of military time (example: '22:30'). If 12-hr format, PM or AM must be included in string.
        :type time_str: String
        :param tz_str: human readable TimeZone. Default is 'America/New_York'
        :type tz_str: String
        """
        self.scheduler.stop_scheduler_at_time(time_str, tz_str)
        return

