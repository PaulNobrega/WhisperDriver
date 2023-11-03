########################################################################################################################
########################################################################################################################
###   Python Wrapper for WhisperTrades.com API                                                                       ###
###                                                                                                                  ###
###   Authored by Paul Nobrgea   Contact: Paul@PaulNobrega.net                                                       ###
###   Python Version 3.10                                                                                            ###
########################################################################################################################
########################################################################################################################
from . import Obj

class ApiWrapper(object):

    def __init__(self, token):
        self.endpts = Obj.WhisperTradesEndpoints(token)
        self.bots = Obj.WhisperTradesBots(self.endpts)
        self.variables = Obj.WhisperTradesVariables(self.endpts)
        self.bot_number_list = []
        self.report_number_list = []
        self.variable_number_list = []
        self.__populate()

    def __del__(self):
        del self.bots
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


