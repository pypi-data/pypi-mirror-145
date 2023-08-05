from .core import get_sas_connect, AbstractSAS
import logging


class SASCS(AbstractSAS):
    def __init__(self, user,
                       password,
                       sasobjsp_host='vs2458.imb.ru',
                       sasobjsp_port='8591',  **kwargs):
        self.platform = 'SASCS'
        self.env_type = 'Prod'
        super(SASCS, self).__init__(sasobjsp_host=sasobjsp_host,
                                    sasobjsp_port=sasobjsp_port,
                                    sasobjsp_user=user,
                                    sasobjsp_pass=password)


