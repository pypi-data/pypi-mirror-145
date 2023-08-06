import os

# Default Java
java_linux = '/usr/bin/java'  # fetch it from env vars???
java_windows = 'java'

# SAS globals...
all_obj_types = ['DeployedFlow', 'DeployedJob', 'ExternalFile', 'Folder',
                     'Library', 'Role', 'Server', 'StoredProcess', 'Table',
                     'User', 'Job']


#**********************************
# Default platfrom settings
###################################
# SASMA
###################################
sasma_sasobjsp_host = 'vs246.imb.ru'
sasma_sasobjsp_port = '8591'

##################################
# SAS Scoring
###################################
sascs_sasobjsp_host = 'vs2458.imb.ru'
sascs_sasobjsp_port = '8591'
#**********************************


###################################
# HashicorpVault settings variables
###################################
hvac_url = 'https://hvault.intranet'
hvac_token_env_var = 'HVAC_TOKEN'
hvac_token = os.environ.get(hvac_token_env_var, default=None)
hvac_role_id_env_var = 'HVAC_ROLE_ID'
hvac_role_id = os.environ.get(hvac_role_id_env_var, default=None)
hvac_secret_env_var = 'HVAC_SECRET_ID'
hvac_secret_id = os.environ.get(hvac_secret_env_var, default=None)
hvac_connections_path = 'Data_Science/dlake/airflow/connections/'
hvac_connections_mountpoint = 'CDO/'
