from .core import AbstractSAS
from .globals import sasma_sasobjsp_host, sasma_sasobjsp_port


class SASMA(AbstractSAS):
    """
    This class is a wrapper for saspy.SASSession.
    It hides all the 'tricky' parts of establishing connection with SASMA.
    """
    def __init__(self, user,
                       password,
                       sasobjsp_host=sasma_sasobjsp_host,
                       sasobjsp_port=sasma_sasobjsp_port,  **kwargs):
        """
        Establishes sas connection.
        :param user: user, that is used to connect to SASMA.
        :param password: The password.
        :param sasobjsp_host: Host, on which SAS Object spawner is running.
        :param sasobjsp_port: Port, on which SAS Object spawner is running.
        :param kwargs:
        """
        self.platform = 'SASMA'
        self.env_type = 'Prod'
        super(SASMA, self).__init__(sasobjsp_host=sasobjsp_host,
                                    sasobjsp_port=sasobjsp_port,
                                    sasobjsp_user=user,
                                    sasobjsp_pass=password)
