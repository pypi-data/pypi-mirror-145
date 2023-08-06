from .core import AbstractSAS
from .globals import sascs_sasobjsp_host, sascs_sasobjsp_port


class SASCS(AbstractSAS):
    def __init__(self, user,
                       password,
                       sasobjsp_host=sascs_sasobjsp_host,
                       sasobjsp_port=sascs_sasobjsp_port,  **kwargs):
        self.platform = 'SASCS'
        self.env_type = 'Prod'
        super(SASCS, self).__init__(sasobjsp_host=sasobjsp_host,
                                    sasobjsp_port=sasobjsp_port,
                                    sasobjsp_user=user,
                                    sasobjsp_pass=password)
