from .core import get_sas_connect, AbstractSAS


class SASMA(AbstractSAS):
    def __init__(self, user,
                       password,
                       sasobjsp_host='vs246.imb.ru',
                       sasobjsp_port='8591',  **kwargs):
        self.platform = 'SASMA'
        self.env_type = 'Prod'
        super(SASMA, self).__init__(sasobjsp_host=sasobjsp_host,
                                    sasobjsp_port=sasobjsp_port,
                                    sasobjsp_user=user,
                                    sasobjsp_pass=password)
