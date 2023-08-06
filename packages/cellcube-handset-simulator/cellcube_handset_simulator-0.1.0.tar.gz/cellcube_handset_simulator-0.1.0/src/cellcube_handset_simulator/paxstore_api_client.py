from terminal_api import TerminalAPI




class PaxstoreApiClient:

    def __init__(self, api_key, api_secret, base_url="https://api.whatspos.com/p-market-api", options=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self.options = self.__get_default_options(options)

    def __get_default_options(self, options=None):    

        default_options = {
            "serviceEndPoint": self.base_url,  
            "cookie": None,
            "algorithm": "md5",
            "timeout": 3000
        }

        if not options is None:
            for key in options:
                if options[key] is not None:
                    default_options[key] = options[key]

        return default_options


    def get_terminal(self, terminal_id, include_detail_info = False):      
        terminalAPI = TerminalAPI(self.api_key,self.api_secret, self.base_url, self.options)
        return terminalAPI.get_terminal(terminal_id, include_detail_info)
        


    def get_terminal_by_tid(self, terminal_tid, include_installed_apks = False, include_installed_firmwares = False, include_detail_info = False):
        terminalAPI = TerminalAPI(self.api_key,self.api_secret, self.base_url, self.options)
        return terminalAPI.get_terminal_by_tid(terminal_tid, include_installed_apks, include_installed_firmwares, include_detail_info)

    def get_terminal_by_sn(self, serial_number, include_installed_apks = False, include_installed_firmwares = False, include_detail_info = False):
        terminalAPI = TerminalAPI(self.api_key,self.api_secret, self.base_url, self.options)
        return terminalAPI.get_terminal_by_sn(serial_number, include_installed_apks, include_installed_firmwares, include_detail_info)


    def get_terminal_by_name(self, terminal_name, include_installed_apks = False, include_installed_firmwares = False, include_detail_info = False):
        terminalAPI = TerminalAPI(self.api_key,self.api_secret, self.base_url, self.options)
        return terminalAPI.get_terminal_by_name(terminal_name, include_installed_apks, include_installed_firmwares, include_detail_info)

    def get_terminal_by_sn_name_tid(self, sn_name_tid, include_installed_apks = False, include_installed_firmwares = False, include_detail_info = False):
        terminalAPI = TerminalAPI(self.api_key,self.api_secret, self.base_url, self.options)
        return terminalAPI.get_terminal_by_sn_name_tid(sn_name_tid, include_installed_apks, include_installed_firmwares, include_detail_info)

    def get_terminal_id_using_sn(self, serial_number):
        terminalAPI = TerminalAPI(self.api_key,self.api_secret, self.base_url, self.options)
        return terminalAPI.get_terminal_id_using_sn(serial_number)

    def search_terminal(self, order_by=None, status=None, sn_name_tid=None, include_geolocation = False, include_installed_apks = False, include_installed_firmwares = False, include_detail_info = False, page_no = 1, page_size = 30):
        terminalAPI = TerminalAPI(self.api_key,self.api_secret, self.base_url, self.options)
        return terminalAPI.search_terminal(order_by, status, sn_name_tid, include_geolocation, include_installed_apks, include_installed_firmwares, include_detail_info, page_no, page_size)