from .core import get_sas_connect, Abstract_SAS
import logging


class SASCS(Abstract_SAS):
    def __init__(self, sasobjsp_user,
                       sasobjsp_pass,
                       sasobjsp_host='vs2458.imb.ru',
                       sasobjsp_port='8591',  **kwargs):
        self.platform = 'SASCS'
        super(Abstract_SAS, self).__init__(sasobjsp_host, sasobjsp_port, sasobjsp_user, sasobjsp_pass)


