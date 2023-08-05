from .core import get_sas_connect, Abstract_SAS


class SASMA(Abstract_SAS):
    def __init__(self, sasobjsp_user,
                       sasobjsp_pass,
                       sasobjsp_host='vs246.imb.ru',
                       sasobjsp_port='8591',  **kwargs):
        self.platform = 'SASMA'
        super(SASMA, self).__init__(sasobjsp_host=sasobjsp_host,
                                    sasobjsp_port=sasobjsp_port,
                                    sasobjsp_user=sasobjsp_user,
                                    sasobjsp_pass=sasobjsp_pass)